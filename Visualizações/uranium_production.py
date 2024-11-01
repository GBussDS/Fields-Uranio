import pandas as pd
import os

# Definir o diretório onde os arquivos CSV estão armazenados
directory = "csvs/Produção/"

# Lista de anos para nomear as colunas corretamente
years = list(range(1998, 2023))

# Dicionário para armazenar dados de cada ano
data = {}

# Iterar sobre cada arquivo CSV para cada ano
for year in years:
    file_path = os.path.join(directory, f"UraniumProduction{year}.csv")
    df = pd.read_csv(file_path)
    # Renomear a coluna de produção para o ano atual
    df = df.rename(columns={"tU": year})
    # Configurar a coluna 'Country' como índice e adicionar ao dicionário de dados
    df.set_index("Country", inplace=True)
    data[year] = df[year]

# Concatenar todos os DataFrames ao longo das colunas para criar um único DataFrame
historical_df = pd.concat(data.values(), axis=1)

# Consolidar "Russia" e "USSR -1991" em uma única entrada "Russia"
if "USSR -1991" in historical_df.index:
    historical_df.loc["Russia"] = historical_df.loc["Russia"].fillna(0) + historical_df.loc["USSR -1991"].fillna(0)
    historical_df = historical_df.drop("USSR -1991")

# Remover países com produção sempre zero
historical_df = historical_df.loc[(historical_df != 0).any(axis=1)]

# Adicionar uma linha "Global" com a soma de todas as produções por ano
historical_df.loc["Global"] = historical_df.sum()

# Salvar o DataFrame consolidado em um novo arquivo CSV
historical_df.to_csv("UraniumProductionHistorical.csv")
