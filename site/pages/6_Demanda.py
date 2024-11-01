import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Demanda de Urânio por País", page_icon="📉")

# Carregar os dados
demand_data = pd.read_csv("../csvs/Demand(WNA).csv")

# Filtrar automaticamente os países com dados reais (demanda não-zero)
non_zero_countries = demand_data.groupby("Country")["Uranium Required [T]"].sum()
valid_countries = non_zero_countries[non_zero_countries > 0].index

# Sidebar para filtro de países
st.sidebar.title("Filtros")
selected_countries = st.sidebar.multiselect(
    "Selecione os países para visualizar",
    sorted(valid_countries),  # Ordenar países em ordem alfabética
    default=sorted(valid_countries)  # Default agora mostra todos os países com dados reais
)

# Filtrar dados com base na seleção do usuário
filtered_data = demand_data[demand_data["Country"].isin(selected_countries)]

# Configuração do gráfico interativo com Plotly
st.write("### Demanda de Urânio por País ao Longo dos Anos")

fig = px.line(
    filtered_data,
    x="Year",
    y="Uranium Required [T]",
    color="Country",
    title="Demanda de Urânio por País ao Longo dos Anos",
    labels={"Year": "Ano", "Uranium Required [T]": "Demanda de Urânio (Toneladas)", "Country": "País"},
    markers=True,
)

# Personalizar layout do gráfico
fig.update_layout(
    hovermode="x unified",
    xaxis=dict(title="Ano"),
    yaxis=dict(title="Demanda de Urânio (Toneladas)"),
    legend_title="País",
)

# Exibir gráfico interativo
st.plotly_chart(fig)

# Explicação adicional
st.write("""
### Explicação
- **Demanda de Urânio por País**: Este gráfico permite comparar a demanda de urânio entre os países selecionados ao longo do tempo.
- **Filtros**: Utilize a barra lateral para selecionar os países que deseja visualizar no gráfico.
""")
