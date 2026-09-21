import pandas as pd
import gc  

print("--- INICIANDO O PROCESSAMENTO DOS DADOS ---")

# 1. PROCESSAR O ANO DE 2024
print("\n[1/4] Lendo o arquivo nacional de 2024...")
# O sep=";" e o encoding="latin-1" são necessários porque a PRF salva as planilhas nesse formato
df_2024 = pd.read_csv("C:\\Users\\ezequiel\\OneDrive\\Desktop\\PI_Trânsito_GO\\datatran2024\\datatran2024.csv", sep=";", encoding="latin-1")

print("Filtrando os acidentes apenas de Goiás...")
df_go_2024 = df_2024[df_2024['uf'] == 'GO'].copy()

# Remove o arquivo do Brasil inteiro da memória do seu notebook
print("Limpando a memória RAM...")
del df_2024
gc.collect()


# 2. PROCESSAR O ANO DE 2025
print("\n[2/4] Lendo o arquivo nacional de 2025...")
df_2025 = pd.read_csv("C:\\Users\\ezequiel\\OneDrive\\Desktop\\PI_Trânsito_GO\\datatran2025\\datatran2025.csv", sep=";", encoding="latin-1")

print("Filtrando os acidentes apenas de Goiás...")
df_go_2025 = df_2025[df_2025['uf'] == 'GO'].copy()

# Remove o arquivo do Brasil inteiro da memória
print("Limpando a memória RAM...")
del df_2025
gc.collect()


# 3. UNIFICAR E SALVAR OS DADOS DE GOIÁS
print("\n[3/4] Juntando os dados de Goiás de 2024 e 2025...")
# O concat junta as linhas de 2024 com as linhas de 2025
df_goias_final = pd.concat([df_go_2024, df_go_2025], ignore_index=True)

print("[4/4] Salvando o arquivo final limpo...")
# Salva o arquivo CSV menor contendo apenas o estado de Goiás
df_goias_final.to_csv("acidentes_goias_2024_2025.csv", index=False)

print("\n--- PROCESSO CONCLUÍDO COM SUCESSO! ---")
print(f"O seu arquivo 'acidentes_goias_2024_2025.csv' foi criado com {len(df_goias_final)} linhas.")
print("Ele está super leve e pronto para ser usado no seu dashboard do Streamlit!")
