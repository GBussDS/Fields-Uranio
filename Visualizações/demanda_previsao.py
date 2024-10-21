import pandas as pd
import numpy as np

# Uranium consumption rate (tU/year per GW capacity)
uranium_per_gw = 0.16819814606373054

# Load reactor info
reactor_info = pd.read_csv('./csvs/Reatores_Info.csv')

# Load predicted completion data
completion_data = pd.read_csv('./csvs/Reatores_Finalização.csv')

# Load historical and predicted uranium demand data
historical_demand = pd.read_csv('./csvs/Demanda_tUGW.csv', index_col=0)
previsao_demand = pd.read_csv('./csvs/Demanda_Previsão_tUGW.csv', index_col=0)

# Remove 'Global Sum' from historical data if exists
historical_demand.drop('Global Sum', inplace=True, errors='ignore')

# Merge reactor info with predicted completion data
reactor_info = pd.merge(reactor_info, completion_data[['Name', 'Country', 'Predicted Completion Date']], 
                        on=['Name', 'Country'], how='left')

# Convert 'Predicted Completion Date' to datetime
reactor_info['Predicted Completion Date'] = pd.to_datetime(reactor_info['Predicted Completion Date'], errors='coerce')

# Filter only reactors that are "Under Construction"
reactors_under_construction = reactor_info[reactor_info['Status'] == 'Under Construction']

# Define a range of years for future prediction (2024 to 2050)
years = np.arange(2024, 2051)

# Initialize an empty dictionary to store uranium demand data per country
uranium_demand_by_country_year = {}

# Calculate uranium demand for each reactor in each future year
for year in years:
    for idx, row in reactors_under_construction.iterrows():
        country = row['Country']
        completion_year = row['Predicted Completion Date'].year
        
        # Initialize the country in the dictionary if not already present
        if country not in uranium_demand_by_country_year:
            uranium_demand_by_country_year[country] = {year: 0 for year in years}
        
        # Add uranium demand if the reactor is completed in or before the given year
        if completion_year <= year:
            net_capacity_gw = row['Reference Unit Power (Net Capacity)']
            uranium_demand_by_country_year[country][year] += uranium_per_gw * net_capacity_gw  # in tons of uranium (tU)

# Convert the dictionary to a DataFrame (countries as rows, years as columns)
uranium_demand_df = pd.DataFrame.from_dict(uranium_demand_by_country_year, orient='index')

# Add any missing countries from historical data
for country in historical_demand.index:
    if country not in uranium_demand_df.index:
        # Create a row for countries without construction reactors with 0 demand for future years
        uranium_demand_df.loc[country] = 0

# For countries in both historical and future data, add 2023 demand to 2024 onwards
for country in historical_demand.index:
    last_value_2023 = historical_demand.loc[country, '2023']
    if country in uranium_demand_df.index:
        # Add the 2023 demand to the future demand (2024 onwards)
        uranium_demand_df.loc[country] += last_value_2023
    else:
        # If no future reactors, set 2024 onward to the 2023 value
        uranium_demand_df.loc[country] = last_value_2023

# Combine historical data (1961-2023) with predicted data (2024-2050)
combined_demand_df = pd.concat([historical_demand, uranium_demand_df], axis=1)

# Add a row for the global total by summing all country rows
combined_demand_df.loc['Global'] = combined_demand_df.sum(axis=0)

# Reorder columns to ensure they are in chronological order
combined_demand_df = combined_demand_df[sorted(combined_demand_df.columns.astype(int))]

# Save the combined demand matrix to the same CSV file
combined_demand_df.to_csv('./csvs/Demanda_Previsão_tUGW.csv')

# Print the final DataFrame for inspection
print(combined_demand_df)
