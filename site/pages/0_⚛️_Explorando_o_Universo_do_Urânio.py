import streamlit as st
import random
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Explorando o Processo de Mineração de Urânio", page_icon="⚛️", layout="wide")

# Função para gerar círculos aleatórios
def generate_random_circles(n=30, mean=50, std_dev=10):
    circles = ""
    for _ in range(n):
        # Gerar valores para top e left usando distribuição normal
        top = min(max(random.gauss(mean, std_dev), 0), 90)  # Restringir entre 0% e 90%
        left = min(max(random.gauss(mean, std_dev), 0), 90)  # Restringir entre 0% e 90%
        circles += f'<div class="circle" style="top: {top}%; left: {left}%;"></div>\n'
    return circles

# Título da Página
st.write("# ⚛️ Entendendo o Processo de Mineração e Enriquecimento de Urânio")

st.write("""
Explore os principais estágios do processo de mineração e enriquecimento do urânio. Clique nos botões abaixo para entender 
mais sobre cada etapa e visualizar animações ou gráficos que explicam cada parte do ciclo.
""")

# Botões para alternar entre os estágios
st.write("## Escolha uma etapa para explorar:")
selected_stage = None

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🪨 Mineração"):
        selected_stage = "mineração"

with col2:
    if st.button("⚗️ Enriquecimento"):
        selected_stage = "enriquecimento"

with col3:
    if st.button("🔄 Reprocessamento"):
        selected_stage = "reprocessamento"

# Gerar círculos aleatórios
random_circles = generate_random_circles()

# HTML e CSS para a animação
html_content = ""
if selected_stage == "mineração":
    html_content = f"""
    <div class="container">
        <div class="animation-layer">
            {random_circles}
        </div>
        <div class="text">
            <h2>🪨 Mineração de Urânio</h2>
            <p>
                A mineração de urânio tem evoluído significativamente ao longo das décadas. Em 1990, 55% da produção global 
                vinha de minas subterrâneas. Entretanto, com o avanço de técnicas modernas, como a lixiviação in situ (ISL),
                esse cenário mudou. Em 2022, mais de 55% da produção mundial de urânio utilizou o método ISL.
            </p>
            <p>
                Existem três métodos principais de mineração de urânio:
                <ul>
                    <li>
                        <b>Mineração a Céu Aberto:</b> 
                        Este método é usado quando o urânio está próximo à superfície. Envolve a remoção de grandes
                        quantidades de solo e rocha, seguido do transporte do minério para processamento. Exemplos incluem
                        minas no Canadá, Austrália e Namíbia.
                    </li>
                    <li>
                        <b>Mineração Subterrânea:</b> 
                        Utilizada para depósitos mais profundos, este método requer a escavação de túneis e galerias. É 
                        comum em locais como a mina de Cigar Lake, no Canadá, e na África do Sul.
                    </li>
                    <li>
                        <b>Lixiviação In Situ (ISL):</b> 
                        Uma solução química é injetada no subsolo para dissolver o urânio em depósitos de arenito. A solução 
                        é bombeada de volta à superfície, reduzindo o impacto ambiental e os custos. Este método é amplamente
                        utilizado no Cazaquistão, o maior produtor mundial de urânio.
                    </li>
                </ul>
            </p>
            <p>
                Após a extração, o minério passa por etapas como trituração, lixiviação e concentração, resultando na 
                produção do concentrado de urânio, conhecido como <b>yellowcake</b>, usado como combustível nuclear.
            </p>
        </div>
    </div>
    """
elif selected_stage == "enriquecimento":
    html_content = f"""
    <div class="container">
        <div class="animation-layer">
            {random_circles}
        </div>
        <div class="text">
            <h2>⚗️ Enriquecimento de Urânio</h2>
            <p>
                O enriquecimento de urânio é um processo essencial para fornecer combustível a usinas nucleares, que 
                atualmente desempenham um papel vital no fornecimento de energia global. Em 2022, a energia nuclear 
                respondeu por 9% da geração de eletricidade no mundo, com 2.677 TWh produzidos. 
                Os maiores produtores incluem os EUA (805 TWh), China (418 TWh) e França (295 TWh).
            </p>
            <p>
                O urânio natural contém predominantemente o isótopo U-238, que não é ideal para reações nucleares 
                controladas. Por isso, ele é enriquecido para aumentar a concentração de U-235, o isótopo físsil 
                utilizado em reatores nucleares. Durante o processo de enriquecimento, o urânio é convertido em 
                hexafluoreto de urânio (UF6) e passa por centrífugas ou difusão gasosa para separar os isótopos.
            </p>
            <p>
                Existem quatro categorias principais de urânio enriquecido:
                <ul>
                    <li><b>Urânio Ligeiramente Enriquecido (SEU):</b> Entre 0,9% e 3% de U-235.</li>
                    <li><b>Urânio Pouco Enriquecido (LEU):</b> Entre 3% e 5%, utilizado em reatores comerciais.</li>
                    <li><b>Urânio Pouco Enriquecido de Alto Teor (HALEU):</b> Entre 5% e 20%.</li>
                    <li><b>Urânio Altamente Enriquecido (HEU):</b> Acima de 20%, limite definido pela IAEA.</li>
                </ul>
            </p>
            <p>
                A eficiência do processo é medida em Unidades de Trabalho Separativo (SWUs). Estratégias como 
                <b>subalimentação</b> (aumentando a eficiência do UF6) e <b>superalimentação</b> (maximizando o 
                aproveitamento de U-235) são utilizadas para atender às demandas de diferentes reatores.
            </p>
            <p>
                As taxas de enriquecimento variam dependendo do tipo de reator nuclear:
                <ul>
                    <li><b>Reatores Comerciais (PWR e BWR):</b> Entre 3% e 5% de U-235.</li>
                    <li><b>Reatores Avançados (HTGR e FNR):</b> Até 26% de U-235.</li>
                    <li><b>Reatores de Água Pesada (PHWR):</b> Urânio natural ou ligeiramente enriquecido.</li>
                </ul>
            </p>
        </div>
    </div>
    """
elif selected_stage == "reprocessamento":
    html_content = f"""
    <div class="container">
        <div class="animation-layer">
            {random_circles}
        </div>
        <div class="text">
            <h2>🔄 Reprocessamento do Combustível</h2>
            <p>
                Após a utilização em reatores nucleares, o combustível irradiado pode ser reprocessado para separar materiais ainda utilizáveis.
                Este processo envolve dissolver o combustível irradiado em ácido e separá-lo em etapas químicas.
            </p>
        </div>
    </div>
    """
else:
    html_content = """
    <div class="container">
        <div class="text">
            <h2>Selecione uma etapa para começar</h2>
            <p>
                Clique em um dos botões acima para explorar uma etapa do ciclo do combustível nuclear.
            </p>
        </div>
    </div>
    """

css_animation = """
<style>
.container {
    position: relative;
    width: 100%;
    max-width: 800px;
    margin: 50px auto;
    padding: 20px;
    border: 2px solid green;
    border-radius: 15px;
    background-color: #f0fff0;
    box-shadow: 0px 0px 10px rgba(0, 255, 0, 0.5);
    overflow: hidden;
}

.animation-layer {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1;
    animation: popAnimation 1.5s forwards;
}

.circle {
    position: absolute;
    width: 25px;
    height: 25px;
    border-radius: 50%;
    background-color: green;
    animation: circleAnimation 1s infinite alternate;
}

.text {
    position: relative;
    z-index: 2;
    opacity: 0;
    animation: fadeInText 1s forwards 0.5s;
}

@keyframes circleAnimation {
    from {
        transform: scale(1) translateY(0);
    }
    to {
        transform: scale(2) translateY(-20px);
    }
}

@keyframes popAnimation {
    from {
        transform: scale(1);
    }
    to {
        transform: scale(20);
        opacity: 0;
    }
}

@keyframes fadeInText {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}
</style>
"""
if selected_stage == "mineração":
    # Renderizar o HTML com animação
    st.components.v1.html(css_animation + html_content, height=600)
elif selected_stage == "enriquecimento":
    st.components.v1.html(css_animation + html_content, height=800)
else:
    st.components.v1.html(css_animation + html_content, height=400)



# Adicionar gráfico interativo explicativo (opcional)
st.write("## Gráfico: Comparação de Métodos de Mineração de Urânio")

data = pd.DataFrame({
    "Método": ["Céu Aberto", "Subterrânea", "In Situ Leaching"],
    "Custos ($/tonelada)": [40, 70, 30],
    "Impacto Ambiental (%)": [50, 60, 20],
})

fig = px.bar(
    data,
    x="Método",
    y=["Custos ($/tonelada)", "Impacto Ambiental (%)"],
    barmode="group",
    title="Custos e Impactos Ambientais por Método de Mineração",
    labels={"value": "Valor", "variable": "Métrica"},
)

st.plotly_chart(fig, use_container_width=True)

# Adicionar gráfico interativo explicativo (opcional)
st.write("## Gráfico: Comparação de Métodos de Mineração de Urânio")

data = pd.DataFrame({
    "Método": ["Céu Aberto", "Subterrânea", "In Situ Leaching"],
    "Custos ($/tonelada)": [40, 70, 30],
    "Impacto Ambiental (%)": [50, 60, 20],
})

fig = px.bar(
    data,
    x="Método",
    y=["Custos ($/tonelada)", "Impacto Ambiental (%)"],
    barmode="group",
    title="Custos e Impactos Ambientais por Método de Mineração",
    labels={"value": "Valor", "variable": "Métrica"},
)

# st.plotly_chart(fig, use_container_width=True)

# Informações adicionais
st.write("### Detalhes:")
with st.expander("Por que o enriquecimento é necessário?"):
    st.write("""
    O urânio natural contém apenas uma pequena fração do isótopo físsil U-235, que é necessário para sustentar reações nucleares.
    Sem enriquecimento, o urânio não seria adequado para a maioria dos reatores nucleares comerciais.
    """)

with st.expander("O que é mineração 'In Situ Leaching'?"):
    st.write("""
    Este é um método de mineração onde uma solução é injetada diretamente no depósito de urânio para dissolver o mineral, que é
    posteriormente bombeado para a superfície. Este método tem menor impacto ambiental comparado à mineração tradicional.
    """)

# Finalização
st.write("""
Explore cada seção e veja como o ciclo do combustível nuclear começa com a mineração e termina em aplicações práticas como
energia nuclear e pesquisas científicas!
""")

# Adicionar gráfico interativo explicativo (exemplo fictício)
st.write("## Gráfico: Comparação de Métodos de Mineração de Urânio")

# Exemplo de dados para o gráfico
data = pd.DataFrame({
    "Método": ["Céu Aberto", "Subterrânea", "In Situ Leaching"],
    "Custos ($/tonelada)": [40, 70, 30],
    "Impacto Ambiental (%)": [50, 60, 20],
})

fig = px.bar(
    data,
    x="Método",
    y=["Custos ($/tonelada)", "Impacto Ambiental (%)"],
    barmode="group",
    title="Custos e Impactos Ambientais por Método de Mineração",
    labels={"value": "Valor", "variable": "Métrica"},
)

# st.plotly_chart(fig, use_container_width=True)

# Informações adicionais
st.write("### Detalhes:")
with st.expander("Por que o enriquecimento é necessário?"):
    st.write("""
    O urânio natural contém apenas uma pequena fração do isótopo físsil U-235, que é necessário para sustentar reações nucleares.
    Sem enriquecimento, o urânio não seria adequado para a maioria dos reatores nucleares comerciais.
    """)

with st.expander("O que é mineração 'In Situ Leaching'?"):
    st.write("""
    Este é um método de mineração onde uma solução é injetada diretamente no depósito de urânio para dissolver o mineral, que é
    posteriormente bombeado para a superfície. Este método tem menor impacto ambiental comparado à mineração tradicional.
    """)

# Finalização
st.write("""
Explore cada seção e veja como o ciclo do combustível nuclear começa com a mineração e termina em aplicações práticas como
energia nuclear e pesquisas científicas!
""")
