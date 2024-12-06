import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Análise de Preço de Urânio", page_icon="💰")

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

# Idiomas disponíveis
idiomas = {"Português": "pt", "English": "en"}
idioma_selecionado = st.sidebar.selectbox("🌐 Escolha o idioma / Select Language:", idiomas.keys())
lang = idiomas[idioma_selecionado]

# Carregar os dados
data = pd.read_csv("csvs/Preço_Urânio.csv")

# Convertendo a coluna 'DATE' para datetime
data["DATE"] = pd.to_datetime(data["DATE"])

# Traduções
textos = {
    "pt": {
        "titulo": "Análise de Preço de Urânio",
        "introducao": "**Este gráfico mostra a evolução do preço do urânio ao longo do tempo**: A partir dos dados fornecidos, podemos observar as flutuações de preço desde o início dos anos 90 até o momento. O gráfico interativo permite explorar como o preço do urânio variou ao longo de diferentes meses e anos. Use o intervalo de datas abaixo para ajustar a visualização conforme sua necessidade.",
        "selecione_intervalo": "Selecione o intervalo de datas",
        "grafico_titulo": "Evolução do Preço do Urânio",
        "grafico_legendas": {"PURANUSDM": "Preço do Urânio (USD)", "DATE": "Data"},
        "tabela_titulo": "Tabela de Preço de Urânio Utilizada",
        "baixar_dados": "📥 Baixar dados como CSV",
    },
    "en": {
        "titulo": "Uranium Price Analysis",
        "introducao": "**This chart shows the evolution of uranium prices over time**: From the provided data, we can observe price fluctuations from the early 1990s to the present. The interactive chart allows you to explore how uranium prices have varied across different months and years. Use the date range below to adjust the visualization as needed.",
        "selecione_intervalo": "Select the date range",
        "grafico_titulo": "Uranium Price Evolution",
        "grafico_legendas": {"PURANUSDM": "Uranium Price (USD)", "DATE": "Date"},
        "tabela_titulo": "Uranium Price Table Used",
        "baixar_dados": "📥 Download data as CSV",
    },
}

# Recuperar textos conforme o idioma
t = textos[lang]

# Título da página
st.write(f"# {t['titulo']}")

# Introdução
st.markdown(t["introducao"])

# Converter para datetime.date para compatibilidade com o slider
min_date = data["DATE"].min().date()  # Extrair apenas a data (sem hora)
max_date = data["DATE"].max().date()  # Extrair apenas a data (sem hora)

# Slider para selecionar o intervalo de datas
date_range = st.slider(
    t["selecione_intervalo"],
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date)
)

# Filtrar os dados de acordo com o intervalo selecionado
filtered_data = data[(data["DATE"] >= pd.to_datetime(date_range[0])) & (data["DATE"] <= pd.to_datetime(date_range[1]))]

# Gráfico interativo do preço do urânio
st.write(f"### {t['grafico_titulo']}")

fig = px.line(
    filtered_data,
    x="DATE",
    y="PURANUSDM",
    labels=t["grafico_legendas"],
    title=t["grafico_titulo"]
)

st.plotly_chart(fig, use_container_width=True)

# Tabela de dados
st.write(f"### {t['tabela_titulo']}")
st.dataframe(filtered_data)

# Botão para download da tabela
csv_data = filtered_data.to_csv(index=False).encode("utf-8")
st.download_button(
    label=t["baixar_dados"],
    data=csv_data,
    file_name="preco_uranio.csv",
    mime="text/csv"
)
