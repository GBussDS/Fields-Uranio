import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import altair as alt
from urllib.error import URLError
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Reatores por Ano",
    page_icon="☢️",
)

conn = st.connection("gsheets", type=GSheetsConnection)

@st.cache_data
def get_reactor_data():
    df = conn.read(
        worksheet="Reatores/Ano",
        ttl="10m",
        usecols=[0,1,2,3,4,5,6,7,8,9,10],
        ) 
    return df

#Body
st.write("# Reatores por Ano")

st.write(
    """
    Nessa página você poderá ver os dados de reatores ao longo do tempo, desde produção de energia por páis até a quantidade
    de reatores ativos por ano no mundo."""
)

try:
    #FIltrando os dados por ano:
    df = get_reactor_data()
    years = st.slider(
        "Escolha os anos", df['Year'].min(), df['Year'].max(), (df['Year'].min(),df['Year'].max())
    )

    data = df[(df['Year'] >= years[0]) & (df['Year'] <= years[1])]

    #Gráfico
    st.write("### Energia prodizida por ano")

    fig, ax = plt.subplots()
    sns.lineplot(data=data, x='Year', y='Electricity Supplied [GW.h]', ax=ax)
 
    st.pyplot(fig)

    #Dados
    st.write("### Dados usados:")

    st.write(data)

except URLError as e:
    st.error(
        """
        **Erro ao conectar aos dados online.**
        Connection error: %s
    """
        % e.reason
    )