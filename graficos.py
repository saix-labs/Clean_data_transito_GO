import pandas as pd
import plotly.express as px
import streamlit as st


def criar_kpis_ato1(df):
    st.title("Ato 1: O Panorama Geral")
    st.markdown("---")

    # --- CARDS DE KPI (TOPO) ---
    total_acidentes = len(df)
    br_mais_critica = f"BR-{df['br'].mode()[0]}"

    # Soma apenas Pista Simples + Pista Dupla
    pct_pista_simples_dupla = (df['tipo_pista'].str.contains('Simples|Dupla', case=False, na=False).sum() / total_acidentes) * 100
    
    # Calcula Céu Claro / Sol
    pct_ceu_claro = (df['condicao_metereologica'].str.contains('Céu Claro|Sol', case=False, na=False).sum() / total_acidentes) * 100

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        st.metric(label="Total de Acidentes", value=f"{total_acidentes:,}".replace(",", "."))

    with kpi2:
        st.metric(label="BR com Maior Volume", value=br_mais_critica)

    with kpi3:
        st.metric(label="Acidentes em Pista Simples e Dupla", value=f"{pct_pista_simples_dupla:.1f}%")

    with kpi4:
        st.metric(label="Acidentes a Céu Claro", value=f"{pct_ceu_claro:.1f}%")

    st.markdown("---")


    # --- LINHA 1: TURNO E RANKING DE BRS ---
    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Distribuição por Turno (Fase do Dia)")
            st.plotly_chart(criar_fig_turno(df), use_container_width=True)

        with col2:
            st.subheader("Ranking de BRs com Mais Ocorrências")
            st.plotly_chart(criar_fig_br(df), use_container_width=True)

    # --- ESPAÇADOR DE TELA (Garante o isolamento da Linha 1 no F11) ---
    st.markdown("<div style='margin-bottom: 35vh;'></div>", unsafe_allow_html=True)

    # --- LINHA 2: TIPO DE PISTA E CONDIÇÃO METEOROLÓGICA ---
    with st.container():
        col3, col4 = st.columns(2)

        with col3:
            st.subheader("Infraestrutura: Tipo de Pista")
            st.plotly_chart(criar_fig_pista(df), use_container_width=True)

        with col4:
            st.subheader("Clima: Condição Meteorológica")
            st.plotly_chart(criar_fig_clima(df), use_container_width=True)

            
    # --- MAPA DE CALOR POR MUNICÍPIO E TOP 5 CIDADES ---
    st.markdown("---")
    st.subheader("Distribuição do Volume de Acidentes por Município")

    fig_mapa, df_municipio = criar_fig_mapa(df)
    st.plotly_chart(fig_mapa, use_container_width=True)

    st.markdown("###  Top 5 Municípios com Maior Registro de Acidentes")

    top5_cidades = df_municipio.head(5)

    col_t1, col_t2, col_t3, col_t4, col_t5 = st.columns(5)
    cols = [col_t1, col_t2, col_t3, col_t4, col_t5]

    for i, row in top5_cidades.iterrows():
        with cols[i]:
            st.metric(
                label=f"{i+1}º {row['Município'].title()}", 
                value=f"{row['Total de Acidentes']:,}".replace(",", ".")
            )


def criar_fig_turno(df):
    df_turno = df['fase_dia'].value_counts().reset_index()
    df_turno.columns = ['Fase do Dia', 'Total']
    
    fig = px.pie(
        df_turno, 
        values='Total', 
        names='Fase do Dia', 
        hole=0.5,
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    fig.update_traces(
        textinfo='percent+label',
        textfont=dict(color='#FFFFFF', size=13)
    )
    
    fig.update_layout(
        showlegend=False, 
        margin=dict(t=20, b=20, l=10, r=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    return fig


def criar_fig_br(df):
    df_br = df['br'].value_counts().head(5).reset_index()
    df_br.columns = ['BR', 'Total']
    df_br['BR'] = "BR-" + df_br['BR'].astype(str)
    
    fig = px.bar(
        df_br, 
        x='Total', 
        y='BR', 
        orientation='h',
        text='Total',
        color_discrete_sequence=['#1f77b4'] # Azul sólido mantendo o padrão visual
    )
    fig.update_layout(
        yaxis={'categoryorder':'total ascending', 'tickfont': {'color': '#FFFFFF', 'size': 14}}, 
        xaxis=dict(tickfont=dict(color='#FFFFFF', size=13)),
        showlegend=False, 
        coloraxis_showscale=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    # Garante que os valores e textos dentro do gráfico fiquem brancos
    fig.update_traces(
        textfont=dict(color='#FFFFFF', size=13)
    )
    
    return fig


def criar_fig_pista(df):
    df_pista = df['tipo_pista'].value_counts().reset_index()
    df_pista.columns = ['Tipo de Pista', 'Total']
    
    fig = px.bar(
        df_pista, 
        x='Tipo de Pista', 
        y='Total', 
        text='Total',
        color_discrete_sequence=['#1f77b4']
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(tickfont=dict(color='#FFFFFF', size=13)),
        yaxis=dict(tickfont=dict(color='#FFFFFF', size=14))
    )
    
    # Garante que os rótulos e valores internos fiquem brancos
    fig.update_traces(
        textfont=dict(color='#FFFFFF', size=13)
    )
    
    return fig


def criar_fig_clima(df):
    df_clima = df['condicao_metereologica'].value_counts().head(5).reset_index()
    df_clima.columns = ['Condição', 'Total']
    
    fig = px.bar(
        df_clima, 
        x='Condição', 
        y='Total', 
        text='Total',
        color_discrete_sequence=['#2b5c8f']
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(tickfont=dict(color='#FFFFFF', size=13)),
        yaxis=dict(tickfont=dict(color='#FFFFFF', size=14))
    )
    
    # Força os rótulos diretos do gráfico (números, porcentagens ou legendas internas) a ficarem brancos
    fig.update_traces(
        textfont=dict(color='#FFFFFF', size=13)
    )
    
    return fig


def criar_fig_mapa(df):
    df_municipio = df['municipio'].value_counts().reset_index()
    df_municipio.columns = ['Município', 'Total de Acidentes']

    df_coords = df.groupby('municipio')[['latitude', 'longitude']].mean().reset_index()
    df_coords.columns = ['Município', 'latitude', 'longitude']

    df_mapa_cidades = pd.merge(df_municipio, df_coords, on='Município')

    fig = px.scatter_mapbox(
        df_mapa_cidades, 
        lat='latitude', 
        lon='longitude', 
        size='Total de Acidentes',
        color='Total de Acidentes',
        color_continuous_scale='Reds',
        hover_name='Município',
        hover_data={'latitude': False, 'longitude': False, 'Total de Acidentes': True},
        zoom=5.5,
        center=dict(lat=-16.6869, lon=-49.2648),
        mapbox_style="open-street-map"
    )
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    return fig, df_municipio











def criar_kpis_ato2(df):
    st.title("Ato 2: Investigação e Hotspots")
    st.markdown("---")

    # --- CSS EXCLUSIVO DO ATO 2 ---
    # 1. Espaçamento entre as linhas de blocos
    # 2. Ajuste do tamanho da fonte no Card 3
    st.markdown(
        """
        <style>
            div[data-testid="stHorizontalBlock"] {
                margin-bottom: 10rem !important;
            }
            div[data-testid="stColumn"]:nth-child(3) [data-testid="stMetricValue"] {
                font-size: 1.05rem !important;
                line-height: 1.2 !important;
                white-space: normal !important;
                word-break: break-word !important;
                min-height: 2.4rem !important;
                display: flex !important;
                align-items: center !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # --- CARDS DE KPI (TOPO) ---
    total = len(df)
    if total == 0:
        st.warning("Nenhum dado disponível.")
        return

    # 1. Traçado Predominante
    qtd_reta = df['tracado_via'].astype(str).str.contains('Reta', case=False, na=False).sum()
    pct_reta = (qtd_reta / total) * 100

    # 2. Gravidade Controlada (Não Fatais)
    qtd_controlada = df['classificacao_acidente'].isin(['Com Vítimas Feridas', 'Sem Vítimas']).sum()
    pct_controlada = (qtd_controlada / total) * 100

    # 3. Causa Principal #1
    causa_series = df['causa_acidente'].dropna()
    causa_top1 = causa_series.mode()[0] if not causa_series.empty else "N/A"
    
    if "Reação tardia" in causa_top1 or "ineficiente" in causa_top1:
        causa_exibicao = "Reação Tardia / Ineficiente"
    elif len(causa_top1) > 22:
        causa_exibicao = causa_top1[:22] + "..."
    else:
        causa_exibicao = causa_top1

    # 4. Dias Úteis
    dias_uteis = ['segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira']
    qtd_dias_uteis = df['dia_semana'].astype(str).str.lower().isin(dias_uteis).sum()
    pct_dias_uteis = (qtd_dias_uteis / total) * 100

    # Renderização dos 4 Cards
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        st.metric(label="Traçado Predominante", value=f"{pct_reta:.1f}%")

    with kpi2:
        st.metric(label="Acidentes Não Fatais", value=f"{pct_controlada:.1f}%")

    with kpi3:
        st.metric(label="Causa Principal #1", value=causa_exibicao)

    with kpi4:
        st.metric(label="Acidentes em Dias Úteis", value=f"{pct_dias_uteis:.1f}%")

    st.markdown("---")

    # --- LINHA 1 DE GRÁFICOS: TRAÇADO E CLASSIFICAÇÃO ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top Traçados da Via")
        st.plotly_chart(criar_fig_tracado(df), use_container_width=True)

    with col2:
        st.subheader("Classificação dos Acidentes")
        st.plotly_chart(criar_fig_classificacao(df), use_container_width=True)

    st.markdown("---")

    # --- LINHA 2 DE GRÁFICOS: CAUSAS E TIPOS ---
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Top 5 Causas de Acidentes")
        st.plotly_chart(criar_fig_causa_funnel(df), use_container_width=True)

    with col4:
        st.subheader("Top 5 Tipos de Acidentes")
        st.plotly_chart(criar_fig_tipo_treemap(df), use_container_width=True)



def criar_fig_tracado(df):
    """
    Gera gráfico de barras verticais para o Top 7 traçados de via.
    """
    df_tracado = df['tracado_via'].value_counts().head(7).reset_index()
    df_tracado.columns = ['Traçado', 'Total']
    
    fig = px.bar(
        df_tracado,
        x='Traçado',
        y='Total',
        text='Total',
        color_discrete_sequence=['#1f77b4'] # Azul mantendo o padrão
    )
    
    fig.update_traces(
        textposition='outside',
        texttemplate='%{text:,}'
    )
    
    fig.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        margin=dict(t=20, b=20, l=10, r=10),
        xaxis=dict(tickfont=dict(color='#FFFFFF', size=13)),
        yaxis=dict(showticklabels=False, tickfont=dict(color='#FFFFFF', size=14))
    )
    
    # Garante que os rótulos diretos (números/textos sobre as barras ou elementos) fiquem brancos
    fig.update_traces(
        textfont=dict(color='#FFFFFF', size=13)
    )
    
    return fig


def criar_fig_classificacao(df):
    """
    Gera gráfico de rosca (Donut) com rótulos internos, tamanho de fonte 13
    e paleta de cores azuis padronizada com o modelo.
    """
    df_class = df['classificacao_acidente'].value_counts().reset_index()
    df_class.columns = ['Classificação', 'Total']

    # Paleta de tons de azul alinhada ao modelo
    tons_impacto = ['#08306b', '#2171b5', '#6baed6']

    fig = px.pie(
        df_class,
        values='Total',
        names='Classificação',
        hole=0.5,
        color='Classificação',
        color_discrete_sequence=tons_impacto
    )
    
    # Rótulos DENTRO dos blocos, com tamanho 13 e cor branca (igual ao modelo)
    fig.update_traces(
        textinfo='percent+label',
        textposition='inside',
        textfont=dict(
            color='#FFFFFF',  # Branco puro
            size=13           # Tamanho exatamente igual ao do modelo
        )
    )
    
    # Layout transparente
    fig.update_layout(
        showlegend=False,
        margin=dict(t=20, b=20, l=10, r=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    return fig




def criar_fig_causa_funnel(df):
    """
    Gráfico de Funil para o Top 5 Causas de Acidentes.
    Mantém o padrão de cores graduais em tons de azul e transparência do Ato 1.
    """
    # 1. Filtra Top 5 e ordena de forma descendente para a maior barra ficar no topo
    df_causa = df['causa_acidente'].value_counts().head(5).reset_index()
    df_causa.columns = ['Causa', 'Total']
    df_causa = df_causa.sort_values(by='Total', ascending=True)
    
    # 2. Tratamento para encurtar rótulos longos
    mapa_causas = {
        'Reação tardia ou ineficiente do condutor': 'Reação Tardia/Ineficiente',
        'Acessar a via sem observar a presença dos outros veículos': 'Entrar na Via sem Atenção'
    }
    df_causa['Causa'] = df_causa['Causa'].replace(mapa_causas)

    # 3. Gráfico de Funil com azul marinho intenso e vibrante no topo
    tons_impacto = ['#08306b', '#08519c', '#2171b5', '#4292c6', '#6baed6']
    
    fig = px.funnel(
        df_causa,
        y='Causa',
        x='Total',
        color='Causa',
        color_discrete_sequence=tons_impacto[::-1]
    )


    # 4. Ajuste de layout com fonte do eixo Y maior e branca
    fig.update_layout(
        showlegend=False,
        margin=dict(t=20, b=20, l=10, r=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        yaxis=dict(
            tickfont=dict(
                color='#FFFFFF',  # Branco puro
                size=14,          # Tamanho da fonte ajustado
            )
        )
    )
    
    # Exibe apenas o valor e ajusta os rótulos para a cor branca
    fig.update_traces(
        textinfo="value",
        textfont=dict(color="white", size=13)
    )
    return fig

def criar_fig_tipo_treemap(df):
    """
    Gráfico de Treemap para o Top 5 Tipos de Acidentes.
    Alinhado com as margens e paleta de azuis do Ato 1.
    """
    # 1. Filtra Top 5
    df_tipo = df['tipo_acidente'].value_counts().head(5).reset_index()
    df_tipo.columns = ['Tipo', 'Total']

    # 2. Gráfico Treemap com escala customizada (escuro no maior, legível nos menores)
    escala_azuis_impacto = ['#4292c6', '#2171b5', '#08519c', '#08306b']

    fig = px.treemap(
        df_tipo,
        path=['Tipo'],
        values='Total',
        color='Total',
        color_continuous_scale=escala_azuis_impacto
    )

    # Estilização do texto e das bordas dos blocos
    fig.update_traces(
        textinfo="label+value",
        textfont=dict(
            color='#FFFFFF',  # Branco puro
            size=14
        ),
        marker=dict(
            line=dict(color='#111827', width=1.5) # Borda escura para destacar cada bloco
        )
    )

    # 3. Ajuste de layout mantendo fundo transparente
    fig.update_layout(
        margin=dict(t=20, b=20, l=10, r=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        coloraxis_showscale=False
    )
    
    fig.update_traces(
        textinfo="label+value",
        marker=dict(cornerradius=4)
    )
    return fig



import streamlit as st

def obter_dados_causa_dia(df, dia_semana_str):
    """Calcula total, causa #1 e % para o dia selecionado (em minúsculo)."""
    # Converte para minúsculo para bater exatamente com os dados do DF
    dia_chave = dia_semana_str.lower()
    
    # Filtra mantendo compatibilidade com texto em minúsculo
    df_dia = df[df['dia_semana'].astype(str).str.lower() == dia_chave]
    total_dia = len(df_dia)
    
    if total_dia == 0:
        return {"total": 0, "causa_top1": "Nenhum registro", "pct_top1": 0.0}

    causas_count = df_dia['causa_acidente'].value_counts()
    causa_top1 = causas_count.index[0]
    qtd_top1 = causas_count.iloc[0]
    pct_top1 = (qtd_top1 / total_dia) * 100

    # Dicionário ajustado para os nomes reais da sua base
    mapa_causas = {
        'Reação tardia ou ineficiente do condutor': 'Reação Tardia/Ineficiente',
        'Ausência de reação do condutor': 'Ausência de Reação',
        'Ingestão de álcool pelo condutor': 'Ingestão de Álcool',
        'Acessar a via sem observar a presença dos outros veículos': 'Acessar Via sem Atenção',
        'Velocidade Incompatível': 'Velocidade Incompatível'
    }
    causa_formatada = mapa_causas.get(causa_top1, causa_top1)

    return {
        "total": total_dia,
        "causa_top1": causa_formatada,
        "pct_top1": pct_top1
    }


def renderizar_infografico_dias(df):
    """
    Renderiza os 7 dias como cards/botões enxutos na esquerda e o painel Neon Cyan na direita.
    """
    if 'dia_focado' not in st.session_state:
        st.session_state['dia_focado'] = 'Segunda-Feira'

    dias_exibicao = ['Segunda-Feira', 'Terça-Feira', 'Quarta-Feira', 'Quinta-Feira', 'Sexta-Feira', 'Sábado', 'Domingo']

    # Estilização para garantir que tudo caiba na tela sem scroll
    st.markdown("""
        <style>
        div[data-testid="stVerticalBlock"] > div {
            gap: 0.25rem !important;
        }

        /* Ajuste do botão nativo para virar o próprio card compacto */
        div.stButton > button {
            width: 100% !important;
            padding: 2px 8px !important;
            min-height: 28px !important;
            height: 28px !important;
            font-size: 12px !important;
            font-weight: 500 !important;
            background-color: rgba(255, 255, 255, 0.03) !important;
            color: #A0AEC0 !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 5px !important;
        }

        div.stButton > button:hover {
            border-color: #00F3FF !important;
            color: #00F3FF !important;
        }

        /* Painel Neon Cyan proporcional aos 7 botões */
        .painel-neon-box {
            border: 1.5px solid #00F3FF;
            box-shadow: 0px 0px 10px rgba(0, 243, 255, 0.25);
            border-radius: 8px;
            padding: 14px;
            background: rgba(10, 25, 47, 0.6);
            text-align: center;
            height: 220px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }

        .btn-scroll-container {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 4px;
            margin-bottom: 4px;
        }
        .btn-scroll-circle {
            width: 28px;
            height: 28px;
            border-radius: 50%;
            border: 1.5px solid #00F3FF;
            box-shadow: 0 0 6px rgba(0, 243, 255, 0.4);
            background: transparent;
            color: #00F3FF;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 14px;
            cursor: pointer;
        }
        </style>
    """, unsafe_allow_html=True)

    st.subheader("Análise Detalhada: Causa Principal por Dia")

    # Coluna 1 justa (0.7) e Coluna 2 (1.3)
    col_cards, col_painel = st.columns([0.7, 1.3])

    # Coluna Esquerda: 7 botões/cards
    with col_cards:
        for dia in dias_exibicao:
            is_ativo = (st.session_state['dia_focado'] == dia)
            tipo_btn = "primary" if is_ativo else "secondary"
            
            if st.button(dia, key=f"card_dia_{dia}", type=tipo_btn, use_container_width=True):
                st.session_state['dia_focado'] = dia
                st.rerun()

    # Coluna Direita: Painel Neon Cyan
    with col_painel:
        dia_atual = st.session_state['dia_focado']
        dados_dia = obter_dados_causa_dia(df, dia_atual)
        
        st.markdown(f"""
            <div class="painel-neon-box">
                <h4 style="color: #00F3FF; margin: 0; font-size: 17px;">{dia_atual}</h4>
                <div style="font-size: 12px; color: #A0AEC0; margin-top: 2px; margin-bottom: 8px;">
                    Total do dia: <b style="color: #FFFFFF;">{dados_dia['total']:,} acidentes</b>
                </div>
                <hr style="border: 0.5px solid rgba(0, 243, 255, 0.2); width: 85%; margin: 2px 0 8px 0;">
                <div style="font-size: 10px; color: #A0AEC0; text-transform: uppercase; letter-spacing: 0.8px;">Causa #1 Mais Frequente</div>
                <div style="font-size: 14px; color: #FFFFFF; font-weight: bold; margin: 4px 0;">
                    {dados_dia['causa_top1']}
                </div>
                <div style="font-size: 18px; color: #00F3FF; font-weight: bold; margin-top: 2px;">
                    {dados_dia['pct_top1']:.1f}%
                    <span style="font-size: 10px; color: #A0AEC0; font-weight: normal;">dos acidentes</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Botão de scroll compacto logo abaixo
    st.markdown("<div id='grafico-barras-dias'></div>", unsafe_allow_html=True)
    st.markdown("""
        <div class="btn-scroll-container">
            <a href="#grafico-barras-dias" style="text-decoration: none;">
                <div class="btn-scroll-circle" title="Rolar para baixo">
                    ↓
                </div>
            </a>
        </div>
    """, unsafe_allow_html=True)