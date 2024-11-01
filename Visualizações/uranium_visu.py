import pandas as pd
import matplotlib.pyplot as plt

# Carregar o arquivo de dados consolidado
data = pd.read_csv("UraniumProductionHistorical.csv", index_col="Country")

# Configurar o gráfico de linhas
plt.figure(figsize=(16, 10))
for country in data.index:
    plt.plot(data.columns, data.loc[country], label=country, linewidth=0.8)

# Ajustes do gráfico
plt.xlabel("Year")
plt.ylabel("Uranium Production (tU)")
plt.title("Annual Uranium Production by Country (1998 - 2022)")

# Ajuste da legenda para ficar ao lado do gráfico e não sobrepô-lo
plt.legend(loc="center left", bbox_to_anchor=(1, 0.5), fontsize="small", title="Country", ncol=2)
plt.grid(True)
plt.tight_layout(rect=[0, 0, 0.85, 1])  # Ajuste para dar espaço à legenda ao lado

# Exibir o gráfico
plt.show()
