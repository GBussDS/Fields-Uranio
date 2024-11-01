import pandas as pd
import numpy as np

# Adjusted deposit type values based on updated industry understanding
deposit_type_values = {
    'Sandstone': 9,
    'Phosphate': 6,
    'Surficial': 7,
    'Polymetallic Iron Oxide Breccia Complex': 8,
    'Proterozoic Unconformity': 9,
    'Carbonate': 5,
    'Granite-related': 4,
    'Intrusive': 5,
    'Volcanic-related': 7,
    'Metamorphite': 6,
    'Metasomatite': 5
}

# Adjusted deposit subtype values for more accurate cost predictions
deposit_subtype_values = {
    'Rollfront': 9,
    'Basal Channel': 8,
    'Tabular': 7,
    'Minerochemical phosphorite': 6,
    'Lacustrine-playa': 6,
    'Perigranitic': 5,
    'Endogranitic': 4,
    'Structurally-controlled': 7,
    'Plutonic': 6,
    'Na-metasomatite': 4
}

# Read the CSV file with deposit data
df = pd.read_csv('csvs/Depósitos.csv')

# Map the deposit type and subtype values
df['Deposit Type'] = df['Deposit Type'].apply(lambda x: deposit_type_values.get(x, 5))
df['Deposit Subtype'] = df['Deposit Subtype'].apply(lambda x: deposit_subtype_values.get(x, 5))

# Function to extract min and max values from the resource and grade ranges
def extract_values(range_str):
    if pd.isnull(range_str):
        return 0.0, 0.0
    if not isinstance(range_str, str):
        range_str = str(range_str)
    
    range_str = range_str.replace('≥', '').replace('<', '').replace('>', '')
    try:
        min_val, max_val = range_str.split(' - ')
        return float(min_val), float(max_val)
    except ValueError:
        return 0.0, 0.0

# Calculate weighted average of min and max values, with emphasis on the minimum
def calculate_weighted_average(min_val, max_val):
    if min_val == max_val:
        return min_val
    return min_val + (max_val - min_val) * 0.2

# Adjust the acquisition cost using the deposit type, subtype, and resource/grade range
def calculate_adjusted_interval(row):
    min_res, max_res = extract_values(row['Resource Range'])
    min_grade, max_grade = extract_values(row['Grade Range (Teor)'])
    
    if min_grade == 0 or max_grade == 0:
        return 0.0, 0.0
    
    # Calculate weighted resource based on minimum resource value
    weighted_res = calculate_weighted_average(min_res, max_res)
    
    # Adjust alpha for industry-wide uranium pricing pressure
    alpha = 0.10  

    # Calculate acquisition cost based on the grade and resource weight
    adj_min = (1 / max_grade) * (1 - alpha * (weighted_res / 1000000))
    adj_max = (1 / min_grade) * (1 - alpha * (weighted_res / 1000000))
    
    # Adjust using deposit type and subtype factors
    deposit_type_factor = (11 - row['Deposit Type']) / 1.5
    deposit_subtype_factor = (11 - row['Deposit Subtype']) / 1.5
    
    acquisition_cost_min = adj_min * deposit_type_factor * deposit_subtype_factor
    acquisition_cost_max = adj_max * deposit_type_factor * deposit_subtype_factor
    
    # Ensure costs below 40 are rare, and adjust the output to be realistic
    acquisition_cost_min = max(acquisition_cost_min, 60)
    acquisition_cost_max = max(acquisition_cost_max, 100)
    
    return acquisition_cost_min, acquisition_cost_max

# Apply the calculation to each row in the dataframe
df['Acquisition Cost Min'], df['Acquisition Cost Max'] = zip(*df.apply(calculate_adjusted_interval, axis=1))

# Round the acquisition costs and clean the dataset
df['Acquisition Cost Min'] = df['Acquisition Cost Min'].round(0)
df['Acquisition Cost Max'] = df['Acquisition Cost Max'].round(0)
df_cleaned = df.dropna(subset=['Acquisition Cost Min', 'Acquisition Cost Max'])

# Calculate the average resource and cost for each deposit
df_cleaned['Average Resource'] = df_cleaned['Resource Range'].apply(lambda x: calculate_weighted_average(*extract_values(x)))
df_cleaned['Average Cost'] = df_cleaned[['Acquisition Cost Min', 'Acquisition Cost Max']].mean(axis=1)

# Group data by country to calculate total uranium resources and costs
def calculate_country_summary(df):
    summary = df.groupby('Country').agg(
        Total_Uranium=('Average Resource', 'sum'),
        Cost_Below_40=('Average Resource', lambda x: x[df['Average Cost'] < 40].sum()),
        Cost_Below_80=('Average Resource', lambda x: x[df['Average Cost'] < 80].sum()),
        Cost_Below_130=('Average Resource', lambda x: x[df['Average Cost'] < 130].sum()),
        Cost_Below_260=('Average Resource', lambda x: x[df['Average Cost'] < 260].sum()),
        Average_Deposit_Cost=('Average Cost', 'mean')
    ).reset_index()
    
    return summary

# Generate the country summary
country_summary = calculate_country_summary(df_cleaned)

# Save the updated acquisition cost summary to a CSV
country_summary.to_csv('csvs/Predição_Custo_Aquisição.csv', index=False)

# Print the first few rows of the summary for inspection
print(country_summary.head())
