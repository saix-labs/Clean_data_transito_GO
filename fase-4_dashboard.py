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



import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração da página e layout
st.set_page_config(page_title="Painel de Acidentes - GO", layout="wide")

# 2. Carregamento dos dados com Cache (Otimizado)
@st.cache_data
def carregar_dados():
    # Caminho do seu arquivo limpo
    caminho = r"C:\Users\ezequiel\OneDrive\Desktop\PI Trânsito GO\acidentes-GO-2024_2025_limpo.csv"
    df = pd.read_csv(caminho)
    return df

df = carregar_dados()

# =========================================================
# ATO 1: PANORAMA GERAL
# =========================================================

st.title("Ato 1: O Panorama Geral")
st.markdown("---")

# --- CARDS DE KPI (TOPO) ---
total_acidentes = len(df)
br_mais_critica = f"BR-{df['br'].mode()[0]}"

# Cálculo das porcentagens de mito
pct_pista_dupla = (df['tipo_pista'].str.contains('Múltipla|Dupla', case=False, na=False).sum() / total_acidentes) * 100
pct_ceu_claro = (df['condicao_metereologica'].str.contains('Céu Claro|Sol', case=False, na=False).sum() / total_acidentes) * 100

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(label="Total de Acidentes", value=f"{total_acidentes:,}".replace(",", "."))

with kpi2:
    st.metric(label="BR com Maior Volume", value=br_mais_critica)

with kpi3:
    st.metric(label="Acidentes em Pista Dupla/Múltipla", value=f"{pct_pista_dupla:.1f}%")

with kpi4:
    st.metric(label="Acidentes com Tempo Bom", value=f"{pct_ceu_claro:.1f}%")

st.markdown("---")

# --- LINHA 1: TURNO E RANKING DE BRS ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Distribuição por Turno (Fase do Dia)")
    df_turno = df['fase_dia'].value_counts().reset_index()
    df_turno.columns = ['Fase do Dia', 'Total']
    
    fig_turno = px.pie(
        df_turno, 
        values='Total', 
        names='Fase do Dia', 
        hole=0.5,
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    fig_turno.update_traces(textinfo='percent+label')
    fig_turno.update_layout(showlegend=False, margin=dict(t=20, b=20, l=10, r=10))
    st.plotly_chart(fig_turno, use_container_width=True)

with col2:
    st.subheader("Ranking de BRs com Mais Ocorrências")
    df_br = df['br'].value_counts().head(5).reset_index()
    df_br.columns = ['BR', 'Total']
    df_br['BR'] = "BR-" + df_br['BR'].astype(str)
    
    fig_br = px.bar(
        df_br, 
        x='Total', 
        y='BR', 
        orientation='h',
        text='Total',
        color='Total',
        color_continuous_scale='Blues'
    )
    fig_br.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False, coloraxis_showscale=False)
    st.plotly_chart(fig_br, use_container_width=True)

# --- LINHA 2: TIPO DE PISTA E CONDIÇÃO METEOROLÓGICA ---
col3, col4 = st.columns(2)

with col3:
    st.subheader("Infraestrutura: Tipo de Pista")
    df_pista = df['tipo_pista'].value_counts().reset_index()
    df_pista.columns = ['Tipo de Pista', 'Total']
    
    fig_pista = px.bar(
        df_pista, 
        x='Tipo de Pista', 
        y='Total', 
        text='Total',
        color_discrete_sequence=['#1f77b4']
    )
    st.plotly_chart(fig_pista, use_container_width=True)

with col4:
    st.subheader("Clima: Condição Meteorológica")
    df_clima = df['condicao_metereologica'].value_counts().head(5).reset_index()
    df_clima.columns = ['Condição', 'Total']
    
    fig_clima = px.bar(
        df_clima, 
        x='Condição', 
        y='Total', 
        text='Total',
        color_discrete_sequence=['#2b5c8f']
    )
    st.plotly_chart(fig_clima, use_container_width=True)

# --- MAPA DE CALOR POR MUNICÍPIO E TOP 5 CIDADES ---
st.markdown("---")
st.subheader("Distribuição do Volume de Acidentes por Município")

# 1. Agrupamento de acidentes por município
df_municipio = df['municipio'].value_counts().reset_index()
df_municipio.columns = ['Município', 'Total de Acidentes']

# Para desenhar o mapa agrupado por cidade, pegamos a média de lat/lon de cada município
df_coords = df.groupby('municipio')[['latitude', 'longitude']].mean().reset_index()
df_coords.columns = ['Município', 'latitude', 'longitude']

# Une a contagem de acidentes com a coordenada média da cidade
df_mapa_cidades = pd.merge(df_municipio, df_coords, on='Município')

# 2. Gráfico do Mapa Agrupado (A cor reflete a intensidade/intensidade de acidentes)
fig_mapa = px.scatter_mapbox(
    df_mapa_cidades, 
    lat='latitude', 
    lon='longitude', 
    size='Total de Acidentes',
    color='Total de Acidentes',
    color_continuous_scale='Reds', # Quanto mais acidentes, mais escuro/vermelho
    hover_name='Município',
    hover_data={'latitude': False, 'longitude': False, 'Total de Acidentes': True},
    zoom=5.5,
    center=dict(lat=-16.6869, lon=-49.2648),
    mapbox_style="open-street-map"
)

fig_mapa.update_layout(margin=dict(t=0, b=0, l=0, r=0))
st.plotly_chart(fig_mapa, use_container_width=True)

# 3. Top 5 Cidades com mais acidentes (Logo abaixo do mapa)
st.markdown("### 🏆 Top 5 Municípios com Maior Registro de Acidentes")

top5_cidades = df_municipio.head(5)

col_t1, col_t2, col_t3, col_t4, col_t5 = st.columns(5)
cols = [col_t1, col_t2, col_t3, col_t4, col_t5]

for i, row in top5_cidades.iterrows():
    with cols[i]:
        st.metric(
            label=f"{i+1}º {row['Município'].title()}", 
            value=f"{row['Total de Acidentes']:,}".replace(",", ".")
        )