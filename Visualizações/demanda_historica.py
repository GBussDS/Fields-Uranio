import numpy as np
import pandas as pd

# Map country names to standardize
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

# Load data
reatores_ano = pd.read_csv('./csvs/Reatores_Ano.csv')
reatores_info = pd.read_csv('./csvs/Reatores_Info.csv')
uranium_demand = pd.read_csv('./csvs/Demand(WNA).csv')
demanda_historica = pd.read_csv('./csvs\RedBook\Demanda(RedBook).csv')  # For years <= 2006

demanda_historica = demanda_historica[demanda_historica['ano'] >= 1980]
# Standardize country names in uranium_demand
uranium_demand['Country'] = uranium_demand['Country'].replace(country_name_map)
uranium_demand = uranium_demand.dropna(subset=['Country'])

# Ensure 'Year' is integer
uranium_demand['Year'] = uranium_demand['Year'].astype(int)
demanda_historica.rename(columns={'ano': 'Year', 'uranio(ton.)': 'Uranium_Required'}, inplace=True)
demanda_historica['Year'] = demanda_historica['Year'].astype(int)

# Merge reactor data
reatores_merged = pd.merge(
    reatores_ano,
    reatores_info[['Name', 'Country', 'Reactor Type']],
    on='Name',
    how='left'
)

# Create DataFrame with required columns
df = pd.DataFrame()
df['Country'] = reatores_merged['Country']
df['Year'] = reatores_merged['Year'].astype(int)
df['Reactor_Type'] = reatores_merged['Reactor Type']
df['Production'] = reatores_merged['Electricity Supplied [GW.h]']

# Remove rows with missing values
df = df.dropna(subset=['Country', 'Year', 'Reactor_Type', 'Production'])

# Separate data for pre-2007 and post-2007
df_pre_2007 = df[df['Year'] <= 2006]
df_post_2006 = df[df['Year'] >= 2007]

# ========================
# Pre-2007 Calculation
# ========================

def compute_mean_energy_per_uranium_pre_2007(energy_data, uranium_data):
    # Aggregate energy production by Year and Reactor_Type
    energy_grouped = energy_data.groupby(['Year', 'Reactor_Type'], as_index=False)['Production'].sum()

    # Total energy production per year
    total_energy_per_year = energy_grouped.groupby('Year', as_index=False)['Production'].sum()
    total_energy_per_year.rename(columns={'Production': 'Total_Energy'}, inplace=True)

    # Merge with uranium demand data
    uranium_energy = pd.merge(uranium_data, total_energy_per_year, on='Year', how='inner')

    # Calculate annual energy per uranium ratio (GWh/tU)
    uranium_energy['Energy_per_Uranium'] = uranium_energy['Total_Energy'] / uranium_energy['Uranium_Required']

    # Merge with energy data by reactor type
    energy_grouped = pd.merge(energy_grouped, uranium_energy[['Year', 'Energy_per_Uranium']], on='Year', how='left')

    # Apply the annual ratio to each reactor type
    energy_grouped['Energy_per_Uranium_Type'] = energy_grouped['Energy_per_Uranium']

    # Remove any missing values
    energy_grouped = energy_grouped.dropna(subset=['Energy_per_Uranium_Type'])

    # Calculate the mean energy per uranium for each reactor type
    mean_energy_per_uranium = energy_grouped.groupby('Reactor_Type')['Energy_per_Uranium_Type'].mean().reset_index()

    # Add the 'Period' column with value 'pre'
    mean_energy_per_uranium['Period'] = 'pre'

    # Rename columns
    mean_energy_per_uranium.rename(columns={'Energy_per_Uranium_Type': 'GWh_per_tU'}, inplace=True)

    return mean_energy_per_uranium

# Compute for pre-2007
uranium_demand_pre_2007 = demanda_historica[demanda_historica['Year'] <= 2006]
result_pre_2007 = compute_mean_energy_per_uranium_pre_2007(df_pre_2007, uranium_demand_pre_2007)

# ========================
# Post-2007 Calculation
# ========================

# Filter uranium_demand for years >= 2007
uranium_demand_post_2006 = uranium_demand[uranium_demand['Year'] >= 2007]

# Group energy production by Country, Year, Reactor_Type
energy_grouped_post_2006 = df_post_2006.groupby(['Country', 'Year', 'Reactor_Type'], as_index=False)['Production'].sum()

# Calculate total production per Country and Year
total_production = energy_grouped_post_2006.groupby(['Country', 'Year'])['Production'].sum().reset_index()
total_production.rename(columns={'Production': 'Total_Production'}, inplace=True)

# Calculate production proportion
energy_grouped_post_2006 = pd.merge(energy_grouped_post_2006, total_production, on=['Country', 'Year'], how='left')
energy_grouped_post_2006['Production_Proportion'] = energy_grouped_post_2006['Production'] / energy_grouped_post_2006['Total_Production']

# Merge with uranium_demand
merged_df = pd.merge(uranium_demand_post_2006, energy_grouped_post_2006, on=['Country', 'Year'], how='inner')

# Allocate uranium
merged_df['Allocated_Uranium'] = merged_df['Uranium Required [T]'] * merged_df['Production_Proportion']

# Calculate the energy per uranium ratio
merged_df['Energy_Uranium_Ratio'] = merged_df['Production'] / merged_df['Allocated_Uranium']

# Replace infinities and drop NaNs
merged_df.replace([np.inf, -np.inf], np.nan, inplace=True)
merged_df.dropna(subset=['Energy_Uranium_Ratio'], inplace=True)

# Calculate mean ratios per Reactor Type
mean_ratios = merged_df.groupby('Reactor_Type')['Energy_Uranium_Ratio'].mean().reset_index()

# Add the 'Period' column with value 'pos'
mean_ratios['Period'] = 'pos'

# Rename columns
mean_ratios.rename(columns={'Energy_Uranium_Ratio': 'GWh_per_tU'}, inplace=True)
mean_ratios = mean_ratios[['Reactor_Type', 'Period', 'GWh_per_tU']]

# ========================
# Combine Results
# ========================

# Ensure the pre-2007 result has the same columns
result_pre_2007 = result_pre_2007[['Reactor_Type', 'Period', 'GWh_per_tU']]

# Combine the two DataFrames
combined_results = pd.concat([result_pre_2007, mean_ratios], ignore_index=True)

# Display the combined results
print("Combined Energy per Uranium Ratios:")
print(combined_results)

# Save the combined results to a single CSV file
combined_results.to_csv('./csvs/Energia_Tipo.csv', index=False)
