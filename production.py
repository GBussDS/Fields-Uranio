import numpy as np
import pandas as pd

reatores_ano = pd.read_csv('./csvs/Reatores_Ano.csv')
reatores_info = pd.read_csv('./csvs/Reatores_info.csv')

df = pd.DataFrame()

reatores_merged = pd.merge(reatores_ano, reatores_info[['Name', 'Country']], on='Name', how='left')
df_merge = reatores_merged[reatores_merged['Year'] == reatores_ano['Year']]

df['Nome'] = df_merge['Name']
df['Produção'] = df_merge['Electricity Supplied [GW.h]']
df['Ano'] = df_merge['Year']
df['Países'] = df_merge['Country']

df = df.groupby(['Países', 'Ano'])['Produção'].sum().reset_index()

df_diff = pd.DataFrame()

df_diff['Países'] = df['Países'].unique()

for a in df['Ano'].unique()[1:]: 
    df_diff[a] = None 
    
    for p in df_diff['Países']:
        producao_atual = df.loc[(df['Países'] == p) & (df['Ano'] == a), 'Produção']
        producao_anterior = df.loc[(df['Países'] == p) & (df['Ano'] == a - 1), 'Produção']
        
        if not producao_atual.empty and not producao_anterior.empty:
            diferenca = producao_atual.values[0] - producao_anterior.values[0]
            df_diff.loc[df_diff['Países'] == p, a] = diferenca

df_diff.to_csv('./csvs/diferenca_producao.csv', index=False)