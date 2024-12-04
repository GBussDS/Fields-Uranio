import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from urllib.error import URLError
import seaborn as sns
import matplotlib.pyplot as plt

# Configuração da página (deve ser o primeiro comando)
st.set_page_config(page_title="Reatores por Ano", page_icon="☢️")

# Idiomas disponíveis
idiomas = {"Português": "pt", "English": "en"}
idioma_selecionado = st.sidebar.selectbox("🌐 Escolha o idioma / Select Language:", idiomas.keys())
lang = idiomas[idioma_selecionado]

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

conn = st.connection("gsheets", type=GSheetsConnection)

@st.cache_data
def get_reactor_data():
    df = conn.read(
        worksheet="Reatores/Ano",
        ttl="10m",
        usecols=[0,1,2,3,4,5,6,7,8,9,10],
    ) 
    return df

# Tradução de títulos e mensagens
if lang == "pt":
    title = "Reatores por Ano"
    description = """
    Nessa página você poderá ver os dados de reatores ao longo do tempo, desde produção de energia por países até a quantidade
    de reatores ativos por ano no mundo.
    """
    chart_title = "Energia produzida por ano"
    data_title = "Dados usados:"
    error_message = """
        **Erro ao conectar aos dados online.**
        Erro de conexão: %s
    """
else:
    title = "Reactors by Year"
    description = """
    On this page, you can view reactor data over time, from energy production by countries to the number
    of active reactors worldwide per year.
    """
    chart_title = "Energy Produced by Year"
    data_title = "Data Used:"
    error_message = """
        **Error connecting to online data.**
        Connection error: %s
    """

# Body
st.write(f"# {title}")

st.write(description)

try:
    # Filtrando os dados por ano:
    df = get_reactor_data()
    years = st.slider(
        "Escolha os anos" if lang == "pt" else "Select years", df['Year'].min(), df['Year'].max(), (df['Year'].min(), df['Year'].max())
    )

    data = df[(df['Year'] >= years[0]) & (df['Year'] <= years[1])]

    # Gráfico
    st.write(f"### {chart_title}")

    fig, ax = plt.subplots()
    sns.lineplot(data=data, x='Year', y='Electricity Supplied [GW.h]', ax=ax)
 
    st.pyplot(fig)

    # Dados
    st.write(f"### {data_title}")

    st.write(data)

except URLError as e:
    st.error(error_message % e.reason)
