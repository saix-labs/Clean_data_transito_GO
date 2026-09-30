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
    caminho = "acidentes-GO-2024_2025_limpo.csv"  # Caminho relativo para a nuvem encontrar
    df = pd.read_csv(caminho)
    return df


df = carregar_dados()

# 4. Barra Lateral (Sidebar)
with st.sidebar:
    st.title("Navegação")
    st.markdown("---")
    st.write("Escolha o foco da análise:")

    # Inicializa a página padrão no estado da sessão caso não exista
    if "pagina" not in st.session_state:
        st.session_state.pagina = "Panorama"

    # --- CONFIGURAÇÃO INDIVIDUAL DOS BOTÕES ---
    
    # Botão da Página 1
    k1 = "btn_menu_ativa_1" if st.session_state.pagina == "Panorama" else "btn_menu_1"
    if st.button("Panorama", key=k1):
        st.session_state.pagina = "Panorama"
        st.rerun()

    # Botão da Página 2
    k2 = "btn_menu_ativa_2" if st.session_state.pagina == "Investigação" else "btn_menu_2"
    if st.button("Investigação", key=k2):
        st.session_state.pagina = "Investigação"
        st.rerun()

    # Botão da Página 3
    k3 = "btn_menu_ativa_3" if st.session_state.pagina == "Comprovação" else "btn_menu_3"
    if st.button("Comprovação", key=k3):
        st.session_state.pagina = "Comprovação"
        st.rerun()

    
    st.caption("Sinistros em Rodovias Federais (BR-GO) • 2024–2025")

# Alimenta a sua variável antiga para não quebrar a lógica do restante do dashboard.py
pagina = st.session_state.pagina


if pagina == "Panorama":
    
    st.markdown("<script>window.parent.scrollTo(0,0);</script>", unsafe_allow_html=True)
    criar_kpis_ato1(df)
    # (Chamadas dos gráficos do Ato 1 continuam aqui)


elif pagina == "Investigação":

    st.markdown("<script>window.parent.scrollTo(0,0);</script>", unsafe_allow_html=True)
    criar_kpis_ato2(df)

    renderizar_infografico_dias(df)
    criar_fig_top2_causa_dia(df)

elif pagina == "Comprovação":
    # 1. Renderiza os cartões de KPIs
   
    st.markdown("<script>window.parent.scrollTo(0,0);</script>", unsafe_allow_html=True)
    criar_kpis_ato3(df)
    criar_fig_acidentes_por_hora(df)
    
    # 3. Chamada da Seção de Sentido da Via (Barras Bipolares + Card Explicativo em 2 Colunas)
    renderizar_secao_sentido_via(df)

    # 4. Chamada do Mapa Interativo de Hotspots (Agrupamentos de 10km + Filtro Pendular e Cards)
    renderizar_secao_mapa_hotspots_interativo(df)

        # --- NOTA DE RODAPÉ COM A FONTE DOS DADOS (FIM DA PÁGINA 3) ---
    st.markdown("---") # Linha fina de separação para criar o efeito de rodapé
    st.markdown(
        """
        <div style='text-align: center; color: #A0AEC0; font-size: 13px; padding: 15px 0 30px 0;'>
            Base de dados oficial: Polícia Rodoviária Federal (PRF) | 
            <a href='https://www.gov.br' 
               target='_blank' 
               style='color: #FF1744; text-decoration: none; font-weight: bold;'>
               Portal de Dados Abertos ↗
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )
