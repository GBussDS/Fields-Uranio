import pandas as pd
import numpy as np

# Etapa 1: Atribuir valores de 'Deposit Type' e 'Deposit Subtype'
deposit_type_values = {
    'Sandstone': 10,
    'Phosphate': 8,
    'Surficial': 7,
    'Polymetallic Iron Oxide Breccia Complex': 7,
    'Proterozoic Unconformity': 6,
    'Carbonate': 5,
    'Granite-related': 4,
    'Intrusive': 4,
    'Volcanic-related': 3,
    'Metamorphite': 3,
    'Metasomatite': 2
}

deposit_subtype_values = {
    'Rollfront': 10,
    'Basal Channel': 9,
    'Tabular': 8,
    'Minerochemical phosphorite': 7,
    'Lacustrine-playa': 6,
    'Perigranitic': 5,
    'Endogranitic': 4,
    'Structurally-controlled': 3,
    'Plutonic': 3,
    'Na-metasomatite': 2
}

# Ler o arquivo CSV
df = pd.read_csv('csvs/depositos.csv')

# Mapear os valores de 'Deposit Type' e 'Deposit Subtype'
df['Deposit Type'] = df['Deposit Type'].apply(lambda x: deposit_type_values.get(x, 5))
df['Deposit Subtype'] = df['Deposit Subtype'].apply(lambda x: deposit_subtype_values.get(x, 5))

# Salvar o CSV modificado
df.to_csv('csvs/depositos_modificados.csv', index=False)

# Etapa 2: Calcular o intervalo ajustado com ponderação para valores mínimos
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

def calculate_weighted_average(min_val, max_val):
    """Calcula um valor médio ponderado com base em 20% acima do mínimo."""
    if min_val == max_val:
        return min_val
    return min_val + (max_val - min_val) * 0.2

def calculate_adjusted_interval(row):
    min_res, max_res = extract_values(row['Resource Range'])
    min_grade, max_grade = extract_values(row['Grade Range (Teor)'])
    
    if min_grade == 0 or max_grade == 0:
        return 0.0, 0.0
    
    # Usar a média ponderada para calcular a influência
    weighted_res = calculate_weighted_average(min_res, max_res)
    
    alpha = 0.05
    
    # Calcular Acquisition Cost Min com o max_grade (para pior cenário) e min_grade (para melhor cenário)
    adj_min = (1 / max_grade) * (1 - alpha * (weighted_res / 1000000))
    adj_max = (1 / min_grade) * (1 - alpha * (weighted_res / 1000000))
    
    deposit_type_factor = (11 - row['Deposit Type'])
    deposit_subtype_factor = (11 - row['Deposit Subtype'])
    
    acquisition_cost_min = adj_min * deposit_type_factor * deposit_subtype_factor
    acquisition_cost_max = adj_max * deposit_type_factor * deposit_subtype_factor
    
    return acquisition_cost_min, acquisition_cost_max

df['Acquisition Cost Min'], df['Acquisition Cost Max'] = zip(*df.apply(calculate_adjusted_interval, axis=1))

# Arredondar os valores e remover linhas vazias
df['Acquisition Cost Min'] = df['Acquisition Cost Min'].round(0)
df['Acquisition Cost Max'] = df['Acquisition Cost Max'].round(0)
df_cleaned = df.dropna(subset=['Acquisition Cost Min', 'Acquisition Cost Max'])

# Salvar o CSV limpo
df_cleaned.to_csv('csvs/depositos_acquisition_cost_cleaned.csv', index=False)

# Etapa 3: Calcular as métricas por país
df_cleaned['Average Resource'] = df_cleaned['Resource Range'].apply(lambda x: calculate_weighted_average(*extract_values(x)))
df_cleaned['Average Cost'] = df_cleaned[['Acquisition Cost Min', 'Acquisition Cost Max']].mean(axis=1)

# Calcular métricas por país
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

country_summary = calculate_country_summary(df_cleaned)

# Salvar o resumo por país
country_summary.to_csv('csvs/country_uranium_summary.csv', index=False)

# Exibir o resumo final
print(country_summary.head())
