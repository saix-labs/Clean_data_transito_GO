#%%
import pandas as pd
import datetime


#importando arquivo csv
#%%
df = pd.read_csv('acidentes-GO-2024_2025_limpo.csv')
df['data_inversa'] = pd.to_datetime(df['data_inversa'])
# %%


#informacoes gerais
#%%
df.info()

# %%






#CODIGO GERADO POR IA A MEU PEDIDO
#%%
# 1. Converte a coluna 'horario' para extrair a hora (0 a 23)
hora_num = pd.to_datetime(df['horario'], format='%H:%M:%S').dt.hour

# 2. Cria a regra para categorizar os 4 turnos
def classificar_turno(h):
    if 6 <= h < 12:
        return '1. Manhã (06h-11h59)'
    elif 12 <= h < 18:
        return '2. Tarde (12h-17h59)'
    elif 18 <= h < 24:
        return '3. Noite (18h-23h59)'
    else:
        return '4. Madrugada (00h-05h59)'

# 3. Aplica a função para criar a coluna 'turno'
df['turno'] = hora_num.apply(classificar_turno)

# 4. Gera a tabela cruzada simples: Turno x Sentido da Via
tabela_turno_sentido = pd.crosstab(
    df['turno'], 
    df['sentido_via'], 
    margins=True, 
    margins_name='TOTAL'
)

print("=== QUANTIDADE DE ACIDENTES POR TURNO E SENTIDO DA VIA ===")
print(tabela_turno_sentido)
# %%






#CODIGO GERADO POR IA A MEU PEDIDO
#Para ver a quantidade de acidentes a cada hora
#%%
# 1. Extrai a hora exata (0 a 23) da coluna 'horario'
df['hora_exata'] = pd.to_datetime(df['horario'], format='%H:%M:%S').dt.hour

# 2. Conta a quantidade de acidentes para cada hora
acidentes_por_hora = df['hora_exata'].value_counts().sort_index()

# 3. Exibe o resultado de 0h até 23h
print("=== ACIDENTES POR HORA EXATA (0h as 23h) ===")
for hora, total in acidentes_por_hora.items():
    print(f"{hora:02d}h: {total} acidentes")
# %%








#CODIGO GERADO POR IA A MEU PEDIDO
#analisar o pico de acidentes no turno da tarde e noite e o sentido
#%%
# 1. Extrai a hora exata
df['hora_exata'] = pd.to_datetime(df['horario'], format='%H:%M:%S').dt.hour

# 2. Cria a tabela cruzada de Hora x Sentido da Via
tabela_hora_sentido = pd.crosstab(
    df['hora_exata'], 
    df['sentido_via']
)

# 3. Filtra a janela crítica da tarde/noite (16h às 21h) para comparar os sentidos
janela_pico = tabela_hora_sentido.loc[16:21, ['Crescente', 'Decrescente']]

# Adiciona o percentual do sentido Crescente no total daquela hora
janela_pico['Total_Hora'] = janela_pico['Crescente'] + janela_pico['Decrescente']
janela_pico['%_Crescente'] = (janela_pico['Crescente'] / janela_pico['Total_Hora'] * 100).round(1)

print("=== JANELA CRÍTICA (16h as 21h) - CRESCENTE vs DECRESCENTE ===")
print(janela_pico)
# %%






#CODIGO GERADO POR IA
#analisar a quantidade de ocorrencias por fase_dia
#%%
# Tabela cruzada entre Fase do Dia e Sentido da Via
tabela_fase = pd.crosstab(
    df['fase_dia'], 
    df['sentido_via'], 
    margins=True, 
    margins_name='Total'
)

# Cálculo do percentual no sentido Crescente
tabela_fase['%_Crescente'] = (tabela_fase['Crescente'] / tabela_fase['Total'] * 100).round(1)

# Ordenação pelo total de ocorrências
tabela_fase_ordenada = tabela_fase.sort_values(by='Total', ascending=False)

# Exibição limpa sem índices desalinhados
print("=== ACIDENTES POR FASE DO DIA x SENTIDO DA VIA ===")
print(tabela_fase_ordenada.to_string())
# %%





#CODIGO GERADO POR IA A MEU PEDIDO
#analisar a quantidade de acidentes por sentido_via
#o objetivo é validar a minha hipótese de os acidentes ocorrerem na volta para casa
#%%
# Contagem total de ocorrências por sentido da via
contagem_sentido = df['sentido_via'].value_counts()

# Exibe o resultado com a porcentagem
porcentagem_sentido = df['sentido_via'].value_counts(normalize=True) * 100

# Tabela consolidada
resumo_sentido = pd.DataFrame({
    'Total_Acidentes': contagem_sentido,
    'Porcentagem (%)': porcentagem_sentido.round(2)
})

print("=== CONTAGEM TOTAL POR SENTIDO DA VIA ===")
print(resumo_sentido.to_string())
# %%






#CODIGO GERADO POR IA A MEU PEDIDO
#analisar a causa_acidente com a hora
#%%
# 1. Cria a coluna com a hora exata
df['hora_num'] = pd.to_datetime(df['horario'], format='mixed', errors='coerce').dt.hour

# 2. Categoriza as horas em períodos do dia
df['periodo_dia'] = pd.cut(
    df['hora_num'],
    bins=[-1, 5, 11, 17, 23],
    labels=['Madrugada (00h-05h)', 'Manhã (06h-11h)', 'Tarde (12h-17h)', 'Noite (18h-23h)']
)

# 3. Filtra as Top 5 causas
top_causas = df['causa_acidente'].value_counts().head(5).index
df_top = df[df['causa_acidente'].isin(top_causas)]

# 4. Gera a tabela agrupada por período e aplica destaque visual de cor
tabela_periodos = pd.crosstab(
    df_top['causa_acidente'], 
    df_top['periodo_dia'], 
    margins=True, 
    margins_name='Total'
)

# Renderiza com destaque de intensidade (gradiente) na Janela Interativa
tabela_periodos.style.background_gradient(cmap='YlOrRd', axis=None)
# %%


#analisar a linha da coluna
#%%
df['classificacao_acidente'].value_counts()
# %%


#analisar a linha da coluna
#%%
df['tipo_acidente'].value_counts()
# %%


#analisar a linha da coluna
#%%
df['veiculos'].value_counts()
# %%





#CODIGO GERADO POR IA A MEU PEDIDO
#analisar a quantidade de ocorrências por hora, dia da semana e o sentido
#%%
# Agrupa somando os acidentes por Dia da Semana e Sentido da Via
tabela_dias = df.groupby(['dia_semana', 'sentido_via']).size().reset_index(name='total_acidentes')

# Ordena os dias da semana em ordem lógica (de segunda a domingo)
ordem_dias = [
    'segunda-feira', 'terça-feira', 'quarta-feira', 
    'quinta-feira', 'sexta-feira', 'sábado', 'domingo'
]

# Aplica a ordenação correta
tabela_dias['dia_semana'] = pd.Categorical(tabela_dias['dia_semana'], categories=ordem_dias, ordered=True)
tabela_dias = tabela_dias.sort_values(by=['dia_semana', 'sentido_via'])

# Exibe a tabela completa
print(tabela_dias.to_string(index=False))
# %%






#CODIGO GERADO POR IA A MEU PEDIDO
#observar a quantidade de acidentes por sentido_via
#%%
# 1. Filtra apenas os dias úteis (segunda a sexta)
dias_uteis = ['segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira']
df_uteis = df[df['dia_semana'].isin(dias_uteis)].copy()

# 2. Extrai a hora em formato numérico (0 a 23)
df_uteis['hora'] = pd.to_datetime(df_uteis['horario'].astype(str), format='%H:%M:%S', errors='coerce').dt.hour

# 3. Filtra apenas os sentidos conhecidos
df_uteis = df_uteis[df_uteis['sentido_via'].isin(['Crescente', 'Decrescente'])]

# 4. Tabela cruzada: Linhas = Hora (0 a 23), Colunas = Sentido da Via
tabela_fluxo_horario = pd.pivot_table(
    df_uteis,
    index='hora',
    columns='sentido_via',
    values='id',
    aggfunc='count',
    fill_value=0
)

# 5. Cria uma coluna mostrando a diferença total e qual sentido liderou naquela hora
tabela_fluxo_horario['Total'] = tabela_fluxo_horario['Crescente'] + tabela_fluxo_horario['Decrescente']
tabela_fluxo_horario['Diferença (Cres - Dec)'] = tabela_fluxo_horario['Crescente'] - tabela_fluxo_horario['Decrescente']

# Exibe a tabela organizada de 0h a 23h
print("=== DISTRIBUIÇÃO DE ACIDENTES POR HORA E SENTIDO (DIAS ÚTEIS) ===")
print(tabela_fluxo_horario)
# %%
