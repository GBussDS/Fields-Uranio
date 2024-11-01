import pandas as pd
import numpy as np

# Carregar os dados de produção e demanda
production_df = pd.read_csv("csvs/RedBook/Produção(RedBook).csv")
demand_df = pd.read_csv("csvs/RedBook/Demanda(RedBook).csv")

# Mesclar os DataFrames com base no ano
merged_df = pd.merge(production_df, demand_df, on="Year", how="inner")

# Renomear as colunas para facilitar o entendimento
merged_df.columns = ["Year", "Production", "Demand"]

# Calcular o Stock
merged_df["Stock"] = merged_df["Production"] - merged_df["Demand"]

# Inicializar o Accumulated Stock, Years of Stock e Years of Stock(w/Production)
accumulated_stock = 0
accumulated_stock_list = []
years_of_stock = []
years_of_stock_with_production = []

# Calcular o Accumulated Stock, Years of Stock e Years of Stock(w/Production)
for i, row in merged_df.iterrows():
    # Calcular Accumulated Stock
    accumulated_stock += row["Stock"]
    accumulated_stock_list.append(accumulated_stock)
    
    # Calcular Years of Stock
    if row["Demand"] != 0:
        years_stock = accumulated_stock / row["Demand"]
        years_of_stock.append(years_stock)
    else:
        years_of_stock.append(np.nan)
        
    # Calcular Years of Stock(w/Production), sendo null quando Demand > Production
    if row["Production"] > row["Demand"]:
        years_of_stock_with_production.append(np.nan)
    elif (row["Production"] - row["Demand"]) != 0:
        years_stock_with_prod = accumulated_stock / (row["Demand"] - row["Production"])
        years_of_stock_with_production.append(years_stock_with_prod)
    else:
        years_of_stock_with_production.append(np.nan)

# Adicionar as novas colunas ao DataFrame
merged_df["Accumulated Stock"] = accumulated_stock_list
merged_df["Years of Stock"] = years_of_stock
merged_df["Years of Stock(w/Production)"] = years_of_stock_with_production

# Salvar o DataFrame em um novo CSV
merged_df.to_csv("Anos_Estoque.csv", index=False)
