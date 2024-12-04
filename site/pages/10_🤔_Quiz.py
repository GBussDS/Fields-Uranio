import streamlit as st

# Configuração da página
st.set_page_config(page_title="Quiz sobre Urânio", page_icon="🤔")

# Dicionário de idiomas
idiomas = {"Português": "pt", "English": "en"}
idioma_selecionado = st.sidebar.selectbox("🌐 Escolha o idioma / Select Language:", idiomas.keys())
lang = idiomas[idioma_selecionado]

# Textos em ambos os idiomas
textos = {
    "pt": {
        "title": "🎉 Bem-vindo ao Quiz sobre Urânio! 🤔",
        "intro": "Você sabia que o urânio não é apenas uma matéria-prima para energia nuclear, mas também tem um impacto global? 🌍 É a energia do futuro chegando, cada vez mais próxima de eu e você! Veja se você aprendeu alguma coisa com nosso dashboard 🚀",
        "instructions": "Você vai encontrar algumas perguntas divertidas e desafiadoras sobre o urânio e o mundo da energia nuclear. Aproveite para ler todas as páginas antes de responder o quiz! 🌱🌐",
        "hint": "Dica importante: para responder corretamente, você precisa clicar DUAS vezes: 1️⃣ Clique em uma opção para selecionar a resposta; 2️⃣ Em seguida, clique novamente para confirmá-la!",
        "correct": "Resposta correta!",
        "incorrect": "Resposta incorreta. A resposta correta é:",
        "selected": "Você escolheu:",
        "final_score": "### Você acertou {correct_answers} de {total_questions} perguntas!",
        "all_correct": "Parabéns! Você acertou todas as perguntas! 🎉 Muito obrigado por ler nosso dashboard com carinho!",
        "most_correct": "Ótimo! Você acertou a maioria das questões. Obrigado por ler nosso dashboard!",
        "few_correct": "Opa, você errou algumas! Sem problemas, continue aprendendo e olhe mais páginas! 💪"
    },
    "en": {
        "title": "🎉 Welcome to the Uranium Quiz! 🤔",
        "intro": "Did you know that uranium is not only a raw material for nuclear energy but also has a global impact? 🌍 It's the energy of the future coming closer and closer! Test your knowledge with our dashboard quiz 🚀",
        "instructions": "You'll find some fun and challenging questions about uranium and the world of nuclear energy. Make sure to read all the dashboard pages before taking the quiz! 🌱🌐",
        "hint": "Important tip: To answer correctly, you need to click TWICE: 1️⃣ Click an option to select your answer; 2️⃣ Then click again to confirm it!",
        "correct": "Correct answer!",
        "incorrect": "Incorrect answer. The correct answer is:",
        "selected": "You chose:",
        "final_score": "### You got {correct_answers} out of {total_questions} questions right!",
        "all_correct": "Congratulations! You got all the questions right! 🎉 Thank you for carefully reading our dashboard!",
        "most_correct": "Great! You got most of the questions right. Thanks for reading our dashboard!",
        "few_correct": "Oops, you missed a few! No worries, keep learning and check out more pages! 💪"
    }
}

# Definindo a animação CSS
st.markdown("""
    <style>
    div[data-testid="stMainBlockContainer"] > div {
        animation: slideInRight 0.5s ease-in-out;
    }

    @keyframes slideInRight {
        0% { transform: translateX(100%); opacity: 0; }
        100% { transform: translateX(0); opacity: 1; }
    }

    .correct {
        border: 3px solid green !important;
        background-color: #e0ffe0;
    }

    .incorrect {
        border: 3px solid red !important;
        background-color: #ffe0e0;
    }

    .stButton {
        width: 100% !important;
        padding: 20px 0;
        font-size: 18px !important;
        text-align: center !important;
        display: block;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Função para criar a pergunta
def createQuestion(question, options, rightOne, question_index):
    if f'answered_{question_index}' not in st.session_state:
        st.session_state[f'answered_{question_index}'] = False
        st.session_state[f'selected_option_{question_index}'] = None
        st.session_state[f'correct_answers_{question_index}'] = 0

    def highlight_answer(option, idx):
        if st.session_state[f'answered_{question_index}']:
            if option == options[rightOne]:
                return 'correct'
            else:
                return 'incorrect'
        return ''

    st.write(f"### {question}")
    col1, col2 = st.columns(2)
    question_answered = st.session_state[f'answered_{question_index}']
    
    with col1:
        for i in range(2):
            option = options[i]
            if question_answered:
                button_class = highlight_answer(option, i)
                st.markdown(f'<button class="stButton {button_class}" disabled>{option}</button>', unsafe_allow_html=True)
            else:
                selected = st.button(option, key=f"{question_index}-{i}-{option}")
                if selected and not question_answered:
                    st.session_state[f'selected_option_{question_index}'] = option
                    st.session_state[f'answered_{question_index}'] = True
                    if i == rightOne:
                        st.session_state[f'correct_answers_{question_index}'] += 1

    with col2:
        for i in range(2, 4):
            option = options[i]
            if question_answered:
                button_class = highlight_answer(option, i)
                st.markdown(f'<button class="stButton {button_class}" disabled>{option}</button>', unsafe_allow_html=True)
            else:
                selected = st.button(option, key=f"{question_index}-{i}-{option}")
                if selected and not question_answered:
                    st.session_state[f'selected_option_{question_index}'] = option
                    st.session_state[f'answered_{question_index}'] = True
                    if i == rightOne:
                        st.session_state[f'correct_answers_{question_index}'] += 1

    if question_answered:
        st.write(f"**{textos[lang]['selected']}** {st.session_state[f'selected_option_{question_index}']}")
        if st.session_state[f'selected_option_{question_index}'] == options[rightOne]:
            st.success(textos[lang]["correct"])
        else:
            st.error(f"{textos[lang]['incorrect']} {options[rightOne]}")

# Perguntas em português e inglês
questions = {
    "pt": [
        ("Qual país que mais produziu urânio nos últimos 10 anos?", ["Cazaquistão", "Brasil", "Austrália", "China"], 0),
        ("Quanto de estoque acumulado de urânio temos disponível?", ["1 milhão Ton.", "200 mil Ton.", "5 milhões Ton.", "500 mil Ton."], 3),
        ("Qual país tem mais reatores nucleares?", ["Estados Unidos", "Rússia", "Canadá", "Japão"], 0),
        ("Qual desses países não possui usinas nucleares?", ["Argentina", "Austrália", "Cazaquistão", "México"], 1),
        ("O urânio atingiu seu pico de preço em 2007, custando ___ dólares por libra.", ["100", "240", "70", "140"], 3),
        ("Qual país está crescendo rapidamente em demanda de urânio?", ["Japão", "China", "Alemanha", "Brasil"], 1),
        ("Qual dos países abaixo possui maior demanda atualmente?", ["Canadá", "Japão", "Coreia do Sul", "Inglaterra"], 2)
    ],
    "en": [
        ("Which country produced the most uranium in the last 10 years?", ["Kazakhstan", "Brazil", "Australia", "China"], 0),
        ("How much accumulated uranium stock do we currently have?", ["1 million tons", "200k tons", "5 million tons", "500k tons"], 3),
        ("Which country has the most nuclear reactors?", ["United States", "Russia", "Canada", "Japan"], 0),
        ("Which of these countries does not have nuclear power plants?", ["Argentina", "Australia", "Kazakhstan", "Mexico"], 1),
        ("Uranium peaked in price in 2007, costing ___ dollars per pound.", ["100", "240", "70", "140"], 3),
        ("Which country is rapidly increasing its demand for uranium?", ["Japan", "China", "Germany", "Brazil"], 1),
        ("Which of the following countries currently has the highest uranium demand?", ["Canada", "Japan", "South Korea", "England"], 2)
    ]
}

st.markdown(f"""
    <h2 style="text-align:center; color: #2e8b57;">{textos[lang]["title"]}</h2>
    <p style="font-size:18px; text-align:center;">{textos[lang]["intro"]}</p>
    <p style="font-size:18px; text-align:center;">{textos[lang]["intro"]}</p>
    <p style="font-size:18px; text-align:center;">{textos[lang]["instructions"]}</p>
    <p style="font-size:18px; text-align:center; color: #ff4500;">{textos[lang]["hint"]}</p>
""", unsafe_allow_html=True)

# Exibindo as perguntas
for idx, (question, options, rightOne) in enumerate(questions[lang]):
    createQuestion(question, options, rightOne, idx)

# Mostrar o resultado final
total_questions = len(questions[lang])
correct_answers = sum([st.session_state.get(f'correct_answers_{i}', 0) for i in range(total_questions)])

# Verificar se todas as perguntas foram respondidas
if all(st.session_state.get(f'answered_{i}', False) for i in range(total_questions)):
    st.write(f"{textos[lang]['final_score'].format(correct_answers=correct_answers, total_questions=total_questions)}")

    # Exibir uma mensagem baseada na quantidade de acertos
    if correct_answers == total_questions:
        st.success(textos[lang]["all_correct"])
    elif correct_answers >= total_questions // 2:
        st.success(textos[lang]["most_correct"])
    else:
        st.warning(textos[lang]["few_correct"])
