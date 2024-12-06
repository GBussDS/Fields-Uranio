import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Análise de Construção e Demanda de Reatores", page_icon="⏳")

# Idiomas disponíveis
idiomas = {"Português": "pt", "English": "en"}
idioma_selecionado = st.sidebar.selectbox("🌐 Escolha o idioma / Select Language:", idiomas.keys())
lang = idiomas[idioma_selecionado]

# Funções para texto com base no idioma
def translate(key, lang):
    translations = {
        "pt": {
            "title": "Análise de Construção e Demanda de Reatores",
            "main_header": "O Futuro do Urânio",
            "intro_text": """
                Este estudo tem como objetivo principal estimar o mercado futuro do urânio, um recurso essencial para a geração de energia nuclear.
                A análise foi conduzida utilizando dados dos maiores consumidores de urânio: os reatores nucleares.
            """,
            "select_country": "Selecione os países para visualizar:",
            "uranium_demand_title": "Demanda de Urânio por País ao Longo do Tempo",
            "construction_time_title": "Tempo Médio de Construção de Reatores por País",
            "completion_table_title": "Datas estimadas da Finalização por Reator",
            "completion_table_text": "Com isso conseguimos estimar a demanda futura:",
            "analysis_option": "Escolha o tipo de análise:",
            "by_country": "Demanda por País",
            "global_demand": "Demanda Global",
            "historical_demand_title": "Demanda Histórica e Projeções de Urânio por País",
            "global_demand_title": "Demanda Global de Urânio",
        },
        "en": {
            "title": "Analysis of Reactor Construction and Demand",
            "main_header": "The Future of Uranium",
            "intro_text": """
                This study aims to estimate the future uranium market, a key resource for nuclear power generation.
                The analysis was conducted using data from the largest uranium consumers: nuclear reactors.
            """,
            "select_country": "Select countries to view:",
            "uranium_demand_title": "Uranium Demand by Country Over Time",
            "construction_time_title": "Average Reactor Construction Time by Country",
            "completion_table_title": "Estimated Reactor Completion Dates",
            "completion_table_text": "With this, we can estimate future demand:",
            "analysis_option": "Choose the type of analysis:",
            "by_country": "Demand by Country",
            "global_demand": "Global Demand",
            "historical_demand_title": "Historical and Projected Uranium Demand by Country",
            "global_demand_title": "Global Uranium Demand",
        },
    }
    return translations[lang][key]

# Definindo a animação CSS para o efeito de slide da direita para a esquerda
st.markdown("""
    <style>
    div[data-testid="stMainBlockContainer"] > div {
        animation: slideInRight 0.5s ease-in-out;
    }

    @keyframes slideInRight {
        0% { transform: translateX(100%); opacity: 0; }
        100% { transform: translateX(0); opacity: 1; }
    }
    </style>
    """, unsafe_allow_html=True)

# Carregar dados com cache para não carregar repetidamente
@st.cache_data
def load_data():
    construction_data = pd.read_csv("csvs/Tempo_Construção_País.csv")
    reactor_completion_data = pd.read_csv("csvs/Reatores_Finalização.csv")
    historical_demand_data = pd.read_csv("csvs/Demanda_Completa.csv")

    historical_demand_long = historical_demand_data.melt(
        id_vars="Country", var_name="Year", value_name="Demand"
    )
    historical_demand_long["Year"] = historical_demand_long["Year"].astype(int)

    return construction_data, reactor_completion_data, historical_demand_long

# Carregar os dados
construction_data, reactor_completion_data, historical_demand_long = load_data()

st.markdown(f"<h1 style='text-align: center; font-size: 3em;'>{translate('main_header', lang)}</h1>", unsafe_allow_html=True)
st.markdown(translate("intro_text", lang))

# Gráfico da demanda por país
file_path = 'csvs/Demand(WNA).csv'
uranium_data = pd.read_csv(file_path)

selected_countries = st.multiselect(
    translate("select_country", lang),
    sorted(uranium_data["Country"].unique()),
    default=["USA", "China"]
)

filtered_data = uranium_data[uranium_data["Country"].isin(selected_countries)]

fig = px.line(
    filtered_data,
    x="Year",
    y="Uranium Required [T]",
    color="Country",
    labels={"Year": "Year", "Uranium Required [T]": "Uranium Demand (t)"},
    title=translate("uranium_demand_title", lang),
)

st.plotly_chart(fig, use_container_width=True)

# Gráfico do tempo de construção
avg_construction_time = construction_data.groupby("Country")["Construction Duration"].mean().reset_index().sort_values(by="Construction Duration")

fig_construction = px.bar(
    avg_construction_time,
    x="Construction Duration",
    y="Country",
    orientation="h",
    labels={"Construction Duration": "Average Construction Time (years)", "Country": "Country"},
    title=translate("construction_time_title", lang),
    height=800,
)
fig_construction.update_layout(yaxis={"categoryorder": "total ascending"})
st.plotly_chart(fig_construction, use_container_width=True)

# Tabela: Datas de Finalização dos Reatores
st.markdown(f"<h1 style='text-align: center; font-size: 1.5em;'>{translate('completion_table_title', lang)}</h1>", unsafe_allow_html=True)
reactor_completion_data["Construction Start Date"] = pd.to_datetime(reactor_completion_data["Construction Start Date"])
reactor_completion_data["Predicted Completion Date"] = pd.to_datetime(reactor_completion_data["Predicted Completion Date"])
completion_table = reactor_completion_data.sort_values(by=["Country", "Predicted Completion Date"])
st.dataframe(completion_table[["Name", "Country", "Construction Start Date", "Predicted Completion Date"]])

st.markdown(translate("completion_table_text", lang))

# Análise de demanda histórica
historical_demand_long = historical_demand_long[historical_demand_long["Year"] <= 2031]

analysis_type = st.radio(
    translate("analysis_option", lang),
    (translate("by_country", lang), translate("global_demand", lang)),
    index=0
)

if analysis_type == translate("by_country", lang):
    st.write(f"### {translate('by_country', lang)}")
    selected_countries = st.multiselect(
        translate("select_country", lang),
        sorted(historical_demand_long["Country"].unique()),
        default=["UNITED STATES OF AMERICA", "CHINA"],
    )
    filtered_demand_data = historical_demand_long[historical_demand_long["Country"].isin(selected_countries)]
    
    fig_demand = px.line(
        filtered_demand_data,
        x="Year",
        y="Demand",
        color="Country",
        labels={"Year": "Year", "Demand": "Uranium Demand (tU)", "Country": "Country"},
        title=translate("historical_demand_title", lang),
    )
    fig_demand.update_layout(xaxis=dict(tickangle=90))
    st.plotly_chart(fig_demand, use_container_width=True)

elif analysis_type == translate("global_demand", lang):
    st.write(f"### {translate('global_demand', lang)}")
    global_demand = historical_demand_long.groupby("Year", as_index=False).agg({"Demand": "sum"})
    
    fig_global = px.line(
        global_demand,
        x="Year",
        y="Demand",
        labels={"Year": "Year", "Demand": "Global Uranium Demand (tU)"},
        title=translate("global_demand_title", lang),
    )
    fig_global.update_layout(xaxis=dict(tickangle=90))
    st.plotly_chart(fig_global, use_container_width=True)
