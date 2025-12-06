"""
Módulo Maestro - Define as classes subordinadas para cada apresentação.

Classes:
- Maestro_TTP: Apresentação sobre Python (Trabalho de Conclusão)
- Maestro_Artigo: Apresentação sobre Python e R na Análise de Precipitação
"""

from core.presentation import Presentation, Orchestrator
from flask import render_template, Response
from typing import List, Dict, Any


class Maestro_TTP(Presentation):
    """
    Classe subordinada para a apresentação TTP (Relatório sobre Python).
    Gerencia estrutura de navegação e conteúdo da apresentação sobre Python.
    """
    
    KEY = 'ttp'
    INSTITUICAO = 'Pontifícia Universidade de Minas Gerais (PUC Minas)'
    AUTORES = ['Gabriel da Silva Cassino', 'Welbert Junio Afonso de Almeida']
    MATERIAS = ['Linguagens de Programação']
    PROFESSORES = ['Marco Rodrigo Costa']
    CURSOS = ['Graduação em Engenharia da Computação', 'Bacharelado em Ciência da Computação']
    TITLE = 'Trabalho Teórico Prático Python'
    TEMPLATE_PATH = 'ttp/python_presentation.html'
    
    # Desativado por Hora
    def render_module(self, module_id: str) -> str:
        """
        Renderiza um módulo específico da apresentação TTP.
        """
        if module_id == 'exampleinteractive/pygamewelbert':
            return render_template('ttp/modules/chess_module.html')
        
        return Response(f"Módulo {module_id} não encontrado.", status=404)

    def get_navigation_structure(self) -> List[Dict[str, Any]]:

        return [
        # 1. Introdução
        {
            'id': 'introducao',
            'title': '1. Introdução',
            'has_submenu': False
        },

        # 2. História do Python
        {
            'id': 'history',
            'title': '2. História do Python',
            'has_submenu': True,
            'submenu': [
                {'id': 'history/context', 'title': 'Contexto'},
                {'id': 'history/genealogia', 'title': 'Genealogia'},
                {'id': 'history/overview', 'title': 'Visão Geral'},
                {'id': 'history/creator', 'title': 'Criador'},
                {'id': 'history/h1989', 'title': '1989 - Início'},
                {'id': 'history/h1991', 'title': '1991 - Primeira Versão'},
                {'id': 'history/h1994', 'title': '1994 - Python 1.0'},
                {'id': 'history/h2000', 'title': '2000 - Python 2.0'},
                {'id': 'history/h2001', 'title': '2001 - Python 2.2'},
                {'id': 'history/h2008', 'title': '2008 - Python 3.0'},
                {'id': 'history/h2015a2019', 'title': '2015-2019 - Melhorias'},
                {'id': 'history/h2020a2025', 'title': '2020-Hoje - Atualidade'},
                {'id': 'history/heventos', 'title': 'Eventos Institucionais'}
            ]
        },

        # 3. Características
        {
            'id': 'characteristics',
            'title': '3. Características',
            'has_submenu': True,
            'submenu': [
                {'id': 'characteristics/overview', 'title': 'Visão Geral'},
                {'id': 'characteristics/syntax', 'title': 'Sintaxe'},
                {'id': 'characteristics/tipagem', 'title': 'Tipagem Dinâmica'},
                {'id': 'characteristics/interpretada', 'title': 'Linguagem Interpretada'},
                {'id': 'characteristics/multiparadigma', 'title': 'Multi-paradigma'},
                {'id': 'characteristics/baterias', 'title': 'Baterias Incluídas'},
                {'id': 'characteristics/memoria', 'title': 'Gerenciamento Automático'},
                {'id': 'characteristics/portabilidade', 'title': 'Portabilidade'},
                {'id': 'characteristics/extensivel', 'title': 'Extensível'},
                {'id': 'characteristics/comunidade', 'title': 'Comunidade Ativa'},
                {'id': 'characteristics/opensource', 'title': 'Open Source'},
                {'id': 'characteristics/zen', 'title': 'Zen do Python'}
            ]
        },

        # 4. Paradigmas
        {
            'id': 'paradigms',
            'title': '4. Paradigmas',
            'has_submenu': True,
            'submenu': [
                {'id': 'paradigms/overview', 'title': 'Visão Geral'},
                {'id': 'paradigms/imperativo', 'title': 'Programação Imperativa'},
                {'id': 'paradigms/oop', 'title': 'Orientação a Objetos'},
                {'id': 'paradigms/functional', 'title': 'Funcional'},
                {'id': 'paradigms/procedural', 'title': 'Procedural'},
                {'id': 'paradigms/estruturado', 'title': 'Programação Estruturada'},
                {'id': 'paradigms/assincrono', 'title': 'Programação Assíncrona'},
                {'id': 'paradigms/generico', 'title': 'Programação Genérica'},
                {'id': 'paradigms/multi', 'title': 'Python Multi-paradigma'}
            ]
        },

        # 5. Linguagens Relacionadas
        {
            'id': 'languages',
            'title': '5. Linguagens Relacionadas',
            'has_submenu': True,
            'submenu': [
                {'id': 'languages/overview', 'title': 'Visão Geral'},
                {'id': 'languages/influenciadores', 'title': 'Linguagens Influenciadoras'},
                {'id': 'languages/influenciadas', 'title': 'Linguagens Influenciadas'},
                {'id': 'languages/similares', 'title': 'Linguagens Similares'},
                {'id': 'languages/opostas', 'title': 'Linguagens Opostas'}
            ]
        },

        # 6. Aplicações
        {
            'id': 'applications',
            'title': '6. Aplicações',
            'has_submenu': True,
            'submenu': [
                {'id': 'applications/overview', 'title': 'Visão Geral'},
                {'id': 'applications/cases', 'title': 'Casos de Uso'},
                {'id': 'applications/web', 'title': 'Desenvolvimento Web'},
                {'id': 'applications/data', 'title': 'Ciência de Dados'},
                {'id': 'applications/ai', 'title': 'Inteligência Artificial'},
                {'id': 'applications/automation', 'title': 'Automação'},
                {'id': 'applications/gaming', 'title': 'Jogos'}
            ]
        },

        # 7. Ecossistema
        {
            'id': 'ecosystem',
            'title': '7. Ecossistema',
            'has_submenu': True,
            'submenu': [
                {'id': 'ecosystem/overview', 'title': 'Visão Geral'},
                {'id': 'ecosystem/libraries', 'title': 'Bibliotecas'},
                {'id': 'ecosystem/frameworks', 'title': 'Frameworks'},
                {'id': 'ecosystem/tools', 'title': 'Ferramentas'}
            ]
        },

        # 8. Desafios
        {
            'id': 'example',
            'title': '8. Prática e Exemplos',
            'has_submenu': True,
            'submenu': [
                {'id': 'example/pratica', 'title': 'Prática e Tutorial'},
                {'id': 'example/gabriel', 'title': 'Exemplos Gabriel'},
                {'id': 'example/welbert', 'title': 'Exemplos Welbert'}
            ]
        },

        # Desativado por Hora
        # 9. Exemplo Interativo
        #{
         #   'id': 'exampleinteractive',
          #  'title': '9. Exemplo Interativo',
           # 'has_submenu': True,
            #'submenu': [
             #   {'id': 'exampleinteractive/etiquetagabriel', 'title': 'Módulo de Gerador de Etiqueta'},
             #   {'id': 'exampleinteractive/pygamewelbert', 'title': 'Módulo de Xadrez (Pygame)'}
            #]
        #},

        # 10. Conclusão
        {
            'id': 'conclusion',
            'title': '9. Conclusão',
            'has_submenu': False
        },

        # 11. Apêndices
        {
            'id': 'apendices',
            'title': '10. Apêndices',
            'has_submenu': True,
            'submenu': [
                {'id': 'apendices/gabriel', 'title': 'Apêndice Gabriel'},
                {'id': 'apendices/welbert', 'title': 'Apêndice Welbert'}
            ]
        },

        # 12. Referências
        {
            'id': 'referencias',
            'title': '11. Referências',
            'has_submenu': False
        },

        # 13. Agradecimentos
        {
            'id': 'agradecimento',
            'title': '12. Agradecimentos',
            'has_submenu': False
        }
    ]




class Maestro_Artigo(Presentation):
    """
    Classe subordinada para a apresentação do Artigo.
    Gerencia estrutura de navegação e conteúdo sobre Python e R na análise de precipitação.
    """
    
    KEY = 'artigo'
    INSTITUICAO = 'Pontifícia Universidade de Minas Gerais (PUC Minas)'
    AUTORES = ['Gabriel da Silva Cassino', 'Welbert Junio Afonso de Almeida']
    MATERIAS = ['Linguagens de Programação']
    PROFESSORES = ['Marco Rodrigo da Costa']
    CURSOS = ['Graduação em Engenharia da Computação', 'Bacharelado em Ciência da Computação']
    TITLE = 'Trabalho de Pesquisa - Python e R na Análise de Precipitação'
    TEMPLATE_PATH = 'artigo/article_presentation.html'
    
    # Desativado por Hora
    def render_module(self, module_id: str) -> str:
        """
        Renderiza um módulo específico da apresentação TTP.
        """
        if module_id == 'example/pygamewelbert':
            return render_template('ttp/modules/chess_module.html')
        
        return Response(f"Módulo {module_id} não encontrado.", status=404)

    def get_navigation_structure(self) -> List[Dict[str, Any]]:
        """
        Retorna a estrutura de navegação da apresentação do Artigo.
        
        Returns:
            Lista com seções do artigo científico
        """
        return [
            {
                'id': 'title',
                'title': '1. Título',
                'has_submenu': False
            },
            {
                'id': 'resumo',
                'title': '2. Resumo',
                'has_submenu': False
            },
            {
                'id': 'introducao',
                'title': '3. Introdução',
                'has_submenu': False
            },
            {
                'id': 'referencial-teorico',
                'title': '4. Referencial Teórico',
                'has_submenu': True,
                'submenu': [
                    {'id': 'referencial-teorico/eventos', 'title': 'Eventos Extremos'},
                    {'id': 'referencial-teorico/enos', 'title': 'ENOS'},
                    {'id': 'referencial-teorico/oma-odp', 'title': 'OMA e ODP'}
                ]
            },
            {
                'id': 'metodologia',
                'title': '5. Metodologia',
                'has_submenu': True,
                'submenu': [
                    {'id': 'metodologia/area', 'title': 'Área de Estudo'},
                    {'id': 'metodologia/dados', 'title': 'Dados'},
                    {'id': 'metodologia/analise', 'title': 'Análise'}
                ]
            },
            {
                'id': 'resultados-discussao',
                'title': '6. Resultados e Discussão',
                'has_submenu': True,
                'submenu': [
                    {'id': 'resultados-discussao/temporal', 'title': 'Análise Temporal'},
                    {'id': 'resultados-discussao/espacial', 'title': 'Análise Espacial'},
                    {'id': 'resultados-discussao/correlacao', 'title': 'Correlações'}
                ]
            },
            {
                'id': 'consideracoes',
                'title': '7. Considerações',
                'has_submenu': True,
                'submenu': [
                    {'id': 'consideracoes/gabriel', 'title': 'Considerações Gabriel'},
                    {'id': 'consideracoes/welbert', 'title': 'Considerações Welbert'}
                ]
            },
            {
                'id': 'conclusao',
                'title': '8. Conclusão',
                'has_submenu': False
            },
            {
                'id': 'referencias',
                'title': '9. Referências',
                'has_submenu': False
            },
            {
                'id': 'agradecimento',
                'title': '10. Agradecimentos',
                'has_submenu': False
            }
        ]


# Registrar as classes no Orchestrator automaticamente ao importar o módulo
Orchestrator.register_presentation(Maestro_TTP)
Orchestrator.register_presentation(Maestro_Artigo)
