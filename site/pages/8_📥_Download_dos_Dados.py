import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Download dos Dados", page_icon="📥")

# Configuração do idioma
idiomas = {"Português": "pt", "English": "en"}
idioma_selecionado = st.sidebar.selectbox("🌐 Escolha o idioma / Select Language:", idiomas.keys())
lang = idiomas[idioma_selecionado]

# Textos em português e inglês
textos = {
    "pt": {
        "titulo": "Download de Dados",
        "introducao": """
            Esta página foi criada para disponibilizar todos os dados utilizados neste estudo. Aqui você encontrará conjuntos de dados relevantes que apoiam a análise do mercado de urânio e a projeção do consumo futuro.
            
            Para facilitar sua navegação, cada conjunto de dados possui uma breve descrição explicando seu conteúdo e finalidade no estudo. Você pode baixar as tabelas em formato CSV para análise e uso próprio.
            
            Todos os dados fornecidos foram cuidadosamente coletados e estruturados a partir de fontes confiáveis:
            - [World Nuclear Association](https://world-nuclear.org/)
            - [Power Reactor Information System](https://pris.iaea.org/PRIS/home.aspx)
            - [Nuclear Energy Agency](https://www.oecd-nea.org/)
            - [International Atomic Energy Agency](https://www.iaea.org/)
        """,
        "dados_disponiveis": "📥 Dados Disponíveis para Download",
        "selecione_categoria": "Selecione uma categoria abaixo para explorar os dados disponíveis.",
        "escolha_categoria": "Escolha uma categoria:",
        "arquivos_categoria": "Arquivos na categoria:",
        "erro_carregar": "Erro ao carregar o arquivo",
        "baixar_csv": "📥 Baixar como CSV",
    },
    "en": {
        "titulo": "Data Download",
        "introducao": """
            This page was created to provide access to all data used in this study. Here you will find relevant datasets that support the uranium market analysis and future consumption projection.
            
            To make navigation easier, each dataset has a brief description explaining its content and purpose in the study. You can download the tables in CSV format for your analysis and personal use.
            
            All data provided has been carefully collected and structured from reliable sources:
            - [World Nuclear Association](https://world-nuclear.org/)
            - [Power Reactor Information System](https://pris.iaea.org/PRIS/home.aspx)
            - [Nuclear Energy Agency](https://www.oecd-nea.org/)
            - [International Atomic Energy Agency](https://www.iaea.org/)
        """,
        "dados_disponiveis": "📥 Available Data for Download",
        "selecione_categoria": "Select a category below to explore the available data.",
        "escolha_categoria": "Choose a category:",
        "arquivos_categoria": "Files in the category:",
        "erro_carregar": "Error loading file",
        "baixar_csv": "📥 Download as CSV",
    }
}

# Título e introdução
st.markdown(
    f"<h1 style='text-align: center; font-size: 3em;'>{textos[lang]['titulo']}</h1>",
    unsafe_allow_html=True,
)
st.markdown(textos[lang]["introducao"])

# Função para disponibilizar arquivos
def disponibilizar_csv(path, descricao, nome_arquivo):
    st.markdown(f"### {nome_arquivo}")
    st.markdown(descricao)
    try:
        data = pd.read_csv(path)
        st.dataframe(data)
        csv_data = data.to_csv(index=False).encode("utf-8")
        st.download_button(
            label=f"{textos[lang]['baixar_csv']} - {nome_arquivo}",
            data=csv_data,
            file_name=f"{nome_arquivo}.csv",
            mime="text/csv",
        )
    except Exception as e:
        st.error(f"{textos[lang]['erro_carregar']} {nome_arquivo}: {e}")

# Categorias de dados
categorias = {
    "Minas / Mines": [
        {
            "path": "../csvs/Depósitos(RAR-Infered)/identified_in_situ_resources.csv",
            "descricao": {
                "pt": "Este arquivo contém dados sobre recursos de urânio identificados **in situ**, ou seja, localizados no local de origem antes de qualquer processo de extração.",
                "en": "This file contains data on **in situ** uranium resources, i.e., located at the site of origin before any extraction process.",
            },
            "nome_amigavel": {
                "pt": "Recursos Identificados In Situ",
                "en": "Identified In Situ Resources",
            },
        },
        {
            "path": "../csvs/Depósitos(RAR-Infered)/identified_recoverable_resources.csv",
            "descricao": {
                "pt": "Este arquivo apresenta recursos de urânio identificados que podem ser extraídos e recuperados economicamente, considerando a viabilidade técnica.",
                "en": "This file presents identified uranium resources that can be extracted and recovered economically, considering technical feasibility.",
            },
            "nome_amigavel": {
                "pt": "Recursos Identificados Recuperáveis",
                "en": "Identified Recoverable Resources",
            },
        },
        {
            "path": "../csvs/Depósitos(RAR-Infered)/inferred_in_situ_resources.csv",
            "descricao": {
                "pt": "Contém dados sobre recursos de urânio inferidos **in situ**, estimados com base em levantamentos preliminares e com menor grau de confiança.",
                "en": "Contains data on **inferred in situ** uranium resources, estimated based on preliminary surveys with a lower confidence level.",
            },
            "nome_amigavel": {
                "pt": "Recursos Inferidos In Situ",
                "en": "Inferred In Situ Resources",
            },
        },
        {
            "path": "../csvs/Depósitos(RAR-Infered)/inferred_recoverable_resources.csv",
            "descricao": {
                "pt": "Apresenta recursos de urânio inferidos que são economicamente recuperáveis, baseados em estimativas preliminares e dados indiretos.",
                "en": "Presents inferred uranium resources that are economically recoverable, based on preliminary estimates and indirect data.",
            },
            "nome_amigavel": {
                "pt": "Recursos Inferidos Recuperáveis",
                "en": "Inferred Recoverable Resources",
            },
        },
        {
            "path": "../csvs/Depósitos(RAR-Infered)/reasonably_assured_in_situ_resources_complete.csv",
            "descricao": {
                "pt": "Contém dados completos sobre recursos de urânio **in situ** razoavelmente assegurados, baseados em levantamentos detalhados e confiáveis.",
                "en": "Contains complete data on **reasonably assured in situ** uranium resources, based on detailed and reliable surveys.",
            },
            "nome_amigavel": {
                "pt": "Recursos Razoavelmente Assegurados In Situ",
                "en": "Reasonably Assured In Situ Resources",
            },
        },
        {
            "path": "../csvs/Depósitos(RAR-Infered)/reasonably_assured_recoverable_resources_complete.csv",
            "descricao": {
                "pt": "Apresenta dados completos sobre recursos de urânio recuperáveis que são razoavelmente assegurados, indicando alta viabilidade econômica e técnica.",
                "en": "Presents complete data on recoverable uranium resources that are reasonably assured, indicating high economic and technical feasibility.",
            },
            "nome_amigavel": {
                "pt": "Recursos Razoavelmente Assegurados Recuperáveis",
                "en": "Reasonably Assured Recoverable Resources",
            },
        },
        {
            "path": "../csvs/Depósitos(RAR-Infered)/Minas-Intervalo.csv",
            "descricao": {
                "pt": "Este arquivo contém dados sobre minas de urânio, incluindo intervalos de produção, seus países e características gerais.",
                "en": "This file contains data on uranium mines, including production intervals, their countries, and general characteristics.",
            },
            "nome_amigavel": {
                "pt": "Minas de Urânio (Intervalada)",
                "en": "Uranium Mines (Interval-Based)",
            },
        },
        {
            "path": "../csvs/Depósitos(RAR-Infered)/Minas.csv",
            "descricao": {
                "pt": "Apresenta informações completas sobre as minas de urânio, como seus países, sua produção acumulada e disponibilidade.",
                "en": "Presents complete information on uranium mines, such as their countries, accumulated production, and availability.",
            },
            "nome_amigavel": {
                "pt": "Minas de Urânio (Acumulado)",
                "en": "Uranium Mines (Cumulative Data)",
            },
        },
    ],
    "Produção (Urânio) / Production (Uranium)": [
        {
            "path": "../csvs/Produção/UraniumProductionHistorical.csv",
            "descricao": {
                "pt": "Dados sobre a produção de urânio, desde 1998, por país.",
                "en": "Data on uranium production since 1998, by country.",
            },
            "nome_amigavel": {
                "pt": "Produção de Urânio por País",
                "en": "Uranium Production by Country",
            },
        },
        {
            "path": "../csvs/RedBook/Produção(RedBook).csv",
            "descricao": {
                "pt": "Dados sobre a produção de urânio por ano.",
                "en": "Data on uranium production by year.",
            },
            "nome_amigavel": {
                "pt": "Produção de Urânio por Ano",
                "en": "Uranium Production by Year",
            },
        },
        {
            "path": "../csvs/Outros/Gasto_Exploração.csv",
            "descricao": {
                "pt": "Dados sobre quanto cada país gastou com a exploração de urânio, por ano.",
                "en": "Data on how much each country spent on uranium exploration, by year.",
            },
            "nome_amigavel": {
                "pt": "Gastos com Exploração de Urânio por País e Ano",
                "en": "Uranium Exploration Spending by Country and Year",
            },
        },
    ],
    "Demanda / Demand": [
        {
            "path": "../csvs/RedBook/Demanda(RedBook).csv",
            "descricao": {
                "pt": "Dados sobre a demanda mundial de urânio por ano.",
                "en": "Data on the global uranium demand by year.",
            },
            "nome_amigavel": {
                "pt": "Demanda Mundial de Urânio por Ano",
                "en": "Global Uranium Demand by Year",
            },
        },
        {
            "path": "../csvs/Demand(WNA).csv",
            "descricao": {
                "pt": "Dados sobre a demanda de urânio por país por ano.",
                "en": "Data on uranium demand by country per year.",
            },
            "nome_amigavel": {
                "pt": "Demanda de Urânio por País e Ano",
                "en": "Uranium Demand by Country and Year",
            },
        },
        {
            "path": "../csvs/Demanda_Completa.csv",
            "descricao": {
                "pt": "Previsão sobre a demanda de urânio por país por ano até 2050, feita por regressão polinomial.",
                "en": "Forecast of uranium demand by country per year until 2050, made using polynomial regression.",
            },
            "nome_amigavel": {
                "pt": "Previsão da Demanda de Urânio por País e Ano Até 2050",
                "en": "Uranium Demand Forecast by Country and Year Until 2050",
            },
        },
    ],
    "Depósitos e Estoques / Deposits and Stocks": [
        {
            "path": "../csvs/Depósitos.csv",
            "descricao": {
                "pt": "Todos depósitos de urânio com informações gerais.",
                "en": "All uranium deposits with general information.",
            },
            "nome_amigavel": {
                "pt": "Depósitos de Urânio",
                "en": "Uranium Deposits",
            },
        },
        {
            "path": "../csvs/Depósitos_Aquisição.csv",
            "descricao": {
                "pt": "Capacidade de todos depósitos de urânio com seus custos de aquisição.",
                "en": "Capacity of all uranium deposits with their acquisition costs.",
            },
            "nome_amigavel": {
                "pt": "Aquisição de Urânio",
                "en": "Uranium Acquisition",
            },
        },
        {
            "path": "../csvs/Predição_Custo_Aquisição.csv",
            "descricao": {
                "pt": "Predição do custo de aquisição por depósito de urânio, feito por modelos de Machine Learning.",
                "en": "Prediction of acquisition cost per uranium deposit, made using Machine Learning models.",
            },
            "nome_amigavel": {
                "pt": "Predição do Custo de Aquisição de Urânio",
                "en": "Prediction of Uranium Acquisition Cost",
            },
        },
        {
            "path": "../csvs/RedBook/Estoque(RedBook).csv",
            "descricao": {
                "pt": "Dados sobre o estoque mundial de urânio por ano.",
                "en": "Data on global uranium stock by year.",
            },
            "nome_amigavel": {
                "pt": "Estoque Acumulado de Urânio por Ano",
                "en": "Accumulated Uranium Stock by Year",
            },
        },
    ],
    "Produção (Energia) / Production (Energy)": [
        {
            "path": "../csvs/Diff_Produção.csv",
            "descricao": {
                "pt": "Diferença entre o ano atual e o anterior na produção de energia por país.",
                "en": "Difference between the current and previous year in energy production by country.",
            },
            "nome_amigavel": {
                "pt": "Diferença Anual na Produção de Energia",
                "en": "Annual Difference in Energy Production",
            },
        },
    ],
    "Reatores Nucleares / Nuclear Reactors": [
        {
            "path": "../csvs/Energia_Tipo.csv",
            "descricao": {
                "pt": "Predição da produção de GWh/tU por tipo de reator, feito por modelos de Machine Learning.",
                "en": "Prediction of GWh/tU production by reactor type, made using Machine Learning models.",
            },
            "nome_amigavel": {
                "pt": "Predição da Produção de Energia por Tipo de Reator",
                "en": "Prediction of Energy Production by Reactor Type",
            },
        },
        {
            "path": "../csvs/Reatores_Info.csv",
            "descricao": {
                "pt": "Informações gerais sobre todos reatores do mundo.",
                "en": "General information about all reactors in the world.",
            },
            "nome_amigavel": {
                "pt": "Informações sobre Reatores",
                "en": "Reactor Information",
            },
        },
        {
            "path": "../csvs/Reatores_Ano.csv",
            "descricao": {
                "pt": "Dados sobre todos reatores e sua produção por ano, estejam eles operando, desativados ou até mesmo apenas planejados.",
                "en": "Data on all reactors and their production by year, whether they are operating, decommissioned, or even just planned.",
            },
            "nome_amigavel": {
                "pt": "Reatores por Ano",
                "en": "Reactors by Year",
            },
        },
        {
            "path": "../csvs/Tempo_Construção_País.csv",
            "descricao": {
                "pt": "Média do tempo que um país leva para construir um reator nuclear.",
                "en": "Average time a country takes to build a nuclear reactor.",
            },
            "nome_amigavel": {
                "pt": "Tempo Médio de Construção de Reator por País",
                "en": "Average Reactor Construction Time by Country",
            },
        },
        {
            "path": "../csvs/Reatores_Finalização.csv",
            "descricao": {
                "pt": "Previsão da finalização da construção dos reatores que estão atualmente em construção.",
                "en": "Forecast of the completion of reactors currently under construction.",
            },
            "nome_amigavel": {
                "pt": "Previsão de Finalização da Construção de Reatores",
                "en": "Forecast of Reactor Construction Completion",
            },
        },
    ],
}

# Seleção de categoria e exibição de arquivos
st.markdown(f"## {textos[lang]['dados_disponiveis']}")
st.markdown(textos[lang]["selecione_categoria"])

categoria_selecionada = st.selectbox(
    textos[lang]["escolha_categoria"], list(categorias.keys())
)

st.markdown(f"## {textos[lang]['arquivos_categoria']} {categoria_selecionada}")
for arquivo in categorias[categoria_selecionada]:
    disponibilizar_csv(
        arquivo["path"],
        arquivo["descricao"][lang],
        arquivo["nome_amigavel"][lang],
    )