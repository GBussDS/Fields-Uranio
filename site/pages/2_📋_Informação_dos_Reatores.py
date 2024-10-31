import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(
    page_title="Informações dos Reatores",
    page_icon="📋",
)

# Initialize connection to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Read data from Google Sheets
df = conn.read(
    worksheet="Reatores Info",
    ttl="10m",
    usecols=[0,1,2,3,4,5,6,7,8,9,10],
)

st.write("# Informações dos Reatores")

st.write(
    """
    Nessa página você poderá ver oinformações específicas sobre cada reator, 
    além de análises sobre modelos/tipos de reatores."""
)

st.write(df)