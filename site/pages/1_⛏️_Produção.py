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

# Idiomas disponíveis
idiomas = {"Português": "pt", "English": "en"}
idioma_selecionado = st.sidebar.selectbox("🌐 Escolha o idioma / Select Language:", idiomas.keys())
lang = idiomas[idioma_selecionado]

# Textos em diferentes idiomas
textos = {
    "pt": {
        "titulo": "Produção de Urânio por Ano",
        "descricao": "Nesta página, você pode explorar a produção anual de urânio por país, de 1998 a 2022. A visualização abaixo mostra a quantidade de urânio produzido em toneladas (tU) ao longo dos anos.",
        "slider": "Escolha o intervalo de anos",
        "pais": "Escolha os países para exibir:",
        "producao_total": "Produção Total de Urânio de {0} a {1} por Países Selecionados",
        "mapa": "Mapa 3D de Produção de Urânio por País",
        "producao_anual": "Produção Anual de Urânio por País (Interativo)",
        "dados": "Dados usados:",
        "download": "📥 Baixar tabela como CSV",
    },
    "en": {
        "titulo": "Uranium Production by Year",
        "descricao": "On this page, you can explore the annual uranium production by country from 1998 to 2022. The visualization below shows the amount of uranium produced in tons (tU) over the years.",
        "slider": "Select year range",
        "pais": "Choose countries to display:",
        "producao_total": "Total Uranium Production from {0} to {1} by Selected Countries",
        "mapa": "3D Map of Uranium Production by Country",
        "producao_anual": "Annual Uranium Production by Country (Interactive)",
        "dados": "Data used:",
        "download": "📥 Download table as CSV",
    }
}

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
st.write(f"# {textos[lang]['titulo']}")
st.write(textos[lang]['descricao'])

# Obter os dados
df = get_uranium_data()

# Selecionar o intervalo de anos
anos = list(map(int, df.columns))
years = st.slider(textos[lang]['slider'], min(anos), max(anos), (min(anos), max(anos)))

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
all_option = "Todos" if lang == "pt" else "All"
country_options = [all_option] + filtered_df.index.tolist()

# Seleção de países
selected_countries = st.multiselect(
    textos[lang]['pais'],
    options=country_options,
    default=[all_option]  # "Todos/All" selecionado por padrão
)

# Se "Todos/All" for selecionado, inclui todos os países
if all_option in selected_countries:
    selected_countries = filtered_df.index.tolist()

# Filtrar dados pelos países selecionados
filtered_df = filtered_df.loc[selected_countries]

# Mostrar produção total de urânio
st.write(f"### {textos[lang]['producao_total'].format(years[0], years[1])}")

# Calcular a produção total para o intervalo selecionado
total_production = filtered_df.drop("Global", axis=0, errors='ignore').sum(axis=1)

# Criar o mapa 3D com Plotly
st.write(f"### {textos[lang]['mapa']}")

# Dados geográficos (usaremos Plotly para mapear os países)
fig = go.Figure(go.Choropleth(
    locations=filtered_df.index,
    z=total_production,  # Produção total de urânio
    hoverinfo="location+z",  # Exibe o nome do país e a produção
    locationmode="country names",  # Usa os nomes dos países
    colorscale="Viridis",  # Escolhe uma paleta de cores
    colorbar_title="Produção (tU)" if lang == "pt" else "Production (tU)"
))

# Layout do gráfico 3D
fig.update_layout(
    geo=dict(
        showcoastlines=True,
        coastlinecolor="Black",
        projection_type="orthographic",  # Estilo de projeção 3D
        projection_scale=0.8  # Ajustando o zoom inicial (aumente o valor para zoom out)
    ),
    title=f"{textos[lang]['mapa']} ({years[0]} - {years[1]})",
    template="plotly_white",
    height=700,  # Ajuste o tamanho vertical do gráfico
    width=1000,  # Ajuste o tamanho horizontal do gráfico
)

# Exibir o gráfico de mapa 3D
st.plotly_chart(fig, use_container_width=True)

# Criar o gráfico interativo com Plotly para produção anual
st.write(f"### {textos[lang]['producao_anual']}")

# Transformar o dataframe para o formato adequado ao Plotly
filtered_df_reset = filtered_df.reset_index()
melted_df = filtered_df_reset.melt(id_vars="Country", var_name="Ano", value_name="Produção (tU)")

# Criar o gráfico com Plotly
line_fig = px.line(
    melted_df,
    x="Ano",
    y="Produção (tU)",
    color="Country",
    labels={"Produção (tU)": "Produção de Urânio (tU)" if lang == "pt" else "Uranium Production (tU)", "Ano": "Ano" if lang == "pt" else "Year"},
    title=f"{textos[lang]['producao_anual']} ({years[0]} - {years[1]})",
    hover_name="Country",
)

# Ajustar o layout do gráfico de linha
line_fig.update_layout(
    xaxis_title="Ano" if lang == "pt" else "Year",
    yaxis_title="Produção de Urânio (tU)" if lang == "pt" else "Uranium Production (tU)",
    legend_title="País" if lang == "pt" else "Country",
    template="plotly_white",
)

# Exibir o gráfico interativo
st.plotly_chart(line_fig, use_container_width=True)

# Exibir dados usados
st.write(f"### {textos[lang]['dados']}")
st.dataframe(filtered_df.T)  # Transposto para facilitar visualização por ano

# Converter o DataFrame para CSV
csv_data = filtered_df.T.to_csv(index=False).encode("utf-8")

# Botão para download
st.download_button(
    label=textos[lang]['download'],
    data=csv_data,
    file_name="dados_uranio.csv" if lang == "pt" else "uranium_data.csv",
    mime="text/csv",
)
