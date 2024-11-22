import pandas as pd
import os

# Caminho dos arquivos
input_path = r'csvs\RedBook\Estoque(RedBook).csv'
output_path = r'csvs\RedBook\Anos_Estoque.csv'

# Ler os dados do arquivo CSV de entrada
df = pd.read_csv(input_path)

# Criar colunas adicionais para o novo DataFrame
df['Accumulated Stock'] = df['Stock'].cumsum()

# Calcular "Years of Stock"
df['Years of Stock'] = df.apply(
    lambda row: row['Accumulated Stock'] / row['Demand'] if row['Demand'] > 0 else None, axis=1
)

# Calcular "Years of Stock (w/Production)"
df['Years of Stock(w/Production)'] = df.apply(
    lambda row: -row['Accumulated Stock'] / row['Stock'] if row['Stock'] < 0 else None, axis=1
)

# Garantir que o diretório existe
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Salvar o novo DataFrame no arquivo de saída
df.to_csv(output_path, index=False)

print(f"Arquivo salvo em {output_path}")
