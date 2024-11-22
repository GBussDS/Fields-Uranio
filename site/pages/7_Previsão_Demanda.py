import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Análise de Construção e Demanda de Reatores", page_icon="⏳")

# Carregar dados
construction_data = pd.read_csv("../csvs/Tempo_Construção_País.csv")
reactor_completion_data = pd.read_csv("../csvs/Reatores_Finalização.csv")
historical_demand_data = pd.read_csv("../csvs/Demanda_Completa.csv")

# Transformar demanda histórica para formato longo
historical_demand_long = historical_demand_data.melt(
    id_vars="Country", var_name="Year", value_name="Demand"
)
historical_demand_long["Year"] = historical_demand_long["Year"].astype(int)

# Gráfico 1: Tempo médio de construção por país
st.write("## Tempo Médio de Construção de Reatores por País")
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
st.write("## Datas de Finalização dos Reatores")
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
st.write("## Demanda Histórica e Previsão de Demanda de Urânio por País")
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

