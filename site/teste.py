import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Initialize connection to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Read data from Google Sheets
df = conn.read(
    worksheet="Reatores/Ano",
    ttl="10m",
    usecols=[0,1,2,3,4,5,6,7,8,9,10],
    nrows=15,
)

st.write(df)
