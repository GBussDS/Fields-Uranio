import streamlit as st
import pandas as pd

st.write("Isso é apenas testes")
x = st.text_input("Escolhe algum dado aqui: ")
st.write(f"O dado escolhido foi {x}")

df = pd.read_csv('../csvs/Reatores_Ano.csv')
st.write(df)