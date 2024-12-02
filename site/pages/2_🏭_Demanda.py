import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Demanda de Urânio por País", page_icon="📉")

# Definindo a animação CSS para o efeito de slide da direita para a esquerda
st.markdown("""
    <style>
    /* Aplica o slide-in da direita para a esquerda apenas no conteúdo principal */
    div[data-testid="stMainBlockContainer"] > div {
        animation: slideInRight 0.5s ease-in-out;
    }

    @keyframes slideInRight {
        0% { transform: translateX(100%); opacity: 0; }
        100% { transform: translateX(0); opacity: 1; }
    }
    </style>
    """, unsafe_allow_html=True)

# Função para carregar os dados e calcular a demanda global
@st.cache_data
def load_and_prepare_data():
    demand_data = pd.read_csv("../csvs/Demand(WNA).csv")
    # Garantir que a coluna "Year" é tratada como numérica
    demand_data["Year"] = demand_data["Year"].astype(int)
    # Filtrar países com dados reais (demanda não-zero)
    non_zero_countries = demand_data.groupby("Country")["Uranium Required [T]"].sum()
    valid_countries = non_zero_countries[non_zero_countries > 0].index
    filtered_data = demand_data[demand_data["Country"].isin(valid_countries)]
    # Calcular demanda global por ano
    global_data = (
        filtered_data.groupby("Year")["Uranium Required [T]"]
        .sum()
        .reset_index()
        .assign(Country="Global")
    )
    # Adicionar os dados globais ao dataset original
    combined_data = pd.concat([filtered_data, global_data], ignore_index=True)
    return combined_data

# Carregar e preparar os dados
demand_data = load_and_prepare_data()

# Lista inicial de países
initial_countries = [
    "USA",
    "China",
    "Japan",
    "Korea RO (South)",
    "Russia",
    "Ukraine",
    "Canada",
    "United Kingdom",
    "Global"
]

# Configurar e criar o gráfico interativo com Plotly
st.write("# Demanda de Urânio por País ao Longo dos Anos")

st.write(
    """
    Nesta página, você pode explorar a demanda anual de urânio por país, de 2007 a 2022. A visualização abaixo 
    mostra a quantidade de urânio demandado em toneladas (tU) ao longo dos anos.
    """
)

# Seleção de países
selected_countries = st.multiselect(
    "Escolha os países para exibir:",
    options=demand_data["Country"].unique(),
    default=initial_countries
)

# Selecionar o intervalo de anos
anos = sorted(demand_data["Year"].unique())
years = st.slider("Escolha o intervalo de anos", min(anos), max(anos), (min(anos), max(anos)))

# Filtrar os dados pelos países selecionados e pelo intervalo de anos
filtered_data = demand_data[
    (demand_data["Country"].isin(selected_countries)) & 
    (demand_data["Year"].between(years[0], years[1]))
]

fig = px.line(
    filtered_data,
    x="Year",
    y="Uranium Required [T]",
    color="Country",
    labels={"Uranium Required [T]": "Demanda de Urânio (tU)", "Year": "Ano"},
    title=f"Demanda de Urânio por País ({years[0]} - {years[1]})",
    hover_name="Country"
)

# Ajustar o layout
fig.update_layout(
    xaxis_title="Ano",
    yaxis_title="Demanda de Urânio (tU)",
    legend_title="País",
    template="plotly_white",
)

# Exibir o gráfico interativo
st.plotly_chart(fig, use_container_width=True)

# Exibir dados usados
st.write("### Dados usados:")
st.dataframe(filtered_data)

# Converter o DataFrame para CSV
csv_data = filtered_data.T.to_csv(index=False).encode("utf-8")

# # Botão para download
st.download_button(
    label="📥 Baixar tabela como CSV",
    data=csv_data,
    file_name="dados_uranio.csv",
    mime="text/csv",
)
