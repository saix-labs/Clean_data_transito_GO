#%%
import pandas as pd
import datetime

#importar o arquivo csv
#%%
df = pd.read_csv('acidentes-GO-2024_2025_limpo.csv')
 # %%



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



# #%%
# df.info()
# # %%


# #%%
# df['fase_dia'].value_counts
# # %%


# # %% Calcular porcentagem do horário pendular (16h às 19h59)

# # 1. Extrai apenas o número da hora (0 a 23), ignorando os minutos
# # 1. Extrai apenas o número da hora (0 a 23) tratando qualquer formato (com ou sem data/segundos)
# df['hora_inteira'] = pd.to_datetime(df['horario'], errors='coerce').dt.hour

# # 2. Define o bloco do horário pendular (horas 16, 17, 18 e 19)
# horas_pendulares = [16, 17, 18, 19]

# # 3. Calcula os totais e a porcentagem
# total_acidentes = len(df.dropna(subset=['hora_inteira']))
# acidentes_pendular = len(df[df['hora_inteira'].isin(horas_pendulares)])
# porcentagem_pendular = (acidentes_pendular / total_acidentes) * 100

# # 4. Exibe os resultados para a tese
# print(f"Total Geral (24h): {total_acidentes}")
# print(f"Total Pendular (16h-20h): {acidentes_pendular}")
# print(f"Porcentagem do Bloco Pendular: {porcentagem_pendular:.2f}%")

# # %%





# # %% Calcular porcentagem do horário pendular (16h às 20h00)

# # 1. Converte a coluna para o tipo datetime/time para extrair hora e minuto
# df_temp = df.copy()
# df_temp['dt_temp'] = pd.to_datetime(df_temp['horario'], errors='coerce')
# df_temp['hora_num'] = df_temp['dt_temp'].dt.hour
# df_temp['min_num'] = df_temp['dt_temp'].dt.minute

# # 2. Filtra das 16:00 às 19:59 (horas 16, 17, 18 e 19) + o minuto exato das 20:00
# filtro_pendular = (
#     (df_temp['hora_num'].isin([16, 17, 18, 19])) | 
#     ((df_temp['hora_num'] == 20) & (df_temp['min_num'] == 0))
# )

# # 3. Calcula os totais e a porcentagem com precisão cirúrgica
# total_acidentes = len(df_temp.dropna(subset=['hora_num']))
# acidentes_pendular = filtro_pendular.sum()
# porcentagem_pendular = (acidentes_pendular / total_acidentes) * 100

# # 4. Exibe os resultados para a tese
# print(f"Total Geral (24h): {total_acidentes}")
# print(f"Total Pendular (16h-20h00): {acidentes_pendular}")
# print(f"Porcentagem do Bloco Pendular: {porcentagem_pendular:.2f}%")

# # %%






# # %% Validação e Comparação do Filtro Horário (16h-20h00)

# import pandas as pd

# # 1. Carregue seu DataFrame aqui (substitua 'seu_arquivo.csv' se necessário)
# # df = pd.read_csv("seu_arquivo.csv")

# # Fazemos uma cópia para não alterar o DataFrame original
# df_temp = df.copy()

# # 2. Extração segura de Hora e Minuto
# hora_min = df_temp['horario'].astype(str).str.split(':', expand=True)
# df_temp['hora_num'] = pd.to_numeric(hora_min[0], errors='coerce')
# df_temp['min_num'] = pd.to_numeric(hora_min[1], errors='coerce')

# # --- MÉTODO 1: <= 20 (Inclui de 20:01 até 20:59) ---
# filtro_metodo1 = (df_temp['hora_num'] >= 16) & (df_temp['hora_num'] <= 20)
# df_m1 = df_temp[filtro_metodo1].copy()

# # Cálculo de Trechos Críticos no Método 1
# df_m1['km_num'] = pd.to_numeric(df_m1['km'], errors='coerce')
# df_m1['trecho_5km'] = (df_m1['km_num'] // 5) * 5
# trechos_m1 = df_m1.groupby(['br', 'trecho_5km']).size().reset_index(name='total_acidentes')
# kms_criticos_m1 = len(trechos_m1[trechos_m1['total_acidentes'] >= 10])


# # --- MÉTODO 2: Cirúrgico (16:00 até exatas 20:00) ---
# filtro_metodo2 = (
#     (df_temp['hora_num'].isin([16, 17, 18, 19])) | 
#     ((df_temp['hora_num'] == 20) & (df_temp['min_num'] == 0))
# )
# df_m2 = df_temp[filtro_metodo2].copy()

# # Cálculo de Trechos Críticos no Método 2
# df_m2['km_num'] = pd.to_numeric(df_m2['km'], errors='coerce')
# df_m2['trecho_5km'] = (df_m2['km_num'] // 5) * 5
# trechos_m2 = df_m2.groupby(['br', 'trecho_5km']).size().reset_index(name='total_acidentes')
# kms_criticos_m2 = len(trechos_m2[trechos_m2['total_acidentes'] >= 10])


# # --- EXIBIÇÃO E PROVA REAL NO TERMINAL ---
# print("=" * 65)
# print("📊 COMPARAÇÃO DE MÉTODOS DE FILTRAGEM DE HORÁRIO")
# print("=" * 65)

# print(f"\n1️⃣ Método Genérico (hora_num <= 20) [Inclui 20:01 às 20:59]:")
# print(f"   • Total de Ocorrências: {len(df_m1)}")
# print(f"   • Trechos Críticos (10+ acidentes em 5km): {kms_criticos_m1}")

# print(f"\n2️⃣ Método Cirúrgico (16:00h até exatas 20:00h):")
# print(f"   • Total de Ocorrências: {len(df_m2)}")
# print(f"   • Trechos Críticos (10+ acidentes em 5km): {kms_criticos_m2}")

# diferenca_registros = len(df_m1) - len(df_m2)
# print("\n" + "-" * 65)
# print(f"⚠️ DIFERENÇA: {diferenca_registros} registros ocorridos APÓS as 20:00h estavam no Método 1.")
# print("=" * 65)

# # %%






#%%
import pandas as pd

# 1. Garante que a coluna de horário está no formato string limpo (HH:MM:SS ou HH:MM)
# Se a sua coluna já for string, isso apenas padroniza os dados
df["horario_str"] = df["horario"].astype(str).str.strip()

# 2. Aplica o filtro ultra-estrito: das 16:00:00 até as 20:00:00 cravadas
# Isso garante que 16:00 entra, 19:59 entra, 20:00 entra, mas 20:01 fica de fora
df_pico_estrito = df[
    (df["horario_str"] >= "16:00") & (df["horario_str"] <= "20:00")
]

# 3. Faz a contagem por sentido da via
contagem_sentido = df_pico_estrito["sentido_via"].value_counts()

# 4. Exibe os resultados detalhados no console
print("=" * 50)
print("ACIDENTES NO PERÍODO PENDULAR CRÍTICO (16h às 20h00)")
print("=" * 50)
print(contagem_sentido)
print("-" * 50)
print(f"Total Geral no Período: {df_pico_estrito.shape[0]} acidentes")
print("=" * 50)

# %%




df.info()
# %%


df.dtypes
# %%


df['sentido_via'].value_counts
# %%



# %%
import pandas as pd

# 1. Garante que os horários estão como string sem espaços extras nas pontas
df["horario_limpo"] = df["horario"].astype(str).str.strip()

# 2. Filtro cirúrgico: inclui tudo de 16:00:00 até exatas 20:00:00
# (Qualquer registro a partir de 20:00:01 fica fora automaticamente)
df_faixa_pendular = df[
    (df["horario_limpo"] >= "16:00:00") & (df["horario_limpo"] <= "20:00:00")
]

# 3. Contagem exata por sentido da via
contagem_sentido = df_faixa_pendular["sentido_via"].value_counts()

# 4. Exibição dos resultados no console
print("=" * 60)
print("📊 OCORRÊNCIAS POR SENTIDO NA FAIXA PENDULAR (16h às 20h00)")
print("=" * 60)
print(contagem_sentido)
print("-" * 60)
print(f"Total Geral no Período: {df_faixa_pendular.shape[0]} acidentes")
print("=" * 60)

# %%




# %%
# O total geral do período crítico é 1723
total_periodo = 1723

# Valores retornados no seu terminal
valores = {"Crescente": 969, "Decrescente": 749, "Não Informado": 5}

print("=" * 50)
print("📊 PORCENTAGEM POR SENTIDO NO PERÍODO CRÍTICO")
print("=" * 50)
for sentido, qtd in valores.items():
    porcentagem = (qtd / total_periodo) * 100
    print(f"• {sentido}: {porcentagem:.2f}% ({qtd} acidentes)")
print("=" * 50)

# %%




# %%
import pandas as pd

# Copia a base para evitar alterações no df original
df_valida = df.copy()

# 1. Padroniza a string de horário retirando espaços nas pontas
df_valida["horario_limpo"] = df_valida["horario"].astype(str).str.strip()

# 2. Filtro cirúrgico com segundos (16:00:00 até exatas 20:00:00)
# (Qualquer ocorrência a partir de 20:00:01 é ignorada)
df_pico = df_valida[
    (df_valida["horario_limpo"] >= "16:00:00")
    & (df_valida["horario_limpo"] <= "20:00:00")
].copy()

# 3. Tratamento e agrupamento por KMs (Janelas de 5 km)
df_pico["km_num"] = pd.to_numeric(df_pico["km"], errors="coerce")
# O operador // faz a divisão inteira (ex: KM 14 // 5 = 2 -> 2 * 5 = Trecho do KM 10)
df_pico["trecho_5km"] = (df_pico["km_num"] // 5) * 5

# 4. Agrupamento por BR e Trecho de 5km, contando os acidentes
trechos_agrupados = (
    df_pico.groupby(["br", "trecho_5km"])
    .size()
    .reset_index(name="total_acidentes")
)

# 5. Filtra apenas os trechos com 10 ou mais acidentes
trechos_criticos = trechos_agrupados[
    trechos_agrupados["total_acidentes"] >= 10
].sort_values(by="total_acidentes", ascending=False)

# 6. Exibe os resultados no console
print("=" * 65)
print(f"📊 TRECHOS CRÍTICOS (10+ ACIDENTES) - 16h às 20h00")
print("=" * 65)
print(trechos_criticos.to_string(index=False))
print("-" * 65)
print(f"Total de Trechos Críticos Encontrados: {len(trechos_criticos)}")
print("=" * 65)

# %%





# %%
import pandas as pd

# 1. Cria uma cópia e padroniza a string de horário
df_valida = df.copy()
df_valida["horario_limpo"] = df_valida["horario"].astype(str).str.strip()

# 2. Filtro cirúrgico com segundos: das 16:00:00 até exatas 20:00:00 cravadas
df_pico = df_valida[
    (df_valida["horario_limpo"] >= "16:00:00")
    & (df_valida["horario_limpo"] <= "20:00:00")
].copy()

# 3. Remove "Não Informado" e nulos da coluna de causas (igualzinho faz o seu card)
causas_limpas = (
    df_pico["causa_acidente"].fillna("").astype(str).str.strip().str.lower()
)
df_causas_validas = df_pico[
    (causas_limpas != "não informado") & (causas_limpas != "")
]

# 4. Calcula o ranking e as porcentagens
if not df_causas_validas.empty:
    contagem_causas = df_causas_validas["causa_acidente"].value_counts()
    total_causas_validas = len(df_causas_validas)

    # Pega os dados do Top 1
    top_causa_nome = contagem_causas.index[0]
    top_causa_qtd = contagem_causas.iloc[0]

    # Percentual bruto e truncado
    pct_bruto = (top_causa_qtd / total_causas_validas) * 100
    pct_truncado = int(pct_bruto * 10) / 10

    # Exibe no console
    print("=" * 65)
    print("📊 ANÁLISE DE CAUSAS NO PERÍODO PENDULAR (16h às 20h00)")
    print("=" * 65)
    print(f"Total de acidentes com causas válidas na janela: {total_causas_validas}")
    print(f"Causa #1 Principal: {top_causa_nome}")
    print(f"Quantidade de ocorrências: {top_causa_qtd}")
    print(f"Porcentagem Bruta: {pct_bruto:.3f}%")
    print(f"Porcentagem Truncada (1 casa): {pct_truncado:.1f}%")
    print("=" * 65)
else:
    print("Nenhuma causa válida encontrada no período.")

# %%



# %%
import pandas as pd

# 1. Cria uma cópia e padroniza a string de horário
df_valida = df.copy()
df_valida["horario_limpo"] = df_valida["horario"].astype(str).str.strip()

# 2. Filtro cirúrgico com segundos: das 16:00:00 até exatas 20:00:00 cravadas
df_pico = df_valida[
    (df_valida["horario_limpo"] >= "16:00:00")
    & (df_valida["horario_limpo"] <= "20:00:00")
].copy()

# 3. Remove "Não Informado" e nulos da coluna de tipos (igualzinho faz o seu card)
tipos_limpos = (
    df_pico["tipo_acidente"].fillna("").astype(str).str.strip().str.lower()
)
df_tipos_validos = df_pico[
    (tipos_limpos != "não informado") & (tipos_limpos != "")
]

# 4. Calculates o ranking e as porcentagens
if not df_tipos_validos.empty:
    contagem_tipos = df_tipos_validos["tipo_acidente"].value_counts()
    total_tipos_validos = len(df_tipos_validos)

    # Pega os dados do Top 1
    top_tipo_nome = contagem_tipos.index[0]
    top_tipo_qtd = contagem_tipos.iloc[0]

    # Percentual bruto e truncado
    pct_bruto = (top_tipo_qtd / total_tipos_validos) * 100
    pct_truncado = int(pct_bruto * 10) / 10

    # Exibe no console
    print("=" * 65)
    print("📊 ANÁLISE DE TIPOS NO PERÍODO PENDULAR (16h às 20h00)")
    print("=" * 65)
    print(f"Total de acidentes com tipos válidos na janela: {total_tipos_validos}")
    print(f"Tipo #1 Principal: {top_tipo_nome}")
    print(f"Quantidade de ocorrências: {top_tipo_qtd}")
    print(f"Porcentagem Bruta: {pct_bruto:.3f}%")
    print(f"Porcentagem Truncada (1 casa): {pct_truncado:.1f}%")
    print("=" * 65)
else:
    print("Nenhum tipo válido encontrado no período.")

# %%
