import numpy as np
import pandas as pd

#Pra evitar a diferença de nomes
country_name_map = {
    'Argentina': 'ARGENTINA',
    'Armenia': 'ARMENIA',
    'Bangladesh': None,
    'Belarus': 'BELARUS',
    'Belgium': 'BELGIUM',
    'Brazil': 'BRAZIL',
    'Bulgaria': 'BULGARIA',
    'Canada': 'CANADA',
    'China': 'CHINA',
    'Czech Republic': 'CZECH REPUBLIC',
    'Egypt': None,
    'Finland': 'FINLAND',
    'France': 'FRANCE',
    'Germany': 'GERMANY',
    'Ghana': None,
    'Hungary': 'HUNGARY',
    'India': 'INDIA',
    'Iran': 'IRAN, ISLAMIC REPUBLIC OF',
    'Japan': 'JAPAN',
    'Kazakhstan': 'KAZAKHSTAN',
    'Korea RO (South)': 'KOREA, REPUBLIC OF',
    'Mexico': 'MEXICO',
    'Netherlands': 'NETHERLANDS, KINGDOM OF THE',
    'Pakistan': 'PAKISTAN',
    'Poland': None,
    'Romania': 'ROMANIA',
    'Russia': 'RUSSIA',
    'Saudi Arabia': None,
    'Slovakia': 'SLOVAKIA',
    'Slovenia': 'SLOVENIA',
    'South Africa': 'SOUTH AFRICA',
    'Spain': 'SPAIN',
    'Sweden': 'SWEDEN',
    'Switzerland': 'SWITZERLAND',
    'Turkey': None,
    'Ukraine': 'UKRAINE',
    'UAE': 'UNITED ARAB EMIRATES',
    'United Kingdom': 'UNITED KINGDOM',
    'USA': 'UNITED STATES OF AMERICA',
    'Uzbekistan': None,
    'Jordan': None,
    'Lithuania': 'LITHUANIA',
    'Thailand': None,
    'Israel': None,
    'Chile': None,
    'Indonesia': None,
    'Italy': 'ITALY',
    'Korea DPR (North)': None,
    'Malaysia': None,
    'Vietnam': None,
    'Canada*': 'CANADA',
}

reatores_ano = pd.read_csv('./csvs/Reatores_Ano.csv')
reatores_info = pd.read_csv('./csvs/Reatores_info.csv')
uranium_demand = pd.read_csv('./csvs/Uranium_demand.csv')

#Troca os nomes de um deles pros dois ficarem iguais
uranium_demand['Country'] = uranium_demand['Country'].replace(country_name_map)
uranium_demand = uranium_demand.dropna(subset=['Country'])

reatores_merged = pd.merge(reatores_ano, reatores_info[['Name', 'Country', 'Reactor Type']], on='Name', how='left')

# DataFrame com so o que vamos usar
df = pd.DataFrame()
df['Country'] = reatores_merged['Country']
df['Year'] = reatores_merged['Year']
df['Reactor Type'] = reatores_merged['Reactor Type']
df['Production'] = reatores_merged['Electricity Supplied [GW.h]']

energy_grouped = df.groupby(['Country', 'Year', 'Reactor Type'], as_index=False)['Production'].sum()

#Calcula produção total
total_production = energy_grouped.groupby(['Country', 'Year'])['Production'].sum().reset_index()
total_production.rename(columns={'Production': 'Total_Production'}, inplace=True)

#Calcula quanto de uranio o tipo gastou pela proporção do total que ele produziu de energia
energy_grouped = pd.merge(energy_grouped, total_production, on=['Country', 'Year'], how='left')
energy_grouped['Production_Proportion'] = energy_grouped['Production'] / energy_grouped['Total_Production']

merged_df = pd.merge(uranium_demand, energy_grouped, on=['Country', 'Year'], how='inner')

merged_df['Allocated_Uranium'] = merged_df['Uranium Required [T]'] * merged_df['Production_Proportion']

# Calculas as demandas
merged_df['Energy_Uranium_Ratio'] = merged_df['Production'] / merged_df['Allocated_Uranium']


merged_df.replace([np.inf, -np.inf], np.nan, inplace=True)

#Calcula as médias
mean_ratios_by_reactor_type = merged_df.groupby('Reactor Type')['Energy_Uranium_Ratio'].mean()
overall_mean = merged_df['Energy_Uranium_Ratio'].mean()

print(f"\nMédia total: {overall_mean}")

mean_ratios_by_reactor_type.to_csv('./csvs/Energy_uranium_by_type.csv')