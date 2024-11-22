import pandas as pd
import streamlit as st
import plotly.express as px

# Carregar os dados do CSV
@st.cache_data
def get_uranium_data():
    file_path = "../csvs/Produção/UraniumProductionHistorical.csv"  # caminho relativo ao script do Streamlit
    df = pd.read_csv(file_path, index_col="Country")
    return df

# Corpo da página
st.write("# Produção de Urânio por Ano")

st.write(
    """
    Nesta página, você pode explorar a produção anual de urânio por país, de 1998 a 2022. A visualização abaixo 
    mostra a quantidade de urânio produzido em toneladas (tU) ao longo dos anos.
    """
)

# Obter os dados
df = get_uranium_data()

# Selecionar o intervalo de anos
anos = list(map(int, df.columns))
years = st.slider("Escolha o intervalo de anos", min(anos), max(anos), (min(anos), max(anos)))

# Filtrar dados por ano selecionado
filtered_df = df.loc[:, str(years[0]):str(years[1])]

# Lista inicial de países
initial_countries = [
    "Kazakhstan",
    "Canada",
    "Australia",
    "Mongolia",
    "Russia",
    "Romania",
    "Netherlands",
    "China continental",
    "Global"
]

# Seleção de países
selected_countries = st.multiselect(
    "Escolha os países para exibir:",
    options=filtered_df.index.tolist(),
    default=initial_countries
)

# Filtrar dados pelos países selecionados
filtered_df = filtered_df.loc[selected_countries]

# Configurar e criar o gráfico interativo com Plotly
st.write("### Produção Anual de Urânio por País (Interativo)")

# Transformar o dataframe para o formato adequado ao Plotly
filtered_df_reset = filtered_df.reset_index()
melted_df = filtered_df_reset.melt(id_vars="Country", var_name="Ano", value_name="Produção (tU)")

# Criar o gráfico com Plotly
fig = px.line(
    melted_df,
    x="Ano",
    y="Produção (tU)",
    color="Country",
    labels={"Produção (tU)": "Produção de Urânio (tU)", "Ano": "Ano"},
    title=f"Produção de Urânio por País ({years[0]} - {years[1]})",
    hover_name="Country",
)

# Ajustar o layout
fig.update_layout(
    xaxis_title="Ano",
    yaxis_title="Produção de Urânio (tU)",
    legend_title="País",
    template="plotly_white",
)

# Exibir o gráfico interativo
st.plotly_chart(fig, use_container_width=True)

# Exibir dados usados
st.write("### Dados usados:")
st.dataframe(filtered_df.T)  # Transposto para facilitar visualização por ano

# Converter o DataFrame para CSV
csv_data = filtered_df.T.to_csv(index=False).encode("utf-8")

# # Botão para download
st.download_button(
    label="📥 Baixar tabela como CSV",
    data=csv_data,
    file_name="dados_uranio.csv",
    mime="text/csv",
)