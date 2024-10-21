import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

reatores_ano = pd.read_csv('./csvs/Reatores_Ano.csv')
reatores_info = pd.read_csv('./csvs/Reatores_info.csv')

#Dados Red Book
# uranium_demand = pd.read_csv('./csvs/Demanda_historica.csv')
# uranium_demand.rename(columns={'ano': 'Year', 'uranio(ton.)': 'tU'}, inplace=True)

#Dados World Uranium
uranium_demand = pd.read_csv('./csvs/Uranium_demand.csv')
uranium_demand.rename(columns={'Uranium Required [T]': 'tU'}, inplace=True)
uranium_demand = uranium_demand[['Year', 'tU']]
uranium_demand = uranium_demand.groupby(['Year']).sum().reset_index()
print(uranium_demand)

#Ajeitando os dados
reatores_info.rename(columns={'Reference Unit Power (Net Capacity)': 'Net Capacity'}, inplace=True)

reatores_merged = pd.merge(reatores_ano, reatores_info[['Name', 'Net Capacity']], on='Name', how='left')
reatores_merged = reatores_merged[['Year', 'Net Capacity']]
reatores_merged = reatores_merged.groupby(['Year']).sum().reset_index()

full_df = pd.merge(reatores_merged, uranium_demand[['Year', 'tU']], on='Year', how='left').dropna()

# #Calculo

#Média
resultado = full_df['tU'].sum() / full_df['Net Capacity'].sum()

#Regressao
# model = LinearRegression()
# model.fit(full_df[['Net Capacity']], full_df[['tU']])

# resultado = model.coef_[0]

print(f"Valor tU/Net Capacity estimado: {resultado}")

