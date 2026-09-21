import pandas as pd
import plotly.express as px

def criar_fig_turno(df):
    df_turno = df['fase_dia'].value_counts().reset_index()
    df_turno.columns = ['Fase do Dia', 'Total']
    
    fig = px.pie(
        df_turno, 
        values='Total', 
        names='Fase do Dia', 
        hole=0.5,
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(
        showlegend=False, 
        margin=dict(t=20, b=20, l=10, r=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    return fig


def criar_fig_br(df):
    df_br = df['br'].value_counts().head(5).reset_index()
    df_br.columns = ['BR', 'Total']
    df_br['BR'] = "BR-" + df_br['BR'].astype(str)
    
    fig = px.bar(
        df_br, 
        x='Total', 
        y='BR', 
        orientation='h',
        text='Total',
        color='Total',
        color_continuous_scale='Blues'
    )
    fig.update_layout(
        yaxis={'categoryorder':'total ascending'}, 
        showlegend=False, 
        coloraxis_showscale=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    return fig


def criar_fig_pista(df):
    df_pista = df['tipo_pista'].value_counts().reset_index()
    df_pista.columns = ['Tipo de Pista', 'Total']
    
    fig = px.bar(
        df_pista, 
        x='Tipo de Pista', 
        y='Total', 
        text='Total',
        color_discrete_sequence=['#1f77b4']
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    return fig


def criar_fig_clima(df):
    df_clima = df['condicao_metereologica'].value_counts().head(5).reset_index()
    df_clima.columns = ['Condição', 'Total']
    
    fig = px.bar(
        df_clima, 
        x='Condição', 
        y='Total', 
        text='Total',
        color_discrete_sequence=['#2b5c8f']
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    return fig


def criar_fig_mapa(df):
    df_municipio = df['municipio'].value_counts().reset_index()
    df_municipio.columns = ['Município', 'Total de Acidentes']

    df_coords = df.groupby('municipio')[['latitude', 'longitude']].mean().reset_index()
    df_coords.columns = ['Município', 'latitude', 'longitude']

    df_mapa_cidades = pd.merge(df_municipio, df_coords, on='Município')

    fig = px.scatter_mapbox(
        df_mapa_cidades, 
        lat='latitude', 
        lon='longitude', 
        size='Total de Acidentes',
        color='Total de Acidentes',
        color_continuous_scale='Reds',
        hover_name='Município',
        hover_data={'latitude': False, 'longitude': False, 'Total de Acidentes': True},
        zoom=5.5,
        center=dict(lat=-16.6869, lon=-49.2648),
        mapbox_style="open-street-map"
    )
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    return fig, df_municipio