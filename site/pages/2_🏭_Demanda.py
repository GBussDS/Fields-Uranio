import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Demanda de Urânio por País", page_icon="📉")

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

# Função para carregar os dados e calcular a demanda global
@st.cache_data
def load_and_prepare_data():
    demand_data = pd.read_csv("../csvs/Demand(WNA).csv")
    # Garantir que a coluna "Year" é tratada como numérica
    demand_data["Year"] = demand_data["Year"].astype(int)
    # Filtrar países com dados reais (demanda não-zero)
    non_zero_countries = demand_data.groupby("Country")["Uranium Required [T]"].sum()
    valid_countries = non_zero_countries[non_zero_countries > 0].index
    filtered_data = demand_data[demand_data["Country"].isin(valid_countries)]
    # Calcular demanda global por ano
    global_data = (
        filtered_data.groupby("Year")["Uranium Required [T]"]
        .sum()
        .reset_index()
        .assign(Country="Global")
    )
    # Adicionar os dados globais ao dataset original
    combined_data = pd.concat([filtered_data, global_data], ignore_index=True)
    return combined_data

# Carregar e preparar os dados
demand_data = load_and_prepare_data()

# Lista inicial de países
initial_countries = [
    "USA",
    "China",
    "Japan",
    "Korea RO (South)",
    "Russia",
    "Ukraine",
    "Canada",
    "United Kingdom",
    "Global"
]

# Configurar e criar o gráfico interativo com Plotly
st.write("# Demanda de Urânio por País ao Longo dos Anos")

st.write(
    """
    Nesta página, você pode explorar a demanda anual de urânio por país, de 2007 a 2022. A visualização abaixo 
    mostra a quantidade de urânio demandado em toneladas (tU) ao longo dos anos.
    """
)

# Seleção de países
selected_countries = st.multiselect(
    "Escolha os países para exibir:",
    options=demand_data["Country"].unique(),
    default=initial_countries
)

# Selecionar o intervalo de anos
anos = sorted(demand_data["Year"].unique())
years = st.slider("Escolha o intervalo de anos", min(anos), max(anos), (min(anos), max(anos)))

# Filtrar os dados pelos países selecionados e pelo intervalo de anos
filtered_data = demand_data[
    (demand_data["Country"].isin(selected_countries)) & 
    (demand_data["Year"].between(years[0], years[1]))
]

fig = px.line(
    filtered_data,
    x="Year",
    y="Uranium Required [T]",
    color="Country",
    labels={"Uranium Required [T]": "Demanda de Urânio (tU)", "Year": "Ano"},
    title=f"Demanda de Urânio por País ({years[0]} - {years[1]})",
    hover_name="Country"
)

# Ajustar o layout
fig.update_layout(
    xaxis_title="Ano",
    yaxis_title="Demanda de Urânio (tU)",
    legend_title="País",
    template="plotly_white",
)

# Exibir o gráfico interativo
st.plotly_chart(fig, use_container_width=True)

# Exibir dados usados
st.write("### Dados usados:")
st.dataframe(filtered_data)

# Converter o DataFrame para CSV
csv_data = filtered_data.T.to_csv(index=False).encode("utf-8")

# # Botão para download
st.download_button(
    label="📥 Baixar tabela como CSV",
    data=csv_data,
    file_name="dados_uranio.csv",
    mime="text/csv",
)

# Carregar dados
construction_data = pd.read_csv("../csvs/Tempo_Construção_País.csv")
reactor_completion_data = pd.read_csv("../csvs/Reatores_Finalização.csv")
historical_demand_data = pd.read_csv("../csvs/Demanda_Completa.csv")

# Transformar demanda histórica para formato longo
historical_demand_long = historical_demand_data.melt(
    id_vars="Country", var_name="Year", value_name="Demand"
)
historical_demand_long["Year"] = historical_demand_long["Year"].astype(int)

st.write("""
Para conseguir fazer uma previsão da Demanda para cada país para os próximos anos, observamos nos dados do PRIS
quanto tempo cada país leva em média para finalizar a construção de um reator, analisando o tempo que levou em 
média para cada país terminar os seus reatores já finalizados (para países que estão a construir o seu primeiro
reator, consideramos a média global) e, a partir dessa média, olhando os reatores que estão em construção podemos
aproximar a sua data de finalização.

Após isso, para prever quanto de urânio tal reator irá demandar, consideramos a potência (GW) do reator e,
através dos dados de reatores antigos, conseguimos fazer uma razão de toneladas de urânio por energia (GW) adquirida
(tU/GW). Assim, até 2050, temos a previsão para cada país de quanto urânio seus reatores irão demanda (também 
considerando que nenhum dos reatores ativos no momento irão ser suspendidos)
""")


# Gráfico 1: Tempo médio de construção por país
st.write("### Tempo Médio de Construção de Reatores por País")

avg_construction_time = construction_data.groupby("Country")["Construction Duration"].mean().reset_index().sort_values(by="Construction Duration")

fig_construction = px.bar(
    avg_construction_time,
    x="Construction Duration",
    y="Country",
    orientation="h",
    labels={"Construction Duration": "Tempo Médio de Construção (anos)", "Country": "País"},
    title="Tempo Médio de Construção de Reatores por País",
    height=800,  # Aumentar a altura do gráfico
)
fig_construction.update_layout(yaxis={"categoryorder": "total ascending"})
st.plotly_chart(fig_construction, use_container_width=True)

# Botão para download dos dados de construção
st.download_button(
    label="📥 Baixar Dados de Tempo de Construção",
    data=construction_data.to_csv(index=False).encode("utf-8"),
    file_name="tempo_construcao.csv",
    mime="text/csv",
)

# Tabela: Datas de Finalização dos Reatores
st.write("### Datas de Finalização dos Reatores")
reactor_completion_data["Construction Start Date"] = pd.to_datetime(reactor_completion_data["Construction Start Date"])
reactor_completion_data["Predicted Completion Date"] = pd.to_datetime(reactor_completion_data["Predicted Completion Date"])
completion_table = reactor_completion_data.sort_values(by=["Country", "Predicted Completion Date"])
st.dataframe(completion_table[["Name", "Country", "Construction Start Date", "Predicted Completion Date"]])

# Botão para download da tabela de finalização dos reatores
st.download_button(
    label="📥 Baixar Tabela de Datas de Finalização",
    data=completion_table.to_csv(index=False).encode("utf-8"),
    file_name="datas_finalizacao_reatores.csv",
    mime="text/csv",
)

# Gráfico 3: Demanda Histórica de Urânio com Previsão (1964-2050)
st.write("### Demanda Histórica e Previsão de Demanda de Urânio por País")
selected_countries = st.multiselect(
    "Selecione os países para visualizar",
    sorted(historical_demand_long["Country"].unique()),
    default=["FRANCE", "CHINA"],
)

filtered_demand_data = historical_demand_long[historical_demand_long["Country"].isin(selected_countries)]

fig_demand = px.line(
    filtered_demand_data,
    x="Year",
    y="Demand",
    color="Country",
    labels={"Year": "Ano", "Demand": "Demanda de Urânio (tU)", "Country": "País"},
    title="Demanda Histórica e Projeções de Urânio por País",
)
fig_demand.update_layout(xaxis=dict(tickangle=90))
st.plotly_chart(fig_demand, use_container_width=True)

# Botão para download da tabela de demanda histórica
st.download_button(
    label="📥 Baixar Dados de Demanda Histórica",
    data=historical_demand_data.to_csv(index=False).encode("utf-8"),
    file_name="demanda_historica.csv",
    mime="text/csv",
)

# Explicação
st.write("""
### Explicação dos Gráficos
1. **Tempo Médio de Construção**: Tempo médio necessário para construir reatores nucleares, por país.
2. **Tabela de Datas de Conclusão de Reatores**: Exibe a previsão de conclusão dos reatores em construção, por país e data.
3. **Demanda Histórica e Projeção de Demanda de Urânio**: Acompanha a demanda histórica de urânio e inclui previsões até 2050.
""")
