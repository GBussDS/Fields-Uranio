import pandas as pd

# Load historical data (up to 2023)
historical_data = pd.read_csv('csvs/Demanda_tUGW.csv', index_col=0)

# Load forecast data (from 2024 onwards)
forecast_data = pd.read_csv('csvs/Demanda_Previsão_tUGW.csv', index_col=0)

# Ensure that 'Global' in both datasets is consistent and fix any potential naming issues
historical_data.rename(index={"Global Sum": "Global"}, inplace=True)
forecast_data.rename(index={"Global Sum": "Global"}, inplace=True)

# Merge the two datasets by concatenating them along the columns (years as columns)
combined_data = pd.concat([historical_data, forecast_data], axis=1)

# Save the combined data into a new CSV file
combined_data.to_csv('csvs/Demanda_Completa.csv')

# Print the first few rows for verification
print(combined_data.head())
