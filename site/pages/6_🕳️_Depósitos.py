import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# Configuração da página
st.set_page_config(page_title="Mapa de Urânio", page_icon="🌍")

# Idiomas disponíveis
idiomas = {"Português": "pt", "English": "en"}
idioma_selecionado = st.sidebar.selectbox("🌐 Escolha o idioma / Select Language:", idiomas.keys())
lang = idiomas[idioma_selecionado]

# Textos em múltiplos idiomas
texts = {
    "pt": {
        "title": "Distribuição Global de Urânio",
        "subtitle": "Explore a distribuição de recursos de urânio no mundo. Use os filtros abaixo para ajustar a visualização dos dados.",
        "availability": "Disponibilidade",
        "probability": "Probabilidade",
        "price": "Preço",
        "filters": "### Filtros para Seleção de Depósitos",
        "map": "### Mapa Interativo de Depósitos de Urânio",
        "table_title": "### Tabela de Dados Utilizados",
        "download_button": "📥 Baixar tabela como CSV",
        "country_filter": "### Selecione um País para Detalhes",
        "country_details": "### Dados sobre:",
        "data_table": "Tabela de Informações",
        "total_uranium": "Total de Urânio",
        "uranium_rar": "Urânio RAR",
        "uranium_inferred": "Urânio Inferred",
        "uranium_in_situ": "Urânio In Situ",
        "uranium_recoverable": "Urânio Recoverable",
    },
    "en": {
        "title": "Global Uranium Distribution",
        "subtitle": "Explore the global distribution of uranium resources. Use the filters below to adjust the data visualization.",
        "availability": "Availability",
        "probability": "Probability",
        "price": "Price",
        "filters": "### Filters for Deposit Selection",
        "map": "### Interactive Map of Uranium Deposits",
        "table_title": "### Data Table Used",
        "download_button": "📥 Download table as CSV",
        "country_filter": "### Select a Country for Details",
        "country_details": "### Data about:",
        "data_table": "Information Table",
        "total_uranium": "Total Uranium",
        "uranium_rar": "RAR Uranium",
        "uranium_inferred": "Inferred Uranium",
        "uranium_in_situ": "In Situ Uranium",
        "uranium_recoverable": "Recoverable Uranium",
    },
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

# Função para carregar os dados e aplicar o cache
@st.cache_data
def load_data():
    # Carregar dados
    data = pd.read_csv("csvs/Depósitos(RAR-Infered)/Minas.csv")
    
    # Carregar o shapefile
    path_to_shapefile = "site/geopandas/ne_110m_admin_0_countries.shp"
    world = gpd.read_file(path_to_shapefile)
    
    # Dicionário de correspondência para ajustar nomes de países
    country_name_map = {
        "United States": "United States of America",
        "Viet Nam": "Vietnam",
        "Slovak Republic": "Slovakia",
        "Congo Dem Rep of": "Democratic Republic of the Congo",
        "Iran Islamic Rep of": "Iran",
        "Russia": "Russian Federation",
        "South Korea": "Republic of Korea",
        "North Korea": "Dem. Rep. Korea",
        "United Kingdom": "United Kingdom",
        "Egypt": "Egypt, Arab Rep.",
        "Czech Republic": "Czechia",
        "Central African Republic": "Central African Rep.",
        "Denmark/Greenland": "Greenland",
        "Tanzania": "Tanzania, United Rep.",
    }
    
    # Aplicar a correção de nomes ao conjunto de dados
    data["Country"] = data["Country"].replace(country_name_map)
    
    return data, world

# Carregar dados com cache
data, world = load_data()

# Título da página
st.title(texts[lang]["title"])
st.write(texts[lang]["subtitle"])

# Explicação sobre disponibilidade e probabilidade
explicacao_textos = {
    "pt": """
### Disponibilidade e Probabilidade
No contexto de depósitos de urânio, existem diferentes categorias para classificar os recursos com base no grau de certeza sobre sua presença. Duas dessas categorias são:

- **RAR (Recursos de Áreas Conhecidas)**: São os recursos de urânio que foram bem identificados e mapeados através de estudos detalhados, como perfurações e análises. Esses recursos têm maior confiança de que realmente existem no subsolo.
  
- **Inferred (Recursos Inferidos)**: São estimativas sobre a quantidade de urânio que pode estar presente, mas com menor certeza. Esses recursos são baseados em dados indiretos ou limitados, como análises de superfície, e ainda não foram confirmados por estudos mais profundos.

**Em resumo**:
- **Identified**: É a soma dos dois, nesse caso.
- **RAR**: Maior certeza e confiabilidade.
- **Inferred**: Estimativas com maior incerteza.

Além disso, podemos dividir pela disponibilidade dele, se é "In Situ" ou "Recoverable":

- **In Situ**: Refere-se à quantidade de urânio que está presente no subsolo, mas ainda não foi extraída ou que não pode ser extraída com as tecnologias atuais. É o urânio "no local", ou seja, está no solo, mas ainda não foi processado ou recuperado.
  
- **Recoverable**: Refere-se à quantidade de urânio que pode ser extraída de forma economicamente viável, ou seja, o urânio que, com as tecnologias atuais, pode ser recuperado e trazido à superfície para ser utilizado.

**Em resumo**:
- **In Situ**: Urânio localizado no subsolo, não extraído muitas vezes devido a limitações tecnológicas ou econômicas.
- **Recoverable**: Urânio que pode ser extraído de forma viável e econômica com as tecnologias e métodos de mineração disponíveis.
    """,
    "en": """
### Availability and Probability
In the context of uranium deposits, different categories classify resources based on the degree of certainty about their presence. Two of these categories are:

- **RAR (Reasonably Assured Resources)**: Uranium resources that have been well-identified and mapped through detailed studies, such as drilling and analysis. These resources have a high degree of confidence that they exist underground.
  
- **Inferred Resources**: Estimates of the amount of uranium that may be present, but with less certainty. These resources are based on indirect or limited data, such as surface analysis, and have not yet been confirmed by more in-depth studies.

**In summary**:
- **Identified**: A combined total of both categories.
- **RAR**: Greater certainty and reliability.
- **Inferred**: Estimates with higher uncertainty.

Additionally, availability can be divided into two categories: "In Situ" or "Recoverable":

- **In Situ**: Refers to the amount of uranium present underground but not yet extracted or not recoverable with current technologies. It represents uranium "on-site," still in the ground and unprocessed.
  
- **Recoverable**: Refers to the amount of uranium that can be economically extracted, meaning uranium that can be recovered and brought to the surface with current technologies and mining methods.

**In summary**:
- **In Situ**: Uranium located underground, often unextracted due to technological or economic limitations.
- **Recoverable**: Uranium that can be viably and economically extracted with available technologies and mining methods.
    """
}

# Exibir a explicação no idioma selecionado
st.markdown(explicacao_textos[lang])

# Filtros
st.write(texts[lang]["filters"])
col1, col2, col3 = st.columns(3)

with col1:
    disponibilidade = st.selectbox(texts[lang]["availability"], data["Disponibilidade"].unique())

with col2:
    probabilidade = st.selectbox(texts[lang]["probability"], ["Ambos"] + list(data["Probabilidade"].unique()))

with col3:
    Preço = st.selectbox(texts[lang]["price"], data["Preço"].unique())

# Aplicar filtros
filtered_data = data[
    (data["Disponibilidade"] == disponibilidade)
    & ((data["Probabilidade"] == probabilidade) | (probabilidade == "Ambos"))
    & (data["Preço"] == Preço)
]

# Caso "Ambos" seja selecionado, somar os valores de RAR e Inferred
if probabilidade == "Ambos":
    rar_data = data[
        (data["Disponibilidade"] == disponibilidade)
        & (data["Probabilidade"] == "RAR")
        & (data["Preço"] == Preço)
    ]
    inferred_data = data[
        (data["Disponibilidade"] == disponibilidade)
        & (data["Probabilidade"] == "Inferred")
        & (data["Preço"] == Preço)
    ]
    filtered_data = pd.concat([rar_data, inferred_data]).groupby("Country")["Urânio (Ton.)"].sum().reset_index()
else:
    filtered_data = filtered_data.groupby("Country")["Urânio (Ton.)"].sum().reset_index()

# Merge com o shapefile para o mapa
world = world.merge(filtered_data, left_on="ADMIN", right_on="Country", how="left")
world["Urânio (Ton.)"] = world["Urânio (Ton.)"].fillna(0)  # Substituir NaN por 0 para países sem dados

# Criar mapa interativo com Folium
m = folium.Map(location=[20, 0], zoom_start=2, tiles="cartodb positron")

# Adicionar camada de calor para visualização dos dados
for _, row in world.iterrows():
    if row["Urânio (Ton.)"] > 0:
        folium.CircleMarker(
            location=[row.geometry.centroid.y, row.geometry.centroid.x],
            radius=2 + (row["Urânio (Ton.)"] ** 0.5) / 40,
            color="red",
            fill=True,
            fill_color="red",
            fill_opacity=0.6,
            popup=f"{row['ADMIN']}: {row['Urânio (Ton.)']} toneladas de Urânio",
        ).add_to(m)

# Exibir o mapa interativo
st.write(texts[lang]["map"])
st_folium(m, width=700, height=500)

# Exibir tabela
st.write(texts[lang]["table_title"])
st.dataframe(data)

# Converter o DataFrame para CSV
csv_data = data.to_csv(index=False).encode("utf-8")

# Botão para download
st.download_button(
    label=texts[lang]["download_button"],
    data=csv_data,
    file_name="dados_uranio.csv",
    mime="text/csv",
)

# Filtro de país
st.write(texts[lang]["country_filter"])
country_selected = st.selectbox("Escolha um país / Select a country", data["Country"].unique())

# Filtrar os dados para o país selecionado
country_data = data[data["Country"] == country_selected]

st.write(f"{texts[lang]['country_details']} {country_selected}")

# Gerar tabela de dados para o país selecionado
table_data = [
    [texts[lang]["total_uranium"], f"{int(country_data['Urânio (Ton.)'].sum())} Ton."],
    [texts[lang]["uranium_rar"], f"{int(country_data[country_data['Probabilidade'] == 'RAR']['Urânio (Ton.)'].sum())} Ton."],
    [texts[lang]["uranium_inferred"], f"{int(country_data[country_data['Probabilidade'] == 'Inferred']['Urânio (Ton.)'].sum())} Ton."],
    [texts[lang]["uranium_in_situ"], f"{int(country_data[country_data['Disponibilidade'] == 'in Situ']['Urânio (Ton.)'].sum())} Ton."],
    [texts[lang]["uranium_recoverable"], f"{int(country_data[country_data['Disponibilidade'] == 'Recoverable']['Urânio (Ton.)'].sum())} Ton."],
]

country_table = pd.DataFrame(table_data, columns=["Informação", "Valor"])
st.table(country_table)
