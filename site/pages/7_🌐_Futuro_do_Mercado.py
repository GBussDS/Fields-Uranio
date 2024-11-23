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

st.markdown("<h1 style='text-align: center; font-size: 3em;'>O Futuro do Urânio</h1>", unsafe_allow_html=True)
st.markdown("""
            Este estudo tem como objetivo principal estimar o mercado futuro do urânio, um recurso essencial para a geração de energia nuclear. 

            A análise foi conduzida utilizando dados dos maiores consumidores de urânio: os reatores nucleares. As principais etapas incluíram:
            - Avaliar os dados de produção dos reatores para estimar se o consumo de urânio aumentará, e em que proporção;
            - Examinar a demanda específica de cada reator ou país para entender seus níveis de consumo.

            Contudo, como muitos países não fornecem dados confiáveis e detalhados sobre suas aquisições de urânio, foi necessário recorrer às informações disponíveis. Para isso, utilizamos os dados fornecidos pelo [World Uranium](https://world-nuclear.org/information-library/facts-and-figures/world-nuclear-power-reactors-and-uranium-requireme), que abrangem a demanda a partir de 2007 e informações sobre reatores desde períodos anteriores.
            """)

#Gráfico da demanda por país

file_path = '../csvs/Demand(WNA).csv'
uranium_data = pd.read_csv(file_path)

selected_countries = st.multiselect(
    "Selecione os países para visualizar:",
    sorted(uranium_data["Country"].unique()),
    default=["USA", "China"]
)

filtered_data = uranium_data[uranium_data["Country"].isin(selected_countries)]

fig = px.line(
    filtered_data,
    x="Year",
    y="Uranium Required [T]",
    color="Country",
    labels={"Year": "Ano", "Uranium Required [T]": "Demanda de Urânio (t)"},
    title="Demanda de Urânio por País ao Longo do Tempo"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
            Com base nos dados disponíveis, desenvolvemos uma métrica que correlaciona a potência de cada reator com a quantidade 
            de urânio consumida anualmente. Optamos por usar a potência como referência, pois é a única informação relacionada 
            à produção de energia de um reator que está disponível enquanto ele ainda está em construção.
            
            Para aumentar a precisão das projeções, calculamos o tempo médio que cada país leva para concluir a construção de um 
            reator. Nos casos em que essa informação específica não estava disponível, utilizamos a média global como estimativa.
            """)

avg_construction_time = construction_data.groupby("Country")["Construction Duration"].mean().reset_index().sort_values(by="Construction Duration")

fig_construction = px.bar(
    avg_construction_time,
    x="Construction Duration",
    y="Country",
    orientation="h",
    labels={"Construction Duration": "Tempo Médio de Construção (anos)", "Country": "País"},
    title="Tempo Médio de Construção de Reatores por País",
    height=800,
)
fig_construction.update_layout(yaxis={"categoryorder": "total ascending"})
st.plotly_chart(fig_construction, use_container_width=True)

st.markdown("""
            Dessa maneira, conseguimos projetar o consumo futuro de urânio ao estimar quando um reator em construção 
            estará operacional e qual será a sua demanda anual por urânio.
            """)

# Tabela: Datas de Finalização dos Reatores
st.markdown("<h1 style='text-align: center; font-size: 1.5em;'>Datas estimadas da Finalização por Reator</h1>", unsafe_allow_html=True)

reactor_completion_data["Construction Start Date"] = pd.to_datetime(reactor_completion_data["Construction Start Date"])
reactor_completion_data["Predicted Completion Date"] = pd.to_datetime(reactor_completion_data["Predicted Completion Date"])
completion_table = reactor_completion_data.sort_values(by=["Country", "Predicted Completion Date"])
st.dataframe(completion_table[["Name", "Country", "Construction Start Date", "Predicted Completion Date"]])

st.markdown("""
            Com isso conseguimos estimar a demanda futura:
            """)

historical_demand_long = historical_demand_long[historical_demand_long["Year"] <= 2031]

analysis_type = st.radio(
    "Escolha o tipo de análise:",
    ("Demanda por País", "Demanda Global"),
    index=0
)

if analysis_type == "Demanda por País":
    st.write("### Demanda por País")
    selected_countries = st.multiselect(
        "Selecione os países para visualizar:",
        sorted(historical_demand_long["Country"].unique()),
        default=["UNITED STATES OF AMERICA", "CHINA"],
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

elif analysis_type == "Demanda Global":
    st.write("### Demanda Global")
    
    global_demand = historical_demand_long.groupby("Year", as_index=False).agg({"Demand": "sum"})
    
    fig_global = px.line(
        global_demand,
        x="Year",
        y="Demand",
        labels={"Year": "Ano", "Demand": "Demanda Global de Urânio (tU)"},
        title="Demanda Global de Urânio",
    )
    fig_global.update_layout(xaxis=dict(tickangle=90))
    st.plotly_chart(fig_global, use_container_width=True)
