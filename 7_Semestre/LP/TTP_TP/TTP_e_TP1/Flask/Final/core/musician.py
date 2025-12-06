"""
Módulo Musician - Define as classes seletoras de rotas para cada apresentação.

Classes:
- Musician_TTP: Classe seletora de rotas para apresentação TTP
- Musician_Artigo: Classe seletora de rotas para apresentação do Artigo

Responsabilidades:
- Fazer request do render de cada arquivo .html através do Orchestrator
- Servir como camada intermediária entre rotas Flask e apresentações
"""

from core.presentation import Orchestrator
from core.maestro import Maestro_TTP, Maestro_Artigo
from .musician_exemplo import Musician_Exemplo # Importação relativa para o mesmo pacote
from flask import Response


class Musician_TTP:
    """
    Classe seletora de rotas para a apresentação TTP.
    Responsável por fazer o request do render da classe Maestro_TTP.
    """
    
    @staticmethod
    def render_presentation() -> str:
        """
        Renderiza a apresentação TTP através do Orchestrator.
        
        Returns:
            HTML renderizado da apresentação TTP
            
        Raises:
            Response: 404 se a apresentação não for encontrada
        """
        maestro = Orchestrator.get_presentation(Maestro_TTP.KEY)
        
        if maestro:
            return maestro.render()
        
        return Response(
            "Apresentação TTP não encontrada. Verifique o registro no Orchestrator.",
            status=404
        )


class Musician_Artigo:
    """
    Classe seletora de rotas para a apresentação do Artigo.
    Responsável por fazer o request do render da classe Maestro_Artigo.
    """
    
    @staticmethod
    def render_presentation() -> str:
        """
        Renderiza a apresentação do Artigo através do Orchestrator.
        
        Returns:
            HTML renderizado da apresentação do Artigo
            
        Raises:
            Response: 404 se a apresentação não for encontrada
        """
        maestro = Orchestrator.get_presentation(Maestro_Artigo.KEY)
        
        if maestro:
            return maestro.render()
        
        return Response(
            "Apresentação do Artigo não encontrada. Verifique o registro no Orchestrator.",
            status=404
        )
