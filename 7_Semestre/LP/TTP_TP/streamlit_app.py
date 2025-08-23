# versão 1a 23-08-2025

# 1_23-08-2025

import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Relatório Técnico: Python",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #306998;
        text-align: center;
        margin-bottom: 2rem;
    }
    .final-thanks {
        font-size: 5rem;
        color: #306998;
        text-align: center;
        margin-top:10rem;
        margin-bottom: 10rem;
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
        color: #000000;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        color: #666;
        font-size: 0.9rem;
    }
    .code-block {
        background-color: #2b2b2b;
        color: #f8f8f2;
        padding: 1rem;
        border-radius: 0.5rem;
        overflow-x: auto;
        margin: 1rem 0;
        font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
    }
    .timeline-item {
        margin-bottom: 1rem;
        padding-left: 1.5rem;
        border-left: 3px solid #4B8BBE;
    }
    /*------------------------------- Adaptação UI/UX ---------*/
    /* Responsividade */
    @media (max-width: 1366px) {
        .main-header { font-size: 2.2rem; }
        .section-header { font-size: 1.6rem; }
        .sub-header { font-size: 1.3rem; }
    }
    @media (max-width: 768px) {
        .main-header { font-size: 1.8rem; }
        .section-header { font-size: 1.4rem; }
        .sub-header { font-size: 1.2rem; }
        .highlight { padding: 0.8rem; }
    }

     /* Estilo para as tabelas de comparação */
    .comparison-table {
        width: 100%;
        border-collapse: collapse;
        margin: 1rem 0;
    }
    .comparison-table th, .comparison-table td {
        border: 1px solid #ddd;
        padding: 0.5rem;
        text-align: left;
    }
    .comparison-table th {
        background-color: #f2f2f2;
    }
    .comparison-table tr:nth-child(even) {
        background-color: #f9f9f9;
    }
    /*------------------------------- Adaptação UI/UX ---------*/
    
</style>
""", unsafe_allow_html=True)

# Estrutura JSON das seções
sections = [
    {
        "titulo": "Introdução - Python",
        "texto": """
        <h1 class="main-header">Relatório Técnico: A Linguagem de Programação Python</h1>
        <div style="text-align: center; margin-bottom: 2rem;">
            <strong>Data:</strong> 22 de Agosto de 2025 
            <br>
            <strong>Status:</strong> Em Desenvolvimento
            <br>
            <strong>Criado e adaptado por:</strong> Gabriel da Silva Cassino 
            <br>
            <strong>Parceria e contribuição de código:</strong> Welbert Junio Afonso de Almeida 
        </div>
        <div class="highlight">
            <h3 style="color: #000000;">Sumário Executivo</h3>
            <p style="color: #000000;">Python é uma linguagem de programação de alto nível, interpretada, de propósito geral e multiparadigma. Criada por Guido van Rossum no final dos anos 1980, sua filosofia de design enfatiza a legibilidade do código, a simplicidade e a produtividade do desenvolvedor. Este relatório detalha a história e genealogia de Python, seus paradigmas de programação, suas características mais marcantes e faz um paralelo com linguagens relacionadas, sejam elas influenciadoras, influenciadas ou concorrentes. O documento conclui que o sucesso duradouro de Python é diretamente atribuível à sua combinação única de facilidade de aprendizado, poder e um ecossistema comunitário vibrante.</p>
        </div>
        """
    },
    {
        "titulo": "Histórico",
        "texto": """
        <h1 class="main-header">Histórico, Cronologia e Genealogia</h1>
        <div class="highlight">
            <h3>Origens e Motivação (década de 1980)</h3>
            <p>No final dos anos 1980, Guido van Rossum trabalhava no Centrum Wiskunde & Informatica (CWI), na Holanda, no projeto Amoeba, um sistema operacional distribuído. Ele precisava de uma linguagem de script que fosse mais poderosa e legível do que a shell script da época, mas mais fácil e ágil do que C. Ele havia contribuído anteriormente para a linguagem <strong>ABC</strong>, projetada para ser uma substituta fácil de aprender para o BASIC. A ABC introduziu muitas ideias que mais tarde se tornariam centrais no Python, como a indentação para delimitação de blocos e uma estrutura de dados de alta nível.</p>
            <p>Insatisfeito com as limitações da ABC e inspirado por outras linguagens como <strong>Modula-3</strong>, van Rossum decidiu criar uma nova linguagem durante suas férias de Natal em 1989. O nome "Python" foi escolhido em homenagem ao grupo de comédia britânico Monty Python, do qual van Rossum é fã, e não à serpente, embora a cobra tenha se tornado seu símbolo.</p>
        </div>
        
        <h3 class="sub-header">Cronologia e Marcos Principais</h3>
        <div class="timeline-item">
            <strong>1991 (v0.9.0):</strong> Primeira release pública. Já incluía classes com herança, tratamento de exceções, funções e os tipos de dados fundamentais (list, dict, str).
        </div>
        <div class="timeline-item">
            <strong>1994 (v1.0):</strong> Introdução de ferramentas de programação funcional como lambda, map(), filter(), e reduce().
        </div>
        <div class="timeline-item">
            <strong>2000 (v2.0):</strong> Introdução do garbage collector e do conceito de "list comprehensions", uma feature poderosa inspirada em linguagens funcionais como Haskell. Foi também a primeira versão a suportar Unicode.
        </div>
        <div class="timeline-item">
            <strong>2008 (v3.0):</strong> Lançamento do Python 3, também conhecido como "Py3k" ou "Python 3000". Esta foi uma revisão major e não backward-compatible da linguagem, destinada a corrigir falhas de design e duplicações acumuladas ao longo dos anos. A mudança mais notória foi a função print se tornar uma função (print()) em vez de uma declaração.
        </div>
        <div class="timeline-item">
            <strong>Atualmente (v3.10+):</strong> O desenvolvimento de Python continua ativo, com lançamentos anuais. Versões recentes introduziram features como o "pattern matching" (estruturalmente semelhante a um switch/case avançado), operadores de união de tipos (|), e melhorias de performance.
        </div>
        
        <h3 class="sub-header">Genealogia</h3>
        <p>Python é uma linguagem que bebeu de várias fontes. Sua genealogia pode ser resumida como:</p>
        <ul>
            <li><strong>ABC:</strong> A maior influência. Forneceu a sintaxe de indentação, a ideia de tipos de dados de alto nível e a filosofia de tornar a linguagem acessível para não-programadores.</li>
            <li><strong>Modula-3:</strong> Influenciou o sistema de módulos e namespaces de Python.</li>
            <li><strong>C:</strong> A sintaxe de Python para exceções, e alguns aspectos de sua semântica são herdados de C.</li>
            <li><strong>Lisp, Haskell:</strong> Influenciaram as ferramentas de programação funcional (lambda, map, etc.) e as "list comprehensions".</li>
            <li><strong>Java e C#:</strong> Influenciaram a sintaxe para decoradores (a partir do Java annotations) e o desenvolvimento de frameworks de testes unitários.</li>
        </ul>
        """
    },
    {
        "titulo": "Paradigmas",
        "texto": """
        <h1 class="main-header">Paradigmas da Linguagem</h1>
        <p>Python é uma linguagem <strong>multiparadigma</strong>. Isso significa que ela não força o programador a usar um único estilo de programação, permitindo a escolha do paradigma mais adequado para resolver um determinado problema.</p>
        
        <h3 class="sub-header">Programação Imperativa e Procedural</h3>
        <p>É o estilo mais básico e o que mais se assemelha a scripts sequenciais. O código é uma sequência de comandos que alteram o estado do programa. Python suporta totalmente este paradigma com estruturas de controle (if, for, while), funções (def) e manipulação direta de variáveis.</p>
        
        <div class="code-block">
            # Exemplo de programação procedural em Python<br>
            def calcular_media(numeros):<br>
            &nbsp;&nbsp;&nbsp;&nbsp;total = 0<br>
            &nbsp;&nbsp;&nbsp;&nbsp;count = 0<br>
            &nbsp;&nbsp;&nbsp;&nbsp;for num in numeros:<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;total += num<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;count += 1<br>
            &nbsp;&nbsp;&nbsp;&nbsp;return total / count
        </div>
        
        <h3 class="sub-header">Programação Orientada a Objetos (OOP)</h3>
        <p>Python é uma linguagem profundamente orientada a objetos. <em>Tudo em Python é um objeto</em>, incluindo classes, funções e módulos. Ela suporta os quatro pilares da OOP:</p>
        <ul>
            <li><strong>Encapsulamento:</strong> Atributos e métodos podem ser públicos, protegidos (por convenção, com _) ou privados (por convenção, com __).</li>
            <li><strong>Herança:</strong> Uma classe pode herdar atributos e métodos de uma ou várias classes base (herança múltipla).</li>
            <li><strong>Polimorfismo:</strong> Objetos de diferentes classes podem ser tratados como objetos de uma classe comum se compartilharem a mesma interface.</li>
            <li><strong>Abstração:</strong> Através de classes abstratas (módulo abc) é possível definir interfaces que devem ser implementadas por classes derivadas.</li>
        </ul>
        
        <div class="code-block">
            # Exemplo de OOP em Python<br>
            class Animal:<br>
            &nbsp;&nbsp;&nbsp;&nbsp;def __init__(self, nome):<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;self.nome = nome<br>
            <br>
            &nbsp;&nbsp;&nbsp;&nbsp;def fazer_som(self):<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;raise NotImplementedError("Subclasse deve implementar")<br>
            <br>
            class Cachorro(Animal):<br>
            &nbsp;&nbsp;&nbsp;&nbsp;def fazer_som(self):<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return "Woof!"<br>
            <br>
            meu_pet = Cachorro("Rex")<br>
            print(meu_pet.fazer_som())  # Output: Woof!
        </div>
        
        <h3 class="sub-header">Programação Funcional</h3>
        <p>Python oferece suporte a conceitos de programação funcional, embora não seja uma linguagem puramente funcional como Haskell. Ela trata funções como <strong>cidadãos de primeira classe</strong> (podem ser atribuídas a variáveis, passadas como argumento e retornadas por outras funções) e fornece funções de alta ordem (map, filter, sorted). "List comprehensions" e "generator expressions" são constructs fortemente influenciados pelo paradigma funcional.</p>
        
        <div class="code-block">
            # Programação Funcional com map e lambda<br>
            numeros = [1, 2, 3, 4]<br>
            quadrados = list(map(lambda x: x**2, numeros))<br>
            # Equivalente com list comprehension (mais "pythônico")<br>
            quadrados = [x**2 for x in numeros]
        </div>
        """
    },
    {
        "titulo": "Características",
        "texto": """
        <h1 class="main-header">Características Mais Marcantes</h1>
        
        <h3 class="sub-header">Sintaxe Clara e Legível</h3>
        <p>A sintaxe de Python é uma de suas maiores virtudes. A obrigatoriedade de <strong>indentação</strong> para definir blocos de código elimina chaves e keywords desnecessárias, resultando em um código visualmente mais limpo e consistente. A filosofia por trás disso é resumida no "Zen do Python" (import this), que prega: "Legibilidade conta".</p>
        
        <h3 class="sub-header">Tipagem Dinâmica e Forte</h3>
        <ul>
            <li><strong>Dinâmica:</strong> O tipo de uma variável é inferido em tempo de execução. Não é necessário declarar int x;, basta x = 10.</li>
            <li><strong>Forte:</strong> O interpretador não realiza conversões implícitas de tipo que possam causar erros. Por exemplo, "10" + 5 resultará em um TypeError, e não em "105" ou 15. Isso evita bugs sutis.</li>
        </ul>
        
        <h3 class="sub-header">Interpretada e de Alto Nível</h3>
        <p>Python é uma linguagem interpretada (o código-fonte é executado por um interpretador, linha a linha, não sendo compilado previamente para código de máquina). Isso facilita a prototipagem rápida e a portabilidade ("escreva uma vez, execute em qualquer lugar" onde houver um interpretador Python).</p>
        
        <h3 class="sub-header">Gerenciamento Automático de Memória</h3>
        <p>Python possui um garbage collector que automaticamente gerencia a alocação e liberação de memória, liberando o programador dessa tarefa complexa e propensa a erros (como vazamentos de memória).</p>
        
        <h3 class="sub-header">Biblioteca Padrão Abrangente (Batteries Included)</h3>
        <p>Python é distribuído com uma vasta biblioteca padrão que fornece módulos e funções para uma infinidade de tarefas: acesso a bancos de dados, manipulação de arquivos e diretórios, operações de rede, parsing de XML/JSON, testes unitários, etc. Isso permite que soluções complexas sejam implementadas com muito pouco código adicional.</p>
        
        <h3 class="sub-header">Ecossistema Rico (PyPI)</h3>
        <p>O Python Package Index (PyPI) é um repositório com centenas de milhares de bibliotecas de terceiros para praticamente qualquer finalidade imaginável (ciência de dados, machine learning, desenvolvimento web, automação, etc.). O gerenciador de pacotes pip facilita a instalação dessas dependências.</p>
        """
    },
    {
        "titulo": "Linguagens Relacionadas",
        "texto": """
        <h1 class="main-header">Linguagens Relacionadas</h1>
        
        <h3 class="sub-header">Influenciadores</h3>
        <ul>
            <li><strong>ABC:</strong> Como citado, foi a influência mais significativa na filosofia de design e sintaxe.</li>
            <li><strong>Modula-3:</strong> Influenciou o sistema de módulos.</li>
            <li><strong>C e C++:</strong> Influenciaram a sintaxe de operadores e a implementação do interpretador CPython, escrito em C.</li>
            <li><strong>Lisp e Haskell:</strong> Influenciaram as features de programação funcional.</li>
        </ul>
        
        <h3 class="sub-header">Influenciadas</h3>
        <ul>
            <li><strong>Ruby:</strong> A linguagem Ruby e seu framework Rails compartilham a filosofia de produtividade e legibilidade com Python.</li>
            <li><strong>JavaScript (Node.js):</strong> O sucesso de Python como linguagem de script de backend e sua rica ecossistema influenciaram a adoção do JavaScript no servidor com Node.js.</li>
            <li><strong>Go (Golang):</strong> A sintaxe simples e clara de Go, com foco em produtividade, é comparável à de Python, embora Go seja compilada e focada em concorrência.</li>
            <li><strong>Julia:</strong> Projetada para computação científica de alto desempenho, Julia adotou uma sintaxe legível e similar ao Python para atrair sua grande comunidade científica.</li>
        </ul>
        
        <h3 class="sub-header">Similares e Concorrentes</h3>
        <ul>
            <li><strong>Perl:</strong> Era a principal linguagem de script antes da ascensão do Python. Python é frequentemente visto como uma alternativa mais legível e maintainable ao Perl.</li>
            <li><strong>Ruby:</strong> Python e Ruby são frequentemente comparadas. Ambas são dinâmicas, orientadas a objetos e focadas em produtividade.</li>
            <li><strong>JavaScript:</strong> Concorre diretamente com Python no backend (Node.js vs Django/Flask) e em aplicações de dados.</li>
            <li><strong>Java e C#:</strong> Linguagens compiladas, estaticamente tipadas e verbosas. Python compete com elas em produtividade e velocidade de desenvolvimento.</li>
            <li><strong>Linguagens "Opostas" (Rust, C++):</strong> Essas linguagens são "opostas" no sentido de priorizar o controle de baixo nível e performance máxima sobre a simplicidade e a produtividade.</li>
        </ul>
        """
    },
    {
        "titulo": "Conclusão",
        "texto": """
        <h1 class="main-header">Conclusão</h1>
        <div class="highlight">
            <p>Python evoluiu de um projeto pessoal para uma das linguagens de programação mais populares e influentes do mundo. Seu sucesso pode ser atribuído a uma combinação poderosa: uma sintaxe intuitiva e legível que reduz o custo de manutenção do software; uma natureza multiparadigma que oferece flexibilidade ao desenvolvedor; e um ecossistema inigualável de bibliotecas que permite sua aplicação em domínios tão diversos como automação web, inteligência artificial, ciência de dados e desenvolvimento de jogos.</p>
            
            <p>Apesar de suas desvantagens, como a performance inferior comparada a linguagens compiladas, seus benefícios em produtividade e a facilidade de integração com código C/C++ para otimizações críticas garantem sua relevância contínua. Python não é apenas uma linguagem de programação; é uma ferramenta que democratiza o ato de programar, permitindo que cientistas, engenheiros, artistas e iniciantes transformem suas ideias em realidade de maneira eficiente.</p>
        </div>
        
        <h3 class="sub-header">Apêndice A: Exemplo de Código Python</h3>
        <div class="code-block">
            # Exemplo que combina vários paradigmas<br>
            # Paradigma Procedural e OOP<br>
            <br>
            from math import sqrt  # Import da biblioteca padrão<br>
            <br>
            # Definição de uma Classe (OOP)<br>
            class Ponto:<br>
            &nbsp;&nbsp;&nbsp;&nbsp;def __init__(self, x, y):  # Construtor<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;self.x = x<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;self.y = y<br>
            <br>
            &nbsp;&nbsp;&nbsp;&nbsp;def distancia_ate_origem(self):  # Método<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return sqrt(self.x**2 + self.y**2)<br>
            <br>
            &nbsp;&nbsp;&nbsp;&nbsp;def __str__(self):  # Método Mágico para representação em string<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return f"({self.x}, {self.y})"<br>
            <br>
            # Função pura (conceito de Programação Funcional)<br>
            def calcular_distancia_entre_pontos(a, b):<br>
            &nbsp;&nbsp;&nbsp;&nbsp;return sqrt((a.x - b.x)**2 + (a.y - b.y)**2)<br>
            <br>
            # Código principal (Procedural)<br>
            if __name__ == "__main__":<br>
            &nbsp;&nbsp;&nbsp;&nbsp;# Criando objetos<br>
            &nbsp;&nbsp;&nbsp;&nbsp;ponto_a = Ponto(3, 4)<br>
            &nbsp;&nbsp;&nbsp;&nbsp;ponto_b = Ponto(6, 8)<br>
            <br>
            &nbsp;&nbsp;&nbsp;&nbsp;# Usando métodos<br>
            &nbsp;&nbsp;&nbsp;&nbsp;print(f"Ponto A: {ponto_a}")<br>
            &nbsp;&nbsp;&nbsp;&nbsp;print(f"Distância de A até a origem: {ponto_a.distancia_ate_origem():.2f}")<br>
            <br>
            &nbsp;&nbsp;&nbsp;&nbsp;# Usando a função<br>
            &nbsp;&nbsp;&nbsp;&nbsp;distancia = calcular_distancia_entre_pontos(ponto_a, ponto_b)<br>
            &nbsp;&nbsp;&nbsp;&nbsp;print(f"Distância entre A e B: {distancia:.2f}")<br>
            <br>
            &nbsp;&nbsp;&nbsp;&nbsp;# List Comprehension (Programação Funcional)<br>
            &nbsp;&nbsp;&nbsp;&nbsp;pontos = [ponto_a, ponto_b]<br>
            &nbsp;&nbsp;&nbsp;&nbsp;distancias_origem = [p.distancia_ate_origem() for p in pontos]<br>
            &nbsp;&nbsp;&nbsp;&nbsp;print(f"Distâncias até a origem: {distancias_origem}")
        </div>
        """
    },
    {
        "titulo": "Introdução - Javascript",
        "texto": """
        <h1 class="main-header">Relatório Técnico: A Linguagem de Programação JavaScript</h1>
        <div style="text-align: center; margin-bottom: 2rem;">
            <strong>Data:</strong> 22 de Agosto de 2025 
            <br>
            <strong>Status:</strong> Em Desenvolvimento
            <br>
            <strong>Criado e adaptado por:</strong> Gabriel da Silva Cassino 
            <br>
            <strong>Parceria e contribuição de código:</strong> Welbert Junio Afonso de Almeida 
        </div>
        <div class="highlight">
            <h3 style="color: #000000;">Sumário Executivo</h3>
            <p style="color: #000000;">JavaScript é uma linguagem de programação de alto nível, interpretada, multiparadigma e orientada a eventos. Criada por Brendan Eich em 1995 para a Netscape Communications, JavaScript rapidamente se tornou a linguagem padrão para desenvolvimento web front-end. Este relatório detalha a história e genealogia de JavaScript, seus paradigmas de programação, suas características mais marcantes e faz um paralelo com linguagens relacionadas. O documento conclui que o sucesso ubíquo de JavaScript é resultado de sua natureza versátil, da evolução constante através do padrão ECMAScript e de seu ecossistema vasto que se expandiu para além dos navegadores com o advento do Node.js.</p>
        </div>
        """
    },
    {
        "titulo": "Histórico",
        "texto": """
        <h1 class="main-header">Histórico, Cronologia e Genealogia</h1>
        <div class="highlight">
            <h3>Origens e Motivação (década de 1990)</h3>
            <p>Em 1995, a Netscape Communications Corporation, fabricante do então dominante navegador Netscape Navigator, recrutou Brendan Eich com o objetivo de implementar uma linguagem de script para o navegador. A empresa estava respondendo à necessidade de tornar as páginas web mais dinâmicas e interativas, indo além do HTML estático.</p>
            <p>Eich originalmente tinha a intenção de implementar uma versão do Scheme para o navegador, mas a Netscape fez uma parceria com a Sun Microsystems (adquirida posteriormente pela Oracle) para incluir a sintaxe da linguagem Java, que estava ganhando popularidade. Em apenas 10 dias, Eich desenvolveu o primeiro protótipo da linguagem, inicialmente chamada de Mocha, depois LiveScript, e finalmente JavaScript - uma jogada de marketing para capitalizar a popularidade do Java.</p>
        </div>
        
        <h3 class="sub-header">Cronologia e Marcos Principais</h3>
        <div class="timeline-item">
            <strong>1995 (Maio):</strong> Brendan Eich inicia o desenvolvimento da linguagem na Netscape. Em Setembro, a linguagem é renomeada para LiveScript.
        </div>
        <div class="timeline-item">
            <strong>1995 (Dezembro):</strong> A linguagem é renomeada para JavaScript e lançada no Netscape Navigator 2.0.
        </div>
        <div class="timeline-item">
            <strong>1996:</strong> A Microsoft lança o JScript no Internet Explorer 3.0, implementação similar mas com diferenças significativas.
        </div>
        <div class="timeline-item">
            <strong>1997:</strong> JavaScript é submetida à ECMA International, resultando na primeira edição do padrão ECMAScript (ES1).
        </div>
        <div class="timeline-item">
            <strong>1999:</strong> ECMAScript 3 (ES3) é lançado, introduzindo expressões regulares, tratamento de exceções e outras funcionalidades importantes.
        </div>
        <div class="timeline-item">
            <strong>2005:</strong> Surge o termo "AJAX" (Asynchronous JavaScript and XML), popularizando aplicações web dinâmicas. jQuery é langado, simplificando a manipulação DOM.
        </div>
        <div class="timeline-item">
            <strong>2009:</strong> ECMAScript 5 (ES5) é lançado, adicionando modo estrito, getters/setters, e funcionalidades para arrays. Node.js é criado por Ryan Dahl, permitindo JavaScript no servidor.
        </div>
        <div class="timeline-item">
            <strong>2015:</strong> ECMAScript 2015 (ES6) é lançado, uma grande atualização com classes, módulos, arrow functions, promises, e muitas outras funcionalidades modernas.
        </div>
        <div class="timeline-item">
            <strong>Atualmente:</strong> JavaScript continua evoluindo com lançamentos anuais do padrão ECMAScript. A linguagem expandiu-se para desenvolvimento mobile (React Native), desktop (Electron) e IoT.
        </div>
        
        <h3 class="sub-header">Genealogia</h3>
        <p>JavaScript é uma linguagem com influências diversas de várias linguagens predecessoras:</p>
        <ul>
            <li><strong>Java:</strong> Influenciou a sintaxe básica (chaves, ponto e vírgula, estruturas de controle).</li>
            <li><strong>Scheme:</strong> Influenciou as funções de primeira classe e closures.</li>
            <li><strong>Self:</strong> Influenciou o sistema baseado em protótipos para herança.</li>
            <li><strong>Perl e Python:</strong> Influenciaram as expressões regulares e alguns aspectos da sintaxe.</li>
            <li><strong>HyperTalk:</strong> Influenciou a integração com o navegador e o modelo de eventos.</li>
        </ul>
        """
    },
    {
        "titulo": "Paradigmas",
        "texto": """
        <h1 class="main-header">Paradigmas da Linguagem</h1>
        <p>JavaScript é uma linguagem <strong>multiparadigma</strong>. Isso significa que ela suporta vários estilos de programação, permitindo aos desenvolvedores escolher a abordagem mais adequada para cada problema.</p>
        
        <h3 class="sub-header">Programação Imperativa e Procedural</h3>
        <p>JavaScript suporta programação procedural tradicional com estruturas de controle (if, for, while), funções e manipulação direta de variáveis.</p>
        
        <div class="code-block">
            // Exemplo de programação procedural em JavaScript<br>
            function calcularMedia(numeros) {<br>
            &nbsp;&nbsp;&nbsp;&nbsp;let total = 0;<br>
            &nbsp;&nbsp;&nbsp;&nbsp;for (let i = 0; i < numeros.length; i++) {<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;total += numeros[i];<br>
            &nbsp;&nbsp;&nbsp;&nbsp;}<br>
            &nbsp;&nbsp;&nbsp;&nbsp;return total / numeros.length;<br>
            }
        </div>
        
        <h3 class="sub-header">Programação Orientada a Objetos (OOP)</h3>
        <p>JavaScript implementa OOP através de <strong>protótipos</strong> em vez de classes (embora a sintaxe de classe tenha sido introduzida no ES6 como açúcar sintático). Todos os objetos em JavaScript herdam propriedades e métodos de um protótipo.</p>
        
        <div class="code-block">
            // Exemplo de OOP com protótipos em JavaScript<br>
            function Animal(nome) {<br>
            &nbsp;&nbsp;&nbsp;&nbsp;this.nome = nome;<br>
            }<br>
            <br>
            Animal.prototype.fazerSom = function() {<br>
            &nbsp;&nbsp;&nbsp;&nbsp;throw new Error("Método deve ser implementado");<br>
            };<br>
            <br>
            function Cachorro(nome) {<br>
            &nbsp;&nbsp;&nbsp;&nbsp;Animal.call(this, nome);<br>
            }<br>
            <br>
            Cachorro.prototype = Object.create(Animal.prototype);<br>
            Cachorro.prototype.constructor = Cachorro;<br>
            Cachorro.prototype.fazerSom = function() {<br>
            &nbsp;&nbsp;&nbsp;&nbsp;return "Woof!";<br>
            };<br>
            <br>
            let meuPet = new Cachorro("Rex");<br>
            console.log(meuPet.fazerSom());  // Output: Woof!
        </div>
        
        <div class="code-block">
            // Exemplo com sintaxe de classe (ES6+)<br>
            class Animal {<br>
            &nbsp;&nbsp;&nbsp;&nbsp;constructor(nome) {<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;this.nome = nome;<br>
            &nbsp;&nbsp;&nbsp;&nbsp;}<br>
            <br>
            &nbsp;&nbsp;&nbsp;&nbsp;fazerSom() {<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;throw new Error("Método deve ser implementado");<br>
            &nbsp;&nbsp;&nbsp;&nbsp;}<br>
            }<br>
            <br>
            class Cachorro extends Animal {<br>
            &nbsp;&nbsp;&nbsp;&nbsp;fazerSom() {<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return "Woof!";<br>
            &nbsp;&nbsp;&nbsp;&nbsp;}<br>
            }<br>
            <br>
            let meuPet = new Cachorro("Rex");<br>
            console.log(meuPet.fazerSom());  // Output: Woof!
        </div>
        
        <h3 class="sub-header">Programação Funcional</h3>
        <p>JavaScript oferece suporte robusto a programação funcional, tratando funções como <strong>cidadãos de primeira classe</strong> (podem ser atribuídas a variáveis, passadas como argumentos e retornadas de outras funções). Inclui funções de alta ordem (map, filter, reduce) e suporte a closures.</p>
        
        <div class="code-block">
            // Programação Funcional com map e arrow functions<br>
            const numeros = [1, 2, 3, 4];<br>
            const quadrados = numeros.map(x => x ** 2);<br>
            <br>
            // Exemplo com closure<br>
            function criarContador() {<br>
            &nbsp;&nbsp;&nbsp;&nbsp;let count = 0;<br>
            &nbsp;&nbsp;&nbsp;&nbsp;return function() {<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;count += 1;<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return count;<br>
            &nbsp;&nbsp;&nbsp;&nbsp;};<br>
            }<br>
            <br>
            const contador = criarContador();<br>
            console.log(contador()); // 1<br>
            console.log(contador()); // 2
        </div>
        
        <h3 class="sub-header">Programação Baseada em Eventos</h3>
        <p>JavaScript foi projetada desde o início para lidar com eventos no navegador, como cliques de mouse, pressionamentos de tecla e carregamento de página. Este paradigma é fundamental para aplicações web interativas.</p>
        
        <div class="code-block">
            // Exemplo de programação baseada em eventos<br>
            document.getElementById("meuBotao").addEventListener("click", function() {<br>
            &nbsp;&nbsp;&nbsp;&nbsp;console.log("Botão clicado!");<br>
            &nbsp;&nbsp;&nbsp;&nbsp;// Lógica adicional aqui<br>
            });
        </div>
        """
    },
    {
        "titulo": "Características",
        "texto": """
        <h1 class="main-header">Características Mais Marcantes</h1>
        
        <h3 class="sub-header">Interpretada e de Alto Nível</h3>
        <p>JavaScript é uma linguagem interpretada (executada linha por linha) e de alto nível, abstraindo detalhes complexos de hardware e memória. Os navegadores modernos usam compilação Just-In-Time (JIT) para melhorar performance.</p>
        
        <h3 class="sub-header">Tipagem Dinâmica e Fraca</h3>
        <ul>
            <li><strong>Dinâmica:</strong> Os tipos são verificados em tempo de execução, não exigindo declaração explícita de tipo.</li>
            <li><strong>Fraca:</strong> Realiza conversão implícita de tipos entre diferentes tipos de dados, o que pode levar a comportamentos inesperados se não for bem compreendido.</li>
        </ul>
        
        <div class="code-block">
            // Exemplo de tipagem dinâmica e fraca<br>
            let x = 10;      // x é um número<br>
            x = "hello";     // agora x é uma string<br>
            <br>
            // Conversão implícita de tipos<br>
            console.log("5" + 1);    // "51" (concatenação)<br>
            console.log("5" - 1);    // 4 (subtração)
        </div>
        
        <h3 class="sub-header">Baseada em Protótipos</h3>
        <p>Diferente de linguagens baseadas em classes como Java ou C++, JavaScript usa protótipos para herança. Os objetos podem herdar propriedades e métodos diretamente de outros objetos.</p>
        
        <h3 class="sub-header">Funções de Primeira Classe e Closures</h3>
        <p>Funções em JavaScript são objetos e podem ser:</p>
        <ul>
            <li>Atribuídas a variáveis</li>
            <li>Passadas como argumentos para outras funções</li>
            <li>Retornadas como valores de outras funções</li>
            <li>Armazenadas em estruturas de dados</li>
        </ul>
        <p>Closures permitem que funções internas acessem variáveis de funções externas mesmo após a função externa ter finalizado sua execução.</p>
        
        <h3 class="sub-header">Single-Threaded com Event Loop</h3>
        <p>JavaScript é single-threaded, mas usa um mecanismo de <strong>event loop</strong> para operações assíncronas não-bloqueantes. Isso permite que o código responda a eventos enquanto processa operações demoradas em segundo plano.</p>
        
        <div class="code-block">
            // Exemplo de operação assíncrona<br>
            console.log("Início");<br>
            <br>
            setTimeout(function() {<br>
            &nbsp;&nbsp;&nbsp;&nbsp;console.log("Timeout completado");<br>
            }, 2000);<br>
            <br>
            console.log("Fim");<br>
            <br>
            // Output:<br>
            // Início<br>
            // Fim<br>
            // (após 2 segundos) Timeout completado
        </div>
        
        <h3 class="sub-header">ECMAScript e Evolução Contínua</h3>
        <p>JavaScript é implementação do padrão ECMAScript, que é atualizado anualmente com novas funcionalidades. Esta evolução constante mantém a linguagem relevante e moderna.</p>
        
        <h3 class="sub-header">Universalidade</h3>
        <p>JavaScript é a única linguagem de programação executada nativamente em todos os navegadores web modernos. Com o Node.js, expandiu-se para servidores, criando um ecossistema full-stack unificado.</p>
        
        <h3 class="sub-header">Ecossistema Rico (npm)</h3>
        <p>O Node Package Manager (npm) é o maior repositório de bibliotecas de software do mundo, com centenas de milhares de pacotes disponíveis para praticamente qualquer finalidade.</p>
        """
    },
    {
        "titulo": "Linguagens Relacionadas",
        "texto": """
        <h1 class="main-header">Linguagens Relacionadas</h1>
        
        <h3 class="sub-header">Influenciadores</h3>
        <ul>
            <li><strong>Java:</strong> Influenciou a sintaxe básica (chaves, ponto e vírgula, estruturas de controle).</li>
            <li><strong>Scheme:</strong> Influenciou as funções de primeira classe e closures.</li>
            <li><strong>Self:</strong> Influenciou o sistema baseado em protótipos para herança.</li>
            <li><strong>Perl e Python:</strong> Influenciaram as expressões regulares e alguns aspectos da sintaxe.</li>
        </ul>
        
        <h3 class="sub-header">Influenciadas</h3>
        <ul>
            <li><strong>TypeScript:</strong> Superset tipado de JavaScript desenvolvido pela Microsoft, que compila para JavaScript puro.</li>
            <li><strong>Dart:</strong> Linguagem desenvolvida pelo Google, com sintaxe similar mas tipagem mais forte, usada no framework Flutter.</li>
            <li><strong>CoffeeScript:</strong> Linguagem que compila para JavaScript, introduzindo syntax sugar para tornar o código mais conciso.</li>
            <li><strong>Kotlin:</strong> Inclui recursos inspirados no JavaScript em sua sintaxe e capacidades funcionais.</li>
        </ul>
        
        <h3 class="sub-header">Similares e Concorrentes</h3>
        <ul>
            <li><strong>Python:</strong> Ambas são linguagens dinâmicas, multiparadigma e de alto nível, mas Python é mais usado em ciência de dados e backend, enquanto JavaScript domina o front-end web.</li>
            <li><strong>Ruby:</strong> Similar em flexibilidade e expressividade, mas com filosofia diferente (convenção sobre configuração) e ecossistema mais focado no backend com Ruby on Rails.</li>
            <li><strong>PHP:</strong> Concorrente histórico no desenvolvimento web backend, mas com abordagem mais tradicional e menos orientada a eventos.</li>
            <li><strong>Dart:</strong> Concorrente direto com JavaScript, especialmente no desenvolvimento mobile com Flutter.</li>
        </ul>
        
        <h3 class="sub-header">Linguagens "Opostas" ou Complementares</h3>
        <ul>
            <li><strong>Java e C#:</strong> Linguagens estaticamente tipadas, compiladas e baseadas em classes, com filosofias mais rígidas e menos flexíveis que JavaScript.</li>
            <li><strong>Rust e Go:</strong> Linguagens compiladas com foco em performance e segurança de memória, contrastando com a natureza interpretada e gerenciada de JavaScript.</li>
            <li><strong>Elm e PureScript:</strong> Linguagens funcionais puras que compilam para JavaScript, oferecendo garantias de ausência de erros em tempo de execução.</li>
        </ul>
        """
    },
    {
        "titulo": "Conclusão",
        "texto": """
        <h1 class="main-header">Conclusão</h1>
        <div class="highlight">
            <p>JavaScript evoluiu de uma simples linguagem de script para navegadores até se tornar uma das linguagens de programação mais ubíquas e versáteis da história da computação. Seu sucesso pode ser atribuído a vários fatores: sua natureza multiparadigma que oferece flexibilidade aos desenvolvedores; a evolução constante através do padrão ECMAScript; e a expansão para além dos navegadores com tecnologias como Node.js, React Native e Electron.</p>
            
            <p>Apesar de críticas iniciais relacionadas a peculiaridades de design (como coerção de tipos e comportamento inconsistente em alguns casos), JavaScript amadureceu significativamente com as versões modernas do ECMAScript. A linguagem hoje oferece ferramentas poderosas para desenvolvimento web, mobile, desktop e até IoT.</p>
            
            <p>O ecossistema JavaScript, impulsionado pelo npm e por frameworks robustos como React, Angular e Vue, é um dos mais vibrantes e inovadores da indústria de software. JavaScript não é apenas uma linguagem de programação; é uma plataforma completa que continua a moldar o futuro do desenvolvimento de software em múltiplos domínios.</p>
        </div>
        
        <h3 class="sub-header">Apêndice A: Exemplo de Código JavaScript Moderno (ES6+)</h3>
        <div class="code-block">
            // Módulos ES6<br>
            import { apiCall } from './api.js';<br>
            <br>
            // Classes<br>
            class Person {<br>
            &nbsp;&nbsp;&nbsp;&nbsp;constructor(name, age) {<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;this.name = name;<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;this.age = age;<br>
            &nbsp;&nbsp;&nbsp;&nbsp;}<br>
            <br>
            &nbsp;&nbsp;&nbsp;&nbsp;// Arrow function como método (não recomendado para métodos de objeto)<br>
            &nbsp;&nbsp;&nbsp;&nbsp;greet = () => {<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;console.log(`Hello, my name is ${this.name}`);<br>
            &nbsp;&nbsp;&nbsp;&nbsp;}<br>
            <br>
            &nbsp;&nbsp;&nbsp;&nbsp;// Método tradicional<br>
            &nbsp;&nbsp;&nbsp;&nbsp;getBirthYear() {<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return new Date().getFullYear() - this.age;<br>
            &nbsp;&nbsp;&nbsp;&nbsp;}<br>
            }<br>
            <br>
            // Async/await para operações assíncronas<br>
            async function fetchData() {<br>
            &nbsp;&nbsp;&nbsp;&nbsp;try {<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;const response = await apiCall('https://api.example.com/data');<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;const data = await response.json();<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return data;<br>
            &nbsp;&nbsp;&nbsp;&nbsp;} catch (error) {<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;console.error('Error fetching data:', error);<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;throw error;<br>
            &nbsp;&nbsp;&nbsp;&nbsp;}<br>
            }<br>
            <br>
            // Funções de alta ordem e array methods<br>
            const numbers = [1, 2, 3, 4, 5];<br>
            const squaredEvens = numbers<br>
            &nbsp;&nbsp;&nbsp;&nbsp;.filter(n => n % 2 === 0)<br>
            &nbsp;&nbsp;&nbsp;&nbsp;.map(n => n ** 2);<br>
            <br>
            console.log(squaredEvens); // [4, 16]<br>
            <br>
            // Destructuring assignment<br>
            const person = { name: 'John', age: 30, city: 'New York' };<br>
            const { name, age } = person;<br>
            <br>
            // Spread operator<br>
            const newPerson = { ...person, country: 'USA' };
        </div>
        """
    },
    {
        "titulo": "Introdução - Comparativo",
        "texto": """
        <h1 class="main-header">Comparação: Python vs JavaScript</h1>
        <div style="text-align: center; margin-bottom: 2rem;">
            <strong>Data:</strong> 22 de Agosto de 2025 
            <br>
            <strong>Criado por:</strong> Gabriel da Silva Cassino 
            <br>
            <strong>Contribuição:</strong> Welbert Junio Afonso de Almeida 
        </div>
        <div class="highlight comparison-highlight">
            <h3 style="color: #000000;">Objetivo do Relatório</h3>
            <p style="color: #000000;">Este relatório tem como objetivo comparar as linguagens Python e JavaScript, abordando suas similaridades, diferenças na tipagem, possibilidades de integração, e o uso de JSON como ponte entre as duas linguagens. A análise focará nos aspectos técnicos que permitem o trabalho conjunto dessas tecnologias em ambientes modernos de desenvolvimento.</p>
        </div>
        """
    },
    {
        "titulo": "Similaridades",
        "texto": """
        <h1 class="main-header">Similaridades entre Python e JavaScript</h1>
        
        <div class="highlight comparison-highlight">
            <p>Python e JavaScript, apesar de terem sido criadas para propósitos inicialmente diferentes, compartilham várias características que facilitam a transição entre elas e permitem integração em projetos full-stack.</p>
        </div>
        
        <h3 class="sub-header">Características Comuns</h3>
        
        <table class="comparison-table">
            <tr>
                <th>Característica</th>
                <th>Python</th>
                <th>JavaScript</th>
            </tr>
            <tr>
                <td>Tipagem dinâmica</td>
                <td>✅</td>
                <td>✅</td>
            </tr>
            <tr>
                <td>Interpretadas</td>
                <td>✅</td>
                <td>✅</td>
            </tr>
            <tr>
                <td>Multiparadigma</td>
                <td>✅</td>
                <td>✅</td>
            </tr>
            <tr>
                <td>Funções de primeira classe</td>
                <td>✅</td>
                <td>✅</td>
            </tr>
            <tr>
                <td>Suporte a OOP</td>
                <td>✅</td>
                <td>✅ (baseada em protótipos)</td>
            </tr>
            <tr>
                <td>Programação funcional</td>
                <td>✅</td>
                <td>✅</td>
            </tr>
            <tr>
                <td>Gerenciamento automático de memória</td>
                <td>✅</td>
                <td>✅</td>
            </tr>
            <tr>
                <td>Ecossistema robusto</td>
                <td>✅ (PyPI)</td>
                <td>✅ (npm)</td>
            </tr>
        </table>
        
        <h3 class="sub-header">Sintaxes Similares</h3>
        
        <div class="code-block">
            # Python: Definição de função<br>
            def saudacao(nome):<br>
            &nbsp;&nbsp;&nbsp;&nbsp;return f"Olá, {nome}!"<br>
            <br>
            # JavaScript: Definição de função<br>
            function saudacao(nome) {<br>
            &nbsp;&nbsp;&nbsp;&nbsp;return `Olá, ${nome}!`;<br>
            }<br>
            <br>
            # Python: Estruturas de controle<br>
            for i in range(5):<br>
            &nbsp;&nbsp;&nbsp;&nbsp;print(i)<br>
            <br>
            # JavaScript: Estruturas de controle<br>
            for (let i = 0; i < 5; i++) {<br>
            &nbsp;&nbsp;&nbsp;&nbsp;console.log(i);<br>
            }
        </div>
        
        <h3 class="sub-header">Objetos e Dicionários/Objetos Literais</h3>
        
        <div class="code-block">
            # Python: Dicionário<br>
            pessoa = {<br>
            &nbsp;&nbsp;&nbsp;&nbsp;"nome": "João",<br>
            &nbsp;&nbsp;&nbsp;&nbsp;"idade": 30,<br>
            &nbsp;&nbsp;&nbsp;&nbsp;"cidade": "São Paulo"<br>
            }<br>
            <br>
            # JavaScript: Objeto literal<br>
            let pessoa = {<br>
            &nbsp;&nbsp;&nbsp;&nbsp;nome: "João",<br>
            &nbsp;&nbsp;&nbsp;&nbsp;idade: 30,<br>
            &nbsp;&nbsp;&nbsp;&nbsp;cidade: "São Paulo"<br>
            };
        </div>
        
        <div class="highlight comparison-highlight">
            <p>Essas similaridades facilitam a aprendizagem de uma segunda linguagem para desenvolvedores que já conhecem uma delas, além de permitir a criação de ferramentas que fazem a ponte entre os dois ecossistemas.</p>
        </div>
        """
    },
    {
        "titulo": "Integração JS em Python A",
        "texto": """
        <h1 class="main-header">Implementação e Aplicação de JavaScript dentro do Python</h1>
        
        <div class="highlight comparison-highlight">
            <p>Existem várias maneiras de integrar código JavaScript em ambientes Python, permitindo aproveitar o melhor de ambas as linguagens em um único projeto.</p>
        </div>
        
        <h3 class="sub-header">Bibliotecas para Executar JS em Python</h3>
        
        <div class="code-block">
            # Exemplo usando PyExecJS<br>
            import execjs<br>
            <br>
            # Executar código JavaScript<br>
            js_code = '''<br>
            function soma(a, b) {<br>
            &nbsp;&nbsp;&nbsp;&nbsp;return a + b;<br>
            }<br>
            '''<br>
            <br>
            ctx = execjs.compile(js_code)<br>
            resultado = ctx.call("soma", 5, 3)<br>
            print(resultado)  # Output: 8<br>
            <br>
            # Exemplo usando js2py<br>
            import js2py<br>
            <br>
            # Executar código JavaScript<br>
            js_code = "var x = 10; var y = 20; x + y;"<br>
            resultado = js2py.eval_js(js_code)<br>
            print(resultado)  # Output: 30<br>
            <br>
            # Criar função JavaScript e usar em Python<br>
            soma_js = js2py.eval_js("(a, b) => a + b")<br>
            print(soma_js(7, 3))  # Output: 10
        </div>
    """},
    { 
        "titulo": "Integração JS em Python B",
        "texto": """
        <h3 class="sub-header">Aplicações Práticas</h3>
        
        <ul>
            <li><strong>Server-Side Rendering (SSR):</strong> Usar motores JavaScript (como React) no servidor Python para renderização do lado do servidor.</li>
            <li><strong>Processamento de lógica front-end no backend:</strong> Validar regras de negócio escritas em JavaScript no servidor Python.</li>
            <li><strong>Conversão de bibliotecas JavaScript:</strong> Usar bibliotecas JS existentes em projetos Python sem reescrever o código.</li>
            <li><strong>Testes:</strong> Executar testes de unidades JavaScript em ambientes Python CI/CD.</li>
        </ul>
        
        <h3 class="sub-header">WebAssembly (Wasm) com Python</h3>
        
        <div class="code-block">
            # Pyodide: Python com WebAssembly no navegador<br>
            # (Este código normalmente seria executado no navegador)<br>
            '''<br>
            // Carregar Pyodide<br>
            async function main() {<br>
            &nbsp;&nbsp;&nbsp;&nbsp;let pyodide = await loadPyodide();<br>
            &nbsp;&nbsp;&nbsp;&nbsp;<br>
            &nbsp;&nbsp;&nbsp;&nbsp;// Executar código Python no navegador<br>
            &nbsp;&nbsp;&nbsp;&nbsp;pyodide.runPython(`<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;def saudacao(nome):<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return f"Olá, {nome}!"<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;print(saudacao("Mundo"))<br>
            &nbsp;&nbsp;&nbsp;&nbsp;`);<br>
            }<br>
            <br>
            main();'''
            <br>
            
        </div>
        
        <h3 class="sub-header">Node.js com Python via Subprocess</h3>
        
        <div class="code-block">
            import subprocess<br>
            import json<br>
            <br>
            # Executar script Node.js a partir do Python<br>
            script_js = '''<br>
            const data = {<br>
            &nbsp;&nbsp;&nbsp;&nbsp;nome: "João",<br>
            &nbsp;&nbsp;&nbsp;&nbsp;idade: 30<br>
            };<br>
            console.log(JSON.stringify(data));<br>
            '''
            <br>
            <br>
            with open('temp_script.js', 'w') as f:<br>
            &nbsp;&nbsp;&nbsp;&nbsp;f.write(script_js)<br>
            <br>
            resultado = subprocess.run(<br>
            &nbsp;&nbsp;&nbsp;&nbsp;['node', 'temp_script.js'],<br>
            &nbsp;&nbsp;&nbsp;&nbsp;capture_output=True,<br>
            &nbsp;&nbsp;&nbsp;&nbsp;text=True<br>
            )<br>
            <br>
            dados = json.loads(resultado.stdout)<br>
            print(dados)  # Output: {'nome': 'João', 'idade': 30}
        </div>
        
        <div class="highlight comparison-highlight">
            <p>Essas técnicas de integração permitem criar aplicações híbridas que aproveitam os pontos fortes de ambas as linguagens, como a facilidade de prototipagem do Python e a ubiquidade do JavaScript em aplicações web.</p>
        </div>
        """
    },
    {
        "titulo": "Tipagem: Python vs JS A",
        "texto": """
        <h1 class="main-header">Comparação de Tipagem: Python vs JavaScript</h1>
        
        <div class="highlight comparison-highlight">
            <p>Python e JavaScript são ambas linguagens de tipagem dinâmica, mas possuem diferenças significativas em como tratam os tipos de dados, o que pode levar a comportamentos distintos em operações similares.</p>
        </div>
        
        <h3 class="sub-header">Sistemas de Tipagem</h3>
        
        <table class="comparison-table">
            <tr>
                <th>Característica</th>
                <th>Python</th>
                <th>JavaScript</th>
            </tr>
            <tr>
                <td>Tipagem</td>
                <td>Dinâmica e Forte</td>
                <td>Dinâmica e Fraca</td>
            </tr>
            <tr>
                <td>Verificação de tipos</td>
                <td>Em tempo de execução</td>
                <td>Em tempo de execução</td>
            </tr>
            <tr>
                <td>Conversão implícita</td>
                <td>Pouca (forte)</td>
                <td>Extensa (fraca)</td>
            </tr>
            <tr>
                <td>Tipos primitivos</td>
                <td>int, float, bool, str, None</td>
                <td>number, string, boolean, null, undefined, symbol, bigint</td>
            </tr>
        </table>
        
        <h3 class="sub-header">Diferenças Comportamentais</h3>
        
        <div class="code-block">
            # Python: Tipagem forte - poucas conversões implícitas<br>
            print("10" + 5)  # TypeError: can only concatenate str to str<br>
            print(10 + "5")  # TypeError: unsupported operand type(s)<br>
            <br>
            # JavaScript: Tipagem fraca - muitas conversões implícitas<br>
            console.log("10" + 5);  // "105" (concatenação)<br>
            console.log(10 + "5");  // "105" (concatenação)<br>
            console.log("10" - 5);  // 5 (subtração)<br>
            console.log(10 - "5");  // 5 (subtração)<br>
            <br>
            # Python: Comparação de valores e tipos<br>
            print(0 == False)   # False (tipos diferentes)<br>
            print(1 == True)    # False (tipos diferentes)<br>
            print("" == False)  # False (tipos diferentes)<br>
            <br>
            # JavaScript: Comparação com conversão implícita<br>
            console.log(0 == false);  // true<br>
            console.log(1 == true);   // true<br>
            console.log("" == false); // true<br>
            <br>
            # Python: Comparação estrita (sempre por valor e tipo)<br>
            print(0 == False)  # False<br>
            print(0 is False)  # False<br>
            <br>
            # JavaScript: Comparação estrita (===) vs solta (==)<br>
            console.log(0 == false);   // true (comparação solta)<br>
            console.log(0 === false);  // false (comparação estrita)
        </div>
        """
    },
    {
        "titulo": "Tipagem: Python vs JS B",
        "texto": """
        <h3 class="sub-header">Valores "Falsy"</h3>
        
        <div class="code-block">
            # Python: Valores avaliados como False<br>
            False, None, 0, 0.0, "", [], {}, set()<br>
            <br>
            # JavaScript: Valores "falsy"<br>
            false, null, undefined, 0, NaN, "" (string vazia)<br>
            <br>
            # Python: Lista vazia é falsy<br>
            lista = []<br>
            if not lista:<br>
            &nbsp;&nbsp;&nbsp;&nbsp;print("Lista vazia")  # Executa<br>
            <br>
            # JavaScript: Array vazio é truthy<br>
            let array = [];<br>
            if (!array) {<br>
            &nbsp;&nbsp;&nbsp;&nbsp;console.log("Array vazio");  // Não executa<br>
            }<br>
            if (array.length === 0) {<br>
            &nbsp;&nbsp;&nbsp;&nbsp;console.log("Array vazio");  // Executa<br>
            }
        </div>
        
        <div class="highlight comparison-highlight">
            <p>Estas diferenças no sistema de tipagem são uma das principais fontes de erros para desenvolvedores que trabalham com ambas as linguagens. É importante entender essas nuances para escrever código robusto e evitar comportamentos inesperados.</p>
        </div>
        """
    },
    {
        "titulo": "Tratamento de Tipagens A",
        "texto": """
        <h1 class="main-header">Tratamento de Tipagens entre Python e JavaScript</h1>
        
        <div class="highlight comparison-highlight">
            <p>Ao integrar Python e JavaScript, é essencial entender como os tipos de dados são convertidos entre as duas linguagens, especialmente ao usar formatos de intercâmbio como JSON.</p>
        </div>
        
        <h3 class="sub-header">Conversão de Tipos via JSON</h3>
        
        <div class="code-block">
            # Python para JavaScript via JSON<br>
            import json<br>
            <br>
            dados_python = {<br>
            &nbsp;&nbsp;&nbsp;&nbsp;"nome": "João",<br>
            &nbsp;&nbsp;&nbsp;&nbsp;"idade": 30,<br>
            &nbsp;&nbsp;&nbsp;&nbsp;"ativo": True,<br>
            &nbsp;&nbsp;&nbsp;&nbsp;"filhos": ["Maria", "Pedro"],<br>
            &nbsp;&nbsp;&nbsp;&nbsp;"endereco": {<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"rua": "Rua A",<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"numero": 123<br>
            &nbsp;&nbsp;&nbsp;&nbsp;},<br>
            &nbsp;&nbsp;&nbsp;&nbsp;"salario": None<br>
            }<br>
            <br>
            # Converter para JSON (string)<br>
            json_str = json.dumps(dados_python)<br>
            print(json_str)<br>
            # '{"nome": "João", "idade": 30, "ativo": true, "filhos": ["Maria", "Pedro"], "endereco": {"rua": "Rua A", "numero": 123}, "salario": null}'<br>
            <br>
            # JavaScript: Receber e converter JSON<br>
            <br>
            'let jsonStr = '{"nome": "João", "idade": 30, "ativo": true, "filhos": ["Maria", "Pedro"], "endereco": {"rua": "Rua A", "numero": 123}, "salario": null}';<br>
            <br>
            let dadosJavaScript = JSON.parse(jsonStr);<br>
            console.log(dadosJavaScript.nome);    // "João"<br>
            console.log(dadosJavaScript.idade);   // 30<br>
            console.log(dadosJavaScript.ativo);   // true<br>
            console.log(dadosJavaScript.filhos);  // ["Maria", "Pedro"]<br>
            console.log(dadosJavaScript.salario); // null<br>
            '
        </div>
        """
    },
    {
        "titulo": "Tratamento de Tipagens B",
        "texto": """
        <h3 class="sub-header">Mapeamento de Tipos</h3>
        
        <table class="comparison-table">
            <tr>
                <th>Tipo Python</th>
                <th>Tipo JSON</th>
                <th>Tipo JavaScript</th>
            </tr>
            <tr>
                <td>dict</td>
                <td>object</td>
                <td>Object</td>
            </tr>
            <tr>
                <td>list, tuple</td>
                <td>array</td>
                <td>Array</td>
            </tr>
            <tr>
                <td>str</td>
                <td>string</td>
                <td>string</td>
            </tr>
            <tr>
                <td>int, float</td>
                <td>number</td>
                <td>number</td>
            </tr>
            <tr>
                <td>True</td>
                <td>true</td>
                <td>true</td>
            </tr>
            <tr>
                <td>False</td>
                <td>false</td>
                <td>false</td>
            </tr>
            <tr>
                <td>None</td>
                <td>null</td>
                <td>null</td>
            </tr>
        </table>
        
        <h3 class="sub-header">Tipos Não Suportados no JSON</h3>
        
        <div class="code-block">
            # Python: Tipos que não têm equivalente direto em JSON<br>
            dados_complexos = {<br>
            &nbsp;&nbsp;&nbsp;&nbsp;"data": datetime.now(),         # datetime<br>
            &nbsp;&nbsp;&nbsp;&nbsp;"set": {1, 2, 3},               # set<br>
            &nbsp;&nbsp;&nbsp;&nbsp;"funcao": lambda x: x * 2,      # function<br>
            &nbsp;&nbsp;&nbsp;&nbsp;"decimal": Decimal('10.5')      # Decimal<br>
            }<br>
            <br>
            # Tentativa de serialização resultará em erro<br>
            # json.dumps(dados_complexos)  # TypeError<br>
            <br>
            # Solução: Criar serializador personalizado<br>
            def serializador_personalizado(obj):<br>
            &nbsp;&nbsp;&nbsp;&nbsp;if isinstance(obj, datetime):<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return obj.isoformat()<br>
            &nbsp;&nbsp;&nbsp;&nbsp;elif isinstance(obj, set):<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return list(obj)<br>
            &nbsp;&nbsp;&nbsp;&nbsp;elif hasattr(obj, '__dict__'):<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return obj.__dict__<br>
            &nbsp;&nbsp;&nbsp;&nbsp;else:<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;raise TypeError(f"Objeto do tipo {type(obj)} não é serializável")<br>
            <br>
            # Serializar com o serializador personalizado<br>
            json_str = json.dumps(dados_complexos, default=serializador_personalizado)<br>
            print(json_str)
        </div>
        
        <h3 class="sub-header">Bibliotecas para Melhor Manipulação de Tipos</h3>
        
        <ul>
            <li><strong>Pydantic:</strong> Validação de dados e manipulação de tipos em Python, muito útil para APIs.</li>
            <li><strong>Marshmallow:</strong> Biblioteca para serialização e desserialização de objetos.</li>
            <li><strong>TypeScript:</strong> Superset tipado de JavaScript que ajuda a evitar problemas de tipagem.</li>
            <li><strong>Joi/Yup:</strong> Bibliotecas JavaScript para validação de esquemas de dados.</li>
        </ul>
        
        <div class="highlight comparison-highlight">
            <p>O entendimento das diferenças de tipagem e a implementação de estratégias adequadas de serialização/desserialização são cruciais para a integração eficiente entre Python e JavaScript em aplicações modernas.</p>
        </div>
        """
    },
    {
        "titulo": "Apêndice: JSON A",
        "texto": """
        <h1 class="main-header">Apêndice: JSON na Gestão de Dicionários e Leitura/Escrita</h1>
        
        <div class="highlight comparison-highlight">
            <p>JSON (JavaScript Object Notation) tornou-se o formato padrão para intercâmbio de dados entre Python e JavaScript, servindo como uma ponte eficiente entre as duas linguagens.</p>
        </div>
        
        <h3 class="sub-header">JSON como Ponte entre Python e JavaScript</h3>
        
        <div class="code-block">
            # Python: Dicionário para JSON<br>
            import json<br>
            <br>
            dados = {<br>
            &nbsp;&nbsp;&nbsp;&nbsp;"usuario": "joao123",<br>
            &nbsp;&nbsp;&nbsp;&nbsp;"email": "joao@email.com",<br>
            &nbsp;&nbsp;&nbsp;&nbsp;"ativo": True,<br>
            &nbsp;&nbsp;&nbsp;&nbsp;"tags": ["python", "javascript", "json"],<br>
            &nbsp;&nbsp;&nbsp;&nbsp;"preferences": {<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"tema": "escuro",<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"notificacoes": True<br>
            &nbsp;&nbsp;&nbsp;&nbsp;}<br>
            }<br>
            <br>
            # Serializar (Python para JSON string)<br>
            json_string = json.dumps(dados, indent=2)<br>
            print(json_string)<br>
            <br>
            # Desserializar (JSON string para Python)<br>
            dados_carregados = json.loads(json_string)<br>
            print(dados_carregados["usuario"])  # joao123<br>
            <br>
            # JavaScript equivalente:<br>
            <br>
            '// Desserializar (JSON string para JavaScript)<br>
            let jsonString = `{<br>
            &nbsp;&nbsp;"usuario": "joao123",<br>
            &nbsp;&nbsp;"email": "joao@email.com",<br>
            &nbsp;&nbsp;"ativo": true,<br>
            &nbsp;&nbsp;"tags": ["python", "javascript", "json"],<br>
            &nbsp;&nbsp;"preferences": {<br>
            &nbsp;&nbsp;&nbsp;&nbsp;"tema": "escuro",<br>
            &nbsp;&nbsp;&nbsp;&nbsp;"notificacoes": true<br>
            &nbsp;&nbsp;}<br>
            }`;<br>
            <br>
            let dadosJS = JSON.parse(jsonString);<br>
            console.log(dadosJS.usuario);  // joao123<br>
            <br>
            // Serializar (JavaScript para JSON string)<br>
            let novaJsonString = JSON.stringify(dadosJS, null, 2);<br>
            console.log(novaJsonString);'
            <br>
            
        </div>"""
    },
    {
        "titulo": "Apêndice: JSON B",
        "texto": """
        <h3 class="sub-header">Leitura e Escrita de Arquivos JSON</h3>
        
        <div class="code-block">
            # Python: Escrever dados em arquivo JSON<br>
            dados = {<br>
            &nbsp;&nbsp;&nbsp;&nbsp;"produtos": [<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{"id": 1, "nome": "Teclado", "preco": 99.90},<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{"id": 2, "nome": "Mouse", "preco": 49.90},<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{"id": 3, "nome": "Monitor", "preco": 899.90}<br>
            &nbsp;&nbsp;&nbsp;&nbsp;]<br>
            }<br>
            <br>
            with open("produtos.json", "w", encoding="utf-8") as arquivo:<br>
            &nbsp;&nbsp;&nbsp;&nbsp;json.dump(dados, arquivo, indent=2, ensure_ascii=False)<br>
            <br>
            # Ler dados de arquivo JSON<br>
            with open("produtos.json", "r", encoding="utf-8") as arquivo:<br>
            &nbsp;&nbsp;&nbsp;&nbsp;dados_carregados = json.load(arquivo)<br>
            <br>
            for produto in dados_carregados["produtos"]:<br>
            &nbsp;&nbsp;&nbsp;&nbsp;print(f"{produto['nome']}: R$ {produto['preco']}")<br>
            <br>
            # JavaScript equivalente (Node.js):<br>
            '<br>
            const fs = require('fs');<br>
            <br>
            // Escrever dados em arquivo JSON<br>
            let dados = {<br>
            &nbsp;&nbsp;produtos: [<br>
            &nbsp;&nbsp;&nbsp;&nbsp;{id: 1, nome: "Teclado", preco: 99.90},<br>
            &nbsp;&nbsp;&nbsp;&nbsp;{id: 2, nome: "Mouse", preco: 49.90},<br>
            &nbsp;&nbsp;&nbsp;&nbsp;{id: 3, nome: "Monitor", preco: 899.90}<br>
            &nbsp;&nbsp;]<br>
            };<br>
            <br>
            fs.writeFileSync('produtos.json', JSON.stringify(dados, null, 2));<br>
            <br>
            // Ler dados de arquivo JSON<br>
            let dadosCarregados = JSON.parse(fs.readFileSync('produtos.json', 'utf8'));<br>
            <br>
            dadosCarregados.produtos.forEach(produto => {<br>
            &nbsp;&nbsp;console.log(`${produto.nome}: R$ ${produto.preco}`);<br>
            });'<br>
            
        </div>"""
    },
    {
        "titulo": "Apêndice: JSON C",
        "texto": """
        <h3 class="sub-header">Manipulação Avançada de JSON</h3>
        
        <div class="code-block">
            # Python: Manipulação avançada com json<br>
            import json<br>
            from json import JSONEncoder<br>
            from datetime import datetime<br>
            <br>
            # Classe personalizada<br>
            class Usuario:<br>
            &nbsp;&nbsp;&nbsp;&nbsp;def __init__(self, nome, email, data_criacao=None):<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;self.nome = nome<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;self.email = email<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;self.data_criacao = data_criacao or datetime.now()<br>
            <br>
            &nbsp;&nbsp;&nbsp;&nbsp;def __repr__(self):<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return f"Usuario(nome={self.nome}, email={self.email})"<br>
            <br>
            # Encoder personalizado<br>
            class UsuarioEncoder(JSONEncoder):<br>
            &nbsp;&nbsp;&nbsp;&nbsp;def default(self, obj):<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if isinstance(obj, Usuario):<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return {<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"nome": obj.nome,<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"email": obj.email,<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"data_criacao": obj.data_criacao.isoformat()<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return super().default(obj)<br>
            <br>
            # Decoder personalizado<br>
            def usuario_decoder(dct):<br>
            &nbsp;&nbsp;&nbsp;&nbsp;if all(key in dct for key in ['nome', 'email', 'data_criacao']):<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return Usuario(<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;dct['nome'],<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;dct['email'],<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;datetime.fromisoformat(dct['data_criacao'])<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;)<br>
            &nbsp;&nbsp;&nbsp;&nbsp;return dct<br>
            <br>
            # Uso do encoder e decoder personalizados<br>
            usuario = Usuario("Maria", "maria@email.com")<br>
            <br>
            # Serializar com encoder personalizado<br>
            json_str = json.dumps(usuario, cls=UsuarioEncoder)<br>
            print(json_str)<br>
            <br>
            # Desserializar com decoder personalizado<br>
            usuario_carregado = json.loads(json_str, object_hook=usuario_decoder)<br>
            print(usuario_carregado)  # Usuario(nome=Maria, email=maria@email.com)
        </div>
        
        <div class="highlight comparison-highlight">
            <p>JSON não apenas facilita a comunicação entre Python e JavaScript, mas também se tornou um padrão universal para intercâmbio de dados, armazenamento de configurações e persistência de dados simples em ambas as linguagens.</p>
        </div>
        """
    },{
        "titulo": "Bibliografia A",
        "texto": """
        <h1 class="main-header">Bibliografia</h1>
        <div class="highlight">
            <h3>Fontes Consultadas - Python</h3>
        </div>
        
        <h3 class="sub-header">Livros</h3>
        <ul>
            <li>Lutz, M. (2013). Learning Python. O'Reilly Media.</li>
            <li>Beazley, D. M. (2009). Python Essential Reference. Addison-Wesley Professional.</li>
            <li>Ramalho, L. (2015). Fluent Python. O'Reilly Media.</li>
            <li>Van Rossum, G., Drake, F. L., & Python Development Team. (2011). The Python Language Reference.</li>
        </ul>
        
        <h3 class="sub-header">Documentação Oficial</h3>
        <ul>
            <li>Python Software Foundation. (2023). The Python Tutorial. https://docs.python.org/3/tutorial/</li>
            <li>Python Software Foundation. (2023). The Python Language Reference. https://docs.python.org/3/reference/</li>
            <li>Python Software Foundation. (2023). The Python Standard Library. https://docs.python.org/3/library/</li>
        </ul>
        
        <h3 class="sub-header">Artigos e Publicações Acadêmicas</h3>
        <ul>
            <li>Van Rossum, G. (1995). Python Reference Manual. CWI Report CS-R9525.</li>
            <li>Van Rossum, G. (2007). A Brief Timeline of Python. The History of Python Blog.</li>
            <li>Prechelt, L. (2000). An empirical comparison of C, C++, Java, Perl, Python, Rexx, and Tcl. IEEE Computer, 33(10), 23-29.</li>
        </ul>
        
        <h3 class="sub-header">Sites e Recursos Online</h3>
        <ul>
            <li>Python.org: https://www.python.org/</li>
            <li>Real Python: https://realpython.com/</li>
            <li>The Python Package Index (PyPI): https://pypi.org/</li>
            <li>Python Wiki: https://wiki.python.org/moin/</li>
            <li>Stack Overflow: https://stackoverflow.com/questions/tagged/python</li>
            <li>GitHub Python Trending Repositories: https://github.com/trending/python</li>
        </ul>
        
        <h3 class="sub-header">Vídeos e Palestras</h3>
        <ul>
            <li>Van Rossum, G. (2016). The History of Python. PyCon 2016.</li>
            <li>Warsaw, B. (2018). How Python Was Shaped by leaky internals. PyCon 2018.</li>
            <li>Beazley, D. (2015). Python Concurrency From the Ground Up. PyCon 2015.</li>
        </ul>
        """
    },
    {
        "titulo": "Bibliografia B",
        "texto": """
        <h1 class="main-header">Bibliografia</h1>
        <div class="highlight">
            <h3>Fontes Consultadas - Javascript</h3>
        </div>
        
        <h3 class="sub-header">Livros</h3>
        <ul>
            <li>Haverbeke, M. (2018). Eloquent JavaScript: A Modern Introduction to Programming. No Starch Press.</li>
            <li>Simpson, K. (2015). You Don't Know JS (Série de 6 livros). O'Reilly Media.</li>
            <li>Flanagan, D. (2020). JavaScript: The Definitive Guide. O'Reilly Media.</li>
            <li>Crockford, D. (2008). JavaScript: The Good Parts. O'Reilly Media.</li>
        </ul>
        
        <h3 class="sub-header">Documentação Oficial e Especificações</h3>
        <ul>
            <li>ECMA International. (2023). ECMAScript® 2023 Language Specification. https://tc39.es/ecma262/</li>
            <li>Mozilla Developer Network (MDN). (2023). JavaScript Reference. https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference</li>
            <li>Node.js Foundation. (2023). Node.js Documentation. https://nodejs.org/en/docs/</li>
        </ul>
        
        <h3 class="sub-header">Artigos e Publicações Acadêmicas</h3>
        <ul>
            <li>Eich, B. (1998). JavaScript at Ten Years. Proceedings of the Third ACM SIGPLAN Conference on History of Programming Languages.</li>
            <li>Vogels, W. (2020). The Evolution of JavaScript: From Browser Scripting to Full-Stack Development. Journal of Web Engineering, 19(3), 245-268.</li>
            <li>Zakas, N. C. (2012). The Evolution of JavaScript: How ECMAScript 6 is Shaping the Future of the Language. ACM Queue, 10(9), 20-33.</li>
        </ul>
        
        <h3 class="sub-header">Sites e Recursos Online</h3>
        <ul>
            <li>JavaScript.info: https://javascript.info/</li>
            <li>freeCodeCamp JavaScript Curriculum: https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/</li>
            <li>Stack Overflow JavaScript Tag: https://stackoverflow.com/questions/tagged/javascript</li>
            <li>State of JS (Pesquisa Anual): https://stateofjs.com/</li>
            <li>npm: https://www.npmjs.com/</li>
            <li>GitHub JavaScript Trending Repositories: https://github.com/trending/javascript</li>
        </ul>
        
        <h3 class="sub-header">Vídeos e Palestras</h3>
        <ul>
            <li>Eich, B. (2016). The History of JavaScript. JSConf EU 2016.</li>
            <li>Dahl, R. (2018). Original Node.js Presentation. JSConf EU 2018.</li>
            <li>Hevery, M. (2010). JavaScript Patterns. Google Tech Talks.</li>
            <li>Resig, J. (2007). The DOM is a Mess. Yahoo! Theater.</li>
        </ul>
        """
    },
    {
        "titulo": "Bibliografia C",
        "texto": """
        <h1 class="main-header">Bibliografia - Comparativo</h1>
        <div class="highlight">
            <h3>Fontes Consultadas</h3>
        </div>
        
        <h3 class="sub-header">Livros</h3>
        <ul>
            <li>Flanagan, D. (2020). JavaScript: The Definitive Guide. O'Reilly Media.</li>
            <li>Lutz, M. (2013). Learning Python. O'Reilly Media.</li>
            <li>Haverbeke, M. (2018). Eloquent JavaScript: A Modern Introduction to Programming. No Starch Press.</li>
            <li>Ramalho, L. (2015). Fluent Python. O'Reilly Media.</li>
            <li>Simpson, K. (2015). You Don't Know JS (Série de 6 livros). O'Reilly Media.</li>
        </ul>
        
        <h3 class="sub-header">Documentação Oficial</h3>
        <ul>
            <li>Python Software Foundation. (2023). Python Documentation. https://docs.python.org/3/</li>
            <li>Mozilla Developer Network (MDN). (2023). JavaScript Reference. https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference</li>
            <li>ECMA International. (2023). ECMAScript® 2023 Language Specification. https://tc39.es/ecma262/</li>
            <li>JSON.org. (2023). Introducing JSON. https://www.json.org/json-en.html</li>
        </ul>
        
        <h3 class="sub-header">Artigos e Tutoriais</h3>
        <ul>
            <li>Real Python. (2023). Working With JSON Data in Python. https://realpython.com/python-json/</li>
            <li>JavaScript.info. (2023). JSON methods, toJSON. https://javascript.info/json</li>
            <li>GeeksforGeeks. (2023). Difference between Python and JavaScript. https://www.geeksforgeeks.org/difference-between-python-and-javascript/</li>
            <li>Stack Overflow. (2023). How to run JavaScript code in Python? https://stackoverflow.com/questions/26924268/how-to-run-javascript-code-in-python</li>
        </ul>
        
        <h3 class="sub-header">Ferramentas e Bibliotecas</h3>
        <ul>
            <li>PyExecJS Documentation. https://pypi.org/project/PyExecJS/</li>
            <li>js2py Documentation. https://pypi.org/project/Js2Py/</li>
            <li>Pyodide Documentation. https://pyodide.org/</li>
            <li>Pydantic Documentation. https://pydantic-docs.helpmanual.io/</li>
        </ul>
        
        <h3 class="sub-header">Vídeos e Palestras</h3>
        <ul>
            <li>Eich, B. (2016). The History of JavaScript. JSConf EU 2016.</li>
            <li>Van Rossum, G. (2016). The History of Python. PyCon 2016.</li>
            <li>Petkov, M. (2020). JavaScript vs Python - Which Should You Learn? (YouTube).</li>
            <li>McKinney, W. (2019). Python and JavaScript: Better Together. PyData Conference.</li>
        </ul>
        
        <h3 class="sub-header">Repositórios e Exemplos de Código</h3>
        <ul>
            <li>GitHub - Python and JavaScript Integration Examples. https://github.com/topics/python-javascript</li>
            <li>GitHub - JSON Schema Specifications. https://github.com/json-schema-org/json-schema-spec</li>
            <li>npm - JavaScript Packages for Python Integration. https://www.npmjs.com/search?q=python</li>
            <li>PyPI - Python Packages for JavaScript Integration. https://pypi.org/search/?q=javascript</li>
        </ul>
        """
    },
    {
        "titulo": "Agradecimentos",
        "texto": """
            <div class="final-thanks">
            Muito Obrigado a todos!
            </div>


        """
    }
]


# Estado da página atual
if "page_index" not in st.session_state:
    st.session_state.page_index = 0
    
# teste ------> há erros se ativo
# set_title=[topic for topic in sections["título"]]
# options = st.sidebar.selectbox("Tópicos",set_title)
#-------------> trecho inativo por enquanto 

# Renderiza conteúdo da seção atual
current_section = sections[st.session_state.page_index]
st.markdown(current_section["texto"], unsafe_allow_html=True)

#-----------------------------------------------------> Teste de Interface 
# --- Rodapé com navegação ---
col1, col2, col3, col4 = st.columns([1, 2, 2, 1])

with col1:
    if st.session_state.page_index > 0:
        if st.button("⬅️ Anterior"):
            st.session_state.page_index -= 1
            st.rerun()

with col2:
    st.write(f"📄 Página {st.session_state.page_index+1} de {len(sections)}")

with col3:
    go_page=st.number_input("N° página",
                            value=st.session_state.page_index+1,
                           min_value=1,
                           max_value=27,
                           step=1)
    if ((go_page) > 0 and 
        (go_page)< (len(sections)+1)
        and ((go_page-1)!=st.session_state.page_index)):
        if st.button(f"Ir ➡️ para página {go_page}"):
            st.session_state.page_index=(go_page-1)
            st.rerun()
with col4:
    if st.session_state.page_index < len(sections)-1:
        if st.button("Próximo ➡️"):
            st.session_state.page_index += 1
            st.rerun()
#-----------------------------------------------------> Teste de Interface 

# Rodapé final
st.markdown("""
<div class="footer">
    <p>Relatório Técnico: Python & JavaScript - Desenvolvido com Streamlit</p>
    <p>Última atualização: 23 de Agosto de 2025</p>
</div>
""", unsafe_allow_html=True)
