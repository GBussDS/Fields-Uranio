import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import altair as alt
from urllib.error import URLError
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(
    page_title="Informações dos Reatores",
    page_icon="📋",
)


# Carregando os dados
df = pd.read_csv('../csvs/Reatores_Info.csv')

# Título
st.title("Informações dos Reatores Nucleares")

# Introdução
st.markdown("""
Bem-vindo à página de informações dos reatores nucleares. Aqui você encontrará dados atualizados sobre os reatores nucleares em todo o mundo, incluindo detalhes sobre seu status, tipo, modelo e muito mais.
""")

# Informações gerais dos reatores
st.subheader("Informações Gerais dos Reatores")

status_counts = df['Status'].value_counts()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Reatores", len(df))
col2.metric("Reatores Operando", status_counts.get('Operational', 0))
col3.metric("Reatores em Construção", status_counts.get('Under Construction', 0))
col4.metric("Reatores Desativados", status_counts.get('Permanent Shutdown', 0))

# Seção para visualizar reatores por país
st.subheader("Reatores por País")

st.markdown("""
Nesta seção, você pode filtrar os reatores por país e visualizar informações específicas sobre cada um deles. Selecione um país para começar.
""")

# Filtro por país
paises = df['Country'].unique()
pais_selecionado = st.selectbox("Selecione o País", options=sorted(paises))

df_pais = df[df['Country'] == pais_selecionado]

# Informações específicas do país selecionado
st.subheader(f"Informações dos Reatores em {pais_selecionado}")

status_counts_pais = df_pais['Status'].value_counts()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Reatores", len(df_pais))
col2.metric("Reatores Operando", status_counts_pais.get('Operational', 0))
col3.metric("Reatores em Construção", status_counts_pais.get('Under Construction', 0))
col4.metric("Reatores Desativados", status_counts_pais.get('Permanent Shutdown', 0))

# Capacidade total e média
df_pais['Reference Unit Power (Net Capacity)'] = pd.to_numeric(df_pais['Reference Unit Power (Net Capacity)'], errors='coerce')
capacidade_total = df_pais['Reference Unit Power (Net Capacity)'].sum()
capacidade_media = df_pais['Reference Unit Power (Net Capacity)'].mean()

col1, col2 = st.columns(2)
col1.metric("Capacidade Total (MW)", f"{capacidade_total:.2f}")
col2.metric("Capacidade Média (MW)", f"{capacidade_media:.2f}")

# Gráfico de reatores por status no país selecionado
fig = px.bar(
    x=status_counts_pais.index,
    y=status_counts_pais.values,
    labels={'x': 'Status', 'y': 'Número de Reatores'},
    title=f"Número de Reatores por Status em {pais_selecionado}"
)
st.plotly_chart(fig)

# Lista de reatores com função de pesquisa
st.subheader("Lista de Reatores")

termo_pesquisa = st.text_input("Pesquisar Reator")

if termo_pesquisa:
    df_pais_filtrado = df_pais[df_pais['Name'].str.contains(termo_pesquisa, case=False, na=False)]
else:
    df_pais_filtrado = df_pais

for index, row in df_pais_filtrado.iterrows():
    with st.expander(row['Name']):
        st.write(f"**Nome:** {row['Name']}")
        st.write(f"**País:** {row['Country']}")
        st.write(f"**Status:** {row['Status']}")
        st.write(f"**Tipo de Reator:** {row['Reactor Type']}")
        st.write(f"**Modelo de Reator:** {row['Reactor Model']}")
        st.write(f"**Capacidade de Referência (MW):** {row['Reference Unit Power (Net Capacity)']}")
        st.write(f"**Data de Início de Construção:** {row['Construction Start Date']}")
        st.write(f"**Primeira Conexão à Rede:** {row['First Grid Connection']}")
        st.write(f"**Data de Operação Comercial:** {row['Commercial Operation Date']}")
        st.write(f"**Data de Desativação Permanente:** {row['Permanent Shutdown Date']}")
        st.write(f"**Data de Suspensão de Operação:** {row['Suspended Operation Date']}")
        st.write(f"**Data de Reinício:** {row['Restart Date']}")

# conn = st.connection("gsheets", type=GSheetsConnection)

# @st.cache_data
# def get_info_data():
#     df = conn.read(
#         worksheet="Reatores Info",
#         ttl="10m",
#         usecols=[0,1,2,3,4,5,6,7,8,9,10],
#         ) 
    
#     df['Country'] = df['Country'].astype(str)
#     df['Status'] = df['Status'].astype(str)

#     return df

# st.write("# Informações dos Reatores")

# st.write(
#     """
#     Nessa página você poderá ver oinformações específicas sobre cada reator, 
#     além de análises sobre modelos/tipos de reatores."""
# )

# try:
#     #Filtrando os dados por país:
#     df = get_info_data()

#     data = df.groupby(['Country', 'Status']).size().reset_index(name='Count')
#     data = data.pivot(index='Country', columns='Status', values='Count').fillna(0)

#     operational_counts = df[df['Status'] == 'Operational'].groupby('Country').size()
#     sorted_countries = operational_counts.sort_values(ascending=False).index

#     data = data.loc[sorted_countries]

#     #Gráfico
#     st.write("### Número de reatores por país:")

#     fig, ax = plt.subplots(figsize=(12, 6))
#     data.plot(kind='bar', stacked=True, ax=ax)
#     ax.set_title("Número de Reatores por Status e País")
#     ax.set_xlabel("País")
#     ax.set_ylabel("Contagem")
#     plt.xticks(rotation=45, ha='right', fontsize=8)
#     st.pyplot(fig)

#     #Dados
#     st.write("### Dados usados:", data)

# except URLError as e:
#     st.error(
#         """
#         **Erro ao conectar aos dados online.**
#         Connection error: %s
#     """
#         % e.reason
#     )
    