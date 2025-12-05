import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, render_template, send_from_directory, jsonify
from flask_cors import CORS
from src.models.presentation_data import PresentationData
from src.models.advanced_python_features import (
    ConfigurationManager, 
    PythonDataProcessor, 
    functional_data_analysis,
    demonstrate_python_features
)
def start_presentation():
    app = Flask(__name__, 
            static_folder=os.path.join(os.path.dirname(__file__), 'static'),
            template_folder=os.path.join(os.path.dirname(__file__), 'templates'))
    app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

    # Habilitar CORS para interação frontend-backend
    CORS(app)

    # Instância da classe que contém os dados da apresentação (Singleton)
    config_manager = ConfigurationManager()
    presentation_data = PresentationData()

    # Processador de dados demonstrando POO
    data_processor = PythonDataProcessor(
        name="Flask Presentation Processor",
        version="1.0.0",
        features=["Flask", "Jinja2", "POO", "Decoradores", "Context Managers"]
    )

    @app.route('/')
    def index():
        """Página inicial da apresentação"""
        return render_template('index.html', 
                            title="Relatório Detalhado sobre Python e JavaScript",
                            author="Gabriel da Silva Cassino",
                            author2="Welbert Junio Afonso de Almeida")

    #======================> Modularizando HomePage <=====================================================
    @app.route('/inicio-ttp')
    def app_start():
        """Página inicial da apresentação - Capa"""
        return render_template('capa.html', 
                            title="Relatório Detalhado sobre Python e JavaScript",
                            author="Gabriel da Silva Cassino",
                            author2="Welbert Junio Afonso de Almeida")

    @app.route('/intro-ttp')
    def app_intro():
        """Página inicial da apresentação - Introdução"""
        return render_template('intro_apresentacao.html',
                            title="Relatório Detalhado sobre Python e JavaScript",
                            author="Gabriel da Silva Cassino",
                            author2="Welbert Junio Afonso de Almeida")


    @app.route('/topicos-ttp')
    def app_topics():
        """Página inicial da apresentação - Tópicos"""
        return render_template('topicos_apresentacao.html',
                            title="Relatório Detalhado sobre Python e JavaScript",
                            author="Gabriel da Silva Cassino",
                            author2="Welbert Junio Afonso de Almeida")


    @app.route('/about-ttp')
    def app_about():
        """Página inicial da apresentação - Sobre"""
        return render_template('about_apresentacao.html',
                            title="Relatório Detalhado sobre Python e JavaScript",
                            author="Gabriel da Silva Cassino",
                            author2="Welbert Junio Afonso de Almeida")

    #=====================> Fim Modularização HomePage <===================================================

    @app.route('/python')
    def python_intro():
        """Introdução ao Python"""
        return render_template('python_intro.html', 
                            data=presentation_data.get_python_intro())

    @app.route('/python/historico')
    def python_historico():
        """Histórico do Python"""
        return render_template('python_historico.html', 
                            data=presentation_data.get_python_historico())

    @app.route('/python/paradigmas')
    def python_paradigmas():
        """Paradigmas de Programação do Python"""
        return render_template('python_paradigmas.html', 
                            data=presentation_data.get_python_paradigmas())

    @app.route('/python/caracteristicas')
    def python_caracteristicas():
        """Características Mais Marcantes do Python"""
        return render_template('python_caracteristicas.html', 
                            data=presentation_data.get_python_caracteristicas())

    @app.route('/python/linguagens_relacionadas')
    def python_linguagens_relacionadas():
        """Linguagens Relacionadas ao Python"""
        return render_template('python_linguagens_relacionadas.html', 
                            data=presentation_data.get_python_linguagens_relacionadas())

    @app.route('/python/exemplos')
    def python_exemplos():
        """Exemplos de Programas em Python"""
        return render_template('python_exemplos.html', 
                            data=presentation_data.get_python_exemplos())

    @app.route('/python/arquitetura')
    def python_arquitetura():
        """Aprofundamento na Arquitetura do Python"""
        return render_template('python_arquitetura.html', 
                            data=presentation_data.get_python_arquitetura())

    @app.route('/javascript')
    def javascript_intro():
        """Introdução ao JavaScript"""
        return render_template('javascript_intro.html', 
                            data=presentation_data.get_javascript_intro())

    @app.route('/javascript/historico')
    def javascript_historico():
        """Histórico do JavaScript"""
        return render_template('javascript_historico.html', 
                            data=presentation_data.get_javascript_historico())

    @app.route('/javascript/paradigmas')
    def javascript_paradigmas():
        """Paradigmas de Programação do JavaScript"""
        return render_template('javascript_paradigmas.html', 
                            data=presentation_data.get_javascript_paradigmas())

    @app.route('/javascript/caracteristicas')
    def javascript_caracteristicas():
        """Características Mais Marcantes do JavaScript"""
        return render_template('javascript_caracteristicas.html', 
                            data=presentation_data.get_javascript_caracteristicas())

    @app.route('/javascript/linguagens_relacionadas')
    def javascript_linguagens_relacionadas():
        """Linguagens Relacionadas ao JavaScript"""
        return render_template('javascript_linguagens_relacionadas.html', 
                            data=presentation_data.get_javascript_linguagens_relacionadas())

    @app.route('/javascript/exemplos')
    def javascript_exemplos():
        """Exemplos de Programas em JavaScript"""
        return render_template('javascript_exemplos.html', 
                            data=presentation_data.get_javascript_exemplos())

    @app.route('/consideracoes_finais')
    def consideracoes_finais():
        """Considerações Finais"""
        return render_template('consideracoes_finais.html', 
                            data=presentation_data.get_consideracoes_finais())

    @app.route('/bibliografia')
    def bibliografia():
        """Bibliografia"""
        return render_template('bibliografia.html', 
                            data=presentation_data.get_bibliografia())

    @app.route('/static/<path:filename>')
    def serve_static(filename):
        """Servir arquivos estáticos"""
        return send_from_directory(app.static_folder, filename)

    # Rotas API para demonstrar características do Python
    @app.route('/api/python-features')
    def api_python_features():
        """API que demonstra características avançadas do Python"""
        try:
            # Demonstrar programação funcional
            sample_data = [1, 2, 3, 4, 5, 10, 15, 20]
            analysis = functional_data_analysis(sample_data)
            
            # Demonstrar processamento de dados com POO
            processed_data = data_processor.process("API Request Data")
            
            # Demonstrar uso do Singleton
            config = {
                "app_name": config_manager.get_config("app_name"),
                "version": config_manager.get_config("version"),
                "features": config_manager.get_config("features")
            }
            
            return jsonify({
                "success": True,
                "message": "Demonstração de características Python via API",
                "data": {
                    "functional_analysis": analysis,
                    "oop_processing": processed_data,
                    "singleton_config": config,
                    "python_paradigmas": ["POO", "Funcional", "Imperativa"],
                    "flask_features": ["Rotas", "Templates", "JSON API", "CORS"]
                }
            })
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500

    @app.route('/api/demo')
    def api_demo():
        """API de demonstração simples"""
        return jsonify({
            "message": "API Flask funcionando!",
            "python_version": "3.11+",
            "framework": "Flask",
            "paradigmas_demonstrated": [
                "Programação Orientada a Objetos",
                "Programação Funcional", 
                "Decoradores",
                "Context Managers",
                "Type Hints"
            ]
        })
    def run():
         app.run(host='0.0.0.0', port=5000, debug=True)
    run()
if __name__ == '__main__':
   start_presentation()


