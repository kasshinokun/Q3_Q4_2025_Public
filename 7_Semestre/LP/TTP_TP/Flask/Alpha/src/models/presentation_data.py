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
            'subtitle': 'A linguagem da web moderna',
            'description': '''JavaScript é uma das linguagens mais ubíquas e influentes da web, criada em 1995 
                           por Brendan Eich. Originalmente desenvolvida para adicionar interatividade às páginas web, 
                           hoje é usada tanto no frontend quanto no backend.''',
            'key_points': [
                'Linguagem interpretada e dinâmica',
                'Multiparadigma com foco em programação funcional',
                'Execução no navegador e servidor (Node.js)',
                'Ecossistema vasto com NPM',
                'Padrão ECMAScript em constante evolução'
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
                    {'year': '1995', 'event': 'Criação por Brendan Eich em 10 dias'},
                    {'year': '1995', 'event': 'Lançamento no Netscape Navigator 2.0'},
                    {'year': '1996', 'event': 'Microsoft lança JScript'},
                    {'year': '1997', 'event': 'Padronização ECMAScript'},
                    {'year': '2005', 'event': 'Termo Ajax cunhado - renascimento do JS'},
                    {'year': '2009', 'event': 'Node.js - JavaScript no servidor'},
                    {'year': '2015', 'event': 'ES6/ES2015 - Revolução da linguagem'}
                ],
                'creator': 'Brendan Eich',
                'company': 'Netscape Communications',
                'original_names': ['Mocha', 'LiveScript', 'JavaScript']
            },
            'paradigmas': {
                'title': 'Paradigmas de Programação',
                'paradigms': [
                    {
                        'name': 'Programação Funcional',
                        'description': 'Funções como cidadãos de primeira classe',
                        'features': ['Higher-order functions', 'Closures', 'Arrow functions']
                    },
                    {
                        'name': 'Orientação a Objetos',
                        'description': 'Baseada em protótipos, não classes tradicionais',
                        'features': ['Prototypes', 'Classes (ES6+)', 'Herança prototípica']
                    },
                    {
                        'name': 'Programação Imperativa',
                        'description': 'Execução sequencial de comandos',
                        'features': ['Loops', 'Condicionais', 'Manipulação de estado']
                    }
                ]
            },
            'caracteristicas': {
                'title': 'Características Marcantes',
                'features': [
                    {
                        'name': 'Tipagem Dinâmica e Fraca',
                        'description': 'Coerção automática entre tipos'
                    },
                    {
                        'name': 'Interpretada',
                        'description': 'Execução direta pelo motor JavaScript'
                    },
                    {
                        'name': 'Event-driven',
                        'description': 'Programação orientada a eventos'
                    },
                    {
                        'name': 'Assíncrona',
                        'description': 'Callbacks, Promises, async/await'
                    },
                    {
                        'name': 'Multiplataforma',
                        'description': 'Navegador, servidor, mobile, desktop'
                    }
                ]
            },
            'linguagens_relacionadas': {
                'title': 'Linguagens Relacionadas',
                'influences': [
                    {'name': 'Scheme', 'type': 'Influenciou', 'description': 'Programação funcional'},
                    {'name': 'Self', 'type': 'Influenciou', 'description': 'Herança prototípica'},
                    {'name': 'Java', 'type': 'Influenciou', 'description': 'Sintaxe similar'},
                    {'name': 'C', 'type': 'Influenciou', 'description': 'Estruturas de controle'}
                ],
                'influenced': [
                    {'name': 'TypeScript', 'description': 'Superset tipado do JavaScript'},
                    {'name': 'CoffeeScript', 'description': 'Sintaxe mais limpa'},
                    {'name': 'Dart', 'description': 'Alternativa do Google'}
                ]
            },
            'exemplos': {
                'title': 'Exemplos de Código JavaScript',
                'examples': [
                    {
                        'name': 'Olá, Mundo!',
                        'code': 'console.log("Olá, Mundo!");',
                        'description': 'Saída no console'
                    },
                    {
                        'name': 'Manipulação DOM',
                        'code': '''document.getElementById("demo").innerHTML = "Olá, JavaScript!";''',
                        'description': 'Alterando conteúdo HTML'
                    },
                    {
                        'name': 'Função com Arrow Function',
                        'code': '''const somar = (a, b) => a + b;
console.log(somar(5, 3));''',
                        'description': 'Sintaxe moderna ES6+'
                    },
                    {
                        'name': 'Programação Assíncrona',
                        'code': '''async function buscarDados() {
    try {
        const response = await fetch('/api/dados');
        const dados = await response.json();
        return dados;
    } catch (error) {
        console.error('Erro:', error);
    }
}''',
                        'description': 'Async/await para operações assíncronas'
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

