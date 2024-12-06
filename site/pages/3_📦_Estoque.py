import streamlit as st
import pandas as pd
import plotly.express as px


# Configuração da página
st.set_page_config(page_title="Análise de Produção, Demanda e Estoque de Urânio", page_icon="📊")

# Idiomas disponíveis
idiomas = {"Português": "pt", "English": "en"}
idioma_selecionado = st.sidebar.selectbox("🌐 Escolha o idioma / Select Language:", idiomas.keys())
lang = idiomas[idioma_selecionado]


# Texto de acordo com o idioma selecionado
if lang == "pt":
    texto_intro = "# Análise de Produção, Demanda e Estoque de Urânio"
    texto_prod_demand = "### Produção e Demanda por Ano"
    texto_prod_demand_desc = """
    **Este gráfico mostra a evolução da produção e da demanda de urânio ao longo do tempo**:
    Você pode usar o intervalo de anos para explorar como a produção e a demanda mudaram em diferentes períodos.
    O gráfico ajuda a visualizar se a produção está acompanhando a demanda, e podemos ver que a demanda está em
    uma crescente, enquanto a produção parece estacionada.
    """
    texto_stock = "### Estoque por Ano"
    texto_stock_desc = """
    **Este gráfico ilustra a evolução do estoque (Produção - Demanda) de urânio**:
    Ao observar as variações no estoque, podemos entender como ele está sendo gerido e como pode impactar a disponibilidade futura de urânio.
    Esse gráfico nos ajuda a visualizar ainda mais como o equilíbro de balança parece estar mudando.
    """
    texto_acc_stock = "### Estoque Acumulado por Ano"
    texto_acc_stock_desc = """
    **Este gráfico exibe o estoque acumulado ao longo dos anos.**
    Ele mostra o total de urânio que foi armazenado e acumulado até cada ano. Para essa análise, só utilizamos os dados de produção
    e de demanda, fazendo uma soma acumulada do estoque que calculamos anteriormente.
    De acordo com o último Red Book, o estoque atual de urânio nos países é de aproximadamente 525 mil quilogramas, bem próximo
    de nossa estimativa.
    """
    texto_years_stock = "### Anos Restantes de Estoque"
    texto_years_stock_desc = """
    **Este gráfico mostra a previsão dos anos restantes de estoque, com base na quantidade atual de urânio disponível.**
    Ele ajuda a entender quanto tempo, para cada ano, tínhamos de estoque para abastecer a demanda total dos países 
    (não considerando produção). Podemos observar uma queda.
    """
    texto_years_stock_prod = "### Anos Restantes de Estoque (Com Produção)"
    texto_years_stock_prod_desc = """
    **Agora vemos os anos restantes de estoque considerando a demanda e produção de urânio.**
    Ao levar em conta a produção, podemos ajustar o cálculo de anos restantes de estoque, por isso números maiores.
    """
    texto_table = "### Tabela de Dados Utilizados"
    texto_download_button = "📥 Baixar tabela como CSV"
    slider_text_prod_demand = "Selecione o intervalo de anos para Produção e Demanda"
    slider_text_stock = "Selecione o intervalo de anos para Estoque"
    slider_text_acc_stock = "Selecione o intervalo de anos para Estoque Acumulado"
    slider_text_years_stock = "Selecione o intervalo de anos para Anos Restantes de Estoque"
    slider_text_years_stock_prod = "Selecione o intervalo de anos para Anos Restantes de Estoque (Com Produção)"
    choose_option = "Escolha o que deseja visualizar"
else:
    texto_intro = "# Uranium Production, Demand and Stock Analysis"
    texto_prod_demand = "### Production and Demand by Year"
    texto_prod_demand_desc = """
    **This graph shows the evolution of uranium production and demand over time**:
    You can use the year range to explore how production and demand have changed over different periods.
    The graph helps to visualize if production is keeping up with demand, and we can see that demand is increasing while production seems stalled.
    """
    texto_stock = "### Stock by Year"
    texto_stock_desc = """
    **This graph illustrates the evolution of uranium stock (Production - Demand)**:
    By observing the variations in stock, we can understand how it is being managed and how it might impact future uranium availability.
    This graph further helps to visualize how the balance seems to be changing.
    """
    texto_acc_stock = "### Accumulated Stock by Year"
    texto_acc_stock_desc = """
    **This graph displays the accumulated stock over the years.**
    It shows the total uranium that has been stored and accumulated until each year. For this analysis, we only used production and demand data,
    making a cumulative sum of the stock that we calculated earlier.
    According to the latest Red Book, the current uranium stock in countries is approximately 525,000 kilograms, which is close to our estimate.
    """
    texto_years_stock = "### Remaining Years of Stock"
    texto_years_stock_desc = """
    **This graph shows the forecast of remaining years of stock, based on the current available uranium quantity.**
    It helps to understand how long, for each year, we had enough stock to meet the total demand of countries (not considering production).
    We can observe a decline.
    """
    texto_years_stock_prod = "### Remaining Years of Stock (With Production)"
    texto_years_stock_prod_desc = """
    **Now we see the remaining years of stock considering both uranium demand and production.**
    By taking production into account, we can adjust the remaining years of stock calculation, resulting in higher numbers.
    """
    texto_table = "### Data Table Used"
    texto_download_button = "📥 Download table as CSV"
    slider_text_prod_demand = "Select the year range for Production and Demand"
    slider_text_stock = "Select the year range for Stock"
    slider_text_acc_stock = "Select the year range for Accumulated Stock"
    slider_text_years_stock = "Select the year range for Remaining Years of Stock"
    slider_text_years_stock_prod = "Select the year range for Remaining Years of Stock (With Production)"
    choose_option = "Choose what you want to visualize"

# Carregar os dados
data = pd.read_csv("csvs/RedBook/Anos_Estoque.csv")

# Título
st.write(texto_intro)

# Gráfico de Produção e Demanda
st.write(texto_prod_demand)
st.markdown(texto_prod_demand_desc)
prod_demand_years = st.slider(
    slider_text_prod_demand,
    int(data["Year"].min()),
    int(data["Year"].max()),
    (int(data["Year"].min()), int(data["Year"].max()))
)
prod_demand_options = st.multiselect(
    choose_option,
    ["Production", "Demand"],
    default=["Production", "Demand"]
)

# Filtrar dados por intervalo de anos
prod_demand_filtered = data[(data["Year"] >= prod_demand_years[0]) & (data["Year"] <= prod_demand_years[1])]

# Transformar o DataFrame para o formato longo (melt)
prod_demand_long = prod_demand_filtered.melt(
    id_vars="Year",
    value_vars=prod_demand_options,
    var_name="Variável",
    value_name="Valor"
)

# Criar o gráfico interativo
fig_prod_demand = px.line(
    prod_demand_long,
    x="Year",
    y="Valor",
    color="Variável",
    labels = {
        "Valor": "Toneladas de Urânio" if lang == "pt" else "Uranium Tonnes",
        "Year": "Ano" if lang == "pt" else "Year",
        "Variável": "Tipo" if lang == "pt" else "Type"
    },
    title="Produção e Demanda por Ano" if lang == "pt" else "Production and Demand by Year"
)
st.plotly_chart(fig_prod_demand, use_container_width=True)

# Gráfico de Estoque por Ano
st.write(texto_stock)
st.markdown(texto_stock_desc)
stock_years = st.slider(
    slider_text_stock,
    int(data["Year"].min()),
    int(data["Year"].max()),
    (int(data["Year"].min()), int(data["Year"].max()))
)
stock_filtered = data[(data["Year"] >= stock_years[0]) & (data["Year"] <= stock_years[1])]
fig_stock = px.area(
    stock_filtered,
    x="Year",
    y="Stock",
    labels = {
        "Stock": "Estoque (Toneladas)" if lang == "pt" else "Stock (Tonnes)",
        "Year": "Ano" if lang == "pt" else "Year"
    },
    title="Estoque por Ano" if lang == "pt" else "Stock by Year"
)
st.plotly_chart(fig_stock, use_container_width=True)

# Gráfico de Estoque Acumulado por Ano
st.write(texto_acc_stock)
st.markdown(texto_acc_stock_desc)
acc_stock_years = st.slider(
    slider_text_acc_stock,
    int(data["Year"].min()),
    int(data["Year"].max()),
    (int(data["Year"].min()), int(data["Year"].max()))
)
acc_stock_filtered = data[(data["Year"] >= acc_stock_years[0]) & (data["Year"] <= acc_stock_years[1])]
fig_acc_stock = px.area(
    acc_stock_filtered,
    x="Year",
    y="Accumulated Stock",
    labels = {
    "Accumulated Stock": "Estoque Acumulado (Toneladas)" if lang == "pt" else "Accumulated Stock (Tonnes)",
    "Year": "Ano" if lang == "pt" else "Year"
    },
    title="Estoque Acumulado por Ano" if lang == "pt" else "Accumulated Stock by Year"
)
st.plotly_chart(fig_acc_stock, use_container_width=True)

# Gráfico de Anos Restantes de Estoque
st.write(texto_years_stock)
st.markdown(texto_years_stock_desc)
years_stock = st.slider(
    slider_text_years_stock,
    int(1955),
    int(data["Year"].max()),
    (1955, int(data["Year"].max()))
)
years_stock_filtered = data[(data["Year"] >= years_stock[0]) & (data["Year"] <= years_stock[1])]
fig_years_stock = px.line(
    years_stock_filtered,
    x="Year",
    y="Years of Stock",
    labels = {
        "Years of Stock": "Anos Restantes de Estoque" if lang == "pt" else "Years of Stock",
        "Year": "Ano" if lang == "pt" else "Year"
    },
    title="Anos Restantes de Estoque (Sem Produção)" if lang == "pt" else "Remaining Years of Stock (Without Production)"
)
st.plotly_chart(fig_years_stock, use_container_width=True)

years_stock_prod = st.slider(
    slider_text_years_stock_prod,
    int(1991),
    int(data["Year"].max()),
    (1991, int(data["Year"].max()))
)

# Gráfico de Anos Restantes de Estoque com Produção
st.write(texto_years_stock_prod)
st.markdown(texto_years_stock_prod_desc)
years_stock_prod_filtered = data[(data["Year"] >= years_stock_prod[0]) & (data["Year"] <= years_stock_prod[1])]
fig_years_stock_prod = px.line(
    years_stock_prod_filtered,
    x="Year",
    y="Years of Stock(w/Production)",
    labels = {
        "Years of Stock(w/Production)": "Anos Restantes de Estoque (Com Produção)" if lang == "pt" else "Years of Stock (w/ Production)",
        "Year": "Ano" if lang == "pt" else "Year"
    },
    title="Anos Restantes de Estoque (Com Produção)" if lang == "pt" else "Remaining Years of Stock (With Production)"
)
st.plotly_chart(fig_years_stock_prod, use_container_width=True)

# Tabela de dados
st.write(texto_table)
st.dataframe(data)

# Botão para download da tabela
st.download_button(
    texto_download_button,
    data=data.to_csv(index=False),
    file_name="dados_estoque_urânio.csv",
    mime="text/csv"
)
