"""
Módulo Musician_Exemplo - Define a classe seletora de rotas para a apresentação de Exemplo.

Classe:
- Musician_Exemplo: Classe seletora de rotas para apresentação de Exemplo

Responsabilidades:
- Fazer request do render de cada arquivo .html através do Orchestrator
- Servir como camada intermediária entre rotas Flask e apresentações
"""

from core.presentation import Orchestrator
from core.maestro import Maestro_TTP
from flask import Response
from typing import Optional

# A classe Musician_Exemplo deve ser vinculada a uma classe Maestro.
# Como o módulo de xadrez será integrado ao Maestro_TTP,
# Musician_Exemplo será uma classe auxiliar para renderizar um módulo específico.
# No entanto, para seguir o padrão Musician_X, vamos criar uma classe
# que se vincula ao Maestro_TTP, mas que pode ser usada para módulos específicos.

class Musician_Exemplo:
    """
    Classe seletora de rotas para o módulo de Exemplo (Xadrez).
    Responsável por fazer o request do render do módulo específico dentro do Maestro_TTP.
    """
    
    @staticmethod
    def render_module(module_id: str) -> str:
        """
        Renderiza um módulo específico da apresentação TTP através do Orchestrator.
        
        Args:
            module_id (str): O ID do módulo a ser renderizado (ex: 'example/pygamewelbert').
        
        Returns:
            HTML renderizado do módulo
            
        Raises:
            Response: 404 se a apresentação ou o módulo não for encontrado
        """
        maestro = Orchestrator.get_presentation(Maestro_TTP.KEY)
        
        if maestro:
            # O método render_module deve ser implementado na classe Presentation/Maestro
            # para buscar e renderizar o template específico do módulo.
            # Por enquanto, vamos simular a chamada.
            # A implementação real será feita no Maestro_TTP.
            return maestro.render_module(module_id)
        
        return Response(
            f"Apresentação TTP não encontrada para renderizar o módulo {module_id}.",
            status=404
        )

    @staticmethod
    def render_chess_module() -> str:
        """
        Renderiza o módulo de xadrez (020_Xadrez)
        """
        return Musician_Exemplo.render_module('exampleinteractive/pygamewelbert')
