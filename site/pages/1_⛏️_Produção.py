import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Carregar os dados do CSV
@st.cache_data
def get_uranium_data():
    file_path = "../csvs/Produção/UraniumProductionHistorical.csv"  # caminho relativo ao script do Streamlit
    df = pd.read_csv(file_path, index_col="Country")
    return df

# Configuração da página
st.set_page_config(page_title="Produção e Exportação de Urânio", page_icon="⛏️")

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

# Adicionar a opção "Todos"
all_option = "Todos"
country_options = [all_option] + filtered_df.index.tolist()

# Seleção de países
selected_countries = st.multiselect(
    "Escolha os países para exibir:",
    options=country_options,
    default=[all_option]  # "Todos" selecionado por padrão
)

# Se "Todos" for selecionado, inclui todos os países
if all_option in selected_countries:
    selected_countries = filtered_df.index.tolist()

# Filtrar dados pelos países selecionados
filtered_df = filtered_df.loc[selected_countries]

# Mostrar produção total de urânio
st.write(f"### Produção Total de Urânio de {years[0]} a {years[1]} por Países Selecionados")

# Calcular a produção total para o intervalo selecionado
total_production = filtered_df.drop("Global", axis=0, errors='ignore').sum(axis=1)

# Criar o mapa 3D com Plotly
st.write("### Mapa 3D de Produção de Urânio por País")

# Dados geográficos (usaremos Plotly para mapear os países)
fig = go.Figure(go.Choropleth(
    locations=filtered_df.index,
    z=total_production,  # Produção total de urânio
    hoverinfo="location+z",  # Exibe o nome do país e a produção
    locationmode="country names",  # Usa os nomes dos países
    colorscale="Viridis",  # Escolhe uma paleta de cores
    colorbar_title="Produção (tU)"
))

# Layout do gráfico 3D
fig.update_layout(
    geo=dict(
        showcoastlines=True,
        coastlinecolor="Black",
        projection_type="orthographic",  # Estilo de projeção 3D
        projection_scale=0.8  # Ajustando o zoom inicial (aumente o valor para zoom out)
    ),
    title=f"Produção de Urânio por País (Total de {years[0]} a {years[1]})",
    template="plotly_white",
    height=700,  # Ajuste o tamanho vertical do gráfico
    width=1000,  # Ajuste o tamanho horizontal do gráfico
)

# Exibir o gráfico de mapa 3D
st.plotly_chart(fig, use_container_width=True)

# Criar o gráfico interativo com Plotly para produção anual
st.write("### Produção Anual de Urânio por País (Interativo)")

# Transformar o dataframe para o formato adequado ao Plotly
filtered_df_reset = filtered_df.reset_index()
melted_df = filtered_df_reset.melt(id_vars="Country", var_name="Ano", value_name="Produção (tU)")

# Criar o gráfico com Plotly
line_fig = px.line(
    melted_df,
    x="Ano",
    y="Produção (tU)",
    color="Country",
    labels={"Produção (tU)": "Produção de Urânio (tU)", "Ano": "Ano"},
    title=f"Produção de Urânio por País ({years[0]} - {years[1]})",
    hover_name="Country",
)

# Ajustar o layout do gráfico de linha
line_fig.update_layout(
    xaxis_title="Ano",
    yaxis_title="Produção de Urânio (tU)",
    legend_title="País",
    template="plotly_white",
)

# Exibir o gráfico interativo
st.plotly_chart(line_fig, use_container_width=True)

# Exibir dados usados
st.write("### Dados usados:")
st.dataframe(filtered_df.T)  # Transposto para facilitar visualização por ano

# Converter o DataFrame para CSV
csv_data = filtered_df.T.to_csv(index=False).encode("utf-8")

# Botão para download
st.download_button(
    label="📥 Baixar tabela como CSV",
    data=csv_data,
    file_name="dados_uranio.csv",
    mime="text/csv",
)
