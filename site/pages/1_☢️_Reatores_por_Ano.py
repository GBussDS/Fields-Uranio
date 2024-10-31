import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(
    page_title="Reatores por Ano",
    page_icon="☢️",
)

# Initialize connection to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Read data from Google Sheets
df = conn.read(
    worksheet="Reatores/Ano",
    ttl="10m",
    usecols=[0,1,2,3,4,5,6,7,8,9,10],
)

st.write("# Reatores por Ano")

st.write(
    """
    Nessa página você poderá ver os dados de reatores ao longo do tempo, desde produção de energia por páis até a quantidade
    de reatores ativos por ano no mundo."""
)

st.write(df)