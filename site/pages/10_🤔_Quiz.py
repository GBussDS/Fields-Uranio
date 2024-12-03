import streamlit as st

# Configuração da página
st.set_page_config(page_title="Quiz sobre Urânio", page_icon="🤔")

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

    /* Estilo para os botões */
    .stButton {
        width: 100% !important; /* Todos os botões terão a mesma largura */
        padding: 20px 0; /* Ajuste do padding para aumentar o tamanho vertical */
        font-size: 18px !important; /* Aumentando o tamanho da fonte */
        text-align: center !important; /* Centralizando o texto */
        display: block; /* Garantindo que o botão ocupe a largura completa */
        border-radius: 8px; /* Bordas arredondadas para os botões */
        margin-bottom: 10px; /* Espaçamento entre os botões */
    }
    </style>
""", unsafe_allow_html=True)

# Função para criar a pergunta
def createQuestion(question, options, rightOne, question_index):
    # Inicializando o estado da pergunta
    if f'answered_{question_index}' not in st.session_state:
        st.session_state[f'answered_{question_index}'] = False  # Se já respondeu
        st.session_state[f'selected_option_{question_index}'] = None  # Resposta selecionada
        st.session_state[f'correct_answers_{question_index}'] = 0  # Contador de acertos

    # Função para gerenciar a interação com as alternativas
    def highlight_answer(option, idx):
        if st.session_state[f'answered_{question_index}']:
            if option == options[rightOne]:
                return 'correct'
            else:
                return 'incorrect'
        return ''  # Caso ainda não tenha sido respondido, não aplica estilo

    st.write(f"### {question}")
    
    # Dividir as alternativas em duas colunas
    col1, col2 = st.columns(2)

    # Variável para controlar se a pergunta já foi respondida
    question_answered = st.session_state[f'answered_{question_index}']
    
    with col1:
        for i in range(2):
            option = options[i]
            if question_answered:  # Se a pergunta foi respondida
                button_class = highlight_answer(option, i)
                st.markdown(f'<button class="stButton {button_class}" disabled>{option}</button>', unsafe_allow_html=True)
            else:
                selected = st.button(option, key=f"{question_index}-{i}-{option}")
                if selected and not question_answered:
                    st.session_state[f'selected_option_{question_index}'] = option
                    st.session_state[f'answered_{question_index}'] = True
                    # Se a opção for correta, incrementar o contador de acertos
                    if i == rightOne:
                        st.session_state[f'correct_answers_{question_index}'] += 1

    with col2:
        for i in range(2, 4):
            option = options[i]
            if question_answered:  # Se a pergunta foi respondida
                button_class = highlight_answer(option, i)
                st.markdown(f'<button class="stButton {button_class}" disabled>{option}</button>', unsafe_allow_html=True)
            else:
                selected = st.button(option, key=f"{question_index}-{i}-{option}")
                if selected and not question_answered:
                    st.session_state[f'selected_option_{question_index}'] = option
                    st.session_state[f'answered_{question_index}'] = True
                    # Se a opção for correta, incrementar o contador de acertos
                    if i == rightOne:
                        st.session_state[f'correct_answers_{question_index}'] += 1

    # Mostrar a resposta correta ou incorreta imediatamente após a seleção
    if question_answered:
        st.write(f"**Você escolheu:** {st.session_state[f'selected_option_{question_index}']}")
        if st.session_state[f'selected_option_{question_index}'] == options[rightOne]:
            st.success("Resposta correta!")
        else:
            st.error(f"Resposta incorreta. A resposta correta é: {options[rightOne]}")



# Lista de perguntas e respostas
questions = [
    ("Qual país que mais produziu urânio nos últimos 10 anos?", ["Cazaquistão", "Brasil", "Austrália", "China"], 0),
    ("Quanto de estoque acumulado de urânio (aproximadamente) temos disponível no momento?", ["1 milhão Ton.", "200 mil Ton.", "5 milhões Ton.", "500 mil Ton."], 3),
    ("Qual o país que mais possui reatores nucleares?", ["Estados Unidos", "Rússia", "Canadá", "Japão"], 0),
    ("Qual destes países não possui usinas nucleares?", ["Argentina", "Austrália", "Cazaquistão", "México"], 1),
    ("O urânio atingiu seu pico de preço em 2007, quando chegou a custar aproximadamente ___ dólares por libra. Complete a frase.", ["100", "240", "70", "140"], 3),
    ("Qual dos países abaixo está crescendo o número de reatores rapidamente e teve mais que dobrada sua demanda por urânio nos últimos 10 anos?", ["Japão", "China", "Alemanha", "Brasil"], 1),
    ("Qual dos países dentre os quatro abaixo possui maior demanda de urânio atualmente?", ["Canadá", "Japão", "Coréia do Sul", "Inglaterra"], 2)
]

st.markdown("""
    <h2 style="text-align:center; color: #2e8b57;">🎉 Bem-vindo ao Quiz sobre Urânio! 🤔</h2>
    <p style="font-size:18px; text-align:center;">
        Você sabia que o urânio não é apenas uma matéria-prima para energia nuclear, mas também tem um impacto global? 🌍
        É a energia do futuro chegando, cada vez mais próxima de eu e você! Veja se você aprendeu alguma coisa com
        nosso dashboard 🚀
    </p>
    <p style="font-size:18px; text-align:center;">
        Você vai encontrar algumas perguntas divertidas e desafiadoras sobre o urânio e o mundo da energia nuclear, 
        7 questões com respostas presentes em alguma das páginas desse dashboard. Aproveite para ler todas as páginas
        antes de responder o quiz! 🌱🌐
    </p>
    <p style="font-size:18px; text-align:center; color: #ff4500;">
        Dica importante: para responder corretamente, você precisa clicar DUAS vezes: 
        1️⃣ Clique em uma opção para selecionar a resposta;
        2️⃣ Em seguida, clique novamente para confirmá-la!
    </p>
""", unsafe_allow_html=True)

# Exibindo as perguntas
for idx, (question, options, rightOne) in enumerate(questions):
    createQuestion(question, options, rightOne, idx)

# Mostrar o resultado final
total_questions = len(questions)
correct_answers = sum([st.session_state.get(f'correct_answers_{i}', 0) for i in range(total_questions)])

# Verificar se todas as perguntas foram respondidas
if all(st.session_state.get(f'answered_{i}', False) for i in range(total_questions)):  # Verifica se todas as perguntas foram respondidas
    st.write(f"### Você acertou {correct_answers} de {total_questions} perguntas!")

    # Exibir uma mensagem baseada na quantidade de acertos
    if correct_answers == total_questions:
        st.success("Parabéns! Você acertou todas as perguntas! 🎉 Muito obrigado por ler nosso dashboard com carinho!")
    elif correct_answers >= total_questions // 2:
        st.success("Ótimo! Você acertou a maioria das questões. Obrigado por ler nosso dashboard!")
    else:
        st.warning("Opa, você errou algumas! Sem problemas, continue aprendendo e olhe mais páginas! 💪")
