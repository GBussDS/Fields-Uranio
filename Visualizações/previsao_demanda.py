import pandas as pd
import matplotlib.pyplot as plt

# Definindo o caminho do arquivo CSV
csv_path = 'csvs/Demanda_Predição_tUGW.csv'

# Lendo o arquivo CSV
df = pd.read_csv(csv_path)

# Configurando o index como a primeira coluna (países)
df.set_index(df.columns[0], inplace=True)

# Removendo a linha "Global" do DataFrame
df = df.drop('Global')

# Convertendo os anos para o eixo X
years = df.columns.astype(int)

# Criando o gráfico de linhas para todos os países, exceto "Global"
plt.figure(figsize=(12, 8))

# Percorrendo cada país e plotando sua demanda
for country in df.index:
    plt.plot(years, df.loc[country], label=country)

# Adicionando título e rótulos em português
plt.title('Predição de Demanda de Urânio (2024-2050)', fontsize=16, weight='bold')
plt.xlabel('Ano', fontsize=12)
plt.ylabel('Demanda de Urânio (tU)', fontsize=12)

# Adicionando gridlines
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# Ajustando os ticks do eixo X para cada 5 anos
plt.xticks(ticks=range(2024, 2051, 5))

# Exibindo a legenda
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

# Aplicando layout automático para não sobrepor os elementos
plt.tight_layout()

# Mostrando o gráfico
plt.show()
