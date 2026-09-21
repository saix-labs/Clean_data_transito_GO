#%%
import pandas as pd
import datetime



#importar o arquivo para iniciar a fase 2 - tratamento
#%%
df = pd.read_csv('acidentes_goias_2024_2025.csv')

# %%


#analisar as informacoes gerais
#%%
df.info()
# %%






#INICIANDO ALTERAÇÃO DOS TIPOS DE DADOS
#Codigo gerado por IA a meu pedido
#%%
# 1. Garante que os dados sejam texto para poder substituir vírgulas por pontos
df['latitude'] = df['latitude'].astype(str).str.replace(',', '.')
df['longitude'] = df['longitude'].astype(str).str.replace(',', '.')

# 2. Converte para float de forma segura
df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')

# 3. Verifica se os tipos mudaram corretamente
print(df[['latitude', 'longitude']].dtypes)
# %%


#informacoes gerais
#%%
df.info()
# %%


#alterando a coluna de data_inversa para datetime
#%%
df['data_inversa'] = pd.to_datetime(df['data_inversa'],
                                    errors='coerce')
# %%


#conferindo resultado da alteracao acima
#%%
df.info()
# %%


#alterando o tipo de dado da coluna 'km' para float
#CODIGO GERADO POR IA A MEU PEDIDO
#%%
# 1. Substitui vírgulas por pontos
df['km'] = df['km'].astype(str).str.replace(',', '.')

# 2. Converte para float de forma segura
df['km'] = pd.to_numeric(df['km'], errors='coerce')

# Confirma a alteração
print(df['km'].dtype)
# %%


#alterando o tipo de dado da coluna 'id' para int
#%%
df['id'] = df['id'].astype('int64')
# %%


#confirmando alteracao acima
#%%
df.info()
# %%





#CODIGO GERADO POR IA A MEU PEDIDO
#Salvando o DataFrame limpo em um novo arquivo CSV
#%%
df.to_csv('acidentes-GO-2024_2025_limpo.csv', index=False, encoding='utf-8')

print("Arquivo 'acidentes-GO-2024_2025_limpo.csv' exportado com sucesso!")
# %%
