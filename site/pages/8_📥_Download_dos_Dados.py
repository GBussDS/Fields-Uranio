import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Download dos Dados", page_icon="📥")

# Título e introdução
st.markdown("<h1 style='text-align: center; font-size: 3em;'>Download de Dados</h1>", unsafe_allow_html=True)
st.markdown("""
            Esta página foi criada para disponibilizar todos os dados utilizados neste estudo. Aqui você encontrará conjuntos de dados relevantes que apoiam a análise do mercado de urânio e a projeção do consumo futuro.
            
            Para facilitar sua navegação, cada conjunto de dados possui uma breve descrição explicando seu conteúdo e finalidade no estudo. Você pode baixar as tabelas em formato CSV para análise e uso próprio.
            
            Todos os dados fornecidos foram cuidadosamente coletados e estruturados a partir de fontes confiáveis:
            - [World Nuclear Association](https://world-nuclear.org/)
            - [Power Reactor Information System](https://pris.iaea.org/PRIS/home.aspx)
            - [Nuclear Energy Agency](https://www.oecd-nea.org/)
            - [International Atomic Energy Agency](https://www.iaea.org/)
            """)

def disponibilizar_csv(path, descricao, nome_arquivo):
    st.markdown(f"### {nome_arquivo}")
    st.markdown(descricao)
    try:
        data = pd.read_csv(path)
        st.dataframe(data) 
        csv_data = data.to_csv(index=False).encode("utf-8")
        st.download_button(
            label=f"📥 Baixar {nome_arquivo} como CSV",
            data=csv_data,
            file_name=f"{nome_arquivo}.csv",
            mime="text/csv",
        )
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo {nome_arquivo}: {e}")

st.markdown("## 📥 Dados Disponíveis para Download")

categorias = {
    "Minas": [
        {
            "path": "../csvs/Depósitos(RAR-Infered)/identified_in_situ_resources.csv",
            "descricao": "Este arquivo contém dados sobre recursos de urânio identificados **in situ**, ou seja, localizados no local de origem antes de qualquer processo de extração.",
            "nome_amigavel": "Recursos Identificados In Situ"
        },
        {
            "path": "../csvs/Depósitos(RAR-Infered)/identified_recoverable_resources.csv",
            "descricao": "Este arquivo apresenta recursos de urânio identificados que podem ser extraídos e recuperados economicamente, considerando a viabilidade técnica.",
            "nome_amigavel": "Recursos Identificados Recuperáveis"
        },
        {
            "path": "../csvs/Depósitos(RAR-Infered)/inferred_in_situ_resources.csv",
            "descricao": "Contém dados sobre recursos de urânio inferidos **in situ**, estimados com base em levantamentos preliminares e com menor grau de confiança.",
            "nome_amigavel": "Recursos Inferidos In Situ"
        },
        {
            "path": "../csvs/Depósitos(RAR-Infered)/inferred_recoverable_resources.csv",
            "descricao": "Apresenta recursos de urânio inferidos que são economicamente recuperáveis, baseados em estimativas preliminares e dados indiretos.",
            "nome_amigavel": "Recursos Inferidos Recuperáveis"
        },
        {
            "path": "../csvs/Depósitos(RAR-Infered)/reasonably_assured_in_situ_resources_complete.csv",
            "descricao": "Contém dados completos sobre recursos de urânio **in situ** razoavelmente assegurados, baseados em levantamentos detalhados e confiáveis.",
            "nome_amigavel": "Recursos Razoavelmente Assegurados In Situ"
        },
        {
            "path": "../csvs/Depósitos(RAR-Infered)/reasonably_assured_recoverable_resources_complete.csv",
            "descricao": "Apresenta dados completos sobre recursos de urânio recuperáveis que são razoavelmente assegurados, indicando alta viabilidade econômica e técnica.",
            "nome_amigavel": "Recursos Razoavelmente Assegurados Recuperáveis"
        },
        {
            "path": "../csvs/Depósitos(RAR-Infered)/Minas-Intervalo.csv",
            "descricao": "Este arquivo contém dados sobre minas de urânio, incluindo intervalos de produção, seus países e características gerais.",
            "nome_amigavel": "Minas de Urânio (Intervalada)"
        },
        {
            "path": "../csvs/Depósitos(RAR-Infered)/Minas.csv",
            "descricao": "Apresenta informações completas sobre as minas de urânio, como seus países, sua produção acumulada e disponibilidade.",
            "nome_amigavel": "Minas de Urânio (Acumulado)"
        }
    ],
    "Produção (Urânio)": [
        {
            "path": "../csvs/Produção/UraniumProductionHistorical.csv",
            "descricao": "Dados sobre a produção de urânio, desde 1998, por país.",
            "nome_amigavel": "Produção de Urânio por País"
        },
        {
            "path": "../csvs/RedBook/Produção(RedBook).csv",
            "descricao": "Dados sobre a produção de urânio por ano.",
            "nome_amigavel": "Produção de Urânio por Ano"
        },
        {
            "path": "../csvs/Outros/Gasto_Exploração.csv",
            "descricao": "Dados sobre quanto cada país gastou com a exploração de urânio, por ano.",
            "nome_amigavel": "Gastos com Exploração de Urânio por País e Ano"
        }
    ],
    "Demanda": [
        {
            "path": "../csvs/RedBook/Demanda(RedBook).csv",
            "descricao": "Dados sobre a demanda mundial de urânio por ano.",
            "nome_amigavel": "Demanda Mundial de Urânio por Ano"
        },
        {
            "path": "../csvs/Demand(WNA).csv",
            "descricao": "Dados sobre a demanda de urânio por país por ano.",
            "nome_amigavel": "Demanda de Urânio por País e Ano"
        },
        {
            "path": "../csvs/Demanda_Completa.csv",
            "descricao": "Previsão sobre a demanda de urânio por país por ano até 2050, feita por regressão polinomial.",
            "nome_amigavel": "Previsão da Demanda de Urânio por País e Ano Até 2050"
        }
    ],
    "Depósitos e Estoque": [
        {
            "path": "../csvs/Depósitos.csv",
            "descricao": " Todos depósitos de urânio com informações gerais.",
            "nome_amigavel": "Depósitos de Urânio"
        },
        {
            "path": "../csvs/Depósitos_Aquisição.csv",
            "descricao": "Capacidade de todos depósitos de urânio com seus custos de aquisição.",
            "nome_amigavel": "Aquisição de Urânio"
        },
        {
            "path": "../csvs/Predição_Custo_Aquisição.csv",
            "descricao": "Predição do custo de aquisição por depósito de urânio, feito por modelos de Machine Learning.",
            "nome_amigavel": "Predição do Custa de Aquisição de Urânio"
        },
        {
            "path": "../csvs/RedBook/Estoque(RedBook).csv",
            "descricao": "Dados sobre o estoque mundial de urânio por ano",
            "nome_amigavel": "Estoque Acumulado de Urânio por Ano"
        }
    ],
    "Produção (Energia)": [
        {
            "path": "../csvs/Diff_Produção.csv",
            "descricao": "Diferença entre o ano atual e o anterior na produção de energia por país.",
            "nome_amigavel": "Diferença Anual na Produção de Energia"
        }
    ],
    "Reatores Nucleares": [
        {
            "path": "../csvs/Energia_Tipo.csv",
            "descricao": "Predição da produção de GWh/tU por tipo de reator, feito por modelos de Machine Learning.",
            "nome_amigavel": "Predição da Produção de Energia por Tipo de Reator"
        },
        {
            "path": "../csvs/Reatores_Info.csv",
            "descricao": "Informações gerais sobre todos reatores do mundo.",
            "nome_amigavel": "Informações sobre Reatores"
        },
        {
            "path": "../csvs/Reatores_Ano.csv",
            "descricao": "Dados sobre todos reatores e sua produção por ano, estejam eles operando, desativados ou até mesmo apenas planejados.",
            "nome_amigavel": "Reatores por Ano"
        },
        {
            "path": "../csvs/Tempo_Construção_País.csv",
            "descricao": "Média do tempo que um país leva para construir um reator nuclear.",
            "nome_amigavel": "Tempo Médio de Construção de Reator por País"
        },
        {
            "path": "../csvs/Reatores_Finalização.csv",
            "descricao": "Previsão da finalização da construção dos reatores que estão atualmente em construção.",
            "nome_amigavel": "Previsão de Finalização da Construção de Reatores"
        }
    ]
}

st.markdown("Selecione uma categoria abaixo para explorar os dados disponíveis.")

categoria_selecionada = st.selectbox("Escolha uma categoria:", list(categorias.keys()))

# Exibição dos arquivos da categoria selecionada
st.markdown(f"## Arquivos na categoria: {categoria_selecionada}")

for arquivo in categorias[categoria_selecionada]:
    disponibilizar_csv(arquivo["path"], arquivo["descricao"], arquivo["nome_amigavel"])