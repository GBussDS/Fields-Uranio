import pandas as pd

# Carregar o CSV
df = pd.read_csv('csvs/Reatores_Info.csv')

# Filtrar os reatores já finalizados (aqueles que têm uma data de operação comercial)
df_finalized = df.dropna(subset=['Commercial Operation Date'])

# Função para converter a data em formato datetime
def convert_to_datetime(date_str):
    try:
        return pd.to_datetime(date_str, format='%d %b, %Y')
    except:
        return pd.NaT  # Retornar NaT se a data estiver ausente ou mal formatada

# Converter as colunas de data para o formato datetime
df_finalized['Construction Start Date'] = df_finalized['Construction Start Date'].apply(convert_to_datetime)
df_finalized['Commercial Operation Date'] = df_finalized['Commercial Operation Date'].apply(convert_to_datetime)

# Calcular o tempo de construção em anos
df_finalized['Construction Duration'] = (df_finalized['Commercial Operation Date'] - df_finalized['Construction Start Date']).dt.days / 365.25

# Agrupar por país e calcular a média de demora de construção
avg_construction_duration_by_country = df_finalized.groupby('Country')['Construction Duration'].mean().reset_index()

# Exibir a média de construção por país
print(avg_construction_duration_by_country)

# Salvar o resultado em um novo CSV
avg_construction_duration_by_country.to_csv('csvs/Tempo_Construção_País.csv', index=False)
