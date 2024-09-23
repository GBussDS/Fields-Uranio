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
            df_diff.loc[df_diff['Países'] == p, a] = int(diferenca)

df_diff = df_diff.T
df_diff.columns = df_diff.iloc[0]  # Define the first row as column names
df_diff = df_diff[1:]  # Remove the first row
df_diff = df_diff.sort_index()
df_diff = df_diff.rename_axis('Ano').reset_index()
df_diff = df_diff[~df_diff['Ano'].isin([1964, 1965, 1966, 1967, 1968, 1969])]

df_diff.to_csv('./csvs/diferenca_producao.csv', index=False)

# import matplotlib.pyplot as plt

# fig, ax = plt.subplots(figsize=(10, 6))

# anos = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]

# bottom_pos = [0] * len(anos)
# bottom_neg = [0] * len(anos) 

# df_diff = df_diff.fillna(0)
# df_diff = df_diff[~df_diff['Países'].isin(['ITALY', 'KAZAKHSTAN', 'LITHUANIA'])]

# for p in df_diff['Países'].unique():
#     valores_pais = df_diff.loc[df_diff['Países'] == p, anos].values.flatten()

#     valores_positivos = [v if v >= 0 else 0 for v in valores_pais]
#     valores_negativos = [v if v < 0 else 0 for v in valores_pais]

#     cor = next(ax._get_lines.prop_cycler)['color']

#     ax.bar(anos, valores_positivos, bottom=bottom_pos, label=p, color=cor)
#     ax.bar(anos, valores_negativos, bottom=bottom_neg, color=cor)

#     bottom_pos = [i + j for i, j in zip(bottom_pos, valores_positivos)]
#     bottom_neg = [i + j for i, j in zip(bottom_neg, valores_negativos)]

# soma_total = [i + j for i, j in zip(bottom_pos, bottom_neg)]
# ax.plot(anos, soma_total, label='Soma Total', color = 'black', marker='o')
# ax.set_ylabel('Soma Total de Produção [GW.h]')
# ax.grid(False)

# ax.set_ylim([min(bottom_neg) * 1.05, max(bottom_pos) * 1.05])
# ax.grid(True, which='both', axis='y', linestyle='--', linewidth=0.3)
# ax.axhline(0, color='black', linestyle='--', linewidth=0.7)
# ax.set_title('Diferença de Produção de Energia por País')
# ax.set_xlabel('Ano')
# ax.set_ylabel('Diferença de Produção [GW.h]')
# ax.legend(title="Países", bbox_to_anchor=(1.05, 1), loc='upper left', ncol=2, fontsize='small')
# plt.tight_layout()

# plt.show()