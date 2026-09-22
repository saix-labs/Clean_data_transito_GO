import streamlit as st

def aplicar_estilos():
    st.markdown("""
        <style>
        /* === AJUSTE DO TOPO E CABEÇALHO === */
        header[data-testid="stHeader"] {
            background-color: #0b132b !important;
        }

        .block-container {
            padding-top: 2rem !important;
        }

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

        /* === BOTÕES DA SIDEBAR (ABRIR E FECHAR) EM ESTILO NEON === */
        button[data-testid="stExpandSidebarButton"],
        button[data-testid="stCollapseSidebarButton"] {
            background-color: #0b132b !important;
            border: 2px solid #00f3ff !important;
            border-radius: 8px !important;
            box-shadow: 0 0 10px rgba(0, 243, 255, 0.6) !important;
            transition: all 0.2s ease-in-out !important;
        }

        /* Cor do ícone das setas */
        button[data-testid="stExpandSidebarButton"] *,
        button[data-testid="stCollapseSidebarButton"] * {
            color: #00f3ff !important;
            fill: #00f3ff !important;
        }

        /* Efeito de destaque ao passar o mouse */
        button[data-testid="stExpandSidebarButton"]:hover,
        button[data-testid="stCollapseSidebarButton"]:hover {
            background-color: #00f3ff !important;
            box-shadow: 0 0 18px #00f3ff !important;
        }

        button[data-testid="stExpandSidebarButton"]:hover *,
        button[data-testid="stCollapseSidebarButton"]:hover * {
            color: #0b132b !important;
            fill: #0b132b !important;
        }

        /* === RESPIRO/ESPAÇAMENTO ENTRE LINHAS DO DASHBOARD === */
        div[data-testid="stHorizontalBlock"] {
            margin-bottom: 3.5rem !important;
        }
        </style>
    """, unsafe_allow_html=True)