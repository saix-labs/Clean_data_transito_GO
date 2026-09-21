#importar pandas e datetime
#%%
import pandas as pd
import datetime


#importar o arquivo csv
#%%
df = pd.read_csv('acidentes_goias_2024_2025.csv')








#iniciando a fase 1 - pre analise do dataframe

#analisar as informacoes gerais
#%%
df.info()
# %%


#visualizar linha da coluna
#%%
df['horario'].value_counts()
# %%


#analisar a linha da coluna
#%%
df['br'].value_counts()
# %%


#ver a linha da coluna
#%%
df['uso_solo'].value_counts()
# %%


#analisar linha da coluna
df['condicao_metereologica'].value_counts()
# %%


#analisar coluna
#%%
df['fase_dia'].value_counts()

# %%


#analisar coluna
#%%
df['horario'].value_counts()
# %%


#analise linha da coluna
#%%
df['tipo_acidente'].value_counts()
# %%


#analisando a linha da coluna
#%%
df['causa_acidente'].value_counts()
# %%


#analisar a linha da coluna
#%%
df['tracado_via'].value_counts()
# %%


#analisar a linha da coluna
#%%
df['tipo_pista'].value_counts()
# %%
