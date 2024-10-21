import pandas as pd
import numpy as np

# Load reactor info and the previously calculated predicted completion dates
reactor_info = pd.read_csv('./csvs/Reatores_Info.csv')
completion_data = pd.read_csv('./csvs/Reatores_Predicted_Completion.csv')

# Merge reactor info with predicted completion data
reactor_info = pd.merge(reactor_info, completion_data, on=['Name', 'Country'], how='left')

# Convert 'Predicted Completion Date' to datetime
reactor_info['Predicted Completion Date'] = pd.to_datetime(reactor_info['Predicted Completion Date'], errors='coerce')

# Filter only "Under Construction" reactors
reactors_under_construction = reactor_info[reactor_info['Status'] == 'Under Construction']

# Uranium consumption rate (tU/year per GW capacity)
uranium_per_gw = 25  # You may update this with a more precise value if available

# Function to calculate annual demand based on reactor capacity and proportion of operational year
def calculate_annual_demand(row, year):
    # Skip reactors with missing completion dates
    if pd.isnull(row['Predicted Completion Date']):
        return 0
    
    # Get the completion year of the reactor
    completion_year = row['Predicted Completion Date'].year
    
    # If the reactor is finished after the year in question, it will not contribute to demand
    if year < completion_year:
        return 0
    
    # If the reactor is completed in the target year, calculate part-year operation
    if year == completion_year:
        # Calculate days of operation in the completion year
        days_operational = (pd.Timestamp(year=year, month=12, day=31) - row['Predicted Completion Date']).days + 1
        proportion_year = days_operational / 365
    else:
        # Reactor is fully operational in this year
        proportion_year = 1.0
    
    # Calculate the uranium demand for this reactor in the target year
    annual_demand = proportion_year * uranium_per_gw * (row['Reference Unit Power (Net Capacity)'] / 1000)  # in tons of uranium (tU)
    
    return annual_demand

# Define a range of years to predict uranium demand for (e.g., 2024 to 2050)
years = np.arange(2024, 2051)

# Initialize an empty list to store the uranium demand data
demand_by_country_year = []

# Calculate uranium demand for each reactor in each future year
for year in years:
    for idx, row in reactors_under_construction.iterrows():
        annual_demand = calculate_annual_demand(row, year)
        demand_by_country_year.append({
            'Country': row['Country'],
            'Year': year,
            'Annual_Uranium_Demand_tU': annual_demand
        })

# Convert the list to a DataFrame
demand_df = pd.DataFrame(demand_by_country_year)

# Group by country and year to calculate the total uranium demand per country per year
annual_uranium_demand = demand_df.groupby(['Country', 'Year'])['Annual_Uranium_Demand_tU'].sum().reset_index()

# Save the results to a CSV file
annual_uranium_demand.to_csv('./csvs/Annual_Uranium_Demand_Prediction.csv', index=False)

# Print the first few rows of the result
print(annual_uranium_demand.head())
