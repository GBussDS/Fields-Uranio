import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Configuração da página
st.set_page_config(page_title="Análise de Produção, Demanda e Estoque de Urânio", page_icon="📊")

# Carregar os dados
data = pd.read_csv("../csvs/RedBook/Anos_Estoque.csv")

# Filtro de intervalo de anos
st.sidebar.title("Filtros")
year_range = st.sidebar.slider("Selecione o intervalo de anos", int(data["Year"].min()), int(data["Year"].max()), (int(data["Year"].min()), int(data["Year"].max())))
filtered_data = data[(data["Year"] >= year_range[0]) & (data["Year"] <= year_range[1])]

# Gráfico de Produção e Demanda
st.write("### Produção e Demanda por Ano")
prod_demand_options = st.multiselect("Escolha o que deseja visualizar", ["Produção", "Demanda"], default=["Produção", "Demanda"])

plt.figure(figsize=(12, 6))
if "Produção" in prod_demand_options:
    sns.lineplot(data=filtered_data, x="Year", y="Production", label="Produção", marker="o")
if "Demanda" in prod_demand_options:
    sns.lineplot(data=filtered_data, x="Year", y="Demand", label="Demanda", marker="o")

plt.xlabel("Ano")
plt.ylabel("Toneladas de Urânio")
plt.legend(title="Linhas Selecionadas")
plt.grid(True)
st.pyplot(plt)

# Gráfico de Estoque por Ano (Gráfico de Área)
st.write("### Estoque por Ano")
plt.figure(figsize=(12, 6))
sns.lineplot(data=filtered_data, x="Year", y="Stock", marker="o")
plt.fill_between(filtered_data["Year"], filtered_data["Stock"], alpha=0.3)
plt.xlabel("Ano")
plt.ylabel("Estoque (Toneladas)")
plt.grid(True)
st.pyplot(plt)

# Gráfico de Estoque Acumulado por Ano (Gráfico de Área)
st.write("### Estoque Acumulado por Ano")
plt.figure(figsize=(12, 6))
sns.lineplot(data=filtered_data, x="Year", y="Accumulated Stock", marker="o")
plt.fill_between(filtered_data["Year"], filtered_data["Accumulated Stock"], alpha=0.3)
plt.xlabel("Ano")
plt.ylabel("Estoque Acumulado (Toneladas)")
plt.grid(True)
st.pyplot(plt)

# Gráfico de Anos Restantes de Estoque
st.write("### Anos Restantes de Estoque")
plt.figure(figsize=(12, 6))
sns.lineplot(data=filtered_data, x="Year", y="Years of Stock", marker="o")
plt.xlabel("Ano")
plt.ylabel("Anos Restantes de Estoque")
plt.grid(True)
st.pyplot(plt)

# Gráfico de Anos Restantes de Estoque (Com Produção)
st.write("### Anos Restantes de Estoque (Com Produção)")
plt.figure(figsize=(12, 6))
sns.lineplot(data=filtered_data, x="Year", y="Years of Stock(w/Production)", marker="o")
plt.xlabel("Ano")
plt.ylabel("Anos Restantes de Estoque (Com Produção)")
plt.grid(True)
st.pyplot(plt)

# Explicação dos gráficos
st.write("""
### Explicação dos Gráficos
- **Produção e Demanda por Ano**: Compara a produção e a demanda de urânio ao longo do tempo.
- **Estoque por Ano**: Exibe o estoque disponível em cada ano, destacando o saldo do ano.
- **Estoque Acumulado por Ano**: Representa o estoque acumulado ao longo dos anos.
- **Anos Restantes de Estoque**: Indica o número de anos que o estoque pode durar sem considerar produção adicional.
- **Anos Restantes de Estoque (Com Produção)**: Indica o número de anos restantes considerando a produção contínua.

Use os filtros para ajustar o intervalo de anos e as variáveis mostradas nos gráficos.
""")
