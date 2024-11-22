import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import folium_static

# Configuração da página
st.set_page_config(page_title="Mapa de Urânio", page_icon="🌍")

# Carregar dados
data = pd.read_csv("../csvs/Depósitos(RAR-Infered)/Minas.csv")

# Carregar dados geográficos de países
world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

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

# Título da página
st.title("Distribuição Global de Urânio")
st.write(
    "Explore a distribuição de recursos de urânio no mundo. Use os filtros abaixo para ajustar a visualização dos dados."
)

# Filtros
st.write("### Filtros para Seleção de Depósitos")
col1, col2, col3 = st.columns(3)

with col1:
    disponibilidade = st.selectbox("Disponibilidade", data["Disponibilidade"].unique())

with col2:
    probabilidade = st.selectbox("Probabilidade", ["Ambos"] + list(data["Probabilidade"].unique()))

with col3:
    atributo = st.selectbox("Atributo", data["Atributo"].unique())

# Aplicar filtros
filtered_data = data[
    (data["Disponibilidade"] == disponibilidade)
    & ((data["Probabilidade"] == probabilidade) | (probabilidade == "Ambos"))
    & (data["Atributo"] == atributo)
]

# Caso "Ambos" seja selecionado, somar os valores de RAR e Inferred
if probabilidade == "Ambos":
    rar_data = data[
        (data["Disponibilidade"] == disponibilidade)
        & (data["Probabilidade"] == "RAR")
        & (data["Atributo"] == atributo)
    ]
    inferred_data = data[
        (data["Disponibilidade"] == disponibilidade)
        & (data["Probabilidade"] == "Inferred")
        & (data["Atributo"] == atributo)
    ]
    filtered_data = pd.concat([rar_data, inferred_data]).groupby("Country")["Urânio (Ton.)"].sum().reset_index()
else:
    filtered_data = filtered_data.groupby("Country")["Urânio (Ton.)"].sum().reset_index()

# Merge com o shapefile para o mapa
world = world.merge(filtered_data, left_on="name", right_on="Country", how="left")
world["Urânio (Ton.)"].fillna(0, inplace=True)  # Substituir NaN por 0 para países sem dados

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
            popup=f"{row['name']}: {row['Urânio (Ton.)']} toneladas de Urânio",
        ).add_to(m)

# Exibir o mapa interativo
st.write("### Mapa Interativo de Depósitos de Urânio")
folium_static(m)

# Explicação sobre os tipos de recurso
st.write("### Tipos de Recursos de Urânio: Explicação Detalhada")
st.markdown(
    """
    - **RAR (Reasonably Assured Recoverable Resources)**:
      Recursos extensivamente explorados, economicamente viáveis para extração e com alta confiança.
      
    - **Inferred Recoverable Resources**:
      Estimativas baseadas em dados limitados, geralmente com menor precisão, mas indicativas de potencial extração.
    
    - **Recursos Recuperáveis Identificados**:
      Recursos conhecidos que já foram avaliados como economicamente extraíveis.

    - **Recursos in situ Identificados**:
      Urânio identificado que permanece no local e ainda não foi extraído.

    - **Recursos Recuperáveis Inferidos**:
      Recursos estimados em depósitos com dados insuficientes para alta precisão, mas economicamente viáveis.

    - **Recursos in situ Inferidos**:
      Recursos de urânio estimados que permanecem no local, mas com dados limitados para confirmar sua viabilidade econômica.
    """
)

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