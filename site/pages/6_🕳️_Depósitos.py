import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# Configuração da página
st.set_page_config(page_title="Mapa de Urânio", page_icon="🌍")

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
    data = pd.read_csv("../csvs/Depósitos(RAR-Infered)/Minas.csv")
    
    # Carregar o shapefile
    path_to_shapefile = "geopandas/ne_110m_admin_0_countries.shp"
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
st.title("Distribuição Global de Urânio")
st.write(
    "Explore a distribuição de recursos de urânio no mundo. Use os filtros abaixo para ajustar a visualização dos dados."
)


st.write("### Disponibilidade e Probabilidade")
st.markdown(
    """
    No contexto de depósitos de urânio, existem diferentes categorias para classificar os recursos com base no grau de certeza sobre sua presença. Duas dessas categorias são:

    - **RAR (Recursos de Áreas Conhecidas)**: São os recursos de urânio que foram bem identificados e mapeados através de estudos detalhados, como perfurações e análises. Esses recursos têm maior confiança de que realmente existem no subsolo.

    - **Inferred (Recursos Inferidos)**: São estimativas sobre a quantidade de urânio que pode estar presente, mas com menor certeza. Esses recursos são baseados em dados indiretos ou limitados, como análises de superfície, e ainda não foram confirmados por estudos mais profundos.

    Em resumo:
    - **Identified**: É a soma dos dois, nesse caso.
    - **RAR**: Maior certeza e confiabilidade.
    - **Inferred**: Estimativas com maior incerteza.
    """
)

st.markdown(
    """
    Além disso, podemos dividir pela disponibilidade dele, se é "In Situ" ou "Recoverable":
    
    - **In Situ**: Refere-se à quantidade de urânio que está presente no subsolo, mas ainda não foi extraída ou que não pode ser extraída com as tecnologias atuais. É o urânio "no local", ou seja, está no solo, mas ainda não foi processado ou recuperado.

    - **Recoverable**: Refere-se à quantidade de urânio que pode ser extraída de forma economicamente viável, ou seja, o urânio que, com as tecnologias atuais, pode ser recuperado e trazido à superfície para ser utilizado.
    
    Em resumo:
    - **In Situ**: Urânio localizado no subsolo, não extraído muitas vezes devido a limitações tecnológicas ou econômicas.
    - **Recoverable**: Urânio que pode ser extraído de forma viável e econômica com as tecnologias e métodos de mineração disponíveis.
    """
)

# Filtros
st.write("### Filtros para Seleção de Depósitos")
col1, col2, col3 = st.columns(3)

with col1:
    disponibilidade = st.selectbox("Disponibilidade", data["Disponibilidade"].unique())

with col2:
    probabilidade = st.selectbox("Probabilidade", ["Ambos"] + list(data["Probabilidade"].unique()))

with col3:
    Preço = st.selectbox("Preço", data["Preço"].unique())

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
st.write("### Mapa Interativo de Depósitos de Urânio")
st_folium(m, width=700, height=500)

st.write(
    "A combinação de filtros permite explorar diferentes categorias de depósitos de urânio, considerando sua viabilidade, "
    "localização e características econômicas e geológicas."
)

# Tabela e botão de download
st.write("### Tabela de Dados Utilizados")
st.dataframe(data)

# Converter o DataFrame para CSV
csv_data = data.to_csv(index=False).encode("utf-8")

# # Botão para download
st.download_button(
    label="📥 Baixar tabela como CSV",
    data=csv_data,
    file_name="dados_uranio.csv",
    mime="text/csv",
)

# Filtro de país
st.write("### Selecione um País para Detalhes")
country_selected = st.selectbox("Escolha um país", data["Country"].unique())

# Filtrar os dados para o país selecionado
country_data = data[data["Country"] == country_selected]

st.write(f"### Dados sobre: {country_selected}")

# Tabela de Informações
st.markdown("""
    <style>
        .table {
            width: 100%;
            border-collapse: collapse;
        }
        .table th, .table td {
            padding: 8px 12px;
            border: 1px solid #ddd;
            text-align: center;
            font-size: 20px;
        }
        .table th {
            background-color: #902020;
            font-weight: bold;
        }
        .table td {
            background-color: #1d334a;
        }
        .table .highlight {
            font-size: 24px;
            font-weight: bold;
            background-color: #1d334a;
        }
    </style>
""", unsafe_allow_html=True)

# Gerar a tabela de dados organizados em linhas
table_data = [
    ["Total de Urânio", f"{int(country_data['Urânio (Ton.)'].sum())} Ton."],
    ["Urânio RAR", f"{int(country_data[country_data['Probabilidade'] == 'RAR']['Urânio (Ton.)'].sum())} Ton."],
    ["Urânio Inferred", f"{int(country_data[country_data['Probabilidade'] == 'Inferred']['Urânio (Ton.)'].sum())} Ton."],
    ["Urânio In Situ", f"{int(country_data[country_data['Disponibilidade'] == 'in Situ']['Urânio (Ton.)'].sum())} Ton."],
    ["Urânio Recoverable", f"{int(country_data[country_data['Disponibilidade'] == 'Recoverable']['Urânio (Ton.)'].sum())} Ton."]
]

# Criação da tabela de preço
price_ranges = {
    "< USD 40/kgU": f"{int(country_data[country_data['Preço'] == '<USD 40/kgU']['Urânio (Ton.)'].sum())} Ton.",
    "< USD 80/kgU": f"{int(country_data[country_data['Preço'] == '<USD 80/kgU']['Urânio (Ton.)'].sum())} Ton.",
    "< USD 130/kgU": f"{int(country_data[country_data['Preço'] == '<USD 130/kgU']['Urânio (Ton.)'].sum())} Ton.",
    "< USD 260/kgU": f"{int(country_data[country_data['Preço'] == '<USD 260/kgU']['Urânio (Ton.)'].sum())} Ton."
}

# Adicionando as faixas de preço na tabela
for price_range, value in price_ranges.items():
    table_data.append([price_range, value])

# Renderizando a tabela com os dados
table_html = "<table class='table'>"
table_html += "<tr><th>Categoria</th><th>Quantidade de Urânio</th></tr>"

for row in table_data:
    table_html += f"<tr><td>{row[0]}</td><td class='highlight'>{row[1]}</td></tr>"

table_html += "</table>"

st.markdown(table_html, unsafe_allow_html=True)
