import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração da página
st.set_page_config(page_title="Análise de Construção e Demanda de Reatores", page_icon="⏳")

# Carregar dados
construction_data = pd.read_csv("../csvs/Tempo_Construção_País.csv")
reactor_completion_data = pd.read_csv("../csvs/Reatores_Finalização.csv")
historical_demand_data = pd.read_csv("../csvs/Demanda_tUGW.csv")

# Gráfico 1: Tempo médio de construção por país
st.write("## Tempo Médio de Construção de Reatores por País")
avg_construction_time = construction_data.groupby("Country")["Construction Duration"].mean().sort_values()
plt.figure(figsize=(10, 8))
sns.barplot(x=avg_construction_time, y=avg_construction_time.index, palette="viridis")
plt.xlabel("Tempo Médio de Construção (anos)")
plt.title("Tempo Médio de Construção de Reatores por País")
st.pyplot(plt)

# Tabela: Datas de Finalização dos Reatores
st.write("## Datas de Finalização dos Reatores")
reactor_completion_data["Construction Start Date"] = pd.to_datetime(reactor_completion_data["Construction Start Date"])
reactor_completion_data["Predicted Completion Date"] = pd.to_datetime(reactor_completion_data["Predicted Completion Date"])
completion_table = reactor_completion_data.sort_values(by=["Country", "Predicted Completion Date"])
st.dataframe(completion_table[["Name", "Country", "Construction Start Date", "Predicted Completion Date"]])

# Gráfico 3: Demanda Histórica de Urânio com Previsão (1964-2050)
st.write("## Demanda Histórica e Previsão de Demanda de Urânio por País")
selected_countries = st.multiselect("Selecione os países para visualizar", sorted(historical_demand_data["Country"].unique()), default=["FRANCE", "CHINA"])
filtered_demand_data = historical_demand_data[historical_demand_data["Country"].isin(selected_countries)]
filtered_demand_data = filtered_demand_data.set_index("Country").T  # Transpor para facilitar a visualização por ano
filtered_demand_data.index.name = "Year"  # Define o nome do índice para 'Year'

# Plot da demanda ao longo dos anos para os países selecionados
plt.figure(figsize=(12, 6))
for country in selected_countries:
    plt.plot(filtered_demand_data.index, filtered_demand_data[country], label=country, marker="o")
plt.xlabel("Ano")
plt.ylabel("Demanda de Urânio (tU)")
plt.title("Demanda Histórica e Projeções de Urânio por País")
plt.legend(title="País", loc="upper left", bbox_to_anchor=(1, 1))
plt.grid(True)
st.pyplot(plt)

# Explicação
st.write("""
### Explicação dos Gráficos
1. **Tempo Médio de Construção**: Tempo médio necessário para construir reatores nucleares, por país.
2. **Tabela de Datas de Conclusão de Reatores**: Exibe a previsão de conclusão dos reatores em construção, por país e data.
3. **Demanda Histórica e Projeção de Demanda de Urânio**: Acompanha a demanda histórica de urânio e inclui previsões até 2050.
""")
