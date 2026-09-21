import streamlit as st
import pandas as pd
from estilos import aplicar_estilos
from graficos import (
    criar_fig_turno, 
    criar_fig_br, 
    criar_fig_pista, 
    criar_fig_clima, 
    criar_fig_mapa
)

# 1. Configuração inicial da página
st.set_page_config(
    page_title="Dashboard - Segurança Viária GO",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Aplica o CSS do arquivo estilos.py
aplicar_estilos()

# 3. Carregamento dos dados com Cache (Otimizado)
@st.cache_data
def carregar_dados():
    caminho = r"C:\Users\ezequiel\OneDrive\Desktop\PI Trânsito GO\acidentes-GO-2024_2025_limpo.csv"
    df = pd.read_csv(caminho)
    return df

df = carregar_dados()

# 4. Barra Lateral (Sidebar)
with st.sidebar:
    st.title("Painel de Controle")
    st.markdown("---")
    
    pagina = st.radio(
        "Selecione a etapa de análise:",
        [
            "Ato 1: Panorama Geral",
            "Ato 2: Investigação e Hotspots",
            "Ato 3: Análise Temporal e Solução"
        ]
    )
    
    st.markdown("---")
    st.caption("Análise de Sinistros de Trânsito - PRF / GO")

# 5. Navegação das Páginas
if pagina == "Ato 1: Panorama Geral":
    st.title("Ato 1: O Panorama Geral")
    st.markdown("---")

    # --- CARDS DE KPI (TOPO) ---
    total_acidentes = len(df)
    br_mais_critica = f"BR-{df['br'].mode()[0]}"

    pct_pista_dupla = (df['tipo_pista'].str.contains('Múltipla|Dupla', case=False, na=False).sum() / total_acidentes) * 100
    pct_ceu_claro = (df['condicao_metereologica'].str.contains('Céu Claro|Sol', case=False, na=False).sum() / total_acidentes) * 100

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        st.metric(label="Total de Acidentes", value=f"{total_acidentes:,}".replace(",", "."))

    with kpi2:
        st.metric(label="BR com Maior Volume", value=br_mais_critica)

    with kpi3:
        st.metric(label="Acidentes em Pista Dupla/Múltipla", value=f"{pct_pista_dupla:.1f}%")

    with kpi4:
        st.metric(label="Acidentes com Tempo Bom", value=f"{pct_ceu_claro:.1f}%")

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

    st.markdown("### 🏆 Top 5 Municípios com Maior Registro de Acidentes")

    top5_cidades = df_municipio.head(5)

    col_t1, col_t2, col_t3, col_t4, col_t5 = st.columns(5)
    cols = [col_t1, col_t2, col_t3, col_t4, col_t5]

    for i, row in top5_cidades.iterrows():
        with cols[i]:
            st.metric(
                label=f"{i+1}º {row['Município'].title()}", 
                value=f"{row['Total de Acidentes']:,}".replace(",", ".")
            )

elif pagina == "Ato 2: Investigação e Hotspots":
    st.header("Ato 2: Investigação e Mapeamento")
    st.write("Análise espacial e causas dos sinistros.")

elif pagina == "Ato 3: Análise Temporal e Solução":
    st.header("Ato 3: Picos de Horário e Proposta Técnica")
    st.write("Detalhamento do sentido crescente e sonorizadores.")