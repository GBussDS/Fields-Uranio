import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Análise de Produção, Demanda e Estoque de Urânio", page_icon="📊")

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
data = pd.read_csv("../csvs/RedBook/Anos_Estoque.csv")

st.write("# Análise de Produção, Demanda e Estoque de Urânio")

# Gráfico de Produção e Demanda
st.write("### Produção e Demanda por Ano")
st.markdown("""
    **Este gráfico mostra a evolução da produção e da demanda de urânio ao longo do tempo.**
    Você pode usar o intervalo de anos para explorar como a produção e a demanda mudaram em diferentes períodos.
    O gráfico ajuda a visualizar se a produção está acompanhando a demanda ou se há uma discrepância crescente entre elas.
""")
prod_demand_years = st.slider(
    "Selecione o intervalo de anos para Produção e Demanda",
    int(data["Year"].min()),
    int(data["Year"].max()),
    (int(data["Year"].min()), int(data["Year"].max()))
)
prod_demand_options = st.multiselect(
    "Escolha o que deseja visualizar",
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
    labels={"Valor": "Toneladas de Urânio", "Year": "Ano", "Variável": "Tipo"},
    title="Produção e Demanda por Ano"
)
st.plotly_chart(fig_prod_demand, use_container_width=True)

# Gráfico de Estoque por Ano
st.write("### Estoque por Ano")
st.markdown("""
    **Este gráfico ilustra a evolução do estoque de urânio ao longo dos anos.**
    Ao observar as variações no estoque, podemos entender como ele está sendo gerido e como pode impactar a disponibilidade futura de urânio.
    O gráfico permite visualizar a tendência do estoque ao longo do tempo, se ele está aumentando ou diminuindo.
""")
stock_years = st.slider(
    "Selecione o intervalo de anos para Estoque",
    int(data["Year"].min()),
    int(data["Year"].max()),
    (int(data["Year"].min()), int(data["Year"].max()))
)
stock_filtered = data[(data["Year"] >= stock_years[0]) & (data["Year"] <= stock_years[1])]
fig_stock = px.area(
    stock_filtered,
    x="Year",
    y="Stock",
    labels={"Stock": "Estoque (Toneladas)", "Year": "Ano"},
    title="Estoque por Ano"
)
st.plotly_chart(fig_stock, use_container_width=True)

# Gráfico de Estoque Acumulado por Ano
st.write("### Estoque Acumulado por Ano")
st.markdown("""
    **Este gráfico exibe o estoque acumulado ao longo dos anos.**
    Ele mostra o total de urânio que foi armazenado e acumulado até cada ano. A análise do estoque acumulado pode revelar tendências importantes sobre a gestão e a sustentabilidade do abastecimento.
""")
acc_stock_years = st.slider(
    "Selecione o intervalo de anos para Estoque Acumulado",
    int(data["Year"].min()),
    int(data["Year"].max()),
    (int(data["Year"].min()), int(data["Year"].max()))
)
acc_stock_filtered = data[(data["Year"] >= acc_stock_years[0]) & (data["Year"] <= acc_stock_years[1])]
fig_acc_stock = px.area(
    acc_stock_filtered,
    x="Year",
    y="Accumulated Stock",
    labels={"Accumulated Stock": "Estoque Acumulado (Toneladas)", "Year": "Ano"},
    title="Estoque Acumulado por Ano"
)
st.plotly_chart(fig_acc_stock, use_container_width=True)

# Gráfico de Anos Restantes de Estoque
st.write("### Anos Restantes de Estoque")
st.markdown("""
    **Este gráfico mostra a previsão dos anos restantes de estoque, com base na quantidade atual de urânio disponível.**
    Ele ajuda a entender quanto tempo o estoque atual pode sustentar a demanda, considerando as variáveis do estoque existente.
""")
years_stock = st.slider(
    "Selecione o intervalo de anos para Anos Restantes de Estoque",
    int(1955),
    int(data["Year"].max()),
    (1955, int(data["Year"].max()))
)
years_stock_filtered = data[(data["Year"] >= years_stock[0]) & (data["Year"] <= years_stock[1])]
fig_years_stock = px.line(
    years_stock_filtered,
    x="Year",
    y="Years of Stock",
    labels={"Years of Stock": "Anos Restantes de Estoque", "Year": "Ano"},
    title="Anos Restantes de Estoque"
)
st.plotly_chart(fig_years_stock, use_container_width=True)

# Gráfico de Anos Restantes de Estoque (Com Produção)
st.write("### Anos Restantes de Estoque (Com Produção)")
st.markdown("""
    **Aqui, vemos os anos restantes de estoque considerando a produção de urânio.**
    Ao levar em conta a produção, podemos ajustar o cálculo de anos restantes de estoque, o que pode alterar as previsões de sustentabilidade no futuro.
""")
years_stock_prod = st.slider(
    "Selecione o intervalo de anos para Anos Restantes de Estoque (Com Produção)",
    int(1991),
    int(data["Year"].max()),
    (1991, int(data["Year"].max()))
)
years_stock_prod_filtered = data[(data["Year"] >= years_stock_prod[0]) & (data["Year"] <= years_stock_prod[1])]
fig_years_stock_prod = px.line(
    years_stock_prod_filtered,
    x="Year",
    y="Years of Stock(w/Production)",
    labels={"Years of Stock(w/Production)": "Anos Restantes de Estoque (Com Produção)", "Year": "Ano"},
    title="Anos Restantes de Estoque (Com Produção)"
)
st.plotly_chart(fig_years_stock_prod, use_container_width=True)

# Tabela e botão de download
st.write("### Tabela de Dados Utilizados")
st.dataframe(data)

# Converter o DataFrame para CSV
csv_data = data.to_csv(index=False).encode("utf-8")

# # Botão para download
st.download_button(
    label="📥 Baixar tabela como CSV",
    data=csv_data,
    file_name="dados_uranio.csv",
    mime="text/csv",
)
