"""
Módulo Core - Arquitetura de apresentações Flask.

Expõe as classes principais para uso na aplicação:
- Presentation: Classe base
- Orchestrator: Gerenciador de apresentações
- Maestro_TTP, Maestro_Artigo: Classes de apresentação
- Musician_TTP, Musician_Artigo: Classes de rotas
"""

from core.presentation import Presentation, Orchestrator
from core.maestro import Maestro_TTP, Maestro_Artigo
from core.musician import Musician_TTP, Musician_Artigo

__all__ = [
    'Presentation',
    'Orchestrator',
    'Maestro_TTP',
    'Maestro_Artigo',
    'Musician_TTP',
    'Musician_Artigo'
]
