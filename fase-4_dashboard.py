import streamlit as st
import pandas as pd
from estilos import aplicar_estilos
from graficos import (
    criar_fig_turno, 
    criar_fig_br, 
    criar_fig_pista, 
    criar_fig_clima, 
    criar_fig_mapa,
    criar_kpis_ato1,

    #ato 2
    criar_kpis_ato2,
    criar_fig_tracado,
    criar_fig_classificacao
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

if pagina == "Ato 1: Panorama Geral":
    criar_kpis_ato1(df)
    # (Chamadas dos gráficos do Ato 1 continuam aqui)

elif pagina == "Ato 2: Investigação e Hotspots":
    # 1. Topo: KPIs do Ato 2
    criar_kpis_ato2(df)
    
    st.markdown("---")
    
    # 2. Linha 1: Traçado da Via e Severidade
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top Traçados da Via")
        st.plotly_chart(criar_fig_tracado(df), use_container_width=True)

    with col2:
        st.subheader("Classificação dos Acidentes")
        st.plotly_chart(criar_fig_classificacao(df), use_container_width=True)


