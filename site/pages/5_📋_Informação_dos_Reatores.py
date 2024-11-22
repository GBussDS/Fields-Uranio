import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import altair as alt
from urllib.error import URLError
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Informações dos Reatores",
    page_icon="📋",
)

conn = st.connection("gsheets", type=GSheetsConnection)

@st.cache_data
def get_info_data():
    df = conn.read(
        worksheet="Reatores Info",
        ttl="10m",
        usecols=[0,1,2,3,4,5,6,7,8,9,10],
        ) 
    
    df['Country'] = df['Country'].astype(str)
    df['Status'] = df['Status'].astype(str)

    return df

st.write("# Informações dos Reatores")

st.write(
    """
    Nessa página você poderá ver oinformações específicas sobre cada reator, 
    além de análises sobre modelos/tipos de reatores."""
)

try:
    #Filtrando os dados por país:
    df = get_info_data()

    data = df.groupby(['Country', 'Status']).size().reset_index(name='Count')
    data = data.pivot(index='Country', columns='Status', values='Count').fillna(0)

    operational_counts = df[df['Status'] == 'Operational'].groupby('Country').size()
    sorted_countries = operational_counts.sort_values(ascending=False).index

    data = data.loc[sorted_countries]

    #Gráfico
    st.write("### Número de reatores por país:")

    fig, ax = plt.subplots(figsize=(12, 6))
    data.plot(kind='bar', stacked=True, ax=ax)
    ax.set_title("Número de Reatores por Status e País")
    ax.set_xlabel("País")
    ax.set_ylabel("Contagem")
    plt.xticks(rotation=45, ha='right', fontsize=8)
    st.pyplot(fig)

    #Dados
    st.write("### Dados usados:", data)

except URLError as e:
    st.error(
        """
        **Erro ao conectar aos dados online.**
        Connection error: %s
    """
        % e.reason
    )
    