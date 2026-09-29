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

    #Parte 2
    criar_kpis_ato2,
    criar_fig_tracado,
    criar_fig_classificacao,
    criar_fig_causa_funnel,
    criar_fig_tipo_treemap,
    renderizar_infografico_dias,
    criar_fig_top2_causa_dia,

 
    #Parte 3
    criar_kpis_ato3,
    criar_fig_acidentes_por_hora,
    renderizar_secao_sentido_via,
    renderizar_secao_mapa_hotspots_interativo,
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
    st.write("Selecione a etapa de análise:")

    # Inicializa a página padrão no estado da sessão caso não exista
    if "pagina" not in st.session_state:
        st.session_state.pagina = "Ato 1: Panorama Geral"

    # --- CONFIGURAÇÃO INDIVIDUAL DOS BOTÕES ---
    
    # Botão da Página 1
    k1 = "btn_menu_ativa_1" if st.session_state.pagina == "Ato 1: Panorama Geral" else "btn_menu_1"
    if st.button("Ato 1: Panorama Geral", key=k1):
        st.session_state.pagina = "Ato 1: Panorama Geral"
        st.rerun()

    # Botão da Página 2
    k2 = "btn_menu_ativa_2" if st.session_state.pagina == "Ato 2: Investigação e Hotspots" else "btn_menu_2"
    if st.button("Ato 2: Investigação e Hotspots", key=k2):
        st.session_state.pagina = "Ato 2: Investigação e Hotspots"
        st.rerun()

    # Botão da Página 3
    k3 = "btn_menu_ativa_3" if st.session_state.pagina == "Ato 3: Análise Temporal e Solução" else "btn_menu_3"
    if st.button("Ato 3: Análise Temporal e Solução", key=k3):
        st.session_state.pagina = "Ato 3: Análise Temporal e Solução"
        st.rerun()

    st.markdown("---")
    st.caption("Análise de Sinistros de Trânsito - PRF / GO")

# Alimenta a sua variável antiga para não quebrar a lógica do restante do dashboard.py
pagina = st.session_state.pagina


if pagina == "Ato 1: Panorama Geral":
    criar_kpis_ato1(df)
    # (Chamadas dos gráficos do Ato 1 continuam aqui)

elif pagina == "Ato 2: Investigação e Hotspots":
    criar_kpis_ato2(df)
    renderizar_infografico_dias(df)
    criar_fig_top2_causa_dia(df)

elif pagina == "Ato 3: Análise Temporal e Solução":
    # 1. Renderiza os cartões de KPIs
    criar_kpis_ato3(df)
    
    criar_fig_acidentes_por_hora(df)
    
    # 3. Chamada da Seção de Sentido da Via (Barras Bipolares + Card Explicativo em 2 Colunas)
    renderizar_secao_sentido_via(df)

    # 4. Chamada do Mapa Interativo de Hotspots (Agrupamentos de 10km + Filtro Pendular e Cards)
    renderizar_secao_mapa_hotspots_interativo(df)