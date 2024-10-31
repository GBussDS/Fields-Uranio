import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
)

st.write("# Bem-vindo ao nosso site! 👋")

st.markdown(
    """
    Nosso objetivo é separar dados e mostrar visualizações e análises
    sobre o urânio.

    **👈 Selecione uma página na aba ao lado** para ver o tópico que escolher!
    ### Também veja:
    - Nosso [github](https://github.com);
    - Os dados no [kaggle](https://kaggle.com);
    - Faça perguntas no nosso [email](mailto:fields.uranio@gmail.com).
"""
)