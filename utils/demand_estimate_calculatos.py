import pandas as pd

def calculate_tu_estimado(reatores_ano_path, reatores_info_path, uranium_demand_path):
    reatores_ano = pd.read_csv(reatores_ano_path)
    reatores_info = pd.read_csv(reatores_info_path)
    uranium_demand = pd.read_csv(uranium_demand_path)
    
    uranium_demand.rename(columns={'Uranium Required [T]': 'tU'}, inplace=True)
    uranium_demand = uranium_demand[['Year', 'tU']]
    uranium_demand = uranium_demand.groupby(['Year']).sum().reset_index()
    
    reatores_info.rename(columns={'Reference Unit Power (Net Capacity)': 'Net Capacity'}, inplace=True)
    reatores_merged = pd.merge(reatores_ano, reatores_info[['Name', 'Net Capacity']], on='Name', how='left')
    reatores_merged = reatores_merged[['Year', 'Net Capacity']]
    reatores_merged = reatores_merged.groupby(['Year']).sum().reset_index()
    
    full_df = pd.merge(reatores_merged, uranium_demand[['Year', 'tU']], on='Year', how='left').dropna()
    
    tu_per_capacity = full_df['tU'].sum() / full_df['Net Capacity'].sum()
    
    reatores_info['tU estimado'] = reatores_info['Net Capacity'] * tu_per_capacity
    reatores_ano = pd.merge(reatores_ano, reatores_info[['Name', 'Net Capacity']], on='Name', how='left')
    reatores_ano['tU estimado'] = reatores_ano['Net Capacity'] * tu_per_capacity
    
    reatores_ano_with_tu.to_csv(reatores_ano_path, index=False)

    return tu_per_capacity, reatores_ano

reatores_ano_path = './csvs/Reatores_Ano.csv'
reatores_info_path = './csvs/Reatores_Info.csv'
uranium_demand_path = './csvs/Demand(WNA).csv'

tu_per_capacity, reatores_ano_with_tu = calculate_tu_estimado(
    reatores_ano_path, 
    reatores_info_path, 
    uranium_demand_path
)

tu_2023 = reatores_ano_with_tu[reatores_ano_with_tu['Year'] == 2023]['tU estimado'].sum()
print(f"Estimated tU consumed in 2023: {tu_2023}")
print(tu_per_capacity)