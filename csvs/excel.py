import pandas as pd

reatores_ano = pd.read_csv('Reatores_Ano.csv')
reatores_info = pd.read_csv('Reatores_Info.csv')

reatores_juntos = pd.merge(reatores_ano, reatores_info, on='Name')

soma_por_ano = reatores_juntos.groupby('Year')['Reference Unit Power [MW]'].sum().reset_index()

soma_por_ano.to_csv('Soma_Ano_NetCapacity.csv', index=False)
