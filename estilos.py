import streamlit as st

def aplicar_estilos():
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

        /* === ESTILIZAÇÃO AZUL NEON PARA CARDS E MÉTRICAS === */
        /* Rótulos (Texto/Palavras do Top 5 e Cards de Métricas) */
        [data-testid="stMetricLabel"] {
            color: #00f3ff !important;
            font-weight: bold !important;
            text-shadow: 0 0 8px rgba(0, 243, 255, 0.4);
        }
        
        /* Valores numéricos das métricas */
        [data-testid="stMetricValue"] {
            color: #ffffff !important;
            text-shadow: 0 0 10px rgba(0, 243, 255, 0.6);
        }

        /* === RESPIRO/ESPAÇAMENTO ENTRE LINHAS DO DASHBOARD === */
        div[data-testid="stHorizontalBlock"] {
            margin-bottom: 3.5rem !important;
        }
        </style>
    """, unsafe_allow_html=True)