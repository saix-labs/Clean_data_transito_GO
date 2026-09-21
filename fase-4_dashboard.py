import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Configuração inicial da página
st.set_page_config(
    page_title="Dashboard - Segurança Viária GO",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Estilização CSS profissional e legível
st.markdown("""
    <style>
    /* Fundo da tela central */
    .stApp {
        background-color: #0b132b;
        color: #ffffff;
    }
    
    /* Fundo da barra lateral */
    section[data-testid="stSidebar"] {
        background-color: #1c2541 !important;
    }
    
    /* Forçar a cor branca em todos os textos da barra lateral */
    section[data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    
    /* Ajuste de cor do título e divisores */
    h1, h2, h3 {
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Barra Lateral (Sidebar)
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

# 4. Área de Conteúdo Central
if pagina == "Ato 1: Panorama Geral":
    st.header("Ato 1: Panorama Geral dos Acidentes")
    st.write("Visão macro dos dados em Goiás.")

elif pagina == "Ato 2: Investigação e Hotspots":
    st.header("Ato 2: Investigação e Mapeamento")
    st.write("Análise espacial e causas dos sinistros.")

elif pagina == "Ato 3: Análise Temporal e Solução":
    st.header("Ato 3: Picos de Horário e Proposta Técnica")
    st.write("Detalhamento do sentido crescente e sonorizadores.")