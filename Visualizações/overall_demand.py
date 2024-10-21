import numpy as np
import pandas as pd

# Create a dictionary mapping from uranium_demand country names to energy_grouped country names
country_name_map = {
    'Argentina': 'ARGENTINA',
    'Armenia': 'ARMENIA',
    'Bangladesh': None,  # Not present in energy_grouped
    'Belarus': 'BELARUS',
    'Belgium': 'BELGIUM',
    'Brazil': 'BRAZIL',
    'Bulgaria': 'BULGARIA',
    'Canada': 'CANADA',
    'China': 'CHINA',
    'Czech Republic': 'CZECH REPUBLIC',
    'Egypt': None,  # Not present in energy_grouped
    'Finland': 'FINLAND',
    'France': 'FRANCE',
    'Germany': 'GERMANY',
    'Ghana': None,  # Not present in energy_grouped
    'Hungary': 'HUNGARY',
    'India': 'INDIA',
    'Iran': 'IRAN, ISLAMIC REPUBLIC OF',
    'Japan': 'JAPAN',
    'Kazakhstan': 'KAZAKHSTAN',
    'Korea RO (South)': 'KOREA, REPUBLIC OF',
    'Mexico': 'MEXICO',
    'Netherlands': 'NETHERLANDS, KINGDOM OF THE',
    'Pakistan': 'PAKISTAN',
    'Poland': None,  # Not present in energy_grouped
    'Romania': 'ROMANIA',
    'Russia': 'RUSSIA',
    'Saudi Arabia': None,  # Not present in energy_grouped
    'Slovakia': 'SLOVAKIA',
    'Slovenia': 'SLOVENIA',
    'South Africa': 'SOUTH AFRICA',
    'Spain': 'SPAIN',
    'Sweden': 'SWEDEN',
    'Switzerland': 'SWITZERLAND',
    'Turkey': None,  # Not present in energy_grouped
    'Ukraine': 'UKRAINE',
    'UAE': 'UNITED ARAB EMIRATES',
    'United Kingdom': 'UNITED KINGDOM',
    'USA': 'UNITED STATES OF AMERICA',
    'Uzbekistan': None,  # Not present in energy_grouped
    'Jordan': None,  # Not present in energy_grouped
    'Lithuania': 'LITHUANIA',
    'Thailand': None,  # Not present in energy_grouped
    'Israel': None,  # Not present in energy_grouped
    'Chile': None,  # Not present in energy_grouped
    'Indonesia': None,  # Not present in energy_grouped
    'Italy': 'ITALY',
    'Korea DPR (North)': None,  # Not present in energy_grouped
    'Malaysia': None,  # Not present in energy_grouped
    'Vietnam': None,  # Not present in energy_grouped
    'Canada*': 'CANADA',  # Match Canada* to CANADA
}

reatores_ano = pd.read_csv('./csvs/Reatores_Ano.csv')
reatores_info = pd.read_csv('./csvs/Reatores_Info.csv')
uranium_demand = pd.read_csv('./csvs/Demand(WNA).csv')

# Replace country names in uranium_demand based on the mapping
uranium_demand['Country'] = uranium_demand['Country'].replace(country_name_map)

# Drop any rows where the Country was mapped to None (i.e., countries not present in energy_grouped)
uranium_demand = uranium_demand.dropna(subset=['Country'])

reatores_merged = pd.merge(reatores_ano, reatores_info[['Name', 'Country']], on='Name', how='left')

df = pd.DataFrame()
df['Country'] = reatores_merged['Country']
df['Year'] = reatores_merged['Year']
df['Production'] = reatores_merged['Electricity Supplied [GW.h]']

# Group by 'Country' and 'Year', and sum the 'EnergyProduced'
energy_grouped = df.groupby(['Country', 'Year'], as_index=False)['Production'].sum()

# Merge the two DataFrames on 'Country' and 'Year'
merged_df = pd.merge(uranium_demand, energy_grouped, on=['Country', 'Year'], how='inner')

merged_df['Energy_Uranium_Ratio'] = merged_df['Production'] / merged_df['Uranium Required [T]']

# Step 2: Calculate the mean of this new column
merged_df.replace([np.inf, -np.inf], np.nan, inplace=True)
mean_ratio = merged_df['Energy_Uranium_Ratio'].mean()

print(mean_ratio)
