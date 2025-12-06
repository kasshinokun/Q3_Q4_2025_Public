"""
Módulo de Rotas - Define as rotas Flask da aplicação.

Utiliza Blueprint para organização modular das rotas.
Integra com as classes Musician para renderização das apresentações.
"""

from flask import Blueprint, redirect, url_for, Response, jsonify, request
import base64
from core.musician import Musician_TTP, Musician_Artigo
from core.chess_flask import chess_game
from core.musician_exemplo import Musician_Exemplo

# Criar Blueprint para as rotas principais
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """
    Rota raiz da aplicação.
    Redireciona para a apresentação TTP como padrão.
    
    Returns:
        Redirect para a rota python_presentation
    """
    return redirect(url_for('main.python_presentation'))


@main_bp.route('/python_presentation')
def python_presentation():
    """
    Rota para a apresentação TTP (Relatório sobre Python).
    Utiliza Musician_TTP para renderizar a apresentação.
    
    Returns:
        HTML renderizado da apresentação TTP
    """
    return Musician_TTP.render_presentation()


@main_bp.route('/chess_module')
def chess_module():
    """
    Rota para o módulo de xadrez.
    Utiliza Musician_Exemplo para renderizar o módulo.
    
    Returns:
        HTML renderizado do módulo de xadrez
    """
    return Musician_Exemplo.render_chess_module()

@main_bp.route('/chess_board')
def chess_board():
    """
    Rota para retornar a imagem do tabuleiro de xadrez.
    """
    image_base64 = chess_game.get_board_image()
    image_data = base64.b64decode(image_base64)
    return Response(image_data, mimetype='image/png')

@main_bp.route('/chess_move')
def chess_move():
    """
    Rota para processar o movimento do xadrez.
    """
    x = int(request.args.get('x'))
    y = int(request.args.get('y'))
    
    new_image_base64 = chess_game.handle_click(x, y)
    
    return jsonify({'board_image': new_image_base64})


@main_bp.route('/python_r_comparative')
def python_r_comparative():
    """
    Rota para a apresentação do Artigo (Python e R na Análise de Precipitação).
    Utiliza Musician_Artigo para renderizar a apresentação.
    
    Returns:
        HTML renderizado da apresentação do Artigo
    """
    return Musician_Artigo.render_presentation()


# Rotas adicionais podem ser adicionadas aqui conforme necessário
@main_bp.route('/health')
def health_check():
    """
    Rota de health check para verificar se a aplicação está funcionando.
    
    Returns:
        JSON com status da aplicação
    """
    from core.presentation import Orchestrator
    
    presentations = Orchestrator.get_presentation_list()
    
    return {
        'status': 'ok',
        'presentations_registered': len(presentations),
        'presentations': presentations
    }
