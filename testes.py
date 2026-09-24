#%%
import pandas as pd
import datetime

#importar o arquivo csv
#%%
df = pd.read_csv('acidentes-GO-2024_2025_limpo.csv')
# %%



#informacoes gerais
#%%
df.info()
# %%


#analisar linha da coluna
#%%
df['tipo_pista'].value_counts()
# %%


#ver a linha da coluna
#%%
df['tipo_acidente'].value_counts()
# %%


#analisar linha da coluna
#%%
df['causa_acidente'].value_counts()
# %%
