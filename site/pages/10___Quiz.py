import streamlit as st

# Configuração da página
st.set_page_config(page_title="Quiz - Produção de Urânio", page_icon="🧑‍🏫")

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

    /* Customização das bordas */
    .correct {
        border: 3px solid green !important;
        background-color: #e0ffe0;
    }

    .incorrect {
        border: 3px solid red !important;
        background-color: #ffe0e0;
    }
    </style>
    """, unsafe_allow_html=True)

# Título da página
st.write("# Quiz sobre Produção de Urânio")
st.write("### Pergunta: Qual país mais produz urânio?")

# Alternativas
options = ["Brasil", "China", "Cazaquistão", "EUA"]
correct_answer = "Cazaquistão"

# Variáveis de estado
if 'answered' not in st.session_state:
    st.session_state.answered = False
    st.session_state.selected_option = None

# Função para gerenciar a interação com as alternativas
def highlight_answer(option):
    # Se a resposta já foi selecionada, destacar a correta ou incorreta
    if st.session_state.answered:
        if option == correct_answer:
            return 'correct'
        else:
            return 'incorrect'
    return ''

# Dividir as alternativas em duas colunas
col1, col2 = st.columns(2)

with col1:
    for option in options[:2]:
        selected = st.button(option, key=option, help=f"Escolha {option}")
        if selected and not st.session_state.answered:
            st.session_state.selected_option = option
            st.session_state.answered = True
            st.experimental_rerun()

with col2:
    for option in options[2:]:
        selected = st.button(option, key=option, help=f"Escolha {option}")
        if selected and not st.session_state.answered:
            st.session_state.selected_option = option
            st.session_state.answered = True
            st.experimental_rerun()

# Mostrar a resposta correta ou incorreta após a seleção
if st.session_state.answered:
    st.write(f"**Você escolheu:** {st.session_state.selected_option}")
    if st.session_state.selected_option == correct_answer:
        st.success("Resposta correta! O Cazaquistão é o maior produtor de urânio.")
    else:
        st.error("Resposta incorreta. Tente novamente!")
    
    st.markdown(f"""
        <style>
        .stButton > button[data-baseweb="button"] {{
            border: 3px solid transparent;
            padding: 10px 20px;
            margin: 10px 0;
            border-radius: 5px;
            font-size: 16px;
        }}
        .stButton > button[data-baseweb="button"].correct {{
            border: 3px solid green;
            background-color: #e0ffe0;
        }}
        .stButton > button[data-baseweb="button"].incorrect {{
            border: 3px solid red;
            background-color: #ffe0e0;
        }}
        </style>
    """, unsafe_allow_html=True)

# Atualizar as alternativas para destacá-las com as bordas após a seleção
col1, col2 = st.columns(2)

with col1:
    for option in options[:2]:
        button_class = highlight_answer(option)
        st.markdown(f'<button class="stButton {button_class}">{option}</button>', unsafe_allow_html=True)

with col2:
    for option in options[2:]:
        button_class = highlight_answer(option)
        st.markdown(f'<button class="stButton {button_class}">{option}</button>', unsafe_allow_html=True)
