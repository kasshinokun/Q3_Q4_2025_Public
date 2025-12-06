"""
Módulo de apresentações - Define a arquitetura base para gerenciamento de apresentações.

Arquitetura:
1. Presentation: Classe base para todas as apresentações
2. Orchestrator: Classe seletora de views que gerencia as apresentações disponíveis
"""

from flask import render_template
from typing import Dict, List, Any
import requests

class Presentation:
    """
    Classe base para todas as apresentações.
    Define a estrutura comum e métodos para renderização.
    
    Attributes:
      - KEY (str): Identificador único da apresentação
        - INSTITUICAO (str): Nome da instituição de ensino.
        - AUTORES (List[str]): Lista de nomes dos autores da apresentação.
        - MATERIAS (List[str]): Lista de matérias relacionadas à apresentação.
        - PROFESSORES (List[str]): Lista de nomes dos professores.
        - CURSOS (List[str]): Lista de nomes dos cursos.
        TITLE (str): Título da apresentação exibido na UI
        TEMPLATE_PATH (str): Caminho do template Jinja2
    """
    
    KEY: str = None
    INSTITUICAO: str = None
    AUTORES: List[str] = []
    MATERIAS: List[str] = []
    PROFESSORES: List[str] = []
    CURSOS: List[str] = []
    TITLE: str = None
    TEMPLATE_PATH: str = None
    
    URL_PUC="https://www.pucminas.br/Style%20Library/STATIC/img/2025/brasao-pucminas-2025-versao-positiva.png"
    PATH_PUC="brasao-pucminas-versao-2025.png" 
    
    def __init__(self):
        """Inicializa a apresentação com validação de atributos obrigatórios."""
        if not all([self.KEY, self.TITLE, self.TEMPLATE_PATH]):
            raise ValueError(
                f"Apresentação {self.__class__.__name__} deve definir "
                "KEY, TITLE e TEMPLATE_PATH"
            )
    
    def get_navigation_structure(self) -> List[Dict[str, Any]]:
        """
        Retorna a estrutura de navegação específica da apresentação.
        Deve ser sobrescrito pelas classes filhas.
        """
        
    def render_module(self, module_id: str) -> str:
        """
        Renderiza um módulo específico da apresentação.
        Deve ser sobrescrito pelas classes filhas que suportam módulos.
        """
        raise NotImplementedError(f"Módulo {module_id} não suportado por {self.__class__.__name__}")
        return []
    
    def get_context(self) -> Dict[str, Any]:
        """
        Retorna o contexto de renderização para o template.
        
        Returns:
            Dicionário com variáveis de contexto para o template
        """
        return {
            'title': self.TITLE,
            'presentation_key': self.KEY,
            'instituicao': self.INSTITUICAO,
            'autores': self.AUTORES,
            'materias': self.MATERIAS,
            'professores': self.PROFESSORES,
            'cursos': self.CURSOS,
            'presentation_list': Orchestrator.get_presentation_list(),
            'navigation': self.get_navigation_structure(),
            'logo_puc':self.get_image()
        }
    
    def render(self) -> str:
        """
        Renderiza o template da apresentação com o contexto.
        
        Returns:
            HTML renderizado da apresentação
        """
        context = self.get_context()
        return render_template(self.TEMPLATE_PATH, **context)
    

    def get_puc_image_path(self):
        """Usa a configuração do Flask para obter o caminho"""
        try:
            # Quando executado no contexto Flask
            app_root = current_app.config.get('APP_ROOT')
            if not app_root:
                app_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        except RuntimeError:
            # Fora do contexto Flask (ex: testes)
            app_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        
        return os.path.join(app_root, 'static', 'images', self.PATH_PUC)
    
    def get_image(self) -> str:
        try:
            response = requests.get(self.URL_PUC, timeout=5)
            
            if response.status_code == 404:
                print(f"✅ URL retorna 404 - Arquivo não encontrado")
                return self.get_puc_image_path()
            elif response.status_code == 200:
                print(f"✅ URL retorna 200 - Arquivo encontrado")
                print(f"Tamanho: {len(response.content)} bytes")
                return self.URL_PUC
            else:
                print(f"URL retorna código {response.status_code}")
                return self.get_puc_image_path()
            
        except requests.exceptions.RequestException as e:
            print(f"Erro: {e}")
            return self.get_puc_image_path()
        
class Orchestrator:
    """
    Classe Seletora de view (Orchestrator).
    Gerencia o registro e seleção de apresentações disponíveis.
    
    Responsabilidades:
    - Registrar classes de apresentação
    - Fornecer acesso às apresentações registradas
    - Gerar lista de apresentações para seletor UI
    """
    
    # Dicionário de apresentações registradas {key: presentation_class}
    PRESENTATIONS: Dict[str, type] = {}
    
    @classmethod
    def register_presentation(cls, presentation_class: type) -> None:
        """
        Registra uma classe de apresentação no orquestrador.
        
        Args:
            presentation_class: Classe que herda de Presentation
            
        Raises:
            ValueError: Se a classe não tiver KEY definida
        """
        if not hasattr(presentation_class, 'KEY') or not presentation_class.KEY:
            raise ValueError(
                f"Classe {presentation_class.__name__} deve definir KEY"
            )
        
        cls.PRESENTATIONS[presentation_class.KEY] = presentation_class
        print(f"✓ Apresentação registrada: {presentation_class.KEY} - {presentation_class.TITLE}")
    
    @classmethod
    def get_presentation(cls, key: str) -> Presentation:
        """
        Retorna uma instância da classe de apresentação registrada.
        
        Args:
            key: Chave identificadora da apresentação
            
        Returns:
            Instância da apresentação ou None se não encontrada
        """
        if key in cls.PRESENTATIONS:
            return cls.PRESENTATIONS[key]()
        return None
    
    @classmethod
    def get_presentation_list(cls) -> List[Dict[str, str]]:
        """
        Retorna a lista de apresentações registradas para o seletor de UI.
        
        Returns:
            Lista de dicionários com 'key' e 'title' de cada apresentação
        """
        return [
            {
                'key': key,
                'title': presentation_class.TITLE
            }
            for key, presentation_class in cls.PRESENTATIONS.items()
        ]
    
    @classmethod
    def list_registered_presentations(cls) -> None:
        """Exibe no console todas as apresentações registradas."""
        print("\n" + "="*60)
        print("APRESENTAÇÕES REGISTRADAS NO ORCHESTRATOR")
        print("="*60)
        for key, presentation_class in cls.PRESENTATIONS.items():
            print(f"  • {key}: {presentation_class.TITLE}")
        print("="*60 + "\n")
