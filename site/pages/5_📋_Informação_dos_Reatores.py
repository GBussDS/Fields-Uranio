import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import matplotlib
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Informações dos Reatores", page_icon="📋")

# Idiomas disponíveis
idiomas = {"Português": "pt", "English": "en"}
idioma_selecionado = st.sidebar.selectbox("🌐 Escolha o idioma / Select Language:", idiomas.keys())
lang = idiomas[idioma_selecionado]

if lang == 'pt':
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

    # Função para carregar os dados e aplicar o cache
    @st.cache_data
    def load_data():
        # Carregar os dados dos reatores
        df = pd.read_csv('csvs/Reatores_Info.csv')
        
        # Carregar os dados de contagem de reatores por país
        reactor_counts_by_country = pd.read_csv('csvs/Outros/Country_Count_Location.csv')
        
        return df, reactor_counts_by_country

    # Carregar dados com cache
    df, reactor_counts_by_country = load_data()

    # Título
    st.title("Informações dos Reatores Nucleares")

    # Introdução
    st.markdown("""Bem-vindo à página de informações dos reatores nucleares. Aqui você encontrará dados atualizados sobre os reatores nucleares em todo o mundo, incluindo detalhes sobre seu status, tipo, modelo e muito mais.""")

    # Informações gerais dos reatores
    st.subheader("Informações Gerais dos Reatores")

    status_counts = df['Status'].value_counts()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de Reatores", len(df))
    col2.metric("Reatores Operando", status_counts.get('Operational', 0))
    col3.metric("Reatores em Construção", status_counts.get('Under Construction', 0))
    col4.metric("Reatores Desativados", status_counts.get('Permanent Shutdown', 0))

    # Mapa interativo
    st.subheader("Reatores por País")

    # Normalizar os valores para criar a escala de cores
    norm = matplotlib.colors.Normalize(vmin=reactor_counts_by_country['Reactor Count'].min(),
                                    vmax=reactor_counts_by_country['Reactor Count'].max())

    custom_cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
        'greenRed',  # Nome do colormap
        ['#03ff12', '#ff0000']  # Cores: Amarelo forte para vermelho
    )

    # Escolher uma paleta de cores de dois tons (verde-vermelho)
    colormap = matplotlib.cm.ScalarMappable(norm=norm, cmap=custom_cmap)

    # Criar o mapa base
    m = folium.Map(location=[20, 0], zoom_start=2, tiles="cartodbpositron")

    # Adicionar marcadores circulares para cada país
    for _, row in reactor_counts_by_country.iterrows():
        color = matplotlib.colors.to_hex(colormap.to_rgba(row['Reactor Count']))
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=8,  # Tamanho fixo dos marcadores
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.9,
            popup=f"{row['Country']}: {row['Reactor Count']} Reatores",
            tooltip=f"{row['Country']}: {row['Reactor Count']} Reatores"
        ).add_to(m)

    # Criar uma legenda para o mapa
    colormap._A = []
    legend_html = f"""
    <div style="position: fixed;
                bottom: 50px; left: 50px; width: 200px; height: 90px; 
                background-color: white; border:2px solid grey; z-index:9999; font-size:14px;
                padding: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.3);">
        <b>Legenda: Contagem de Reatores</b><br>
        <i style="background: {matplotlib.colors.to_hex(colormap.to_rgba(norm.vmin))};width:15px;height:15px;display:inline-block;"></i>
        Baixo<br>
        <i style="background: {matplotlib.colors.to_hex(colormap.to_rgba(norm.vmax))};width:15px;height:15px;display:inline-block;"></i>
        Alto
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    # Mostrar o mapa no Streamlit com tamanho especificado
    st_folium(m, width=700, height=500)

    # Filtro por país
    st.markdown("""Nesta seção, você pode filtrar os reatores por país e visualizar informações específicas sobre cada um deles. Selecione um país para começar.""")

    paises = reactor_counts_by_country['Country'].unique()
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
    df_pais.loc[:, 'Reference Unit Power (Net Capacity)'] = pd.to_numeric(df_pais['Reference Unit Power (Net Capacity)'], errors='coerce')

    capacidade_total = df_pais['Reference Unit Power (Net Capacity)'].sum()
    capacidade_media = df_pais['Reference Unit Power (Net Capacity)'].mean()

    col1, col2 = st.columns(2)
    col1.metric("Capacidade Total (MW)", f"{capacidade_total:.2f}")
    col2.metric("Capacidade Média (MW)", f"{capacidade_media:.2f}")

    # Gráfico de barras de reatores por status
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
else: 
    # Defining the CSS animation for the slide effect from right to left
    st.markdown("""
        <style>
        /* Applies the slide-in from right to left only to the main content */
        div[data-testid="stMainBlockContainer"] > div {
            animation: slideInRight 0.5s ease-in-out;
        }

        @keyframes slideInRight {
            0% { transform: translateX(100%); opacity: 0; }
            100% { transform: translateX(0); opacity: 1; }
        }
        </style>
        """, unsafe_allow_html=True)

    # Function to load data and apply caching
    @st.cache_data
    def load_data():
        # Load reactor data
        df = pd.read_csv('csvs/Reatores_Info.csv')
        
        # Load reactor count data by country
        reactor_counts_by_country = pd.read_csv('csvs/Outros/Country_Count_Location.csv')
        
        return df, reactor_counts_by_country

    # Load data with caching
    df, reactor_counts_by_country = load_data()

    # Title
    st.title("Nuclear Reactor Information")

    # Introduction
    st.markdown("""Welcome to the nuclear reactor information page. Here you will find up-to-date data on nuclear reactors worldwide, including details about their status, type, model, and much more.""")

    # General reactor information
    st.subheader("General Reactor Information")

    status_counts = df['Status'].value_counts()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Reactors", len(df))
    col2.metric("Operational Reactors", status_counts.get('Operational', 0))
    col3.metric("Reactors Under Construction", status_counts.get('Under Construction', 0))
    col4.metric("Shut Down Reactors", status_counts.get('Permanent Shutdown', 0))

    # Interactive map
    st.subheader("Reactors by Country")

    # Normalize the values to create the color scale
    norm = matplotlib.colors.Normalize(vmin=reactor_counts_by_country['Reactor Count'].min(),
                                    vmax=reactor_counts_by_country['Reactor Count'].max())

    custom_cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
        'greenRed',  # Name of the colormap
        ['#03ff12', '#ff0000']  # Colors: Bright green to red
    )

    # Choose a two-tone color palette (green-red)
    colormap = matplotlib.cm.ScalarMappable(norm=norm, cmap=custom_cmap)

    # Create the base map
    m = folium.Map(location=[20, 0], zoom_start=2, tiles="cartodbpositron")

    # Add circular markers for each country
    for _, row in reactor_counts_by_country.iterrows():
        color = matplotlib.colors.to_hex(colormap.to_rgba(row['Reactor Count']))
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=8,  # Fixed size of markers
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.9,
            popup=f"{row['Country']}: {row['Reactor Count']} Reactors",
            tooltip=f"{row['Country']}: {row['Reactor Count']} Reactors"
        ).add_to(m)

    # Create a legend for the map
    colormap._A = []
    legend_html = f"""
    <div style="position: fixed;
                bottom: 50px; left: 50px; width: 200px; height: 90px; 
                background-color: white; border:2px solid grey; z-index:9999; font-size:14px;
                padding: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.3);">
        <b>Legend: Reactor Count</b><br>
        <i style="background: {matplotlib.colors.to_hex(colormap.to_rgba(norm.vmin))};width:15px;height:15px;display:inline-block;"></i>
        Low<br>
        <i style="background: {matplotlib.colors.to_hex(colormap.to_rgba(norm.vmax))};width:15px;height:15px;display:inline-block;"></i>
        High
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    # Display the map in Streamlit with specified size
    st_folium(m, width=700, height=500)

    # Country filter
    st.markdown("""In this section, you can filter reactors by country and view specific information about each one. Select a country to start.""")
    countries = reactor_counts_by_country['Country'].unique()
    selected_country = st.selectbox("Select Country", options=sorted(countries))

    df_country = df[df['Country'] == selected_country]

    # Specific information for the selected country
    st.subheader(f"Reactor Information in {selected_country}")

    status_counts_country = df_country['Status'].value_counts()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Reactors", len(df_country))
    col2.metric("Operational Reactors", status_counts_country.get('Operational', 0))
    col3.metric("Reactors Under Construction", status_counts_country.get('Under Construction', 0))
    col4.metric("Shut Down Reactors", status_counts_country.get('Permanent Shutdown', 0))

    # Total and average capacity
    df_country.loc[:, 'Reference Unit Power (Net Capacity)'] = pd.to_numeric(df_country['Reference Unit Power (Net Capacity)'], errors='coerce')

    total_capacity = df_country['Reference Unit Power (Net Capacity)'].sum()
    average_capacity = df_country['Reference Unit Power (Net Capacity)'].mean()

    col1, col2 = st.columns(2)
    col1.metric("Total Capacity (MW)", f"{total_capacity:.2f}")
    col2.metric("Average Capacity (MW)", f"{average_capacity:.2f}")

    # Bar chart of reactors by status
    fig = px.bar(
        x=status_counts_country.index,
        y=status_counts_country.values,
        labels={'x': 'Status', 'y': 'Number of Reactors'},
        title=f"Number of Reactors by Status in {selected_country}"
    )
    st.plotly_chart(fig)

    # Reactor list with search functionality
    st.subheader("Reactor List")

    search_term = st.text_input("Search Reactor")

    if search_term:
        df_country_filtered = df_country[df_country['Name'].str.contains(search_term, case=False, na=False)]
    else:
        df_country_filtered = df_country

    for index, row in df_country_filtered.iterrows():
        with st.expander(row['Name']):
            st.write(f"**Name:** {row['Name']}")
            st.write(f"**Country:** {row['Country']}")
            st.write(f"**Status:** {row['Status']}")
            st.write(f"**Reactor Type:** {row['Reactor Type']}")
            st.write(f"**Reactor Model:** {row['Reactor Model']}")
            st.write(f"**Reference Capacity (MW):** {row['Reference Unit Power (Net Capacity)']}")
            st.write(f"**Construction Start Date:** {row['Construction Start Date']}")
            st.write(f"**First Grid Connection:** {row['First Grid Connection']}")
            st.write(f"**Commercial Operation Date:** {row['Commercial Operation Date']}")
            st.write(f"**Permanent Shutdown Date:** {row['Permanent Shutdown Date']}")
            st.write(f"**Suspended Operation Date:** {row['Suspended Operation Date']}")
            st.write(f"**Restart Date:** {row['Restart Date']}")
