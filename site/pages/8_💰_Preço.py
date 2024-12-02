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

# Carregar os dados
data = pd.read_csv("../csvs/Preço_Urânio.csv")

# Convertendo a coluna 'DATE' para datetime
data["DATE"] = pd.to_datetime(data["DATE"])

# Título da página
st.write("# Análise de Preço de Urânio")

# Introdução
st.markdown("""
    **Este gráfico mostra a evolução do preço do urânio ao longo do tempo**:
    A partir dos dados fornecidos, podemos observar as flutuações de preço desde o início dos anos 90 até o momento.
    O gráfico interativo permite explorar como o preço do urânio variou ao longo de diferentes meses e anos.
    Use o intervalo de datas abaixo para ajustar a visualização conforme sua necessidade.
""")

# Converter para datetime.date para compatibilidade com o slider
min_date = data["DATE"].min().date()  # Extrair apenas a data (sem hora)
max_date = data["DATE"].max().date()  # Extrair apenas a data (sem hora)

# Slider para selecionar o intervalo de datas
date_range = st.slider(
    "Selecione o intervalo de datas",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date)
)

# Filtrar os dados de acordo com o intervalo selecionado
filtered_data = data[(data["DATE"] >= pd.to_datetime(date_range[0])) & (data["DATE"] <= pd.to_datetime(date_range[1]))]

# Gráfico interativo do preço do urânio
st.write("### Evolução do Preço do Urânio")

fig = px.line(
    filtered_data,
    x="DATE",
    y="PURANUSDM",
    labels={"PURANUSDM": "Preço do Urânio (USD)", "DATE": "Data"},
    title="Preço do Urânio por Libra de Urânio)"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
    Você pode perceber que em 2007 houve um pico forte do preço de urânio, atingindo um pico de cerca de 140 dólares por
    libra de urânio, quadriplicando de preço se comparado ao ínicio do ano anterior. De forma breve, isso se deu
    em razão de que:

      - **Inundação da Mina Cigar Lake** no Canadá, afetando a maior reserva de urânio não desenvolvida do mundo.
      - Expectativas de expansão de **programas nucleares** na China e Índia, com futuros reatores podendo ser construídos.
      - **Preocupações com a segurança energética** após o pico dos preços do petróleo e com a dependência de combustíveis fósseis, muitos países buscaram fontes de energia alternativas e mais "limpas", como a energia nuclear.
      - **Crise de oferta**, com uma pressão crescente para suprir a demanda global.

    Já nos últimos anos, especialmente em 2023, estamos vendo uma crescente no preço, porém agora não tão forte (Com uma queda no fim de 2024). 
    Isso se deve:
    
      - A **transição energética global**, com muitos países adotando a energia nuclear para reduzir emissões de carbono.
      - Aumento da **demanda na China e na Índia**, que estão expandindo seus programas nucleares.
      - **Dificuldades na expansão da oferta**, com projetos de mineração demorando para ser implementados e a oferta global limitada.
      - Incertezas geopolíticas, como o **conflito na Ucrânia**, que impactam as cadeias de fornecimento.
""")


# Tabela de dados
st.write("### Tabela de Preço de Urânio Utilizada")
st.dataframe(filtered_data)

# Botão para download da tabela
csv_data = filtered_data.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Baixar dados como CSV",
    data=csv_data,
    file_name="preco_uranio.csv",
    mime="text/csv"
)
