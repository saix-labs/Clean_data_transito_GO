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
                /* === ESTILIZAÇÃO COMPATÍVEL DOS BOTÕES DA SIDEBAR === */
        
        /* 1. Design base para os botões de navegação na sidebar */
        section[data-testid="stSidebar"] div.stButton > button {
            background-color: transparent !important;
            border: 1px solid rgba(255, 23, 68, 0.4) !important; /* Borda vermelha discreta */
            color: #A0AEC0 !important; /* Texto cinza elegante */
            width: 100% !important;
            padding: 14px 12px !important;
            border-radius: 6px !important;
            box-shadow: 0px 0px 8px rgba(255, 23, 68, 0.1) !important; /* Neon bem suave */
            font-weight: 600 !important;
            font-size: 13px !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
            transition: all 0.25s ease-in-out !important;
            margin-bottom: 12px !important;
        }

        /* 2. EFEITO HOVER: Acende o vermelho neon ao passar o mouse */
        section[data-testid="stSidebar"] div.stButton > button:hover {
            border-color: #FF1744 !important;
            color: #FFFFFF !important;
            box-shadow: 0px 0px 16px rgba(255, 23, 68, 0.8) !important; /* Brilho neon expandido */
            background-color: rgba(255, 23, 68, 0.08) !important;
            transform: translateY(-1px);
        }

        /* 3. DESIGN DO BOTÃO ATIVO: Como os botões comuns mudam de cor ao serem clicados nativamente, 
           o Streamlit aplica um estado de foco/active. Para garantir que ele fique fixo com fundo preenchido 
           na página atual, adicionamos a regra de clique ativo: */
        section[data-testid="stSidebar"] div.stButton > button:active,
        section[data-testid="stSidebar"] div.stButton > button:focus {
            border: 1.5px solid #FF1744 !important;
            color: #FFFFFF !important;
            background-color: rgba(255, 23, 68, 0.22) !important; /* Fundo estável da página ativa */
            box-shadow: 0px 0px 18px rgba(255, 23, 68, 0.85) !important; /* Brilho máximo */
        }
        </style>
    """, unsafe_allow_html=True)