import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
)

st.markdown("<h1 style='text-align: center; font-size: 3em;'>Central de Dados e Visualizações sobre Urânio</h1>", unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center; font-size: 2em; color: gray;'>Projeto para o Field Project da FGV - Rio</h3>", unsafe_allow_html=True)

st.markdown(
    """
    Olá, seja bem vindo ao nosso site! 👋 
    Esse site em Streamlit tem como objetivo facilitar o acesso a dados e visualizações sobre o mercado do Urânio 
    para pesquisadores e usuários comuns, onde todos os dados adquiridos durante o projeto estarão disponíveis para
    download, com também gráficos interativos para você, usuário, poder utilizar para sua pesquisa.
    
    Somos um grupo de 4 estudantes do curso de **Ciência de Dados e Inteligência Artificial** na **Fundação Getúlio Vargas (FGV)**,
    localizada no Rio de Janeiro, Brasil. O projeto foi desenvolvido para o Field Project, projeto que visa à articulação teoria 
    e prática, oportunizando o contato dos alunos com desafios concretos do mercado de trabalho, onde aplicamos modelos teóricos 
    aprendidos nas aulas para o desenvolvimento de produtos e a proposição de soluções.

    ### Sobre o projeto:
    - Nosso objetivo principal é **facilitar o acesso a dados sobre urânio**, já que encontramos muita dificuldade durante
    nossa pesquisa.
    - Observamos uma carência de sites e papers que ofereciam essa informação de maneira simples e interativa, e, a partir
    disso, tivemos a ideia de poder, através de nossa pesquisa, mudar isso, criando um **recurso acessível e interativo**.

    ### O que você encontrará aqui:
    - **Dados abrangentes sobre o urânio**, como produção, exportações/importações, demanda e preços históricos.
    - **Visualizações interativas**, que ajudam a entender tendências e padrões do mercado de urânio.
    - **Previsões e análises detalhadas**, baseadas em dados de fontes confiáveis como PRIS, World Nuclear Association 
      e OECD, para compreender o impacto e a importância do urânio no cenário global.

    **👈 Use a aba lateral para navegar** pelas diferentes páginas do site e explorar tópicos específicos!

    ### Também veja:
    - Nosso [github](https://github.com);
    - Faça perguntas no nosso [email](mailto:fields.uranio@gmail.com).
    """
)
