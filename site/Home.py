import streamlit as st

# Configuração inicial da página
st.set_page_config(
    page_title="Home",
    page_icon="🏠",
)

# Função para retornar textos com base no idioma
def get_translations(language):
    translations = {
        "pt": {
            "title": "Central de Dados e Visualizações sobre Urânio",
            "subtitle": "Projeto para o Field Project da FGV - Rio",
            "welcome": "Olá, seja bem-vindo ao nosso site! 👋",
            "about_project": "Sobre o projeto:",
            "objective": "Nosso objetivo principal é **facilitar o acesso a dados sobre urânio**, já que encontramos muita dificuldade durante nossa pesquisa.",
            "features": "O que você encontrará aqui:",
            "feature_1": "- **Dados abrangentes sobre o urânio**, como produção, exportações/importações, demanda e preços históricos.",
            "feature_2": "- **Visualizações interativas**, que ajudam a entender tendências e padrões do mercado de urânio.",
            "feature_3": "- **Previsões e análises detalhadas**, baseadas em dados de fontes confiáveis como PRIS, World Nuclear Association e OECD, para compreender o impacto e a importância do urânio no cenário global.",
            "use_sidebar": "**👈 Use a aba lateral para navegar** pelas diferentes páginas do site e explorar tópicos específicos!",
            "github": "Nosso [github](https://github.com);",
            "email": "Faça perguntas no nosso [email](mailto:fields.uranio@gmail.com).",
        },
        "en": {
            "title": "Uranium Data and Visualization Hub",
            "subtitle": "Project for the FGV Field Project - Rio",
            "welcome": "Hello, welcome to our website! 👋",
            "about_project": "About the project:",
            "objective": "Our main goal is to **facilitate access to uranium data**, as we faced many difficulties during our research.",
            "features": "What you will find here:",
            "feature_1": "- **Comprehensive data on uranium**, such as production, exports/imports, demand, and historical prices.",
            "feature_2": "- **Interactive visualizations**, helping to understand trends and patterns in the uranium market.",
            "feature_3": "- **Forecasts and detailed analyses**, based on data from reliable sources like PRIS, the World Nuclear Association, and OECD, to understand uranium's global impact and importance.",
            "use_sidebar": "**👈 Use the sidebar to navigate** through different pages of the site and explore specific topics!",
            "github": "Our [github](https://github.com);",
            "email": "Ask questions via [email](mailto:fields.uranio@gmail.com).",
        },
    }
    return translations[language]

# Adicionar seletor de idioma
language = st.sidebar.selectbox("🌐 Escolha o idioma / Select Language:", ["Português", "English"])
lang_code = "pt" if language == "Português" else "en"
texts = get_translations(lang_code)

# Estilos e Títulos
st.markdown("""
    <style>
    .stApp {
        animation: fadeIn 0.5s ease-in-out;
    }
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown(f"<h1 style='text-align: center; font-size: 3em;'>{texts['title']}</h1>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align: center; font-size: 2em; color: gray;'>{texts['subtitle']}</h3>", unsafe_allow_html=True)

# Conteúdo principal
st.markdown(f"{texts['welcome']}")
st.markdown(f"### {texts['about_project']}")
st.markdown(f"{texts['objective']}")

st.markdown(f"### {texts['features']}")
st.markdown(f"{texts['feature_1']}")
st.markdown(f"{texts['feature_2']}")
st.markdown(f"{texts['feature_3']}")

st.markdown(f"{texts['use_sidebar']}")
st.markdown(f"{texts['github']}")
st.markdown(f"{texts['email']}")
