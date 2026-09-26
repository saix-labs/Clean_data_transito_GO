import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go



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
        st.metric(label="Em linha Reta", value=f"{pct_reta:.1f}%")

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
        padding: 1px;
        background: rgba(10, 25, 47, 0.6);
        text-align: center;
        height: 290px;
    
        width: 600px; /* <--- ESTA É A LINHA DA LARGURA! */
        margin: 0 auto; /* Centraliza a caixa na coluna se ela for menor */
    
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
            width: 60px;
            height: 60px;
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
    st.markdown('<div style="margin-bottom: 15px;"></div>', unsafe_allow_html=True)  # Espaçador vertical de 15px

    # Coluna 1 justa (0.7) e Coluna 2 (1.3)
    col_cards, col_painel = st.columns([0.4, 1])

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
                <h4 style="color: #00F3FF; margin: 0; font-size: 26px;">{dia_atual}</h4>
                <div style="font-size: 18px; color: #A0AEC0; margin-top: 2px; margin-bottom: 8px;">
                    Total do dia: <b style="color: #FFFFFF;">{dados_dia['total']:,} acidentes</b>
                </div>
                <hr style="border: 0.5px solid rgba(0, 243, 255, 0.2); width: 85%; margin: 2px 0 8px 0;">
                <div style="font-size: 15px; color: #A0AEC0; text-transform: uppercase; letter-spacing: 0.8px;">Causa #1 Mais Frequente</div>
                <div style="font-size: 21px; color: #FFFFFF; font-weight: bold; margin: 4px 0;">
                    {dados_dia['causa_top1']}
                </div>
                <div style="font-size: 27px; color: #00F3FF; font-weight: bold; margin-top: 2px;">
                    {dados_dia['pct_top1']:.1f}%
                    <span style="font-size: 15px; color: #A0AEC0; font-weight: normal;">dos acidentes</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Botão de scroll compacto logo abaixo
    st.markdown("""
        <div class="btn-scroll-container">
            <a href="#grafico-barras-dias" style="text-decoration: none;">
                <div class="btn-scroll-circle" title="Rolar para baixo">
                    ↓
                </div>
            </a>
        </div>
    """, unsafe_allow_html=True)

    
    #ESPAÇADOR ENTRE OS DOIS GRAFICOS
    st.markdown('<div style="height: 200px; display: block; clear: both;"></div>', unsafe_allow_html=True)



def criar_fig_top2_causa_dia(df):
    """
    Processa os dados do Top 2 causas de acidentes por dia da semana
    e renderiza o gráfico (75%) com o painel de legenda lateral (25%).
    """
    # ÂNCORA DO SCROLL: scroll-margin-top dá o "respiro" no topo para centralizar
    st.markdown("<div id='grafico-barras-dias' style='scroll-margin-top: 100px;'></div>", unsafe_allow_html=True)

    # 1. Agrupa por dia da semana e causa para contar as ocorrências
    df_agrupado = df.groupby(['dia_semana', 'causa_acidente']).size().reset_index(name='Total')
    
    # 2. Ordena e pega o Top 2 causas de cada dia da semana
    df_top2_dia = df_agrupado.sort_values(['dia_semana', 'Total'], ascending=[True, False])
    df_top2_dia = df_top2_dia.groupby('dia_semana').head(2).copy()
    
    # Adiciona identificador de Posição ('Causa #1' ou 'Causa #2')
    df_top2_dia['Posicao'] = df_top2_dia.groupby('dia_semana').cumcount() + 1
    df_top2_dia['Posicao'] = df_top2_dia['Posicao'].apply(lambda x: f'Causa #{x}')
    
    # Ordena os dias da semana cronologicamente
    ordem_dias = ['segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira', 'sábado', 'domingo']
    df_top2_dia['dia_semana'] = pd.Categorical(df_top2_dia['dia_semana'], categories=ordem_dias, ordered=True)
    df_top2_dia = df_top2_dia.sort_values('dia_semana')

    # 3. Criação do gráfico agrupado no Plotly
    fig = px.bar(
        df_top2_dia,
        x='dia_semana',
        y='Total',
        color='Posicao',
        barmode='group',
        text='Total',
        custom_data=['causa_acidente'],
        color_discrete_map={
            'Causa #1': 'rgba(0, 243, 255, 0.75)',
            'Causa #2': 'rgba(0, 119, 182, 0.85)'
        }
    )
    
    # Configuração dos rótulos diretos e tooltip
    fig.update_traces(
        textposition='outside',
        texttemplate='%{text:,}',
        textfont=dict(color='#FFFFFF', size=13),
        hovertemplate='<b>%{x}</b><br><b>%{data.name}:</b> %{customdata[0]}<br>Total: %{y:,}<extra></extra>'
    )
    
    # Estilização do Layout
    fig.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        showlegend=False, # Oculta a legenda interna do Plotly pois já usamos a lateral
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        margin=dict(t=30, b=20, l=10, r=10),
        xaxis=dict(tickfont=dict(color='#FFFFFF', size=12)),
        yaxis=dict(showticklabels=False)
    )
    
    # 4. Renderização no Streamlit (Divisão 75% / 25%)
    col_grafico, col_legenda = st.columns([2, 1])
    
    with col_grafico:
        st.plotly_chart(fig, use_container_width=True)
        
    with col_legenda:
        st.markdown("""
            <div style="background: rgba(10, 25, 47, 0.6); padding: 15px; border-radius: 8px; border: 1px solid rgba(0, 243, 255, 0.3); margin-top: 25px;">
                <h5 style="color: #00F3FF; margin-top: 0; font-size: 17px;">Legenda das Causas</h5>
                <p style="font-size: 16px; color: #FFFFFF; margin-bottom: 8px;">
                    <b style="color: #00F3FF;">■ Causa #1:</b> Principal causador do dia.
                </p>
                <p style="font-size: 14px; color: #FFFFFF; margin-bottom: 8px;">
                    <b style="color: #0077B6;">■ Causa #2:</b> Segunda maior ocorrência no mesmo dia.
                </p>
                <hr style="border: 0.5px solid rgba(0, 243, 255, 0.2); margin: 10px 0;">
                <p style="font-size: 14px; color: #A0AEC0; margin: 0;">
                    Passe o mouse sobre as barras para ver a causa exata em cada dia.
                </p>
            </div>
        """, unsafe_allow_html=True)





















def criar_kpis_ato3(df):
    st.title("Ato 3: Proposta de Intervenção e Fechamento")
    st.markdown("---")

    # CSS do Ato 3 para alinhar o espaçamento
    st.markdown(
        """
        <style>
            div[data-testid="stHorizontalBlock"] {
                margin-bottom: 2rem !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    total = len(df)
    if total == 0:
        st.warning("Nenhum dado disponível.")
        return

    # --- CALCULOS DOS 3 KPIS ---

    # KPI 1: Janela Crítica (16h às 20h)
    # Extrai as horas da coluna 'horario' (ex: '19:00:00' -> 19)
    df_temp = df.copy()
    horas = pd.to_datetime(df_temp['horario'].astype(str), format='%H:%M:%S', errors='coerce').dt.hour
    
    # Filtra entre 16h e 20h (inclusive)
    acidentes_pico = horas.between(16, 20).sum()
    pct_janela_critica = (acidentes_pico / total) * 100

    # KPI 2: Sentido Crescente
    qtd_crescente = (df['sentido_via'].astype(str).str.strip().str.lower() == 'crescente').sum()
    pct_crescente = (qtd_crescente / total) * 100

    # KPI 3: Hotspots na BR Líder (BR-153)
    br_series = df['br'].astype(str).str.extract(r'(\d+)')[0] # Extrai número da BR
    br_top1 = br_series.mode()[0] if not br_series.empty else "153"
    
    # Filtra os KMs únicos da BR mais crítica
    df_br_top = df[br_series == br_top1]
    kms_criticos = df_br_top['km'].nunique()

    # CSS cirúrgico para forçar largura 100% e alinhamento central em todos os sub-elementos da métrica
    st.markdown("""
        <style>
            [data-testid="stMetric"] {
                display: flex !important;
                flex-direction: column !important;
                align-items: center !important;
                justify-content: center !important;
                text-align: center !important;
                width: 100% !important;
            }
            [data-testid="stMetricLabel"], 
            [data-testid="stMetricValue"], 
            [data-testid="stMetricDelta"] {
                width: 100% !important;
                display: flex !important;
                justify-content: center !important;
                text-align: center !important;
            }
            /* Garante que o texto dentro das divs filhas também fique centralizado */
            [data-testid="stMetricLabel"] > div, 
            [data-testid="stMetricValue"] > div {
                width: 100% !important;
                text-align: center !important;
            }
        </style>
    """, unsafe_allow_html=True)

    # --- RENDERIZAÇÃO DOS 3 CARDS ---
    kpi1, kpi2, kpi3 = st.columns(3)

    with kpi1:
        st.metric(
            label="Janela Crítica (16h - 20h)", 
            value=f"{pct_janela_critica:.1f}%"
        )

    with kpi2:
        st.metric(
            label="Fluxo Sentido Crescente", 
            value=f"{pct_crescente:.1f}%"
        )

    with kpi3:
        st.metric(
            label=f"Hotspots KMs (BR-{br_top1})", 
            value=f"{kms_criticos} Trechos"
        )

    st.markdown("---")

    # Espaçador idêntico ao respiro vertical da Página 2
    st.markdown('<div style="margin-top: 1.5rem;"></div>', unsafe_allow_html=True)





def criar_fig_acidentes_por_hora(df):
    """
    Cria um gráfico de linha com marcadores para acidentes das 0h às 23h,
    agrupando os minutos na hora cheia e ocupando a largura total da tela.
    """
    # 1. Garante a extração da hora (independente se veio como string '14:30' ou datetime)
    df_temp = df.copy()
    
    if pd.api.types.is_string_dtype(df_temp['horario']):
        # Extrai os dois primeiros dígitos antes dos dois pontos (ex: '14:30' -> 14)
        horas_extraidas = df_temp['horario'].str.split(':').str[0].astype(int)
    else:
        # Caso já seja datetime/time do pandas
        horas_extraidas = pd.to_datetime(df_temp['horario'], format='%H:%M:%S', errors='coerce').dt.hour
    
    # 2. Contagem por hora
    contagem_horas = horas_extraidas.value_counts().reset_index()
    contagem_horas.columns = ['Hora', 'Total']
    
    # 3. Garante que todas as 24 horas (0 a 23) existam na tabela, mesmo com 0 acidentes
    df_24h = pd.DataFrame({'Hora': list(range(24))})
    df_completo = pd.merge(df_24h, contagem_horas, on='Hora', how='left').fillna(0)
    df_completo['Total'] = df_completo['Total'].astype(int)
    df_completo['Hora_Label'] = df_completo['Hora'].apply(lambda x: f"{x:02d}:00h")

    # 4. Construção do Gráfico com Plotly Graph Objects
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df_completo['Hora_Label'],
            y=df_completo['Total'],
            mode='lines+markers',
            name='Acidentes',
            line=dict(color='#00F3FF', width=3),               # Linha Cyan Neon
            marker=dict(size=8, color='#08519c', line=dict(color='#00F3FF', width=2)), # Ponto com borda neon
            hovertemplate='<b>%{x}</b><br>Total: <b>%{y} acidentes</b><extra></extra>'
        )
    )

    # 5. Estilização alinhada com o visual escuro/transparente
    fig.update_layout(
        margin=dict(t=20, b=30, l=20, r=10), 
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        hoverlabel=dict(bgcolor='#111827', font_color='#FFFFFF', font_size=13),
        xaxis=dict(
            title=dict(text="Horário do Dia", font=dict(color='#A0AEC0')),
            showgrid=False,
            zeroline=False,
            tickangle=0,
            tickfont=dict(color='#A0AEC0'),
            range=[-0.2, len(df_completo['Hora_Label']) - 0.8] # Estica o gráfico até as pontas
        ),
        yaxis=dict(
            title=dict(text="Quantidade de Acidentes", font=dict(color='#A0AEC0')),
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.08)', # Linhas de grade bem discretas
            zeroline=False,
            tickfont=dict(color='#A0AEC0')
        )
    )

    return fig





def criar_fig_sentido_bipolar(df):
    """
    Gera gráfico de barras bipolares/divergentes para comparar Sentido Crescente vs Decrescente.
    """
    # 1. Filtra apenas os sentidos principais
    df_sentido = df[df['sentido_via'].isin(['Crescente', 'Decrescente'])].copy()
    
    # 2. Agrupa a contagem
    contagem = df_sentido['sentido_via'].value_counts().reset_index()
    contagem.columns = ['Sentido', 'Total']
    
    qtd_crescente = contagem[contagem['Sentido'] == 'Crescente']['Total'].values[0] if 'Crescente' in contagem['Sentido'].values else 0
    qtd_decrescente = contagem[contagem['Sentido'] == 'Decrescente']['Total'].values[0] if 'Decrescente' in contagem['Sentido'].values else 0
    
    # 3. DataFrame divergente (Decrescente negativo para ir à esquerda)
    df_bipolar = pd.DataFrame({
        'Categoria': ['Fluxo da Via'],
        'Crescente': [qtd_crescente],
        'Decrescente': [-qtd_decrescente]
    })

    # 4. Gráfico Plotly
    fig = px.bar(
        df_bipolar,
        y='Categoria',
        x=['Decrescente', 'Crescente'],
        orientation='h',
        color_discrete_map={
            'Crescente': '#2171b5',   # Azul vibrante
            'Decrescente': '#08306b'  # Azul marinho profundo
        }
    )

    # Ajuste de tooltip/hover
    fig.update_traces(
        hovertemplate='<b>%{data.name}</b><br>Total: %{customdata:,}<extra></extra>'
    )
    fig.data[0].customdata = [qtd_decrescente]
    fig.data[1].customdata = [qtd_crescente]

    # Rótulos diretos sobre as barras
    fig.add_annotation(
        x=-qtd_decrescente / 2, y=0,
        text=f"Decrescente<br><b>{qtd_decrescente:,}</b>",
        showarrow=False,
        font=dict(color='#FFFFFF', size=13)
    )
    fig.add_annotation(
        x=qtd_crescente / 2, y=0,
        text=f"Crescente<br><b>{qtd_crescente:,}</b>",
        showarrow=False,
        font=dict(color='#FFFFFF', size=13)
    )

    # 5. Layout com fundo transparente
    fig.update_layout(
        barmode='relative',
        showlegend=False,
        xaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=True,
            zerolinecolor='#FFFFFF',
            zerolinewidth=1.5
        ),
        yaxis=dict(showticklabels=False, showgrid=False),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=10, b=10, l=10, r=10),
        height=260
    )
    
    return fig


def renderizar_secao_sentido_via(df):
    """
    Função principal que renderiza a seção completa de Sentido da Via em 2 colunas,
    mantendo o padrão visual e de isolamento de tela (F11) do Ato 1.
    """
    # 1. Espaçador no mesmo padrão do Ato 1 (empurra o bloco para o topo da tela)
    st.markdown("<div style='margin-bottom: 35vh;'></div>", unsafe_allow_html=True)

    # 2. Layout em 2 Colunas
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Direcionamento do Fluxo (Sentido da Via)")
        fig_sentido = criar_fig_sentido_bipolar(df)
        st.plotly_chart(fig_sentido, use_container_width=True)

    with col2:
        st.subheader("Análise Estratégica do Fluxo")
        st.markdown("""
        <div style="background-color: #111827; padding: 20px; border-radius: 8px; border-left: 4px solid #2171b5; color: #FFFFFF; min-height: 260px;">
            <h4 style="margin-top: 0; color: #4292c6; font-size: 16px;">Dinâmica Pendular e Retorno ao Lar</h4>
            <p style="font-size: 14px; line-height: 1.5; color: #E2E8F0; margin-bottom: 12px;">
                A maior concentração no <b>Sentido Crescente (3.581 acidentes)</b> reflete o padrão de mobilidade das cidades polos empregatícias. 
                O pico de ocorrências coincide com a janela do final do dia, no trajeto de volta para casa, onde o cansaço do condutor amplia o risco.
            </p>
            <p style="font-size: 13px; line-height: 1.4; color: #94A3B8; margin-bottom: 0;">
                <b>Nota:</b> O volume expressivo no sentido decrescente (2.904 acidentes) valida que os polos de atração também geram fluxo inverso relevante nos trechos limítrofes.
            </p>
        </div>
        """, unsafe_allow_html=True)



import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


# ==============================================================================
# BLOCO 0: FUNÇÃO UTILITÁRIA DE FATOR DOMINANTE (Posicionada no escopo global)
# Extrai o item com maior frequência em uma série, calculando sua porcentagem
# e formatando empates com barra (ex: "Fator A / Fator B (40% cada)").
# ==============================================================================
def extrair_fator_dominante(serie):
    s_clean = serie.dropna().astype(str).str.strip()
    s_clean = s_clean[s_clean.str.lower() != 'não informado']

    if s_clean.empty:
        return 'N/I'

    contagem = s_clean.value_counts()
    total = len(s_clean)
    max_freq = contagem.max()

    top_itens = contagem[contagem == max_freq]
    pct = (max_freq / total) * 100

    if len(top_itens) > 1:
        nomes = ' / '.join([item.title() for item in top_itens.index])
        return f'{nomes} ({pct:.0f}% cada)'

    nome_unico = top_itens.index[0].title()
    return f'{nome_unico} ({pct:.0f}%)'


# ==============================================================================
# FUNÇÃO PRINCIPAL DA SEÇÃO DO MAPA
# ==============================================================================
def renderizar_secao_mapa_hotspots_interativo(df):
    """Renderiza o Mapa Interativo de Hotspots em fatias de 10km (80% da tela)

    e o Painel Lateral de Controle/Card Informativo (20% da tela).
    """
    # CSS customizado para os botões do st.radio: vazados/transparentes com borda destacada
    st.markdown(
        """
        <style>
            div[data-testid="stRadio"] > label {
                display: none !important;
            }
            div[data-testid="stRadio"] div[role="radiogroup"] {
                gap: 10px !important;
                width: 100% !important;
            }
            div[data-testid="stRadio"] div[role="radiogroup"] label {
                background: transparent !important;
                border: 1.5px solid #334155 !important;
                border-radius: 8px !important;
                padding: 12px 14px !important;
                color: #FFFFFF !important;
                font-weight: 600 !important;
                font-size: 13px !important;
                text-align: center !important;
                width: 100% !important;
                transition: all 0.2s ease-in-out !important;
                cursor: pointer !important;
            }
            div[data-testid="stRadio"] div[role="radiogroup"] label p,
            div[data-testid="stRadio"] div[role="radiogroup"] label span {
                color: #FFFFFF !important;
            }
            div[data-testid="stRadio"] div[role="radiogroup"] label:hover {
                border-color: #38BDF8 !important;
                box-shadow: 0px 0px 8px rgba(56, 189, 248, 0.3) !important;
            }
            div[data-testid="stRadio"] div[role="radiogroup"] label[data-checked="true"],
            div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) {
                background: rgba(56, 189, 248, 0.1) !important;
                border-color: #38BDF8 !important;
                box-shadow: 0px 0px 10px rgba(56, 189, 248, 0.4) !important;
            }
            div[data-testid="stRadio"] div[role="radiogroup"] label[data-checked="true"] p,
            div[data-testid="stRadio"] div[role="radiogroup"] label[data-checked="true"] span {
                color: #38BDF8 !important;
                font-weight: bold !important;
            }
            div[data-testid="stRadio"] div[role="radiogroup"] label > div:first-child {
                display: none !important;
            }
        </style>
    """,
        unsafe_allow_html=True,
    )

    # ==============================================================================
    # BLOCO 1: TRATAMENTO DO HORÁRIO DO DATAFRAME
    # Garante a extração da hora inteira (hora_int) a partir da coluna de horário
    # para permitir a filtragem por janelas temporais.
    # ==============================================================================
    df_temp = df.copy()
    if 'horario' in df_temp.columns:
        if pd.api.types.is_string_dtype(df_temp['horario']):
            df_temp['hora_int'] = pd.to_numeric(
                df_temp['horario'].str.split(':').str[0], errors='coerce'
            ).fillna(0)
        else:
            df_temp['hora_int'] = pd.to_datetime(
                df_temp['horario'].astype(str), format='%H:%M:%S', errors='coerce'
            ).dt.hour.fillna(0)
    else:
        df_temp['hora_int'] = 0

    # ==============================================================================
    # BLOCO 2: DIVISÃO DA TELA EM COLUNAS
    # Cria a proporção de 80% (4 partes) para a área visual do mapa e 20% (1 parte)
    # para a área de controles e cards laterais.
    # ==============================================================================
    col_mapa, col_controle = st.columns([4, 1])

    # ==============================================================================
    # BLOCO 3: FILTRO LATERAL E SELEÇÃO DE JANELA TEMPORAL
    # Renderiza os seletores de janela (Geral vs. Pendular) na coluna de controle
    # e aplica o filtro correspondente no DataFrame.
    # ==============================================================================
    with col_controle:
        st.markdown(
            "<p style='color: #FFFFFF !important; font-size: 13px; margin-bottom:"
            " 8px; font-weight: bold;'>JANELA DE ANÁLISE</p>",
            unsafe_allow_html=True,
        )

        opcao_filtro = st.radio(
            label='Selecione a Janela:',
            options=['Visão Geral (24 Horas)', 'Janela Crítica (16h-20h)'],
            index=0,
            key='filtro_mapa_ato3',
        )

        is_pendular = opcao_filtro == 'Janela Crítica (16h-20h)'

        if is_pendular:
            df_filtrado = df_temp[df_temp['hora_int'].between(16, 20)]
        else:
            df_filtrado = df_temp

# ==============================================================================
    # BLOCO 4: AGRUPAMENTO EM TRECHOS DE 5 KM E FATORES DOMINANTES
    # Filtra os dados válidos de localização, agrupa por BR/Trecho de 5km e calcula
    # as métricas de total de acidentes, divisão de sentidos, causa e tipo dominantes.
    # ==============================================================================
    if not df_filtrado.empty and 'km' in df_filtrado.columns:
        df_filtrado['km_num'] = pd.to_numeric(df_filtrado['km'], errors='coerce')
        df_valid = df_filtrado.dropna(
            subset=['km_num', 'latitude', 'longitude']
        ).copy()

        # Criação do trecho de 5 km
        df_valid['trecho_5km'] = (df_valid['km_num'] // 5) * 5

        # Lógica de cálculo por trecho de 5 km
        def calcular_percentual_sentido(sub_df):
            # Filtra 'Não Informado'
            sentidos = sub_df[
                sub_df['sentido_via'].astype(str).str.lower() != 'não informado'
            ]['sentido_via']
            total = len(sentidos)
            if total == 0:
                return 'N/I'
            cres = (sentidos.astype(str).str.lower() == 'crescente').sum()
            pct_cres = (cres / total) * 100
            pct_dec = 100 - pct_cres
            return f'{pct_cres:.0f}% Crescente | {pct_dec:.0f}% Decrescente'

# Agrupando por BR e Trecho de 5 km
        agrupados = []
        for (br_val, trecho_val), g in df_valid.groupby(['br', 'trecho_5km']):
            total_ac = len(g)

            # Filtro de significância: ignora trechos com menos de 10 acidentes
            if total_ac < 10:
                continue

            lat_m = g['latitude'].mean()
            lon_m = g['longitude'].mean()
            pct_sentido_trecho = calcular_percentual_sentido(g)

            # Extração da causa e tipo dominantes do trecho local
            causa_top1 = (
                extrair_fator_dominante(g['causa_acidente'])
                if 'causa_acidente' in g.columns
                else 'N/I'
            )
            tipo_top1 = (
                extrair_fator_dominante(g['tipo_acidente'])
                if 'tipo_acidente' in g.columns
                else 'N/I'
            )

            agrupados.append({
                'br': str(br_val).split('.')[0],
                'trecho_5km': trecho_val,
                'rotulo_trecho': f'KM {int(trecho_val)} - {int(trecho_val)+5}',
                'latitude': lat_m,
                'longitude': lon_m,
                'total_acidentes': total_ac,
                'pct_sentido_trecho': pct_sentido_trecho,
                'causa_top1': causa_top1,
                'tipo_top1': tipo_top1,
            })

        df_mapa = pd.DataFrame(agrupados)
    else:
        df_mapa = pd.DataFrame()

# ==============================================================================
    # BLOCO 5: RENDERIZAÇÃO DO CARD EXPLICATIVO PENDULAR NO PAINEL LATERAL
    # Exibe no painel lateral um resumo com a Causa #1, Tipo #1 e Divisão de Sentidos
    # para o intervalo das 16h às 20h.
    # ==============================================================================
    with col_controle:
        if is_pendular and not df_filtrado.empty:
            # Causa #1 Global
            causa_top1 = (
                str(df_filtrado['causa_acidente'].mode().iloc[0]).title()
                if 'causa_acidente' in df_filtrado.columns
                and not df_filtrado['causa_acidente'].dropna().empty
                else 'N/A'
            )

            # Tipo #1 Global
            tipo_top1 = (
                str(df_filtrado['tipo_acidente'].mode().iloc[0]).title()
                if 'tipo_acidente' in df_filtrado.columns
                and not df_filtrado['tipo_acidente'].dropna().empty
                else 'N/A'
            )

            # Sentido % Global (filtra 'não informado' de forma insensível a maiúsculas/minúsculas)
            sentidos_validos = df_filtrado[
                df_filtrado['sentido_via'].astype(str).str.lower() != 'não informado'
            ]['sentido_via']
            
            total_sent = len(sentidos_validos)
            if total_sent > 0:
                p_cres = (sentidos_validos.astype(str).str.lower() == 'crescente').sum() / total_sent * 100
                p_dec = 100 - p_cres
                str_sentido = f'{p_cres:.1f}% Crescente | {p_dec:.1f}% Decrescente'
            else:
                str_sentido = 'N/A'

            # Estilização do Card em HTML
            card_html = (
                f'<div style="background: transparent; border: 1.5px solid #38BDF8; padding: 14px; border-radius: 8px; margin-top: 15px; box-shadow: 0px 0px 8px rgba(56, 189, 248, 0.25);">'
                f'<p style="color: #FFFFFF !important; font-size: 11px; margin-bottom: 6px; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px;">RESUMO DAS 16H ÀS 20H</p>'
                f'<p style="color: #94A3B8 !important; font-size: 10px; margin: 8px 0 2px 0; font-weight: 600;">CAUSA #1</p>'
                f'<p style="color: #FFFFFF !important; font-size: 12px; font-weight: 600; margin: 0;">{causa_top1}</p>'
                f'<p style="color: #94A3B8 !important; font-size: 10px; margin: 8px 0 2px 0; font-weight: 600;">TIPO DE ACIDENTE #1</p>'
                f'<p style="color: #FFFFFF !important; font-size: 12px; font-weight: 600; margin: 0;">{tipo_top1}</p>'
                f'<p style="color: #94A3B8 !important; font-size: 10px; margin: 8px 0 2px 0; font-weight: 600;">DIVISÃO DOS SENTIDOS</p>'
                f'<p style="color: #38BDF8 !important; font-size: 12px; font-weight: bold; margin: 0;">{str_sentido}</p>'
                f'</div>'
            )

            st.markdown(card_html, unsafe_allow_html=True)

# ==============================================================================
    # BLOCO 6: RENDERIZAÇÃO DO MAPA NA COLUNA PRINCIPAL
    # Desenha o mapa interativo Plotly com os hotspots de acidentes nas BRs,
    # alternando os detalhes do tooltip (hover) entre a Visão Geral e a Janela Crítica.
    # ==============================================================================
    with col_mapa:
        st.subheader('Mapeamento Geográfico de Hotspots das BRs')

        if not df_mapa.empty:
            if is_pendular:
                # Hover no Pendular inclui Sentido, Causa e Tipo
                fig_mapa = px.scatter_mapbox(
                    df_mapa,
                    lat='latitude',
                    lon='longitude',
                    size='total_acidentes',
                    color='total_acidentes',
                    color_continuous_scale='Reds',
                    range_color=[0, 10], # <--- Destaca as cores dos trechos a partir de 10 acidentes
                    size_max=28,
                    zoom=6.5,
                    center=dict(lat=-16.6869, lon=-49.2648),
                    height=550,
                    hover_name='rotulo_trecho',
                    hover_data={
                        'br': True,                 # customdata[0]
                        'total_acidentes': True,    # customdata[1]
                        'pct_sentido_trecho': True, # customdata[2]
                        'causa_top1': True,         # customdata[3]
                        'tipo_top1': True,          # customdata[4]
                        'latitude': False,
                        'longitude': False,
                    },
                    mapbox_style='open-street-map',
                )

                # Mantém as bolinhas bem visíveis e com contorno nítido
                fig_mapa.update_traces(
                    marker=dict(
                        sizemin=8, # Tamanho mínimo para não sumir no mapa
                        opacity=0.9,
                    )
                )
                fig_mapa.update_traces(
                    hovertemplate=(
                        '<b>BR-%{customdata[0]} | %{hovertext}</b><br><br>'
                        'Total de Acidentes: <b>%{customdata[1]}</b><br>'
                        'Divisão dos Sentidos: <b>%{customdata[2]}</b><br>'
                        'Causa Dominante: <b>%{customdata[3]}</b><br>'
                        'Tipo de Acidente: <b>%{customdata[4]}</b><extra></extra>'
                    )
                )
            else:
                # Hover Geral mostra apenas BR, Trecho e Total
                fig_mapa = px.scatter_mapbox(
                    df_mapa,
                    lat='latitude',
                    lon='longitude',
                    size='total_acidentes',
                    color='total_acidentes',
                    color_continuous_scale='Reds',
                    range_color=[10, 60], # <--- Calibra a escala para dar destaque às bolinhas a partir de 10 acidentes
                    size_max=28,
                    zoom=6.5,
                    center=dict(lat=-16.6869, lon=-49.2648),
                    height=550,
                    hover_name='rotulo_trecho',
                    hover_data={
                        'br': True,              # customdata[0]
                        'total_acidentes': True, # customdata[1]
                        'latitude': False,
                        'longitude': False,
                    },
                    mapbox_style='open-street-map',
                )

                # Mantém as bolinhas bem visíveis e com contorno nítido
                fig_mapa.update_traces(
                    marker=dict(
                        sizemin=8, # Tamanho mínimo para garantir visibilidade
                        opacity=0.9,
                    )
                )
                fig_mapa.update_traces(
                    hovertemplate=(
                        '<b>BR-%{customdata[0]} | %{hovertext}</b><br><br>'
                        'Total de Acidentes: <b>%{customdata[1]}</b><extra></extra>'
                    )
                )

            fig_mapa.update_layout(
                margin=dict(l=0, r=0, t=0, b=0),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                coloraxis_showscale=False,
            )

            st.plotly_chart(
                fig_mapa, use_container_width=True, key='mapa_hotspots_ato3'
            )
        else:
            st.warning(
                'Nenhum dado encontrado para os filtros selecionados ou falta de'
                ' coordenadas/KM.'
            )