"""
Aplicação Flask - Sistema de Apresentações Modularizado

Arquitetura:
1. Presentation (classe base) - Define estrutura comum das apresentações
2. Orchestrator (seletor de views) - Gerencia registro e seleção de apresentações
3. Maestro_TTP e Maestro_Artigo (classes subordinadas) - Implementam apresentações específicas
4. Musician_TTP e Musician_Artigo (seletores de rotas) - Fazem request do render dos templates

Autor: Sistema Refatorado
Versão: 2.0
"""

from flask import Flask
import core.maestro  # Importa para registrar as apresentações no Orchestrator
from routes.routes import main_bp
from core.presentation import Orchestrator
import os

class AppConfig:
    @staticmethod
    def get_root_path():
        return os.path.abspath(os.path.dirname(__file__))
    
    @staticmethod
    def get_static_path(filename):
        root = AppConfig.get_root_path()
        return os.path.join(root, 'static', 'images', filename)


def create_app():
    """
    Factory function para criar e configurar a aplicação Flask.
    
    Returns:
        Instância configurada da aplicação Flask
    """
    app = Flask(__name__)
    
    # Configurações da aplicação
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    
    # Disponibiliza a configuração no app
    app.config['APP_ROOT'] = AppConfig.get_root_path()

    @app.context_processor
    def utility_processor():
        def get_image_path(filename):
            return os.path.join(app.config['APP_ROOT'], 'static', 'images', filename)
        return dict(get_image_path=get_image_path)
    
    
    # Registrar Blueprint de rotas
    app.register_blueprint(main_bp)
    
    # Listar apresentações registradas no console
    with app.app_context():
        Orchestrator.list_registered_presentations()
    
    return app


if __name__ == '__main__':
    # Criar aplicação
    app = create_app()
    
    # Executar servidor de desenvolvimento
    print("\n" + "="*60)
    print("🚀 SERVIDOR FLASK INICIADO")
    print("="*60)
    print("📍 Acesse: http://0.0.0.0:5000")
    print("📊 Health Check: http://0.0.0.0:5000/health")
    print("="*60 + "\n")
    
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        use_reloader=True
    )
