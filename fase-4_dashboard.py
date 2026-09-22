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




"""# === VALIDAÇÃO DOS CARDS DE KPI NO TERMINAL ===
print("\n" + "="*50)
print("       VALIDAÇÃO DOS NÚMEROS DOS CARDS DE KPI")
print("="*50)

# Card 1: Traçado Predominante (Reta)
# Considera valores que contêm 'Reta' ou verifica a proporção da categoria exata
total_registros = len(df)
qtd_reta = df['tracado_via'].str.contains('Reta', case=False, na=False).sum()
pct_reta_calc = (qtd_reta / total_registros) * 100
print(f"\n[Card 1] Traçado Predominante (Reta):")
print(f" - Qtd de registros com 'Reta': {qtd_reta} / {total_registros}")
print(f" - Porcentagem Calculada: {pct_reta_calc:.2f}%")

# Card 2: Acidentes Não Fatais (Com Vítimas Feridas + Sem Vítimas)
qtd_nao_fatais = df['classificacao_acidente'].isin(['Com Vítimas Feridas', 'Sem Vítimas']).sum()
pct_controlada_calc = (qtd_nao_fatais / total_registros) * 100
print(f"\n[Card 2] Acidentes Não Fatais:")
print(f" - Qtd de acidentes não fatais: {qtd_nao_fatais} / {total_registros}")
print(f" - Porcentagem Calculada: {pct_controlada_calc:.2f}%")

# Card 3: Causa Principal #1
top_causa = df['causa_acidente'].value_counts().index[0]
qtd_top_causa = df['causa_acidente'].value_counts().iloc[0]
pct_top_causa = (qtd_top_causa / total_registros) * 100
print(f"\n[Card 3] Causa Principal #1:")
print(f" - Causa mais frequente: '{top_causa}'")
print(f" - Frequência: {qtd_top_causa} ocorrências ({pct_top_causa:.2f}% do total)")

# Card 4: Acidentes em Dias Úteis (Segunda a Sexta)
dias_uteis = ['segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira']
qtd_dias_uteis = df['dia_semana'].isin(dias_uteis).sum()
pct_dias_uteis_calc = (qtd_dias_uteis / total_registros) * 100
print(f"\n[Card 4] Acidentes em Dias Úteis:")
print(f" - Qtd em dias úteis: {qtd_dias_uteis} / {total_registros}")
print(f" - Porcentagem Calculada: {pct_dias_uteis_calc:.2f}%")
print("="*50 + "\n")
"""