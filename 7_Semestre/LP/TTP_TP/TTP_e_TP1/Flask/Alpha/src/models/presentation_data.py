"""
Classe que contém todos os dados da apresentação sobre Python e JavaScript.
Aplica paradigmas de POO e características marcantes do Python.
"""

from typing import Dict, List, Any
from dataclasses import dataclass
from functools import lru_cache


@dataclass
class SlideData:
    """Classe para representar dados de um slide"""
    title: str
    content: str
    code_examples: List[str] = None
    highlights: List[str] = None

    def __post_init__(self):
        if self.code_examples is None:
            self.code_examples = []
        if self.highlights is None:
            self.highlights = []


class PresentationData:
    """
    Classe principal que contém todos os dados da apresentação.
    Demonstra uso de POO, encapsulamento e métodos organizados.
    """

    def __init__(self):
        """Inicializa a classe com dados estruturados"""
        self._initialize_data()

    def _initialize_data(self):
        """Método privado para inicializar os dados (encapsulamento)"""
        self._python_data = self._create_python_data()
        self._javascript_data = self._create_javascript_data()
        self._general_data = self._create_general_data()

    @lru_cache(maxsize=None)
    def get_python_intro(self) -> Dict[str, Any]:
        """Retorna dados da introdução ao Python (uso de cache para otimização)"""
        return {
            'title': 'Python',
            'subtitle': 'Uma linguagem versátil e poderosa',
            'description': '''Python é uma das linguagens de programação mais populares e versáteis da atualidade.
                           Criada por Guido van Rossum no final da década de 1980, Python se destaca por sua
                           sintaxe clara, legibilidade e filosofia de design que prioriza a simplicidade.''',
            'key_points': [
                'Linguagem interpretada e de alto nível',
                'Multiparadigma (POO, Funcional, Imperativa)',
                'Sintaxe clara e legível',
                'Vasta biblioteca padrão',
                'Comunidade ativa e ecossistema rico'
            ]
        }

    def get_python_historico(self) -> Dict[str, Any]:
        """Retorna dados do histórico do Python"""
        return self._python_data['historico']

    def get_python_paradigmas(self) -> Dict[str, Any]:
        """Retorna dados dos paradigmas do Python"""
        return self._python_data['paradigmas']

    def get_python_caracteristicas(self) -> Dict[str, Any]:
        """Retorna características do Python"""
        return self._python_data['caracteristicas']

    def get_python_linguagens_relacionadas(self) -> Dict[str, Any]:
        """Retorna linguagens relacionadas ao Python"""
        return self._python_data['linguagens_relacionadas']

    def get_python_exemplos(self) -> Dict[str, Any]:
        """Retorna exemplos de código Python"""
        return self._python_data['exemplos']

    def get_python_arquitetura(self) -> Dict[str, Any]:
        """Retorna dados da arquitetura do Python"""
        return self._python_data['arquitetura']

    def get_javascript_intro(self) -> Dict[str, Any]:
        """Retorna dados da introdução ao JavaScript"""
        return {
            'title': 'JavaScript',
            'subtitle': 'A linguagem ubíqua da web moderna',
            'description': '''JavaScript é a linguagem de programação mais utilizada no mundo, criada em 1995
                       por Brendan Eich. Originalmente desenvolvida para adicionar interatividade às páginas web,
                       evoluiu para uma linguagem full-stack que domina a web, servidores, aplicações móveis,
                       desktop e até IoT.''',
            'key_points': [
                'Linguagem interpretada com compilação JIT',
                'Multiparadigma: funcional, baseada em protótipos, orientada a eventos',
                'Única linguagem nativa dos navegadores web',
                'Ecossistema gigantesco (npm) com mais de 1.5 milhão de pacotes',
                'Padrão ECMAScript com evolução anual contínua',
                'Modelo de execução single-threaded com Event Loop',
                'Programação assíncrona não-bloqueante nativa',
                'Tipagem dinâmica e fraca com TypeScript opcional',
                'Comunidade global extremamente ativa e inovadora',
                'Demanda de mercado ubíqua em todas as áreas de desenvolvimento'
            ]
        }

    def get_javascript_historico(self) -> Dict[str, Any]:
        """Retorna dados do histórico do JavaScript"""
        return self._javascript_data['historico']

    def get_javascript_paradigmas(self) -> Dict[str, Any]:
        """Retorna dados dos paradigmas do JavaScript"""
        return self._javascript_data['paradigmas']

    def get_javascript_caracteristicas(self) -> Dict[str, Any]:
        """Retorna características do JavaScript"""
        return self._javascript_data['caracteristicas']

    def get_javascript_linguagens_relacionadas(self) -> Dict[str, Any]:
        """Retorna linguagens relacionadas ao JavaScript"""
        return self._javascript_data['linguagens_relacionadas']

    def get_javascript_exemplos(self) -> Dict[str, Any]:
        """Retorna exemplos de código JavaScript"""
        return self._javascript_data['exemplos']

    def get_consideracoes_finais(self) -> Dict[str, Any]:
        """Retorna considerações finais"""
        return self._general_data['consideracoes_finais']

    def get_bibliografia(self) -> Dict[str, Any]:
        """Retorna bibliografia"""
        return self._general_data['bibliografia']

    def _create_python_data(self) -> Dict[str, Any]:
        """Cria dados estruturados sobre Python (método privado)"""
        return {
            'historico': {
                'title': 'Histórico do Python',
                'timeline': [
                    {'year': '1989', 'event': 'Início do desenvolvimento por Guido van Rossum'},
                    {'year': '1991', 'event': 'Python 0.9.1 - Primeira versão pública'},
                    {'year': '1994', 'event': 'Python 1.0 - Ferramentas de programação funcional'},
                    {'year': '2000', 'event': 'Python 2.0 - List comprehensions e Unicode'},
                    {'year': '2008', 'event': 'Python 3.0 - Versão incompatível com Python 2'},
                    {'year': '2020', 'event': 'Fim do suporte ao Python 2'}
                ],
                'creator': 'Guido van Rossum',
                'origin': 'Centrum Wiskunde & Informatica (CWI), Holanda',
                'inspiration': 'Linguagem ABC e grupo de comédia Monty Python'
            },
            'paradigmas': {
                'title': 'Paradigmas de Programação',
                'paradigms': [
                    {
                        'name': 'Orientação a Objetos',
                        'description': 'Tudo em Python é um objeto. Suporte completo a POO.',
                        'features': ['Classes', 'Herança', 'Polimorfismo', 'Encapsulamento']
                    },
                    {
                        'name': 'Programação Imperativa/Procedural',
                        'description': 'Execução sequencial de instruções.',
                        'features': ['Funções', 'Módulos', 'Controle de fluxo']
                    },
                    {
                        'name': 'Programação Funcional',
                        'description': 'Funções como objetos de primeira classe.',
                        'features': ['Lambda', 'Map/Filter/Reduce', 'List comprehensions']
                    }
                ]
            },
            'caracteristicas': {
                'title': 'Características Marcantes',
                'features': [
                    {
                        'name': 'Simplicidade e Legibilidade',
                        'description': 'Sintaxe clara usando indentação para blocos'
                    },
                    {
                        'name': 'Alto Nível',
                        'description': 'Abstrai detalhes de baixo nível da máquina'
                    },
                    {
                        'name': 'Interpretada',
                        'description': 'Execução linha por linha pelo interpretador'
                    },
                    {
                        'name': 'Tipagem Dinâmica e Forte',
                        'description': 'Tipos verificados em tempo de execução'
                    },
                    {
                        'name': 'Biblioteca Padrão Rica',
                        'description': 'Filosofia "Batteries Included"'
                    },
                    {
                        'name': 'Multiplataforma',
                        'description': 'Executa em Windows, macOS, Linux'
                    }
                ]
            },
            'linguagens_relacionadas': {
                'title': 'Linguagens Relacionadas',
                'influences': [
                    {'name': 'ABC', 'type': 'Influenciou', 'description': 'Predecessor direto, indentação'},
                    {'name': 'Modula-3', 'type': 'Influenciou', 'description': 'Sistema de módulos'},
                    {'name': 'C', 'type': 'Influenciou', 'description': 'Base do interpretador CPython'},
                    {'name': 'Lisp', 'type': 'Influenciou', 'description': 'Programação funcional'},
                    {'name': 'SETL/Haskell', 'type': 'Influenciou', 'description': 'List comprehensions'}
                ],
                'influenced': [
                    {'name': 'Boo', 'description': 'Sintaxe similar ao Python'},
                    {'name': 'Cobra', 'description': 'Inspirado na legibilidade do Python'},
                    {'name': 'Swift', 'description': 'Clareza e acessibilidade'}
                ]
            },
            'exemplos': {
                'title': 'Exemplos de Código Python',
                'examples': [
                    {
                        'name': 'Olá, Mundo!',
                        'code': 'print("Olá, Mundo!")',
                        'description': 'O programa mais básico'
                    },
                    {
                        'name': 'Soma de Números',
                        'code': '''num1 = float(input("Digite o primeiro número: "))
num2 = float(input("Digite o segundo número: "))
soma = num1 + num2
print(f"A soma é: {soma}")''',
                        'description': 'Entrada do usuário e formatação de strings'
                    },
                    {
                        'name': 'Verificação Par/Ímpar',
                        'code': '''numero = int(input("Digite um número inteiro: "))
if numero % 2 == 0:
    print(f"O número {numero} é par.")
else:
    print(f"O número {numero} é ímpar.")''',
                        'description': 'Estruturas condicionais'
                    },
                    {
                        'name': 'Função Recursiva (Fatorial)',
                        'code': '''def fatorial(n):
    if n == 0:
        return 1
    else:
        return n * fatorial(n-1)

num = int(input("Digite um número: "))
print(f"O fatorial de {num} é {fatorial(num)}.")''',
                        'description': 'Recursão e definição de funções'
                    }
                ]
            },
            'arquitetura': {
                'title': 'Arquitetura do Python',
                'philosophy': 'Zen do Python - Legibilidade, simplicidade e clareza',
                'execution_model': [
                    {
                        'step': 'Parsing',
                        'description': 'Análise sintática e criação da AST'
                    },
                    {
                        'step': 'Compilação',
                        'description': 'Conversão para bytecode Python'
                    },
                    {
                        'step': 'Execução',
                        'description': 'Interpretação pela Máquina Virtual Python'
                    }
                ],
                'abstractions': [
                    'Sintaxe clara e expressiva',
                    'Tipagem dinâmica e forte',
                    'Modelo de objetos consistente',
                    'Gerenciamento automático de recursos'
                ]
            }
        }

    def _create_javascript_data(self) -> Dict[str, Any]:
        """Cria dados estruturados sobre JavaScript (método privado)"""
        return {
            'historico': {
                'title': 'Histórico do JavaScript',
                'timeline': [
                        {"year": "1995", "event": "Criação do JavaScript por Brendan Eich na Netscape"},
                        {"year": "1996", "event": "Lançamento do JavaScript 1.0 no Netscape Navigator 2.0"},
                        {"year": "1997", "event": "Padronização como ECMAScript pela ECMA International"},
                        {"year": "1999", "event": "ECMAScript 3 torna-se o padrão amplamente adotado"},
                        {"year": "2005", "event": "Introdução do AJAX (Google Maps, Gmail) populariza JavaScript"},
                        {"year": "2009", "event": "Lançamento do Node.js e ECMAScript 5"},
                        {"year": "2015", "event": "ECMAScript 6 (ES2015) com grandes atualizações na linguagem"},
                        {"year": "2020", "event": "JavaScript completa 25 anos com ecossistema maduro"}
                ],
                "creator": "Brendan Eich",
                "origin": "1995 na Netscape Communications Corporation",
                "inspiration": "Sintaxe inspirada em Java, funcionalidades de linguagens como Scheme e Self",
                "development": "Criado em apenas 10 dias para a Netscape Navigator 2.0, inicialmente chamado de Mocha, depois LiveScript, e finalmente JavaScript"
            },
            'paradigmas': {
                'title': 'Paradigmas de Programação no JavaScript',
                'paradigms': [
                    {
                        'name': 'Programação Baseada em Protótipos',
                        'description': 'Modelo de herança único onde objetos herdam diretamente de outros objetos',
                        'features': [
                            'Herança prototípica (não baseada em classes)',
                            'Objetos como protótipos para outros objetos',
                            'Classes ES6+ como "açúcar sintático" sobre protótipos',
                            'Flexibilidade na criação e modificação de objetos em runtime'
                        ]
                    },
                    {
                        'name': 'Programação Funcional',
                        'description': 'Funções como cidadãos de primeira classe com suporte a closures',
                        'features': [
                            'Funções de primeira classe e de alta ordem',
                            'Closures e currying',
                            'Imutabilidade (opcional, encorajada)',
                            'Map, filter, reduce para coleções',
                            'Composição de funções'
                        ]
                    },
                    {
                        'name': 'Programação Orientada a Eventos',
                        'description': 'Programação assíncrona e reativa baseada em callbacks e eventos',
                        'features': [
                            'Callbacks para operações assíncronas',
                            'Promises e async/await',
                            'Event loop e programação não-bloqueante',
                            'Event listeners e handlers no DOM'
                        ]
                    },
                    {
                        'name': 'Programação Imperativa/Procedural',
                        'description': 'Estilo tradicional de programação com sequências de comandos',
                        'features': [
                            'Execução sequencial de instruções',
                            'Variáveis mutáveis e estado',
                            'Estruturas de controle (if, for, while)',
                            'Funções procedurais'
                        ]
                    }
                ]
            },
            'caracteristicas': {
                'title': 'Características Marcantes do JavaScript',
                'features': [
                    {
                        'name': 'Tipagem Dinâmica e Fraca',
                        'description': 'Variáveis não têm tipo fixo; podem ser reatribuídas com diferentes tipos e permitem coerção implícita entre tipos'
                    },
                    {
                        'name': 'Interpretada Just-In-Time (JIT)',
                        'description': 'Executada por motores que compilam para código nativo em tempo de execução (V8, SpiderMonkey, JavaScriptCore)'
                    },
                    {
                        'name': 'Programação Assíncrona e Não-Bloqueante',
                        'description': 'Modelo baseado em Event Loop com callbacks, promises e async/await para operações I/O'
                    },
                    {
                        'name': 'Orientada a Eventos',
                        'description': 'Desenvolvimento baseado em eventos, especialmente para interfaces de usuário e operações assíncronas'
                    },
                    {
                        'name': 'Baseada em Protótipos',
                        'description': 'Herança prototípica em vez de herança baseada em classes (embora classes ES6+ sejam suportadas como açúcar sintático)'
                    },
                    {
                        'name': 'Multiplataforma e Ubíqua',
                        'description': 'Executa em navegadores, servidores (Node.js), mobile, desktop, IoT e até em bancos de dados'
                    },
                    {
                        'name': 'Single-Threaded com Concorrência',
                        'description': 'Modelo de execução single-threaded que simula concorrência através do Event Loop'
                    },
                    {
                        'name': 'Primeira Classe de Funções',
                        'description': 'Funções são objetos de primeira classe que podem ser atribuídas a variáveis, passadas como argumentos e retornadas de outras funções'
                    },
                    {
                        'name': 'Closures e Escopo Lexical',
                        'description': 'Funções "lembram" do escopo onde foram criadas, permitindo padrões avançados como factory functions e módulos'
                    },
                    {
                        'name': 'Padronização ECMAScript',
                        'description': 'Evolução gerenciada pelo TC39 com releases anuais que trazem novas funcionalidades constantemente'
                    }
                ]
            },
            'linguagens_relacionadas': {
                'title': 'Linguagens Relacionadas ao JavaScript',
                'influences': [
                    {
                        'name': 'Java',
                        'type': 'Influência Sintática',
                        'description': 'JavaScript foi nomeado para se aproveitar da popularidade do Java em 1995, mas é uma linguagem fundamentalmente diferente.',
                        'features': [
                            'Sintaxe similar (chaves, ponto e vírgula)',
                            'Nomenclatura "JavaScript" para marketing',
                            'Algumas construções de controle (for, while, if)'
                        ]
                    },
                    {
                        'name': 'Scheme',
                        'type': 'Influência Funcional',
                        'description': 'Brendan Eich era fã de Scheme e incorporou conceitos de programação funcional na linguagem.',
                        'features': [
                            'Funções como cidadãos de primeira classe',
                            'Closures e escopo léxico',
                            'Recursos de programação funcional'
                        ]
                    },
                    {
                        'name': 'Self',
                        'type': 'Influência de Protótipos',
                        'description': 'Linguagem de pesquisa que introduziu o conceito de herança prototípica.',
                        'features': [
                            'Sistema de herança baseado em protótipos',
                            'Objetos dinâmicos sem classes',
                            'Delegação de protótipos'
                        ]
                    },
                    {
                        'name': 'C',
                        'type': 'Influência de Sintaxe',
                        'description': 'A família de linguagens C influenciou a sintaxe básica de JavaScript.',
                        'features': [
                            'Sintaxe de chaves para blocos',
                            'Operadores e precedência',
                            'Estruturas de controle básicas'
                        ]
                    },
                    {
                        'name': 'AWK',
                        'type': 'Influência de Design',
                        'description': 'Linguagem de processamento de texto que influenciou o design inicial de JavaScript.',
                        'features': [
                            'Tipagem dinâmica e fraca',
                            'Manipulação fácil de strings',
                            'Foco em tarefas práticas'
                        ]
                    },
                    {
                        'name': 'HyperTalk',
                        'type': 'Influência de Scripting',
                        'description': 'Linguagem de script do HyperCard da Apple que influenciou o modelo de eventos.',
                        'features': [
                            'Modelo de programação orientado a eventos',
                            'Scripting de alto nível',
                            'Fácil acesso a objetos do sistema'
                        ]
                    }
                ],
                'influenced': [
                    {
                        'name': 'TypeScript',
                        'year': '2012',
                        'description': 'Superset tipado do JavaScript desenvolvido pela Microsoft que adiciona tipos estáticos opcionais.',
                        'use_case': 'Desenvolvimento de aplicações web em grande escala'
                    },
                    {
                        'name': 'CoffeeScript',
                        'year': '2009',
                        'description': 'Linguagem que transpila para JavaScript com sintaxe inspirada no Ruby e Python.',
                        'use_case': 'Desenvolvimento mais conciso e elegante'
                    },
                    {
                        'name': 'Dart',
                        'year': '2011',
                        'description': 'Linguagem desenvolvida pelo Google como alternativa ao JavaScript, usada no Flutter.',
                        'use_case': 'Desenvolvimento mobile multiplataforma'
                    },
                    {
                        'name': 'Kotlin/JS',
                        'year': '2017',
                        'description': 'Kotlin compilado para JavaScript, permitindo desenvolvimento full-stack com uma linguagem.',
                        'use_case': 'Desenvolvimento web com interoperabilidade JavaScript'
                    },
                    {
                        'name': 'ReasonML/ReScript',
                        'year': '2016',
                        'description': 'Sintaxe amigável para OCaml que compila para JavaScript mantendo segurança de tipos.',
                        'use_case': 'Aplicações web com garantias de tipo fortes'
                    },
                    {
                        'name': 'WebAssembly',
                        'year': '2017',
                        'description': 'Formato binário que pode ser executado em navegadores, complementando JavaScript.',
                        'use_case': 'Aplicações web de alto desempenho'
                    }
                ],
                'transpilation_ecosystem': [
                    'TypeScript → JavaScript',
                    'CoffeeScript → JavaScript',
                    'Elm → JavaScript',
                    'PureScript → JavaScript',
                    'ClojureScript → JavaScript',
                    'Scala.js → JavaScript',
                    'Babel (ES6+ → ES5)'
                ]
            },
            'exemplos': {
                'title': 'Exemplos de Código JavaScript',
                'examples': [
                    {
                        'name': 'Manipulação do DOM',
                        'code': '''// Selecionar elemento
const elemento = document.getElementById('meuElemento');

// Modificar conteúdo
elemento.textContent = 'Olá, JavaScript!';

// Adicionar evento
elemento.addEventListener('click', function() {
    this.style.backgroundColor = 'blue';
});''',
                        'description': 'Interação com a página web usando DOM API'
                    },
                    {
                        'name': 'Funções e Closures',
                        'code': '''// Função de primeira classe
const somar = (a, b) => a + b;

// Closure
function criarContador() {
    let contador = 0;

    return function() {
        contador++;
        return contador;
    };
}

const contador = criarContador();
console.log(contador()); // 1
console.log(contador()); // 2''',
                        'description': 'Funções como valores e closures'
                    },
                    {
                        'name': 'Programação Assíncrona',
                        'code': '''// Usando async/await
async function buscarDados() {
    try {
        const resposta = await fetch('https://api.exemplo.com/dados');
        const dados = await resposta.json();
        return dados;
    } catch (erro) {
        console.error('Erro:', erro);
        throw erro;
    }
}

// Usando Promise
buscarDados()
    .then(dados => console.log(dados))
    .catch(erro => console.error(erro));''',
                        'description': 'Operações assíncronas com async/await e Promises'
                    },
                    {
                        'name': 'Manipulação de Arrays',
                        'code': '''const numeros = [1, 2, 3, 4, 5];

// Programação funcional com arrays
const pares = numeros.filter(n => n % 2 === 0);
const quadrados = numeros.map(n => n * n);
const soma = numeros.reduce((acc, n) => acc + n, 0);

console.log(pares);    // [2, 4]
console.log(quadrados); // [1, 4, 9, 16, 25]
console.log(soma);      // 15''',
                        'description': 'Métodos funcionais para manipulação de arrays'
                    }
                ]
            }
        }

    def _create_general_data(self) -> Dict[str, Any]:
        """Cria dados gerais da apresentação (método privado)"""
        return {
            'consideracoes_finais': {
                'title': 'Considerações Finais',
                'content': '''Este relatório apresentou uma análise detalhada de Python e JavaScript,
                           duas linguagens fundamentais no cenário tecnológico atual. Ambas demonstram
                           como diferentes filosofias de design podem resultar em ferramentas poderosas
                           para diferentes domínios de aplicação.''',
                'key_takeaways': [
                    'Python: Simplicidade, legibilidade e versatilidade',
                    'JavaScript: Ubiquidade, flexibilidade e evolução constante',
                    'Ambas são multiparadigma e têm comunidades ativas',
                    'Cada uma se destaca em seus domínios específicos'
                ]
            },
            'bibliografia': {
                'title': 'Bibliografia',
                'references': [
                    '[1] Python.org - História oficial do Python',
                    '[2] MDN Web Docs - História do JavaScript',
                    '[3] ECMAScript Specification',
                    '[4] "Learning Python" - Mark Lutz',
                    '[5] "JavaScript: The Good Parts" - Douglas Crockford'
                ]
            }
        }

    def get_all_routes(self) -> List[str]:
        """Retorna todas as rotas disponíveis (método utilitário)"""
        routes = [
            '/', '/python', '/python/historico', '/python/paradigmas',
            '/python/caracteristicas', '/python/linguagens_relacionadas',
            '/python/exemplos', '/python/arquitetura', '/javascript',
            '/javascript/historico', '/javascript/paradigmas',
            '/javascript/caracteristicas', '/javascript/linguagens_relacionadas',
            '/javascript/exemplos', '/consideracoes_finais', '/bibliografia'
        ]
        return routes

    def __str__(self) -> str:
        """Representação string da classe"""
        return f"PresentationData(routes={len(self.get_all_routes())})"

    def __repr__(self) -> str:
        """Representação técnica da classe"""
        return f"PresentationData(python_sections={len(self._python_data)}, js_sections={len(self._javascript_data)})"
