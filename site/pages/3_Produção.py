import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Produção de Urânio por Ano",
    page_icon="☢️",
)

# Carregar os dados do CSV
@st.cache_data
def get_uranium_data():
    file_path = "../csvs/Produção/UraniumProductionHistorical.csv"  # caminho relativo ao script do Streamlit
    df = pd.read_csv(file_path, index_col="Country")
    return df

# Corpo da página
st.write("# Produção de Urânio por Ano")

st.write(
    """
    Nesta página, você pode explorar a produção anual de urânio por país, de 1998 a 2022. A visualização abaixo 
    mostra a quantidade de urânio produzido em toneladas (tU) ao longo dos anos.
    """
)

# Obter os dados
df = get_uranium_data()

# Selecionar o intervalo de anos
anos = list(map(int, df.columns))
years = st.slider("Escolha o intervalo de anos", min(anos), max(anos), (min(anos), max(anos)))

# Filtrar dados por ano selecionado
filtered_df = df.loc[:, str(years[0]):str(years[1])]

# Configurar e criar o gráfico com Seaborn
st.write("### Produção Anual de Urânio por País")

fig, ax = plt.subplots(figsize=(14, 8))
sns.lineplot(data=filtered_df.T, dashes=False, ax=ax)
ax.set_xlabel("Ano")
ax.set_ylabel("Produção de Urânio (tU)")
ax.set_title("Produção Anual de Urânio por País ({} - {})".format(years[0], years[1]))

# Exibir o gráfico
st.pyplot(fig)

# Exibir dados usados
st.write("### Dados usados:")
st.dataframe(filtered_df.T)  # Transposto para facilitar visualização por ano
