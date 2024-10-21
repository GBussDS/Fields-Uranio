import pandas as pd
import numpy as np

# Uranium consumption rate (tU/year per GW capacity)
uranium_per_gw = 0.16819814606373054

# Load reactor info
reactor_info = pd.read_csv('./csvs/Reatores_Info.csv')

# Load predicted completion data
completion_data = pd.read_csv('./csvs/Reatores_Finalização.csv')

# Merge reactor info with predicted completion data based on 'Name' and 'Country'
reactor_info = pd.merge(reactor_info, completion_data[['Name', 'Country', 'Predicted Completion Date']], 
                        on=['Name', 'Country'], how='left')

# Convert 'Predicted Completion Date' to datetime to avoid KeyError
reactor_info['Predicted Completion Date'] = pd.to_datetime(reactor_info['Predicted Completion Date'], errors='coerce')

# Filter only reactors that are "Under Construction"
reactors_under_construction = reactor_info[reactor_info['Status'] == 'Under Construction']

# Define a range of years to predict uranium demand for (e.g., 2024 to 2050)
years = np.arange(2024, 2051)

# Initialize an empty dictionary to store the uranium demand data per country
uranium_demand_by_country_year = {}

# Calculate uranium demand for each reactor in each future year
for year in years:
    for idx, row in reactors_under_construction.iterrows():
        country = row['Country']
        completion_year = row['Predicted Completion Date'].year
        
        # Initialize the country in the dictionary if not already present
        if country not in uranium_demand_by_country_year:
            uranium_demand_by_country_year[country] = {year: 0 for year in years}
        
        # Add the uranium demand if the reactor is completed in or before the given year
        if completion_year <= year:
            net_capacity_gw = row['Reference Unit Power (Net Capacity)']
            uranium_demand_by_country_year[country][year] += uranium_per_gw * net_capacity_gw  # in tons of uranium (tU)

# Convert the dictionary to a DataFrame, with countries as rows and years as columns
uranium_demand_df = pd.DataFrame.from_dict(uranium_demand_by_country_year, orient='index')

# Add a row for the global total by summing all the country rows
uranium_demand_df.loc['Global'] = uranium_demand_df.sum(axis=0)

# Reorder the columns to ensure they are in the correct order of years
uranium_demand_df = uranium_demand_df[sorted(uranium_demand_df.columns)]

# Print the final uranium demand matrix for inspection
print(uranium_demand_df)

# Save the final uranium demand matrix to a CSV file
uranium_demand_df.to_csv('./csvs/Predição_tUGW.csv', index=True)