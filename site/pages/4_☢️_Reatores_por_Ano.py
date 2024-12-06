import streamlit as st
import pandas as pd
import plotly.express as px
from urllib.error import URLError

# Configuração da página (deve ser o primeiro comando)
st.set_page_config(page_title="Reatores por Ano", page_icon="☢️", layout="centered")

# Idiomas disponíveis
idiomas = {"Português": "pt", "English": "en"}
idioma_selecionado = st.sidebar.selectbox("🌐 Escolha o idioma / Select Language:", idiomas.keys())
lang = idiomas[idioma_selecionado]

# Definindo a animação CSS para o efeito de slide da direita para a esquerda
st.markdown("""
    <style>
    /* Aplica o slide-in da direita para a esquerda apenas no conteúdo principal */
    div[data-testid="stAppViewContainer"] > .main .block-container {
        animation: slideInRight 0.5s ease-in-out;
    }

    @keyframes slideInRight {
        0% { transform: translateX(100%); opacity: 0; }
        100% { transform: translateX(0); opacity: 1; }
    }

    /* Reduz a fonte da métrica do país com maior energia */
    .small-font {
        font-size: 0.8em;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_reactor_year_data():
    # Carregar os dados de Reatores_Ano.csv
    file_path = "csvs/Reatores_Ano.csv"
    df_year = pd.read_csv(file_path)
    
    # Garantir que 'Year' seja inteiro e 'Electricity Supplied [GW.h]' seja float
    df_year['Year'] = pd.to_numeric(df_year['Year'], errors='coerce').astype('Int64')
    df_year['Electricity Supplied [GW.h]'] = pd.to_numeric(df_year['Electricity Supplied [GW.h]'], errors='coerce')
    
    return df_year

@st.cache_data
def load_reactor_info():
    # Carregar os dados de Reatores_Info.csv
    file_path = "csvs/Reatores_Info.csv"
    df_info = pd.read_csv(file_path)
    return df_info

# Tradução de títulos e mensagens
if lang == "pt":
    title = "Reatores por Ano"
    description = """
    Nessa página você poderá ver os dados de reatores ao longo do tempo, incluindo a produção de energia mundial e por país.
    Use o controle deslizante para filtrar os anos de interesse e explorar como a produção de energia evoluiu.
    """
    chart_world_title = "Energia Produzida Mundialmente por Ano"
    chart_country_title = "Energia Produzida por País por Ano"
    data_title = "Dados Utilizados:"
    metric_world_title = "Energia Total Mundial (GW.h)"
    metric_top_country_title = "País com Maior Energia"
    energy_unit = "GW.h"
    year_label = "Ano"
    select_country_label = "Selecione um país"
    all_option = "Todos"
    countries_header = "Países com Maior Produção de Energia"
    energy_production_header = "Produção de Energia por País"
else:
    title = "Reactors by Year"
    description = """
    On this page, you can view reactor data over time, including worldwide and country-specific energy production.
    Use the slider to filter the years of interest and explore how energy production has evolved.
    """
    chart_world_title = "Worldwide Energy Produced by Year"
    chart_country_title = "Energy Produced by Country by Year"
    data_title = "Data Used:"
    metric_world_title = "Total Worldwide Energy (GW.h)"
    metric_top_country_title = "Top Energy Producing Country"
    energy_unit = "GW.h"
    year_label = "Year"
    select_country_label = "Select a country"
    all_option = "All"
    countries_header = "Countries with Highest Energy Production"
    energy_production_header = "Energy Production by Country"

# Corpo Principal
st.write(f"# {title}")
st.write(description)

try:
    # Carregar os dados
    df_year = load_reactor_year_data()
    df_info = load_reactor_info()

    # Verificar e tratar possíveis valores faltantes na coluna 'Name'
    df_year = df_year.dropna(subset=['Name'])
    df_info = df_info.dropna(subset=['Name'])

    # Merge dos dataframes em 'Name'
    df_merged = pd.merge(df_year, df_info, on='Name', how='left')

    # Filtragem por anos
    min_year = int(df_merged['Year'].min())
    max_year = int(df_merged['Year'].max())
    years = st.slider(
        "Escolha os anos" if lang == "pt" else "Select years",
        min_year, max_year, (min_year, max_year)
    )

    # Filtrar os dados com base nos anos selecionados
    data_filtered = df_merged[(df_merged['Year'] >= years[0]) & (df_merged['Year'] <= years[1])]

    # Métricas
    total_energy_world = data_filtered['Electricity Supplied [GW.h]'].sum()

    # Energia por país
    energy_by_country = data_filtered.groupby('Country')['Electricity Supplied [GW.h]'].sum().sort_values(ascending=False)

    top_country = energy_by_country.idxmax()
    top_energy = energy_by_country.max()

    if lang == "pt":
        st.subheader("Métricas de Produção de Energia")
    else:
        st.subheader("Energy Production Metrics")

    col1, col2 = st.columns(2)

    # Métrica de energia total mundial
    col1.metric(metric_world_title, f"{total_energy_world:,.2f} {energy_unit}")

    # Métrica de país com maior energia com fonte reduzida
    with col2:
        st.markdown(f"**{metric_top_country_title}:**")
        st.markdown(f"<span class='small-font'>{top_country} ({top_energy:,.2f} {energy_unit})</span>", unsafe_allow_html=True)

    # Gráfico de Energia Mundial usando Plotly Express
    st.write(f"### {chart_world_title}")
    world_energy = data_filtered.groupby('Year')['Electricity Supplied [GW.h]'].sum().reset_index()
    fig_world = px.line(
        world_energy,
        x='Year',
        y='Electricity Supplied [GW.h]',
        markers=True,
        title=chart_world_title
    )
    fig_world.update_layout(
        xaxis_title=year_label,
        yaxis_title=f"{'Energia Produzida' if lang == 'pt' else 'Energy Produced'} ({energy_unit})",
        title=dict(x=0.5)  # Centraliza o título
    )
    st.plotly_chart(fig_world, use_container_width=True)

    # Gráfico de Energia por País usando Plotly Express com seleção de um país
    st.write(f"### {chart_country_title}")
    
    # Obter a lista de países disponíveis
    countries_available = energy_by_country.index.tolist()
    
    # Verificar se 'Brasil' ou 'Brazil' está na lista, dependendo do idioma
    default_country = "Brasil" if lang == "pt" else "Brazil"
    if default_country not in countries_available:
        default_country = all_option

    # Adicionar uma opção para selecionar um país, iniciando com Brasil
    selected_country = st.selectbox(
        select_country_label,
        options=[all_option] + countries_available,
        index= [0] + [i for i, country in enumerate(countries_available) if country == default_country][0:1] if default_country in countries_available else 0
    )
    
    if selected_country != all_option:
        # Filtrar os dados para o país selecionado
        data_country = data_filtered[data_filtered['Country'] == selected_country]
        
        # Garantir que os dados estão no formato correto
        data_country['Year'] = pd.to_numeric(data_country['Year'], errors='coerce').astype('Int64')
        data_country['Electricity Supplied [GW.h]'] = pd.to_numeric(data_country['Electricity Supplied [GW.h]'], errors='coerce')
        
        # Plotar o gráfico para o país selecionado
        fig_country = px.line(
            data_country.groupby('Year')['Electricity Supplied [GW.h]'].sum().reset_index(),
            x='Year',
            y='Electricity Supplied [GW.h]',
            markers=True,
            title=f"{'Energia Produzida em' if lang == 'pt' else 'Energy Produced in'} {selected_country}"
        )
        fig_country.update_layout(
            xaxis_title=year_label,
            yaxis_title=f"{'Energia Produzida' if lang == 'pt' else 'Energy Produced'} ({energy_unit})",
            title=dict(x=0.5)  # Centraliza o título
        )
        st.plotly_chart(fig_country, use_container_width=True)
    else:
        # Se "Todos" for selecionado, mostrar o gráfico original com múltiplos países
        # Limitar a quantidade de países para evitar sobrecarga visual
        top_n = 10
        top_countries = energy_by_country.head(top_n).index.tolist()
        data_top_countries = data_filtered[data_filtered['Country'].isin(top_countries)]
        
        fig_country_all = px.line(
            data_top_countries,
            x='Year',
            y='Electricity Supplied [GW.h]',
            color='Country',
            markers=True,
            title=chart_country_title
        )
        fig_country_all.update_layout(
            xaxis_title=year_label,
            yaxis_title=f"{'Energia Produzida' if lang == 'pt' else 'Energy Produced'} ({energy_unit})",
            legend_title_text='País' if lang == "pt" else 'Country',
            title=dict(x=0.5)  # Centraliza o título
        )
        st.plotly_chart(fig_country_all, use_container_width=True)

    # Dados utilizados
    st.write(f"### {data_title}")
    with st.expander("📄"):
        st.write("**Reatores por Ano:**")
        st.dataframe(data_filtered[['Name', 'Year', 'Electricity Supplied [GW.h]', 'Country']].sort_values(by=['Year', 'Country']))
        st.write("**Informações dos Reatores:**")
        st.dataframe(df_info)

except URLError as e:
    st.error(f"**Erro ao carregar os dados.**\nDetalhes do erro: {e.reason}")
except FileNotFoundError as e:
    if lang == "pt":
        st.error(f"**Erro:** Arquivo não encontrado.\nDetalhes: {e}")
    else:
        st.error(f"**Error:** File not found.\nDetails: {e}")
except Exception as e:
    if lang == "pt":
        st.error(f"**Erro inesperado:** {e}")
    else:
        st.error(f"**Unexpected error:** {e}")

# Seção adicional: Energia por País
st.markdown("---")
if lang == "pt":
    st.header("Energia por País")
    search_label = "Pesquisar País"
else:
    st.header("Energy by Country")
    search_label = "Search Country"

search_term = st.text_input(search_label)

if search_term:
    df_country_filtered = energy_by_country[energy_by_country.index.str.contains(search_term, case=False, na=False)]
else:
    df_country_filtered = energy_by_country

st.write("### " + (countries_header if lang == "pt" else "Countries with Highest Energy Production"))

st.dataframe(df_country_filtered.reset_index().rename(columns={
    'Country': ('País' if lang == "pt" else 'Country'),
    'Electricity Supplied [GW.h]': ('Energia Produzida [GW.h]' if lang == "pt" else 'Electricity Supplied [GW.h]')
}))

# Opcional: Gráfico de Barras da Energia por País
st.write("### " + (energy_production_header if lang == "pt" else "Energy Production by Country"))

fig_bar_country = px.bar(
    df_country_filtered.reset_index(),
    x='Country',
    y='Electricity Supplied [GW.h]',
    labels={
        'Country': ('País' if lang == "pt" else 'Country'),
        'Electricity Supplied [GW.h]': ('Energia Produzida [GW.h]' if lang == "pt" else 'Electricity Supplied [GW.h]')
    },
    title=(energy_production_header if lang == "pt" else 'Energy Production by Country'),
    text='Electricity Supplied [GW.h]'
)
fig_bar_country.update_layout(
    xaxis_title=('País' if lang == "pt" else 'Country'),
    yaxis_title=(f"{'Energia Produzida' if lang == 'pt' else 'Energy Produced'} ({energy_unit})"),
    title=dict(x=0.5)  # Centraliza o título
)
st.plotly_chart(fig_bar_country, use_container_width=True)
