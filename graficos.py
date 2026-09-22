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
    fig.update_traces(textinfo='percent+label')
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
        color='Total',
        color_continuous_scale='Blues'
    )
    fig.update_layout(
        yaxis={'categoryorder':'total ascending'}, 
        showlegend=False, 
        coloraxis_showscale=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
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
        font=dict(color='white')
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
        font=dict(color='white')
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
    total = len(df)
    if total == 0:
        st.warning("Nenhum dado disponível.")
        return

    # 1. Traçado Predominante (Ocorrências em trecho que contém Reta)
    qtd_reta = df['tracado_via'].astype(str).str.contains('Reta', case=False, na=False).sum()
    pct_reta = (qtd_reta / total) * 100

    # 2. Gravidade Controlada (Feridos + Sem Vítimas = Não Fatais)
    qtd_controlada = df['classificacao_acidente'].isin(['Com Vítimas Feridas', 'Sem Vítimas']).sum()
    pct_controlada = (qtd_controlada / total) * 100

    # 3. Causa Principal #1
    causa_series = df['causa_acidente'].dropna()
    causa_top1 = causa_series.mode()[0] if not causa_series.empty else "N/A"
    
    # Tratamento para truncar/formatar nome da causa no card
    if "Reação tardia" in causa_top1 or "ineficiente" in causa_top1:
        causa_exibicao = "Reação Tardia / Ineficiente"
    elif len(causa_top1) > 22:
        causa_exibicao = causa_top1[:22] + "..."
    else:
        causa_exibicao = causa_top1

    # 4. Dias Úteis (segunda a sexta)
    dias_uteis = ['segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira']
    qtd_dias_uteis = df['dia_semana'].astype(str).str.lower().isin(dias_uteis).sum()
    pct_dias_uteis = (qtd_dias_uteis / total) * 100

    # Renderização visual dos 4 cards de KPI
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Traçado Predominante",
            value=f"{pct_reta:.1f}%",
            delta="Trechos Retos"
        )

    with col2:
        st.metric(
            label="Acidentes Não Fatais",
            value=f"{pct_controlada:.1f}%",
            delta="Feridos + Sem Vítimas"
        )

    with col3:
        st.metric(
            label="Causa Principal #1",
            value=causa_exibicao,
            delta="Fator Humano Top 1"
        )

    with col4:
        st.metric(
            label="Acidentes em Dias Úteis",
            value=f"{pct_dias_uteis:.1f}%",
            delta="Segunda a Sexta"
        )
