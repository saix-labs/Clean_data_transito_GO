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
        
                /* Ajuste: Cor branca para textos e rótulos comuns da barra lateral */
        section[data-testid="stSidebar"] p, 
        section[data-testid="stSidebar"] span, 
        section[data-testid="stSidebar"] label {
            color: #ffffff !important;
        }

        /* Restaura TODOS os botões da barra lateral para o padrão nativo do Streamlit */
        section[data-testid="stSidebar"] button[key^="btn_menu_"] {
            width: 100% !important;
            margin-bottom: 12px !important;
            color: #ffffff !important;
        }

        
        /* Ajuste de cor do título e divisores */
        h1, h2, h3 {
            color: #ffffff !important;
        }

        /* === ESTILIZAÇÃO AZUL NEON PARA CARDS E MÉTRICAS === */
        /* Rótulos (Texto/Palavras do Top 5 e Cards de Métricas) */
        [data-testid="stMetricLabel"] {
            color: #ffffff !important;
            font-weight: bold !important;
            text-shadow: none !important;
        }
        
        /* Valores numéricos das métricas */
        [data-testid="stMetricValue"] {
            color: #FF1744 !important;
            text-shadow: 0 0 10px rgba(255, 23, 68, 0.6);
        }

        /* === BOTÃO DE EXPANDIR (FORA DA SIDEBAR) === */
        button[data-testid="stExpandSidebarButton"] {
            background-color: #0b132b !important;
            border: 2px solid #00f3ff !important;
            border-radius: 8px !important;
            box-shadow: 0 0 10px rgba(0, 243, 255, 0.6) !important;
            transition: all 0.2s ease-in-out !important;
        }

        button[data-testid="stExpandSidebarButton"] * {
            color: #00f3ff !important;
            fill: #00f3ff !important;
        }

        button[data-testid="stExpandSidebarButton"]:hover {
            background-color: #00f3ff !important;
            box-shadow: 0 0 18px #00f3ff !important;
        }

        button[data-testid="stExpandSidebarButton"]:hover * {
            color: #0b132b !important;
            fill: #0b132b !important;
        }

        /* === BOTÃO DE RECOLHER (DENTRO DA SIDEBAR - SEMPRE VISÍVEL) === */
        [data-testid="stSidebarHeader"] {
            opacity: 1 !important;
            visibility: visible !important;
        }

        button[data-testid="stCollapseSidebarButton"],
        [data-testid="stSidebarHeader"] button {
            background-color: #1c2541 !important;
            border: 2px solid #00f3ff !important;
            border-radius: 8px !important;
            box-shadow: 0 0 10px rgba(0, 243, 255, 0.6) !important;
            transition: all 0.2s ease-in-out !important;
            opacity: 1 !important;
            visibility: visible !important;
        }

        button[data-testid="stCollapseSidebarButton"] *,
        [data-testid="stSidebarHeader"] button * {
            color: #00f3ff !important;
            fill: #00f3ff !important;
            opacity: 1 !important;
        }

        button[data-testid="stCollapseSidebarButton"]:hover,
        [data-testid="stSidebarHeader"] button:hover {
            background-color: #00f3ff !important;
            box-shadow: 0 0 18px #00f3ff !important;
        }

        button[data-testid="stCollapseSidebarButton"]:hover *,
        [data-testid="stSidebarHeader"] button:hover * {
            color: #1c2541 !important;
            fill: #1c2541 !important;
        }

        /* === RESPIRO/ESPAÇAMENTO ENTRE LINHAS DO DASHBOARD === */
        div[data-testid="stHorizontalBlock"] {
            margin-bottom: 3.5rem !important;
        }
        </style>
    """, unsafe_allow_html=True)