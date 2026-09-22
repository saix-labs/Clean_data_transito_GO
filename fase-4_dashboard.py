import streamlit as st
import pandas as pd
from estilos import aplicar_estilos
from graficos import (
    criar_fig_turno, 
    criar_fig_br, 
    criar_fig_pista, 
    criar_fig_clima, 
    criar_fig_mapa,
    criar_kpis_ato2,
    criar_kpis_ato1
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
    
elif pagina == "Ato 2: Investigação e Hotspots":
    criar_kpis_ato2(df)




# --- SCRIPT DE VALIDAÇÃO DE DADOS ---

# 1. Ver a contagem exata e porcentagem por tipo de pista
print("--- DISTRIBUIÇÃO POR TIPO DE PISTA ---")
contagem_pista = df['tipo_pista'].value_counts(dropna=False)
porcentagem_pista = df['tipo_pista'].value_counts(normalize=True, dropna=False) * 100

df_validacao_pista = pd.DataFrame({
    'Qtd Registros': contagem_pista,
    'Porcentagem (%)': porcentagem_pista.round(2)
})
print(df_validacao_pista)

print("\n--------------------------------------")

# 2. Validar a conta do seu Card (Simples + Dupla)
total = len(df)
simples_dupla = df['tipo_pista'].str.contains('Simples|Dupla', case=False, na=False).sum()
pct_card = (simples_dupla / total) * 100

print(f"Total Geral de Registros: {total}")
print(f"Registros (Simples + Dupla): {simples_dupla}")
print(f"Resultado do Card: {pct_card:.2f}%")

print("\n--- DISTRIBUIÇÃO POR CONDICAO METEREOLOGICA ---")
print((df['condicao_metereologica'].value_counts(normalize=True) * 100).round(2))