import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Relatório Técnico: Python",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para melhorar a aparência
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #306998;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 2rem;
        color: #FFD43B;
        border-bottom: 2px solid #4B8BBE;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .highlight {
        background-color: #f1f1f1;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #4B8BBE;
        margin: 1rem 0;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        color: #666;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Menu de navegação na sidebar
st.sidebar.title("Navegação")
section = st.sidebar.radio(
    "Selecione uma seção:",
    ["Introdução", "Histórico", "Paradigmas", "Características", "Linguagens Relacionadas", "Conclusão", "Bibliografia"]
)

# Conteúdo da Introdução
if section == "Introdução":
    st.markdown('<h1 class="main-header">Relatório Técnico: A Linguagem de Programação Python</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <strong>Data:</strong> 22 de Agosto de 2025 | 
        <strong>Status:</strong>Em Desenvolvimento
        <strong>Criado e adaptado por:</strong> Gabriel da Silva Cassino 
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="highlight">
    <h3>Sumário Executivo</h3>
    <p>Python é uma linguagem de programação de alto nível, interpretada, de propósito geral e multiparadigma. 
    Criada por Guido van Rossum no final dos anos 1980, sua filosofia de design enfatiza a legibilidade do código, 
    a simplicidade e a produtividade do desenvolvedor. Este relatório detalha a história e genealogia de Python, 
    seus paradigmas de programação, suas características mais marcantes e faz um paralelo com linguagens relacionadas, 
    sejam elas influenciadoras, influenciadas ou concorrentes. O documento conclui que o sucesso duradouro de Python 
    é diretamente atribuível à sua combinação única de facilidade de aprendizado, poder e um ecossistema comunitário vibrante.</p>
    </div>
    """, unsafe_allow_html=True)

# Conteúdo do Histórico
elif section == "Histórico":
    st.markdown('<h1 class="main-header">Histórico, Cronologia e Genealogia</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="highlight">
    <h3>Origens e Motivação (década de 1980)</h3>
    <p>No final dos anos 1980, Guido van Rossum trabalhava no Centrum Wiskunde & Informatica (CWI), na Holanda, 
    no projeto Amoeba, um sistema operacional distribuído. Ele precisava de uma linguagem de script que fosse mais 
    poderosa e legível do que a shell script da época, mas mais fácil e ágil do que C.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<h3 class="sub-header">Cronologia e Marcos Principais</h3>', unsafe_allow_html=True)
    
    timeline_data = {
        "1991 (v0.9.0)": "Primeira release pública. Já incluía classes com herança, tratamento de exceções, funções e os tipos de dados fundamentais.",
        "1994 (v1.0)": "Introdução de ferramentas de programação funcional como lambda, map(), filter(), e reduce().",
        "2000 (v2.0)": "Introdução do garbage collector e do conceito de 'list comprehensions'.",
        "2008 (v3.0)": "Lançamento do Python 3, uma revisão major e não backward-compatible da linguagem.",
        "Atualmente (v3.10+)": "O desenvolvimento de Python continua ativo, com lançamentos anuais."
    }
    
    for year, description in timeline_data.items():
        st.markdown(f"**{year}**: {description}")
    
    st.markdown('<h3 class="sub-header">Genealogia</h3>', unsafe_allow_html=True)
    st.markdown("""
    Python é uma linguagem que bebeu de várias fontes. Sua genealogia pode ser resumida como:
    - **ABC:** A maior influência. Forneceu a sintaxe de indentação e a filosofia de acessibilidade.
    - **Modula-3:** Influenciou o sistema de módulos e namespaces de Python.
    - **C:** A sintaxe para exceções e alguns aspectos de sua semântica.
    - **Lisp, Haskell:** Influenciaram as ferramentas de programação funcional.
    - **Java e C#:** Influenciaram a sintaxe para decoradores.
    """)

# Conteúdo dos Paradigmas
elif section == "Paradigmas":
    st.markdown('<h1 class="main-header">Paradigmas da Linguagem</h1>', unsafe_allow_html=True)
    st.markdown("Python é uma linguagem **multiparadigma**. Isso significa que ela não força o programador a usar um único estilo de programação, permitindo a escolha do paradigma mais adequado para resolver um determinado problema.")
    
    st.markdown('<h3 class="sub-header">Programação Imperativa e Procedural</h3>', unsafe_allow_html=True)
    st.markdown("É o estilo mais básico e o que mais se assemelha a scripts sequenciais. O código é uma sequência de comandos que alteram o estado do programa.")
    
    st.code("""
# Exemplo de programação procedural em Python
def calcular_media(numeros):
    total = 0
    count = 0
    for num in numeros:
        total += num
        count += 1
    return total / count
    """, language="python")
    
    st.markdown('<h3 class="sub-header">Programação Orientada a Objetos (OOP)</h3>', unsafe_allow_html=True)
    st.markdown("Python é uma linguagem profundamente orientada a objetos. *Tudo em Python é um objeto*, incluindo classes, funções e módulos.")
    
    st.code("""
# Exemplo de OOP em Python
class Animal:
    def __init__(self, nome):
        self.nome = nome

    def fazer_som(self):
        raise NotImplementedError("Subclasse deve implementar")

class Cachorro(Animal):
    def fazer_som(self):
        return "Woof!"

meu_pet = Cachorro("Rex")
print(meu_pet.fazer_som())  # Output: Woof!
    """, language="python")
    
    st.markdown('<h3 class="sub-header">Programação Funcional</h3>', unsafe_allow_html=True)
    st.markdown("Python oferece suporte a conceitos de programação funcional, embora não seja uma linguagem puramente funcional.")
    
    st.code("""
# Programação Funcional com map e lambda
numeros = [1, 2, 3, 4]
quadrados = list(map(lambda x: x**2, numeros))
# Equivalente com list comprehension (mais "pythônico")
quadrados = [x**2 for x in numeros]
    """, language="python")

# Conteúdo das Características
elif section == "Características":
    st.markdown('<h1 class="main-header">Características Mais Marcantes</h1>', unsafe_allow_html=True)
    
    characteristics = {
        "Sintaxe Clara e Legível": "A obrigatoriedade de indentação para definir blocos de código elimina chaves e keywords desnecessárias, resultando em um código visualmente mais limpo e consistente.",
        "Tipagem Dinâmica e Forte": "O tipo de uma variável é inferido em tempo de execução (dinâmica), mas o interpretador não realiza conversões implícitas de tipo que possam causar erros (forte).",
        "Interpretada e de Alto Nível": "O código-fonte é executado por um interpretador, linha a linha, facilitando a prototipagem rápida e a portabilidade.",
        "Gerenciamento Automático de Memória": "Python possui um garbage collector que automaticamente gerencia a alocação e liberação de memória.",
        "Biblioteca Padrão Abrangente": "Python é distribuído com uma vasta biblioteca padrão para uma infinidade de tarefas (princípio 'Batteries Included').",
        "Ecossistema Rico (PyPI)": "O Python Package Index (PyPI) é um repositório com centenas de milhares de bibliotecas de terceiros."
    }
    
    for char, desc in characteristics.items():
        st.markdown(f"### {char}")
        st.markdown(desc)
        st.markdown("---")

# Conteúdo das Linguagens Relacionadas
elif section == "Linguagens Relacionadas":
    st.markdown('<h1 class="main-header">Linguagens Relacionadas</h1>', unsafe_allow_html=True)
    
    st.markdown('<h3 class="sub-header">Influenciadores</h3>', unsafe_allow_html=True)
    st.markdown("""
    - **ABC:** Como citado, foi a influência mais significativa na filosofia de design e sintaxe.
    - **Modula-3:** Influenciou o sistema de módulos.
    - **C e C++:** Influenciaram a sintaxe de operadores e a implementação do interpretador CPython.
    - **Lisp e Haskell:** Influenciaram as features de programação funcional.
    """)
    
    st.markdown('<h3 class="sub-header">Influenciadas</h3>', unsafe_allow_html=True)
    st.markdown("""
    - **Ruby:** A linguagem Ruby e seu framework Rails compartilham a filosofia de produtividade e legibilidade com Python.
    - **JavaScript (Node.js):** O sucesso de Python como linguagem de script de backend influenciou a adoção do JavaScript no servidor.
    - **Go (Golang):** A sintaxe simples e clara de Go é comparável à de Python.
    - **Julia:** Adotou uma sintaxe legível e similar ao Python para atrair sua grande comunidade científica.
    """)
    
    st.markdown('<h3 class="sub-header">Similares e Concorrentes</h3>', unsafe_allow_html=True)
    st.markdown("""
    - **Perl:** Era a principal linguagem de script antes da ascensão do Python.
    - **Ruby:** Python e Ruby são frequentemente comparadas como alternativas com filosofias diferentes.
    - **JavaScript:** Concorre diretamente com Python no backend e em aplicações de dados.
    - **Java e C#:** Linguagens compiladas, estaticamente tipadas e verbosas.
    - **Linguagens 'Opostas' (Rust, C++):** Priorizam o controle de baixo nível e performance máxima sobre a simplicidade.
    """)

# Conteúdo da Conclusão
elif section == "Conclusão":
    st.markdown('<h1 class="main-header">Conclusão</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="highlight">
    <p>Python evoluiu de um projeto pessoal para uma das linguagens de programação mais populares e influentes do mundo. 
    Seu sucesso pode ser atribuído a uma combinação poderosa: uma sintaxe intuitiva e legível que reduz o custo de 
    manutenção do software; uma natureza multiparadigma que oferece flexibilidade ao desenvolvedor; e um ecossistema 
    inigualável de bibliotecas que permite sua aplicação em domínios tão diversos como automação web, inteligência artificial, 
    ciência de dados e desenvolvimento de jogos.</p>
    
    <p>Apesar de suas desvantagens, como a performance inferior comparada a linguagens compiladas, seus benefícios em 
    produtividade e a facilidade de integração com código C/C++ para otimizações críticas garantem sua relevância contínua. 
    Python não é apenas uma linguagem de programação; é uma ferramenta que democratiza o ato de programar, permitindo que 
    cientistas, engenheiros, artistas e iniciantes transformem suas ideias em realidade de maneira eficiente.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    ### Apêndice A: Exemplo de Código Python
    """)
    
    st.code("""
# Exemplo que combina vários paradigmas
# Paradigma Procedural e OOP

from math import sqrt  # Import da biblioteca padrão

# Definição de uma Classe (OOP)
class Ponto:
    def __init__(self, x, y):  # Construtor
        self.x = x
        self.y = y

    def distancia_ate_origem(self):  # Método
        return sqrt(self.x**2 + self.y**2)

    def __str__(self):  # Método Mágico para representação em string
        return f"({self.x}, {self.y})"

# Função pura (conceito de Programação Funcional)
def calcular_distancia_entre_pontos(a, b):
    return sqrt((a.x - b.x)**2 + (a.y - b.y)**2)

# Código principal (Procedural)
if __name__ == "__main__":
    # Criando objetos
    ponto_a = Ponto(3, 4)
    ponto_b = Ponto(6, 8)

    # Usando métodos
    print(f"Ponto A: {ponto_a}")
    print(f"Distância de A até a origem: {ponto_a.distancia_ate_origem():.2f}")

    # Usando a função
    distancia = calcular_distancia_entre_pontos(ponto_a, ponto_b)
    print(f"Distância entre A e B: {distancia:.2f}")

    # List Comprehension (Programação Funcional)
    pontos = [ponto_a, ponto_b]
    distancias_origem = [p.distancia_ate_origem() for p in pontos]
    print(f"Distâncias até a origem: {distancias_origem}")
    """, language="python")

# Conteúdo da Bibliografia
elif section == "Bibliografia":
    st.markdown('<h1 class="main-header">Bibliografia</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="highlight">
    <h3>Fontes Consultadas</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### Livros
    - Lutz, M. (2013). Learning Python. O'Reilly Media.
    - Beazley, D. M. (2009). Python Essential Reference. Addison-Wesley Professional.
    - Ramalho, L. (2015). Fluent Python. O'Reilly Media.
    - Van Rossum, G., Drake, F. L., & Python Development Team. (2011). The Python Language Reference.
    
    ### Documentação Oficial
    - Python Software Foundation. (2023). The Python Tutorial. https://docs.python.org/3/tutorial/
    - Python Software Foundation. (2023). The Python Language Reference. https://docs.python.org/3/reference/
    - Python Software Foundation. (2023). The Python Standard Library. https://docs.python.org/3/library/
    
    ### Artigos e Publicações Acadêmicas
    - Van Rossum, G. (1995). Python Reference Manual. CWI Report CS-R9525.
    - Van Rossum, G. (2007). A Brief Timeline of Python. The History of Python Blog.
    - Prechelt, L. (2000). An empirical comparison of C, C++, Java, Perl, Python, Rexx, and Tcl. IEEE Computer, 33(10), 23-29.
    
    ### Sites e Recursos Online
    - Python.org: https://www.python.org/
    - Real Python: https://realpython.com/
    - The Python Package Index (PyPI): https://pypi.org/
    - Python Wiki: https://wiki.python.org/moin/
    - Stack Overflow: https://stackoverflow.com/questions/tagged/python
    - GitHub Python Trending Repositories: https://github.com/trending/python
    
    ### Vídeos e Palestras
    - Van Rossum, G. (2016). The History of Python. PyCon 2016.
    - Warsaw, B. (2018). How Python Was Shaped by leaky internals. PyCon 2018.
    - Beazley, D. (2015). Python Concurrency From the Ground Up. PyCon 2015.
    </div>
    """)

# Rodapé
st.markdown("""
<div class="footer">
    <p>Relatório Técnico: A Linguagem de Programação Python - Desenvolvido com Streamlit</p>
</div>
""", unsafe_allow_html=True)
