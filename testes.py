# #%%
# import pandas as pd
# import datetime

# #importar o arquivo csv
# #%%
# df = pd.read_csv('acidentes-GO-2024_2025_limpo.csv')
# # %%



# #informacoes gerais
# #%%
# df.info()
# # %%


# #analisar linha da coluna
# #%%
# df['tipo_pista'].value_counts()
# # %%


# #ver a linha da coluna
# #%%
# df['tipo_acidente'].value_counts()
# # %%


# #analisar linha da coluna
# #%%
# df['causa_acidente'].value_counts()
# # %%


# #ver linha da coluna
# #%%
# df['horario'].value_counts()
# # %%


# #%%
# df['km'].value_counts()
# # %%

# #%%
# df['sentido_via'].value_counts()

# # %%
# df['br'].value_counts()


# # %%
# df['latitude'].value_counts()

# # %%


# df.columns.tolist()
# # %%




# #%%#%% DIAGNÓSTICO DO TRECHO BR-60 KM 165-170

# import pandas as pd

# # 1. Garante a extração da hora como número inteiro (coluna 'hora_int')
# df_temp = df.copy()

# if 'horario' in df_temp.columns:
#   if pd.api.types.is_string_dtype(df_temp['horario']):
#     df_temp['hora_int'] = pd.to_numeric(
#         df_temp['horario'].str.split(':').str[0], errors='coerce'
#     ).fillna(0)
#   else:
#     df_temp['hora_int'] = pd.to_datetime(
#         df_temp['horario'].astype(str), format='%H:%M:%S', errors='coerce'
#     ).dt.hour.fillna(0)

# # Garante que 'km' seja numérico
# if 'km' in df_temp.columns:
#   df_temp['km_num'] = pd.to_numeric(df_temp['km'], errors='coerce')

# # 2. Filtra a Janela Crítica (16h às 20h)
# df_pendular = df_temp[df_temp['hora_int'].between(16, 20)].copy()

# # 3. Filtra a BR-60 no trecho KM 165 ao 170
# trecho_165_170 = df_pendular[
#     (df_pendular['br'].astype(str).str.contains('60'))
#     & (df_pendular['km_num'] >= 165)
#     & (df_pendular['km_num'] <= 170)
# ]

# print(f'Total de acidentes no trecho: {len(trecho_165_170)}')

# print('\n--- DISTRIBUIÇÃO DAS CAUSAS ---')
# if 'causa_acidente' in trecho_165_170.columns:
#   print(trecho_165_170['causa_acidente'].value_counts())
# else:
#   print("Coluna 'causa_acidente' não encontrada.")

# print('\n--- DISTRIBUIÇÃO DOS TIPOS DE ACIDENTE ---')
# if 'tipo_acidente' in trecho_165_170.columns:
#   print(trecho_165_170['tipo_acidente'].value_counts())
# else:
#   print("Coluna 'tipo_acidente' não encontrada.")

# # %%




# #%%

# # 1. Função Utilitária para extrair Fator Dominante e Porcentagem (com empate)
# def extrair_fator_dominante(serie):
#     s_clean = serie.dropna().astype(str).str.strip()
#     s_clean = s_clean[s_clean.str.lower() != 'não informado']

#     if s_clean.empty:
#         return 'N/I'

#     contagem = s_clean.value_counts()
#     total = len(s_clean)
#     max_freq = contagem.max()

#     top_itens = contagem[contagem == max_freq]
#     pct = (max_freq / total) * 100

#     if len(top_itens) > 1:
#         nomes = ' / '.join([item.title() for item in top_itens.index])
#         return f'{nomes} ({pct:.0f}% cada)'

#     nome_unico = top_itens.index[0].title()
#     return f'{nome_unico} ({pct:.0f}%)'


# # 2. Seleção da base e tratamento do horário idêntico ao Streamlit
# df_analise = df_filtrado.copy() if 'df_filtrado' in locals() else df.copy()

# if 'horario' in df_analise.columns:
#     horas_temp = pd.to_datetime(
#         df_analise['horario'].astype(str), format='%H:%M:%S', errors='coerce'
#     ).dt.hour
#     mask_pendular = horas_temp.between(16, 20)
#     df_pendular = df_analise[mask_pendular].copy()
# else:
#     df_pendular = df_analise.copy()

# # 3. Conversão de KM e criação do agrupamento de 5 km
# df_pendular['km_num'] = pd.to_numeric(df_pendular['km'], errors='coerce')
# df_valid = df_pendular.dropna(
#     subset=['km_num', 'latitude', 'longitude']
# ).copy()
# df_valid['trecho_5km'] = (df_valid['km_num'] // 5) * 5

# # 4. Agrupamento e agregação com a nova função de porcentagem/empate
# agrupamento = (
#     df_valid.groupby(['br', 'trecho_5km'])
#     .agg(
#         total_acidentes=('km_num', 'count'),
#         municipio_mais_comum=(
#             'municipio',
#             lambda x: (
#                 x.mode().iloc[0].title() if not x.dropna().empty else 'N/I'
#             ),
#         )
#         if 'municipio' in df_valid.columns
#         else ('km_num', lambda x: 'N/A'),
#         causa_dominante=(
#             'causa_acidente',
#             lambda x: extrair_fator_dominante(x) if not x.empty else 'N/I',
#         ),
#         tipo_dominante=(
#             'tipo_acidente',
#             lambda x: extrair_fator_dominante(x) if not x.empty else 'N/I',
#         ),
#     )
#     .reset_index()
# )

# # 5. Filtro dos Hotspots (>= 10 acidentes)
# hotspots_10plus = agrupamento[agrupamento['total_acidentes'] >= 10].sort_values(
#     by='total_acidentes', ascending=False
# )

# # --- IMPRESSÃO DOS RESULTADOS ---
# print('=' * 60)
# print('📊 RESULTADO DA ANÁLISE DE HOTSPOTS PENDULARES (>= 10 ACIDENTES)')
# print('=' * 60)
# print(
#     f'• Total de trechos críticos (>= 10 acidentes): {len(hotspots_10plus)}'
# )
# print(
#     '• Total de acidentes concentrados nesses hotspots:'
#     f" {hotspots_10plus['total_acidentes'].sum()}"
# )
# print('-' * 60)

# if not hotspots_10plus.empty:
#     print('\n🏆 FREQUÊNCIA DAS CAUSAS DOMINANTES NOS HOTSPOTS:')
#     print(hotspots_10plus['causa_dominante'].value_counts().to_string())

#     print('\n💥 FREQUÊNCIA DOS TIPOS DE ACIDENTES DOMINANTES NOS HOTSPOTS:')
#     print(hotspots_10plus['tipo_dominante'].value_counts().to_string())

#     if 'municipio_mais_comum' in hotspots_10plus.columns:
#         print('\n📍 MUNICÍPIOS COM TRECHOS CRÍTICOS:')
#         print(
#             hotspots_10plus['municipio_mais_comum'].value_counts().to_string()
#         )

#     print('\n🔍 DETALHAMENTO DOS HOTSPOTS (COM % E EMPATES):')
#     print(
#         hotspots_10plus[[
#             'br',
#             'trecho_5km',
#             'total_acidentes',
#             'municipio_mais_comum',
#             'causa_dominante',
#             'tipo_dominante',
#         ]].to_string(index=False)
#     )
# else:
#     print('Nenhum trecho atendeu aos critérios.')
# # %%






# #%%
# # 1. Garante que a coluna está no formato de data/hora se ainda não estiver
# df['horario'] = pd.to_datetime(df['horario'])

# # 2. Agrupa pelas horas (0 a 23) e conta o número de ocorrências
# contagem_por_hora = df.groupby(df['horario'].dt.hour).size()

# # 3. Exibe o resultado formatado de 0h a 23h
# for hora in range(24):
#     qtd = contagem_por_hora.get(hora, 0)
#     print(f"{hora:02d}h: {qtd} ocorrências")
# # %%






# import pandas as pd

# # 1. Copia o DataFrame e trata a coluna de horário
# df_check = df.copy()

# if 'horario' in df_check.columns:
#     if pd.api.types.is_string_dtype(df_check['horario']):
#         df_check['hora_int'] = pd.to_numeric(
#             df_check['horario'].str.split(':').str[0], errors='coerce'
#         ).fillna(0)
#     else:
#         df_check['hora_int'] = pd.to_datetime(
#             df_check['horario'].astype(str), format='%H:%M:%S', errors='coerce'
#         ).dt.hour.fillna(0)
# else:
#     df_check['hora_int'] = 0

# # 2. Filtra exatamente para a Janela Pendular (16h às 20h)
# df_pendular = df_check[df_check['hora_int'].between(16, 20)].copy()

# print(f"=== TOTAL DE REGISTROS ENTRE 16H E 20H: {len(df_pendular)} ===")
# print("-" * 55)

# # 3. Validação da CAUSA #1
# causas_validas = df_pendular[
#     df_pendular['causa_acidente'].dropna().astype(str).str.strip().str.lower() != 'não informado'
# ]['causa_acidente']

# if not causas_validas.empty:
#     top_causa_nome = causas_validas.value_counts().index[0].title()
#     top_causa_qtd = causas_validas.value_counts().iloc[0]
#     pct_causa = (top_causa_qtd / len(causas_validas)) * 100
#     print(f"CAUSA #1: {top_causa_nome}")
#     print(f"Contagem: {top_causa_qtd} de {len(causas_validas)} registros válidos")
#     print(f"Porcentagem: {pct_causa:.1f}%\n")
# else:
#     print("Nenhuma causa válida encontrada.\n")

# print("-" * 55)

# # 4. Validação do TIPO DE ACIDENTE #1
# tipos_validos = df_pendular[
#     df_pendular['tipo_acidente'].dropna().astype(str).str.strip().str.lower() != 'não informado'
# ]['tipo_acidente']

# if not tipos_validos.empty:
#     top_tipo_nome = tipos_validos.value_counts().index[0].title()
#     top_tipo_qtd = tipos_validos.value_counts().iloc[0]
#     pct_tipo = (top_tipo_qtd / len(tipos_validos)) * 100
#     print(f"TIPO DE ACIDENTE #1: {top_tipo_nome}")
#     print(f"Contagem: {top_tipo_qtd} de {len(tipos_validos)} registros válidos")
#     print(f"Porcentagem: {pct_tipo:.1f}%\n")
# else:
#     print("Nenhum tipo válido encontrado.\n")

# print("-" * 55)

# # 5. Validação da DIVISÃO DOS SENTIDOS
# sentidos_validos = df_pendular[
#     df_pendular['sentido_via'].dropna().astype(str).str.strip().str.lower() != 'não informado'
# ]['sentido_via']

# if not sentidos_validos.empty:
#     total_sent = len(sentidos_validos)
#     p_cres = (sentidos_validos.astype(str).str.lower() == 'crescente').sum() / total_sent * 100
#     p_dec = 100 - p_cres
#     print("DIVISÃO DOS SENTIDOS:")
#     print(f"Crescente: {p_cres:.1f}%")
#     print(f"Decrescente: {p_dec:.1f}%")
# # %%
