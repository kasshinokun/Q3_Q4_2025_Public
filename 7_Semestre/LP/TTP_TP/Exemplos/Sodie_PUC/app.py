import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QStackedWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTabWidget, QMessageBox, QComboBox,
    QScrollArea, QGroupBox, QFormLayout, QFileDialog,
    QFrame,QDialog,QTableWidget,QHeaderView,QTableWidgetItem
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QPixmap, QImage
from datetime import date, timedelta
import os
import json
import barcode
from barcode.writer import ImageWriter
import io

# =============================================================================
# CONSTANTES GLOBAIS DE CONFIGURAÇÃO (mantidas do código original)
# =============================================================================
LIST_BASE=("Nome Comercial","Razão Social","CNPJ","Slogan","logomarca")
BACKUPDIR=os.path.dirname(os.path.abspath(__file__))+os.sep+'backups'
# --- Cores da Aplicação ---
COLOR_PRIMARY = "#FF6B9C"  # Rosa 
COLOR_GOLD_START = "#FFD700" # Ouro
COLOR_GOLD_END = "#D4AF37" # Dourado Suave (do CSS web)
COLOR_PRIMARY_HOVER = "#E55A8A"
COLOR_SECONDARY = "#6c757d"
COLOR_SECONDARY_HOVER = "#5a6268"
COLOR_BACKGROUND = "#FFF5F8"  # Fundo rosa claro
COLOR_BACKGROUND_START = "#FFB6C1" # Rosa Claro (do CSS web)
COLOR_BACKGROUND_END = "#FFD1DC" # Rosa Mais Claro (do CSS web)
COLOR_WIDGET_BG = "white"
COLOR_TEXT = "#333"
COLOR_HEADER = "#D81B60"  # Rosa mais escuro para headers
COLOR_DANGER = "#dc3545"
COLOR_DANGER_HOVER = "#c82333"
COLOR_BORDER = "#FFD1DC"  # Borda rosa claro

# --- Dimensões e Espaçamentos ---
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
LOGIN_FRAME_WIDTH = 400
LOGIN_FRAME_HEIGHT = 638 # Aumento de 20% (500 * 1.2 = 600) + 1 cm (aprox. 38px) = 638
INPUT_HEIGHT = 35
BUTTON_HEIGHT = 40
BUTTON_WIDTH = 160  # Ligeiramente maior
PADDING = 30
SPACING = 15
FONT_SIZE_LABEL = 11
FONT_SIZE_HEADER = 20


# =============================================================================
# DATABASE HANDLER (completo do código original)
# =============================================================================

class DatabaseHandler:
    MODELO_ESPERADO = {
        "Empresa": {
            "Nome Comercial": "",
            "Razão Social": "",
            "CNPJ": "",
            "Slogan": "",
            "logomarca": "",
            "Endereço": {
                "Rua": "",
                "Numero": "",
                "Complemento": "",
                "Bairro": "",
                "Cidade": "",
                "Municipalidade": "",
                "Estado/Província": "",
                "País": "",
                "CEP": ""
            },
            "Telefone": [],
            "Email": []
        },
        "Usuários": {
            "Proxima ID Novo Registro": 5,
            "Administrator": {
                "Id": 1,
                "Nome Completo": "Administrator",
                "Nome de Usuário": "Admin",
                "Senha de Usuário": "Admin",
                "Nível de Acesso": "Administrador"
            },
            "Tecnico": {
                "Id": 2,
                "Nome Completo": "Tecnico",
                "Nome de Usuário": "Tecnico",
                "Senha de Usuário": "Tecnico",
                "Nível de Acesso": "Tecnico"
            },
            "Gerente": {
                "Id": 3,
                "Nome Completo": "Gerencia",
                "Nome de Usuário": "Gerencia",
                "Senha de Usuário": "Gerencia",
                "Nível de Acesso": "Gerencia"
            },
            "Funcionários": {
                "Id": 4,
                "Nome Completo": "Funcionário",
                "Nome de Usuário": "Funcionário",
                "Senha de Usuário": "Funcionario",
                "Nível de Acesso": "Comum"
            }
        },
        "Produtos": {
            "Proxima ID Novo Registro": 10,
            "1": {
                "nome": "Bolo de Laranja",
                "porcao": "1 fatia (80g)",
                "codigoBarras12": "789731053003",
                "Pesos": [],
                "Valores": [],
                "tabelaNutricional": {
                    "Valor energético": "224 kcal",
                    "Carboidratos": "48.9g",
                    "Proteínas": "4.3g",
                    "Gorduras totais": "1.2g",
                    "Fibra alimentar": "0.9g",
                    "Sódio": "57mg"
                }
            },
            "2": {
                "nome": "Bolo de Chocolate",
                "porcao": "1 fatia (80g)",
                "codigoBarras12": "789638233195",
                "Pesos": [],
                "Valores": [],
                "tabelaNutricional": {
                    "Valor energético": "217 kcal",
                    "Carboidratos": "45.2g",
                    "Proteínas": "4.3g",
                    "Gorduras totais": "2.3g",
                    "Fibra alimentar": "1.6g",
                    "Sódio": "53mg"
                }
            },
            "3": {
                "nome": "Bolo de Limão",
                "porcao": "1 fatia (80g)",
                "codigoBarras12": "789039378790",
                "Pesos": [],
                "Valores": [],
                "tabelaNutricional": {
                    "Valor energético": "224 kcal",
                    "Carboidratos": "48.9g",
                    "Proteínas": "4.3g",
                    "Gorduras totais": "1.2g",
                    "Fibra alimentar": "0.9g",
                    "Sódio": "57mg"
                }
            },
            "4": {
                "nome": "Bolo Formigueiro",
                "porcao": "1 fatia (80g)",
                "codigoBarras12": "789357328379",
                "Pesos": [],
                "Valores": [],
                "tabelaNutricional": {
                    "Valor energético": "224 kcal",
                    "Carboidratos": "46.8g",
                    "Proteínas": "4.0g",
                    "Gorduras totais": "2.4g",
                    "Fibra alimentar": "1.2g",
                    "Sódio": "48mg"
                }
            },
            "5": {
                "nome": "Bolo de Côco",
                "porcao": "1 fatia (80g)",
                "codigoBarras12": "789071197020",
                "Pesos": [],
                "Valores": [],
                "tabelaNutricional": {
                    "Valor energético": "224 kcal",
                    "Carboidratos": "48.9g",
                    "Proteínas": "4.3g",
                    "Gorduras totais": "1.2g",
                    "Fibra alimentar": "0.9g",
                    "Sódio": "57mg"
                }
            },
            "6": {
                "nome": "Bolo Mesclado",
                "porcao": "1 fatia (80g)",
                "codigoBarras12": "789736502384",
                "Pesos": [],
                "Valores": [],
                "tabelaNutricional": {
                    "Valor energético": "224 kcal",
                    "Carboidratos": "48.9g",
                    "Proteínas": "4.3g",
                    "Gorduras totais": "1.2g",
                    "Fibra alimentar": "0.9g",
                    "Sódio": "57mg"
                }
            },
            "7": {
                "nome": "Bolo Mesclado com Cenoura",
                "porcao": "1 fatia (80g)",
                "codigoBarras12": "789736502385",
                "Pesos": [],
                "Valores": [],
                "tabelaNutricional": {
                    "Valor energético": "224 kcal",
                    "Carboidratos": "48.9g",
                    "Proteínas": "4.3g",
                    "Gorduras totais": "1.2g",
                    "Fibra alimentar": "0.9g",
                    "Sódio": "57mg"
                }
            },
            "8": {
                "nome": "Broa de Fubá Comum",
                "porcao": "1 fatia (80g)",
                "codigoBarras12": "789739468477",
                "Pesos": [],
                "Valores": [],
                "tabelaNutricional": {
                    "Valor energético": "306 kcal",
                    "Carboidratos": "33.0g",
                    "Proteínas": "3.1g",
                    "Gorduras totais": "18.5g",
                    "Fibra alimentar": "0.9g",
                    "Sódio": "73mg"
                }
            },
            "9": {
                "nome": "Broa de Milho Comum",
                "porcao": "1 fatia (80g)",
                "codigoBarras12": "789739468478",
                "Pesos": [],
                "Valores": [],
                "tabelaNutricional": {
                    "Valor energético": "306 kcal",
                    "Carboidratos": "33.0g",
                    "Proteínas": "3.1g",
                    "Gorduras totais": "18.5g",
                    "Fibra alimentar": "0.9g",
                    "Sódio": "73mg"
                }
            }
        },
        "Clientes": {
            "Proxima ID Novo Registro": 1,
            "1": {
                "Nome Comercial": "",
                "Razão Social": "",
                "CNPJ": "",
                "Endereço": {
                    "Rua": "",
                    "Numero": "",
                    "Complemento": "",
                    "Bairro": "",
                    "Cidade": "",
                    "Municipalidade": "",
                    "Estado/Província": "",
                    "País": "",
                    "CEP": ""
                },
                "Telefone": [],
                "Email": []
            }
        },
        "Lotes": {
            "Proxima ID Novo Registro": 1,
            "1": {
                "ID Produto": "",
                "Numero do Lote": "",
                "Fabricação do Lote": "",
                "Validade do Lote": ""
            }
        },
        "Pedidos": {
            "Proxima ID Novo Registro": 1,
            "1": {
                "ID Cliente": "",
                "ID Lote": "",
                "Quantidade": "",
                "Valor": "",
                "Status": "",
                "Data de Pagamento": ""
            }
        },
        "Valores_Diarios": {
            "Valor Energético": 2000,
            "Carboidratos": 300,
            "Proteínas": 75,
            "Gorduras Totais": 55,
            "Gorduras Saturadas": 22,
            "Gorduras Trans": 2,
            "Fibra Alimentar": 25,
            "Sódio": 2400
        }
    }

    def __init__(self):
        self.dados = None
        self.dados_modificados = False  # Nova variável para rastrear modificações

    def verificar_arquivo_existe(self, caminho_arquivo):
        return os.path.exists(caminho_arquivo)

    def _validar_estrutura_recursiva(self, dados_atual, modelo_esperado, caminho=""):
        if type(dados_atual) != type(modelo_esperado):
            return False, f"Tipo incorreto em {caminho}. Esperado: {type(modelo_esperado)}, Encontrado: {type(dados_atual)}"
        
        if isinstance(modelo_esperado, dict):
            for chave in modelo_esperado:
                if chave not in dados_atual:
                    return False, f"Chave '{chave}' não encontrada em {caminho}"
                
                novo_caminho = f"{caminho}.{chave}" if caminho else chave
                valido, mensagem = self._validar_estrutura_recursiva(
                    dados_atual[chave], modelo_esperado[chave], novo_caminho
                )
                if not valido:
                    return False, mensagem
        
        elif isinstance(modelo_esperado, list) and modelo_esperado:
            tipo_esperado = type(modelo_esperado[0])
            for i, item in enumerate(dados_atual):
                if type(item) != tipo_esperado:
                    return False, f"Tipo incorreto em {caminho}[{i}]. Esperado: {tipo_esperado}, Encontrado: {type(item)}"
        
        return True, ""

    def validar_estrutura_json(self, caminho_arquivo):
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            
            valido, mensagem = self._validar_estrutura_recursiva(dados, self.MODELO_ESPERADO)
            return valido, mensagem
            
        except json.JSONDecodeError as e:
            return False, f"Erro ao decodificar JSON: {str(e)}"
        except Exception as e:
            return False, f"Erro inesperado: {str(e)}"

    def criar_ou_validar_backup(self, caminho_arquivo=BACKUPDIR+os.sep+"database.json"):
        if self.verificar_arquivo_existe(caminho_arquivo):
            print(f"Arquivo {caminho_arquivo} encontrado.")
            
            valido, mensagem = self.validar_estrutura_json(caminho_arquivo)
            if valido:
                print("Estrutura do arquivo JSON é válida.")
                try:
                    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                        self.dados = json.load(f)
                    return True, "Backup carregado com sucesso"
                except Exception as e:
                    print(f"Erro ao carregar arquivo: {e}")
                    return False, f"Erro ao carregar arquivo: {e}"
            else:
                print(f"Estrutura inválida: {mensagem}")
                return False, f"Estrutura inválida: {mensagem}"
        else:
            print(f"Arquivo {caminho_arquivo} não encontrado.")
            
            diretorio = os.path.dirname(caminho_arquivo)
            if diretorio and not os.path.exists(diretorio):
                try:
                    os.makedirs(diretorio, exist_ok=True)
                    print(f"Diretório {diretorio} criado.")
                except Exception as e:
                    print(f"Erro ao criar diretório: {e}")
                    return False, f"Erro ao criar diretório: {e}"
            
            try:
                with open(caminho_arquivo, 'w', encoding='utf-8') as f:
                    json.dump(self.MODELO_ESPERADO, f, ensure_ascii=False, indent=4)
                print(f"Arquivo {caminho_arquivo} criado com a estrutura modelo.")
                self.dados = self.MODELO_ESPERADO.copy()
                return True, "Backup criado com sucesso"
            except Exception as e:
                print(f"Erro ao criar arquivo: {e}")
                return False, f"Erro ao criar arquivo: {e}"
            
    def carregar_arquivo_externo(self, caminho_arquivo):
        """Carrega e valida um arquivo JSON externo"""
        valido, mensagem = self.validar_estrutura_json(caminho_arquivo)
        if valido:
            try:
                with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                    novos_dados = json.load(f)
                self.dados = novos_dados
                self.dados_modificados = True
                return True, "Arquivo carregado e validado com sucesso!"
            except Exception as e:
                return False, f"Erro ao carregar arquivo: {str(e)}"
        else:
            return False, f"Arquivo inválido: {mensagem}"

    def salvar_dados_atuais(self, caminho_arquivo=BACKUPDIR+os.sep+"database.json"):
        """Salva os dados atuais em execução para o arquivo padrão"""
        try:
            diretorio = os.path.dirname(caminho_arquivo)
            if diretorio and not os.path.exists(diretorio):
                os.makedirs(diretorio, exist_ok=True)
            
            with open(caminho_arquivo, 'w', encoding='utf-8') as f:
                json.dump(self.dados, f, ensure_ascii=False, indent=4)
            
            self.dados_modificados = False
            return True, "Dados salvos com sucesso!"
        except Exception as e:
            return False, f"Erro ao salvar dados: {str(e)}"
    
    def ler_dados_request_json(self, atributo: str, arquivo_json=BACKUPDIR+os.sep+"database.json"):
        """
        Versão ajustada: retorna o valor se existir, caso contrário retorna o nome do atributo como placeholder
        """
        try:
            with open(arquivo_json, 'r', encoding='utf-8') as file:
                dados = json.load(file)
            
            # Verifica se a estrutura existe
            if 'Empresa' not in dados:
                print("Erro: Seção 'Empresa' não encontrada no JSON")
                return atributo  # Retorna atributo como placeholder
            
            empresa = dados['Empresa']
            valor_atributo = empresa.get(atributo)
            
            # Verifica se o atributo existe e não está vazio
            if valor_atributo is None:
                print(f"Tag {atributo} não encontrada")
                return atributo  # Retorna atributo como placeholder
            elif valor_atributo == "":
                print(f"{atributo} está vazia")
                return atributo  # Retorna atributo como placeholder
            else:
                return valor_atributo  # Retorna o VALOR real
                
        except Exception as e:
            print(f"Erro ao ler {atributo}: {e}")
            return atributo  # Retorna atributo como placeholder em caso de exception

    def verificar_estado_inicial(self):
        """Verifica se os dados básicos da empresa estão no estado inicial"""
        list_base = LIST_BASE
        verificar = []
        try:
            for item in list_base:
                valor = self.ler_dados_request_json(item)
                verificar.append(valor)
                print(f"Item: {item}, Valor retornado: '{valor}'")
            
            return verificar
            
        except Exception as e:
            print(f"Erro ao verificar estado inicial: {e}")
            return list_base  # Retorna LIST_BASE em caso de erro

    def _converter_e_salvar_imagem(self, source_path):
        """
        Converte e salva a imagem como PNG no diretório /images/
        Retorna (sucesso, mensagem)
        """
        try:
            # 1. Definir caminhos
            base_dir = os.path.dirname(os.path.abspath(__file__))
            images_dir = os.path.join(base_dir, 'images')
            target_path = os.path.join(images_dir, 'logo.png')
            
            # 2. Criar diretório se não existir
            if not os.path.exists(images_dir):
                os.makedirs(images_dir)
            
            # 3. Carregar e salvar a imagem usando QPixmap
            pixmap = QPixmap(source_path)
            if pixmap.isNull():
                return False, "Erro: Não foi possível carregar a imagem de origem."
            
            # Redimensionar para um tamanho razoável (opcional)
            scaled_pixmap = pixmap.scaled(256, 256, 
                                          Qt.AspectRatioMode.KeepAspectRatio, 
                                          Qt.TransformationMode.SmoothTransformation)
            
            # Salvar como PNG
            if not scaled_pixmap.save(target_path, "PNG"):
                return False, "Erro: Não foi possível salvar a imagem como logo.png."
            
            # 4. Atualizar o path no database.json
            if not self.dados:
                self.carregar_dados()
            
            if 'Empresa' in self.dados and 'logomarca' in self.dados['Empresa']:
                self.dados['Empresa']['logomarca'] = target_path
                self.dados_modificados = True
                self.salvar_dados_atuais()
                return True, f"Logomarca salva com sucesso em {target_path} e path atualizado no database."
            else:
                return False, "Erro: Estrutura 'Empresa' ou 'logomarca' não encontrada nos dados."
                
        except Exception as e:
            return False, f"Erro inesperado ao converter e salvar imagem: {e}"

    def carregar_dados(self, caminho_arquivo=BACKUPDIR+os.sep+"database.json"):
        """Carrega dados do arquivo JSON para self.dados"""
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                self.dados = json.load(f)
            return True
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            return False

# =============================================================================
# CLASSES BASE COM HERANÇA (ATUALIZADAS)
# =============================================================================

class BaseWidget(QWidget):
    def __init__(self, stacked_widget=None, db_handler=None):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.db_handler = db_handler

        self.setup_ui()
        self.apply_base_styles()
    
    def setup_ui(self):
        pass
    
    def apply_base_styles(self):
        self.setStyleSheet(f"""
            background-color: {COLOR_BACKGROUND}; 
            font-family: 'Segoe UI', Arial, sans-serif;
            color: {COLOR_TEXT};
        """)


class StyledButton(QPushButton):
    def __init__(self, text, normal_color, hover_color, parent=None, rounded=True):
        super().__init__(text, parent)
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.rounded = rounded
        self.apply_styles()
    
    def apply_styles(self):
        radius = "15px" if self.rounded else "5px"
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.normal_color}; 
                color: white; 
                border-radius: {radius};
                border: none;
                padding: 10px 20px;
                font-size: 12px;
                font-weight: bold;
                min-height: {BUTTON_HEIGHT}px;
            }}
            QPushButton:hover {{
                background-color: {self.hover_color}; 
            }}
            QPushButton:pressed {{
                background-color: {self.normal_color};
            }}
        """)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

class PrimaryButton(StyledButton):
    def __init__(self, text, parent=None, rounded=True):
        super().__init__(text, COLOR_PRIMARY, COLOR_PRIMARY_HOVER, parent, rounded)

class SecondaryButton(StyledButton):
    def __init__(self, text, parent=None, rounded=True):
        super().__init__(text, COLOR_SECONDARY, COLOR_SECONDARY_HOVER, parent, rounded)

class StyledLineEdit(QLineEdit):
    def __init__(self, placeholder_text="", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder_text)
        self.apply_styles()
    
    def apply_styles(self):
        self.setStyleSheet(f"""
            QLineEdit {{
                border: 2px solid {COLOR_BORDER}; 
                background-color: {COLOR_WIDGET_BG}; 
                border-radius: 10px; 
                padding: 8px 12px;
                font-size: {FONT_SIZE_LABEL}px;
                selection-background-color: {COLOR_PRIMARY};
            }}
            QLineEdit:focus {{
                border-color: {COLOR_PRIMARY};
            }}
        """)
        self.setMinimumHeight(INPUT_HEIGHT)

class StyledLabel(QLabel):
    def __init__(self, text="", is_header=False, parent=None, font_size=None):
        super().__init__(text, parent)
        self.is_header = is_header
        self.font_size = font_size
        self.apply_styles()
    
    def apply_styles(self):
        if self.is_header:
            self.setStyleSheet(f"color: {COLOR_HEADER}; font-size: {FONT_SIZE_HEADER}px; font-weight: bold;")
            self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            font_size = self.font_size if self.font_size else FONT_SIZE_LABEL
            self.setStyleSheet(f"color: {COLOR_TEXT}; font-size: {font_size}px;")
        
        font_size = FONT_SIZE_HEADER if self.is_header else (self.font_size if self.font_size else FONT_SIZE_LABEL)
        font = QFont("Segoe UI", font_size)
        if self.is_header:
            font.setWeight(QFont.Weight.Bold)
        self.setFont(font)

# =============================================================================
# LOGIN WINDOW (ATUALIZADA)
# =============================================================================

class LoginWindow(BaseWidget):
    
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Container principal com gradiente
        self.login_container = QWidget()
        self.login_container.setFixedSize(LOGIN_FRAME_WIDTH, LOGIN_FRAME_HEIGHT)
        self.login_container.setStyleSheet(f"""
            /* Degradê Rosa (Original) */
            /* background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {COLOR_PRIMARY}, stop:1 {COLOR_BACKGROUND}); */
            
            /* Degradê Amarelo/Dourado (Solicitado) */
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {COLOR_GOLD_START}, stop:1 {COLOR_GOLD_END});
            border-radius: 20px;
            border: 2px solid {COLOR_BORDER};
        """)

        # Frame interno branco
        self.login_frame = QWidget(self.login_container)
        self.login_frame.setGeometry(10, 10, LOGIN_FRAME_WIDTH-20, LOGIN_FRAME_HEIGHT-20)
        self.login_frame.setStyleSheet(f"""
            background-color: {COLOR_WIDGET_BG}; 
            border-radius: 15px;
        """)

        form_layout = QVBoxLayout(self.login_frame)
        form_layout.setContentsMargins(PADDING, PADDING, PADDING, PADDING)
        form_layout.setSpacing(SPACING)

       # Logo/Header
        header_label = StyledLabel(self.db_handler.ler_dados_request_json('Nome Comercial'), is_header=True)
        header_label.setStyleSheet(f"color: {COLOR_HEADER}; font-size: 30.8px; font-weight: bold;")
        form_layout.addWidget(header_label)
        
        subtitle_label = StyledLabel(self.db_handler.ler_dados_request_json('Slogan'))
        subtitle_label.setStyleSheet(f"color: {COLOR_PRIMARY}; font-size: 14px; font-style: italic;")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_layout.addWidget(subtitle_label)
        
        form_layout.addSpacing(20)

        # Imagem da logomarca
        image_label = QLabel()
        LOGO_HEIGHT = 120
        LOGO_RADIUS = LOGO_HEIGHT / 2
        OFFSET_Y = int(LOGO_HEIGHT * 0.5) # 60px
        
        image_label.setFixedSize(LOGO_HEIGHT, LOGO_HEIGHT)
        image_label.setStyleSheet(f"""
            background-color: {COLOR_BACKGROUND};
            border: 2px dashed {COLOR_BORDER};
            border-radius: {LOGO_RADIUS}px;
        """)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Obter caminho da logomarca
        path_logomarca = ""
        if self.db_handler:
            path_logomarca = self.db_handler.ler_dados_request_json('logomarca')
            print(f"Tentando carregar logomarca: {path_logomarca}")
        
        # Tentar carregar a imagem
        try:
            if path_logomarca and os.path.exists(path_logomarca):
                pixmap = QPixmap(path_logomarca)
                if not pixmap.isNull():
                    scaled_pixmap = pixmap.scaled(image_label.size(), 
                                                 Qt.AspectRatioMode.KeepAspectRatio, 
                                                 Qt.TransformationMode.SmoothTransformation)
                    image_label.setPixmap(scaled_pixmap)
                    image_label.setScaledContents(True)
                    print("Logomarca carregada com sucesso")
                else:
                    print("Erro: Imagem da logomarca inválida ou corrompida")
                    image_label.setText("Logomarca\nnão carregada")
            else:
                print(f"Arquivo de logomarca não encontrado: {path_logomarca}")
                image_label.setText("Logomarca\nnão configurada")
        except Exception as e:
            print(f"Erro ao carregar logomarca: {e}")
            image_label.setText("Erro ao\ncarregar imagem")
        
        form_layout.addWidget(image_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        
        form_layout.addSpacing(30 + OFFSET_Y) # Adiciona o deslocamento original ao espaçamento após a logo
        
        # Deslocamento adicional de 0.5 cm (aproximadamente 19 pixels) solicitado pelo usuário
        OFFSET_0_5_CM = 19 
        form_layout.addSpacing(OFFSET_0_5_CM)

        # Campos de entrada
        username_label = StyledLabel('Nome do Usuário')
        form_layout.addWidget(username_label)
        
        self.username_input = StyledLineEdit()
        self.username_input.setFixedSize(LOGIN_FRAME_WIDTH - (2 * PADDING), INPUT_HEIGHT)
        form_layout.addWidget(self.username_input)

        password_label = StyledLabel('Senha do Usuário')
        form_layout.addWidget(password_label)
        
        self.password_input = StyledLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedSize(LOGIN_FRAME_WIDTH - (2 * PADDING), INPUT_HEIGHT)
        form_layout.addWidget(self.password_input)

        form_layout.addSpacing(20)

        # Botões
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(SPACING)
        
        SPACING_1MM = 11
        
        self.clear_btn = SecondaryButton('Limpar', rounded=True)
        self.clear_btn.setFixedSize((LOGIN_FRAME_WIDTH - (2 * PADDING) - SPACING) // 2, BUTTON_HEIGHT)
        self.clear_btn.clicked.connect(self.clear_fields)
        buttons_layout.addWidget(self.clear_btn)
        
        self.login_btn = PrimaryButton('Entrar', rounded=True)
        self.login_btn.setFixedSize((LOGIN_FRAME_WIDTH - (2 * PADDING) - SPACING) // 2, BUTTON_HEIGHT)
        self.login_btn.clicked.connect(self.login)
        buttons_layout.addWidget(self.login_btn)
        
        form_layout.addLayout(buttons_layout)
        
        form_layout.addStretch()
        form_layout.addSpacing(SPACING_1MM)
        
        # Botão Backup
        self.backup_btn = SecondaryButton('Backup do Sistema', rounded=True)
        self.backup_btn.setFixedSize(150, BUTTON_HEIGHT)
        self.backup_btn.clicked.connect(self.backup)
        form_layout.addWidget(self.backup_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        main_layout.addWidget(self.login_container)

    def login(self):
        if not self.username_input.text() or not self.password_input.text():
            QMessageBox.warning(self, 'Erro', 'Preencha todos os campos!')
            return
        
        username = self.username_input.text()
        print(f"Tentativa de login com usuário: {username}")
        
        home_window = self.stacked_widget.widget(1)
        if hasattr(home_window, 'set_current_user'):
            home_window.set_current_user(username)
        
        self.stacked_widget.setCurrentIndex(1)

    def clear_fields(self):
        self.username_input.clear()
        self.password_input.clear()    

    def backup(self):   
        print("Acessando Sessão de Restauração")
        backup_window = self.stacked_widget.widget(4)
        if hasattr(backup_window, 'set_return_index'):
            backup_window.set_return_index(0)
        self.stacked_widget.setCurrentIndex(4)

# =============================================================================
# HOME WINDOW (ATUALIZADA)
# =============================================================================

class HomeWindow(BaseWidget):
    def __init__(self, stacked_widget, db_handler):
        super().__init__(stacked_widget, db_handler)
        self.current_user = None
    
    def setup_ui(self):
        # Estilo QSS para o QTabWidget
        tab_style = f"""
            QTabWidget::pane {{
                border: 1px solid #ccc;
                background-color: {COLOR_WIDGET_BG};
            }}
            QTabBar::tab {{
                background: {COLOR_SECONDARY};
                color: white;
                padding: 8px 15px;
                border: 1px solid #ccc;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                margin-right: 2px;
            }}
            QTabBar::tab:selected {{
                background: {COLOR_PRIMARY};
                color: white;
                border-color: {COLOR_PRIMARY};
                border-bottom-color: {COLOR_WIDGET_BG};
            }}
            QTabBar::tab:hover {{
                background: {COLOR_SECONDARY_HOVER};
            }}
        """
        self.setStyleSheet(self.styleSheet() + tab_style)
        layout = QVBoxLayout()
        layout.setContentsMargins(PADDING, PADDING, PADDING, PADDING)
        layout.setSpacing(SPACING)

        # Top Bar
        top_bar = QHBoxLayout()
        top_bar.setAlignment(Qt.AlignmentFlag.AlignLeft)
        top_bar.setSpacing(SPACING)

        # Logo e título
        logo_layout = QHBoxLayout()
        title_label = StyledLabel(self.db_handler.ler_dados_request_json('Nome Comercial'), is_header=True)
        title_label.setStyleSheet(f"color: {COLOR_HEADER}; font-size: 24px;")
        logo_layout.addWidget(title_label)
        
        subtitle_label = StyledLabel(self.db_handler.ler_dados_request_json('Slogan'))
        subtitle_label.setStyleSheet(f"color: {COLOR_PRIMARY}; font-size: 12px; font-style: italic; margin-left: 10px;")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        logo_layout.addWidget(subtitle_label)
        logo_layout.addStretch()
        
        top_bar.addLayout(logo_layout)
        top_bar.addStretch()

        # Botões de ação
        self.settings_btn = SecondaryButton("Configurações", rounded=True)
        self.settings_btn.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        self.settings_btn.clicked.connect(self.go_to_settings)
        top_bar.addWidget(self.settings_btn)

        self.logout_btn = PrimaryButton("Sair", rounded=True)
        self.logout_btn.setFixedSize(BUTTON_WIDTH, BUTTON_HEIGHT)
        self.logout_btn.clicked.connect(self.logout)
        top_bar.addWidget(self.logout_btn)

        top_bar.addStretch()
        
        self.user_label = StyledLabel("", is_header=False)
        self.user_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.user_label.setStyleSheet(f"color: {COLOR_TEXT}; font-size: {FONT_SIZE_LABEL}px; padding-right: 20px;")
        top_bar.addWidget(self.user_label)
        
        layout.addLayout(top_bar)

        # Abas
        self.tabs = QTabWidget()
        
        # 1. Gerar Tabela Nutricional (ATUALIZADA)
        
        # Widget de conteúdo principal
        content_widget = QWidget()
        tabela_nutricional_layout = QHBoxLayout(content_widget)
        tabela_nutricional_layout.setContentsMargins(PADDING, PADDING, PADDING, PADDING)
        tabela_nutricional_layout.setSpacing(SPACING)
        
        # QScrollArea para permitir rolagem vertical
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(content_widget)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # Widget principal da aba que contém o scroll area
        tabela_nutricional_widget = QWidget()
        main_vbox = QVBoxLayout(tabela_nutricional_widget)
        main_vbox.setContentsMargins(0, 0, 0, 0)
        main_vbox.addWidget(scroll_area)
        
        # Frame esquerdo (1/3 da largura)
        left_frame = QFrame()
        left_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        left_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLOR_WIDGET_BG};
                border: 1px solid {COLOR_BORDER};
                border-radius: 5px;
                margin: 0;
                padding: 11px;
            }}
        """)
        left_layout = QVBoxLayout(left_frame)
        left_layout.setContentsMargins(SPACING, SPACING, SPACING, SPACING)
        left_layout.setSpacing(SPACING)
        
        # Conteúdo do frame esquerdo
        left_title = StyledLabel("Configurações da Tabela", is_header=True)
        left_title.setStyleSheet(f"color: {COLOR_HEADER}; font-size: 16px;")
        left_layout.addWidget(left_title)
        
        # Seleção de produto
        produto_label = StyledLabel("Selecionar Produto:")
        left_layout.addWidget(produto_label)
        
        self.produto_combo = QComboBox()
        self.carregar_produtos_tabela()
        self.produto_combo.currentIndexChanged.connect(self.carregar_dados_nutricionais) # Conecta o sinal
        left_layout.addWidget(self.produto_combo)
        
        # Campos de entrada para dados nutricionais
        dados_label = StyledLabel("Dados Nutricionais:")
        dados_label.setStyleSheet(f"color: {COLOR_HEADER}; font-weight: bold; margin-top: 10px;")
        left_layout.addWidget(dados_label)

        self.campo_energia = StyledLineEdit("")
        self.campo_carboidratos = StyledLineEdit("")
        self.campo_proteinas = StyledLineEdit("")
        self.campo_gorduras = StyledLineEdit("")

        # Usar QFormLayout para os campos de entrada para melhor alinhamento
        form_layout = QFormLayout()
        form_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(SPACING // 2) # Espaçamento menor entre os campos

        # Adicionar campos ao FormLayout
        form_layout.addRow("Valor energético (kcal):", self.campo_energia)
        form_layout.addRow("Carboidratos (g):", self.campo_carboidratos)
        form_layout.addRow("Proteínas (g):", self.campo_proteinas)
        form_layout.addRow("Gorduras totais (g):", self.campo_gorduras)

        left_layout.addLayout(form_layout)
        
        # Botões de ação
        btn_gerar = PrimaryButton("Gerar Tabela", rounded=True)
        btn_gerar.clicked.connect(self.gerar_tabela_nutricional)
        left_layout.addWidget(btn_gerar)
        
        btn_limpar = SecondaryButton("Limpar Campos", rounded=True)
        btn_limpar.clicked.connect(self.limpar_campos_tabela)
        left_layout.addWidget(btn_limpar)
        
        left_layout.addStretch()
        
        # Frame direito (2/3 da largura)
        right_frame = QFrame()
        right_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        right_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLOR_WIDGET_BG};
                border: 1px solid {COLOR_BORDER};
                border-radius: 5px;
                margin: 0;
                padding: 11px;
            }}
        """)
        right_layout = QVBoxLayout(right_frame)
        right_layout.setContentsMargins(SPACING, SPACING, SPACING, SPACING)
        right_layout.setSpacing(SPACING)
        
        # Conteúdo do frame direito
        right_title = StyledLabel("Prévia da Tabela Nutricional", is_header=True)
        right_title.setStyleSheet(f"color: {COLOR_HEADER}; font-size: 16px;")
        right_layout.addWidget(right_title)
        
        # Área de prévia
        self.preview_area = QLabel()
        self.preview_area.setMinimumHeight(400)
        self.preview_area.setStyleSheet(f"""
            border: 2px dashed {COLOR_BORDER};
            background-color: {COLOR_BACKGROUND};
            padding: 15px;
            border-radius: 5px;
        """)
        self.preview_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_area.setText("A tabela nutricional será gerada aqui...\n\nSelecione um produto e clique em 'Gerar Tabela'")
        self.preview_area.setWordWrap(True)
        right_layout.addWidget(self.preview_area)
        
        # Botões de exportação
        btn_layout = QHBoxLayout()
        btn_exportar_pdf = PrimaryButton("Exportar PDF", rounded=True)
        btn_exportar_pdf.clicked.connect(self.exportar_pdf_tabela)
        btn_layout.addWidget(btn_exportar_pdf)
        
        btn_exportar_imagem = SecondaryButton("Exportar Imagem", rounded=True)
        btn_exportar_imagem.clicked.connect(self.exportar_imagem_tabela)
        btn_layout.addWidget(btn_exportar_imagem)
        
        right_layout.addLayout(btn_layout)
        # right_layout.addStretch() # Removido para manter o conteúdo no topo do frame direito
        
        # Adicionar frames ao layout principal
        tabela_nutricional_layout.addWidget(left_frame, 1)  # 1/3 da largura
        tabela_nutricional_layout.addWidget(right_frame, 2)  # 2/3 da largura
        
        self.tabs.addTab(tabela_nutricional_widget, 'Gerar Tabela Nutricional')
        
        # 2. Gerar Etiqueta (Usando a EtiquetaWindow existente)
        etiqueta_widget = QWidget()
        etiqueta_layout = QVBoxLayout(etiqueta_widget)
        etiqueta_layout.addWidget(StyledLabel("Clique no botão abaixo para acessar a tela de Geração de Etiqueta."))
        btn_go_etiqueta = PrimaryButton("Acessar Geração de Etiqueta")
        btn_go_etiqueta.clicked.connect(self.go_to_etiqueta)
        etiqueta_layout.addWidget(btn_go_etiqueta)
        etiqueta_layout.addStretch()
        self.tabs.addTab(etiqueta_widget, 'Gerar Etiqueta')
        
        # 3. Gestão de Produtos
        gestao_produtos_widget = GestaoProdutosWidget(self.db_handler)
        self.tabs.addTab(gestao_produtos_widget, 'Gestão de Produtos')
        
        # 4. Gestão de Pedidos
        gestao_pedidos_widget = GestaoPedidosWidget(self.db_handler)
        self.tabs.addTab(gestao_pedidos_widget, 'Gestão de Pedidos')
        
        # 5. Gestão de Clientes
        gestao_clientes_widget = GestaoClientesWidget(self.db_handler)
        self.tabs.addTab(gestao_clientes_widget, 'Gestão de Clientes')

        layout.addWidget(self.tabs)
        self.setLayout(layout)
        
    def carregar_dados_nutricionais(self):
        """Carrega os dados nutricionais do produto selecionado para os campos de entrada."""
        produto_id = self.produto_combo.currentData()
        
        # Ignora a chamada se o combobox estiver vazio ou o ID for None (ex: durante o clear)
        if not produto_id:
            return

        produtos = self.db_handler.dados.get('Produtos', {})
        produto = produtos.get(produto_id)

        if produto and 'tabelaNutricional' in produto:
            tabela = produto['tabelaNutricional']
            
            # Mapeamento dos campos do JSON para os QLineEdits
            campos = {
                'Valor energético': self.campo_energia,
                'Carboidratos': self.campo_carboidratos,
                'Proteínas': self.campo_proteinas,
                'Gorduras totais': self.campo_gorduras,
                # Adicionar outros campos conforme necessário
            }

            for chave, campo in campos.items():
                # Remove a unidade de medida (kcal, g, mg) para deixar apenas o valor numérico no campo
                valor_com_unidade = tabela.get(chave, '')
                valor_numerico = ''.join(filter(lambda x: x.isdigit() or x == '.' or x == ',', valor_com_unidade)).replace(',', '.')
                
                # Formata de volta para o padrão brasileiro (vírgula como separador decimal)
                if valor_numerico:
                    try:
                        valor_numerico = str(float(valor_numerico)).replace('.', ',')
                    except ValueError:
                        pass # Mantém o valor original se a conversão falhar

                campo.setText(valor_numerico)
        else:
            # Limpa os campos se o produto não tiver dados nutricionais
            self.campo_energia.setText("")
            self.campo_carboidratos.setText("")
            self.campo_proteinas.setText("")
            self.campo_gorduras.setText("")

    def carregar_produtos_tabela(self):
        """Carrega os produtos do banco de dados para o combobox da tabela nutricional"""
        self.produto_combo.clear()
        if self.db_handler.dados and 'Produtos' in self.db_handler.dados:
            produtos = self.db_handler.dados['Produtos']
            for key, produto in produtos.items():
                if key != 'Proxima ID Novo Registro':
                    self.produto_combo.addItem(produto['nome'], key)
            print(f"Carregados {self.produto_combo.count()} produtos para tabela nutricional")
        else:
            print("Nenhum produto encontrado no banco de dados")

    def gerar_tabela_nutricional(self):
        """Gera a prévia da tabela nutricional"""
        produto_selecionado = self.produto_combo.currentText()
        if not produto_selecionado:
            QMessageBox.warning(self, 'Aviso', 'Selecione um produto primeiro!')
            return
        
        # Simulação de geração de tabela nutricional
        preview_text = f"TABELA NUTRICIONAL - {produto_selecionado}\n\n"
        preview_text += f"Valor energético: {self.campo_energia.text() or '--'} kcal\n"
        preview_text += f"Carboidratos: {self.campo_carboidratos.text() or '--'} g\n"
        preview_text += f"Proteínas: {self.campo_proteinas.text() or '--'} g\n"
        preview_text += f"Gorduras totais: {self.campo_gorduras.text() or '--'} g\n\n"
        preview_text += "Esta é uma prévia da tabela nutricional.\n"
        preview_text += "A funcionalidade completa será implementada posteriormente."
        
        self.preview_area.setText(preview_text)
        QMessageBox.information(self, 'Sucesso', f'Tabela nutricional gerada para: {produto_selecionado}')

    def limpar_campos_tabela(self):
        """Limpa os campos da tabela nutricional"""
        self.campo_energia.clear()
        self.campo_carboidratos.clear()
        self.campo_proteinas.clear()
        self.campo_gorduras.clear()
        self.preview_area.setText("A tabela nutricional será gerada aqui...\n\nSelecione um produto e clique em 'Gerar Tabela'")

    def exportar_pdf_tabela(self):
        """Exporta a tabela nutricional como PDF (placeholder)"""
        QMessageBox.information(self, 'Exportar PDF', 'Funcionalidade de exportação PDF será implementada em breve.')

    def exportar_imagem_tabela(self):
        """Exporta a tabela nutricional como imagem (placeholder)"""
        QMessageBox.information(self, 'Exportar Imagem', 'Funcionalidade de exportação de imagem será implementada em breve.')

    def set_current_user(self, username):
        self.current_user = username
        self.user_label.setText(f"Usuário: {self.current_user}")

    def get_current_user(self):
        return self.current_user

    def go_to_settings(self):
        self.stacked_widget.setCurrentIndex(2)

    def go_to_etiqueta(self):
        self.stacked_widget.setCurrentIndex(3)

    def logout(self):
        self.current_user = None
        self.user_label.setText("")
        self.stacked_widget.setCurrentIndex(0)

# =============================================================================
# CLASSE EtiquetaWindow (mantida do código anterior)
# =============================================================================
# =============================================================================
# CLASSE EtiquetaWindow (CORRIGIDA)
# =============================================================================

class EtiquetaWindow(BaseWidget):
    def __init__(self, stacked_widget, db_handler):
        super().__init__(stacked_widget, db_handler)

        self.current_product = None
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(PADDING, PADDING, PADDING, PADDING)
        layout.setSpacing(SPACING)

        # Top Bar com botão Voltar e Título
        top_bar_layout = QHBoxLayout()

        self.back_btn = SecondaryButton('Voltar para Home')
        self.back_btn.clicked.connect(self.go_to_home)
        top_bar_layout.addWidget(self.back_btn, alignment=Qt.AlignmentFlag.AlignLeft)

        top_bar_layout.addStretch()

        title_label = StyledLabel('Gerar Etiqueta com Código de Barras', is_header=True)
        top_bar_layout.addWidget(title_label)
        
        top_bar_layout.addStretch()
        
        layout.addLayout(top_bar_layout)
       
        # Área de conteúdo principal
        content_layout = QHBoxLayout()
        
        # Painel de controle esquerdo
        control_panel = QGroupBox("Configurações da Etiqueta")
        control_panel.setStyleSheet(f"""
            QGroupBox {{
                background-color: {COLOR_WIDGET_BG};
                border: 1px solid #ccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }}
        """)
        control_layout = QFormLayout()
        
        # Seleção de produto
        self.product_combo = QComboBox()
        self.load_products()
        self.product_combo.currentTextChanged.connect(self.on_product_selected)
        control_layout.addRow("Produto:", self.product_combo)
        
        # Código de barras
        self.barcode_input = StyledLineEdit("Código EAN13")
        control_layout.addRow("Código Barras:", self.barcode_input)
        
        # Datas
        self.fabricacao_input = StyledLineEdit()
        self.validade_input = StyledLineEdit()
        
        today = date.today()
        self.fabricacao_input.setText(today.strftime('%d/%m/%Y'))
        self.validade_input.setText((today + timedelta(days=6)).strftime('%d/%m/%Y'))
        
        control_layout.addRow("Data Fabricação:", self.fabricacao_input)
        control_layout.addRow("Data Validade:", self.validade_input)
        
        # Adicionar o QLabel para a prévia do código de barras
        self.barcode_preview_label = QLabel("Prévia do Código de Barras")
        self.barcode_preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.barcode_preview_label.setMinimumHeight(100)
        self.barcode_preview_label.setStyleSheet(f"""
            border: 1px solid {COLOR_BORDER};
            background-color: {COLOR_BACKGROUND};
            padding: 5px;
        """)
        control_layout.addRow(self.barcode_preview_label)
        
        # Botões de ação
        btn_layout = QHBoxLayout()
        self.preview_btn = PrimaryButton('Gerar Prévia', rounded=True)
        self.preview_btn.clicked.connect(self.generate_preview)
        btn_layout.addWidget(self.preview_btn)
        
        self.save_btn = PrimaryButton('Salvar PDF', rounded=True)
        self.save_btn.clicked.connect(self.save_pdf)
        btn_layout.addWidget(self.save_btn)
        
        control_layout.addRow(btn_layout)
        control_panel.setLayout(control_layout)
        
        # Painel de visualização direito
        preview_panel = QGroupBox("Prévia da Etiqueta")
        preview_panel.setStyleSheet(f"""
            QGroupBox {{
                background-color: {COLOR_WIDGET_BG};
                border: 1px solid #ccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }}
        """)
        preview_layout = QVBoxLayout()
        
        self.preview_label = QLabel()
        self.preview_label.setMinimumSize(400, 400)
        self.preview_label.setStyleSheet(f"""
            border: 2px dashed {COLOR_BORDER};
            background-color: {COLOR_WIDGET_BG};
            padding: 10px;
        """)
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setText("Selecione um produto e clique em 'Gerar Prévia'")
        
        preview_layout.addWidget(self.preview_label)
        preview_panel.setLayout(preview_layout)
        
        content_layout.addWidget(control_panel, 1)
        content_layout.addWidget(preview_panel, 2)
        
        layout.addLayout(content_layout)
        layout.addStretch()
        
        self.setLayout(layout)
        
        # Chamada inicial para carregar os dados do primeiro item após a criação de todos os widgets
        self.on_product_selected(self.product_combo.currentText())
    
    def load_products(self):
        """Carrega os produtos do banco de dados (dicionário do /backups)"""
        self.product_combo.clear()
        if self.db_handler.dados and 'Produtos' in self.db_handler.dados:
            produtos = self.db_handler.dados['Produtos']
            for key, produto in produtos.items():
                if key != 'Proxima ID Novo Registro':
                    self.product_combo.addItem(produto['nome'], key)
            print(f"Carregados {self.product_combo.count()} produtos do banco de dados")
        else:
            print("Nenhum produto encontrado no banco de dados")
    
    def on_product_selected(self, product_name):
        """Quando um produto é selecionado, atualiza os campos"""
        if not product_name:
            return
            
        produtos = self.db_handler.dados['Produtos']
        for key, produto in produtos.items():
            if key != 'Proxima ID Novo Registro' and produto['nome'] == product_name:
                self.current_product = produto
                codigo_barras = produto.get('codigoBarras12', '')
                self.barcode_input.setText(codigo_barras)
                print(f"Produto selecionado: {product_name}")
                
                # Chamar a função para gerar e exibir o código de barras
                self.update_barcode_preview(codigo_barras, product_name)
                break
    
    def update_barcode_preview(self, codigo_barras, nome_produto):
        """Gera e exibe a imagem do código de barras, salvando-a no diretório /barcodes."""
        
        # 1. Criar o diretório /barcodes se não existir
        barcode_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'barcodes')
        os.makedirs(barcode_dir, exist_ok=True)
        
        if not codigo_barras or len(codigo_barras) not in [12, 13]:
            self.barcode_preview_label.setText("Código de Barras Inválido (EAN-13 ou EAN-12)")
            self.barcode_preview_label.clear()
            return

        try:
            # 2. Gerar o código de barras
            # O EAN13 requer 13 dígitos. Se for 12, o barcode.EAN13 adiciona o dígito de controle.
            ean = barcode.get('ean13', codigo_barras, writer=ImageWriter())
            
            # 3. Definir o caminho do arquivo
            nome_limpo = "".join(c for c in nome_produto if c.isalnum() or c in (' ', '_')).rstrip()
            file_path = os.path.join(barcode_dir, f"{nome_limpo}_barcode.png")
            
            # 4. Salvar a imagem
            # O ImageWriter salva a imagem. O formato padrão é PNG.
            ean.write(file_path, options={'write_text': False, 'module_height': 10, 'font_size': 0})
            
            # 5. Exibir a imagem no QLabel
            pixmap = QPixmap(file_path)
            
            # Redimensionar para caber no QLabel (ex: 300px de largura)
            if pixmap.width() > 300:
                pixmap = pixmap.scaledToWidth(300, Qt.TransformationMode.SmoothTransformation)
            
            self.barcode_preview_label.setPixmap(pixmap)
            self.barcode_preview_label.setText("") # Limpa o texto de placeholder
            
        except Exception as e:
            print(f"Erro ao gerar código de barras: {e}")
            self.barcode_preview_label.setText(f"Erro ao gerar código de barras: {e}")
            self.barcode_preview_label.clear()
    
    def generate_preview(self):
        """Gera a prévia visual da etiqueta"""
        if not self.current_product:
            QMessageBox.warning(self, 'Aviso', 'Selecione um produto primeiro!')
            return
        
        preview_image = self.create_etiqueta_preview()
        if preview_image:
            pixmap = QPixmap.fromImage(preview_image)
            self.preview_label.setPixmap(pixmap.scaled(
                self.preview_label.width() - 20, 
                self.preview_label.height() - 20,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))
    
    def create_etiqueta_preview(self):
        """Cria uma imagem de prévia da etiqueta usando QPainter"""
        from PyQt6.QtGui import QPainter, QFont
        
        image = QImage(400, 300, QImage.Format.Format_RGB32)
        image.fill(Qt.GlobalColor.white)
        
        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        title_font = QFont("Arial", 14, QFont.Weight.Bold)
        normal_font = QFont("Arial", 10)
        small_font = QFont("Arial", 8)
        
        produto_nome = self.current_product['nome']
        codigo_barras = self.barcode_input.text()
        fabricacao = self.fabricacao_input.text()
        validade = self.validade_input.text()
        
        empresa_nome = self.db_handler.dados['Empresa']['Nome Comercial'] if self.db_handler.dados else "Sodiê PUC"
        cnpj = self.db_handler.dados['Empresa']['CNPJ'] if self.db_handler.dados else "16.256.1024-32"
        
        y_pos = 20
        
        painter.setFont(title_font)
        painter.drawText(0, y_pos, 400, 30, Qt.AlignmentFlag.AlignCenter, empresa_nome)
        y_pos += 40
        
        painter.setFont(normal_font)
        painter.drawText(0, y_pos, 400, 25, Qt.AlignmentFlag.AlignCenter, produto_nome)
        y_pos += 30
        
        painter.setFont(small_font)
        painter.drawText(0, y_pos, 400, 20, Qt.AlignmentFlag.AlignCenter, f"EAN13: {codigo_barras}")
        y_pos += 25
        
        painter.setPen(Qt.GlobalColor.black)
        bar_height = 60
        bar_width = 2
        x_start = 100
        
        for i in range(50):
            if i % 3 == 0:
                painter.drawLine(x_start + i * bar_width, y_pos, 
                               x_start + i * bar_width, y_pos + bar_height)
            else:
                painter.drawLine(x_start + i * bar_width, y_pos + 10, 
                               x_start + i * bar_width, y_pos + bar_height - 10)
        
        y_pos += bar_height + 10
        
        painter.drawText(50, y_pos, 150, 20, Qt.AlignmentFlag.AlignLeft, f"Fab: {fabricacao}")
        painter.drawText(200, y_pos, 150, 20, Qt.AlignmentFlag.AlignRight, f"Val: {validade}")
        y_pos += 25
        
        painter.drawText(0, y_pos, 400, 20, Qt.AlignmentFlag.AlignCenter, f"CNPJ: {cnpj}")
        y_pos += 20
        
        if 'tabelaNutricional' in self.current_product:
            tabela = self.current_product['tabelaNutricional']
            painter.setFont(small_font)
            painter.drawText(0, y_pos, 400, 15, Qt.AlignmentFlag.AlignCenter, "Informação Nutricional (por 100g)")
            y_pos += 20
            
            for nutriente, valor in list(tabela.items())[:3]:
                painter.drawText(50, y_pos, 300, 15, Qt.AlignmentFlag.AlignLeft, f"{nutriente}: {valor}")
                y_pos += 15
        
        painter.end()
        return image
    
    def save_pdf(self):
        """Salva a etiqueta como PDF (placeholder para integração futura)"""
        if not self.current_product:
            QMessageBox.warning(self, 'Aviso', 'Selecione um produto primeiro!')
            return
        
        produto_nome = self.current_product['nome']
        QMessageBox.information(self, 'Sucesso', 
                               f'Etiqueta para "{produto_nome}" gerada com sucesso!\n\n'
                               'PDF salvo no diretório de etiquetas.')
        
        print(f"Gerando PDF para: {produto_nome}")
        print(f"Código de barras: {self.barcode_input.text()}")
        print(f"Data fabricação: {self.fabricacao_input.text()}")
        print(f"Data validade: {self.validade_input.text()}")
    
    def go_to_home(self):
        """Volta para a tela principal"""
        self.stacked_widget.setCurrentIndex(1)

# =============================================================================
# BACKUPWINDOW ATUALIZADA COM SELEÇÃO DE ARQUIVO JSON
# =============================================================================

class BackupWindow(BaseWidget):
    def __init__(self, stacked_widget, db_handler):
        super().__init__(stacked_widget, db_handler)

        self.return_index = 0
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(PADDING, PADDING, PADDING, PADDING)
        layout.setSpacing(SPACING)

        self.back_btn = PrimaryButton('Voltar')
        self.back_btn.clicked.connect(self.go_back)
        layout.addWidget(self.back_btn, alignment=Qt.AlignmentFlag.AlignLeft)

        backup_label = StyledLabel('Página de Backup e Recuperação de Dados', is_header=True)
        layout.addWidget(backup_label)
        
        backup_info = StyledLabel(
            "Esta tela permite fazer backup, restaurar dados e carregar novos arquivos JSON.\n"
            "Escolha uma das opções abaixo:"
        )
        layout.addWidget(backup_info)
        
        file_group = QGroupBox("Operações com Arquivo JSON")
        file_group.setStyleSheet(f"""
            QGroupBox {{
                background-color: {COLOR_WIDGET_BG};
                border: 1px solid #ccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }}
        """)
        file_layout = QVBoxLayout()
        
        self.select_file_btn = PrimaryButton('Selecionar Arquivo JSON')
        self.select_file_btn.clicked.connect(self.select_json_file)
        file_layout.addWidget(self.select_file_btn)
        
        self.file_status_label = StyledLabel('Nenhum arquivo selecionado')
        file_layout.addWidget(self.file_status_label)
        
        self.apply_file_btn = PrimaryButton('Aplicar Arquivo Selecionado')
        self.apply_file_btn.clicked.connect(self.apply_selected_file)
        self.apply_file_btn.setEnabled(False)
        file_layout.addWidget(self.apply_file_btn)
        
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)
        
        backup_group = QGroupBox("Operações de Backup")
        backup_group.setStyleSheet(f"""
            QGroupBox {{
                background-color: {COLOR_WIDGET_BG};
                border: 1px solid #ccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }}
        """)
        backup_ops_layout = QVBoxLayout()
        
        self.create_backup_btn = PrimaryButton('Criar Backup dos Dados Atuais')
        self.create_backup_btn.clicked.connect(self.create_backup)
        backup_ops_layout.addWidget(self.create_backup_btn)
        
        self.restore_backup_btn = SecondaryButton('Restaurar Backup Padrão')
        self.restore_backup_btn.clicked.connect(self.restore_backup)
        backup_ops_layout.addWidget(self.restore_backup_btn)
        
        backup_group.setLayout(backup_ops_layout)
        layout.addWidget(backup_group)
        
        status_group = QGroupBox("Status dos Dados")
        status_group.setStyleSheet(f"""
            QGroupBox {{
                background-color: {COLOR_WIDGET_BG};
                border: 1px solid #ccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }}
        """)
        status_layout = QVBoxLayout()
        
        self.data_status_label = StyledLabel('Carregando status...')
        status_layout.addWidget(self.data_status_label)
        
        status_group.setLayout(status_layout)
        layout.addWidget(status_group)
        
        layout.addStretch()
        self.setLayout(layout)
        
        self.update_data_status()

    def select_json_file(self):
        """Abre diálogo para selecionar arquivo JSON"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar arquivo JSON",
            "",
            "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            self.selected_file_path = file_path
            self.file_status_label.setText(f"Arquivo selecionado: {os.path.basename(file_path)}")
            
            valido, mensagem = self.db_handler.validar_estrutura_json(file_path)
            if valido:
                self.file_status_label.setText(f"✓ Arquivo válido: {os.path.basename(file_path)}")
                self.apply_file_btn.setEnabled(True)
            else:
                self.file_status_label.setText(f"✗ Arquivo inválido: {mensagem}")
                self.apply_file_btn.setEnabled(False)

    def apply_selected_file(self):
        """Aplica o arquivo JSON selecionado aos dados em execução"""
        if hasattr(self, 'selected_file_path'):
            sucesso, mensagem = self.db_handler.carregar_arquivo_externo(self.selected_file_path)
            if sucesso:
                QMessageBox.information(self, 'Sucesso', 
                                       f"Arquivo aplicado com sucesso!\n\n"
                                       f"Dados em execução atualizados.\n"
                                       f"Modificações não salvas: {self.db_handler.dados_modificados}")
                self.update_data_status()
                self.notify_data_update()
            else:
                QMessageBox.warning(self, 'Erro', f"Falha ao aplicar arquivo: {mensagem}")

    def create_backup(self):
        """Cria um backup dos dados atuais em execução"""
        if self.db_handler.dados_modificados:
            resposta = QMessageBox.question(
                self,
                "Dados Modificados",
                "Os dados em execução foram modificados. Deseja salvar antes de criar o backup?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel
            )
            
            if resposta == QMessageBox.StandardButton.Yes:
                sucesso, mensagem = self.db_handler.salvar_dados_atuais()
                if sucesso:
                    QMessageBox.information(self, 'Backup', 'Dados salvos e backup criado com sucesso!')
                else:
                    QMessageBox.warning(self, 'Erro', f"Erro ao salvar dados: {mensagem}")
                    return
            elif resposta == QMessageBox.StandardButton.Cancel:
                return
        
        QMessageBox.information(self, 'Backup', 'Backup dos dados atuais criado com sucesso!')
        self.update_data_status()

    def restore_backup(self):
        """Restaura o backup padrão"""
        resposta = QMessageBox.question(
            self,
            "Restaurar Backup",
            "Isso irá restaurar os dados padrão e perder quaisquer modificações não salvas. Continuar?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if resposta == QMessageBox.StandardButton.Yes:
            # CORREÇÃO: criar_ou_validar_backup() retorna apenas os dados, não uma tupla (sucesso, mensagem)
            dados_restaurados = self.db_handler.criar_ou_validar_backup()
            if dados_restaurados is not None:
                QMessageBox.information(self, 'Restauração', 'Backup padrão restaurado com sucesso!')
                self.db_handler.dados_modificados = False
                self.update_data_status()
                self.notify_data_update()
            else:
                QMessageBox.warning(self, 'Erro', 'Erro ao restaurar backup: Não foi possível carregar ou criar o arquivo de backup.')

    def update_data_status(self):
        """Atualiza o status dos dados exibido"""
        status_text = f"Dados carregados: {self.db_handler.dados is not None}\n"
        status_text += f"Modificações não salvas: {self.db_handler.dados_modificados}\n"
        
        if self.db_handler.dados:
            produtos_count = len([k for k in self.db_handler.dados['Produtos'].keys() 
                                if k != 'Proxima ID Novo Registro'])
            status_text += f"Produtos cadastrados: {produtos_count}\n"
            status_text += f"Empresa: {self.db_handler.dados['Empresa']['Nome Comercial']}"
        
        self.data_status_label.setText(status_text)

    def notify_data_update(self):
        """Notifica outras janelas sobre a atualização dos dados"""
        print("Dados atualizados - notificando outras janelas...")
        
        etiqueta_window = self.stacked_widget.widget(3)
        if hasattr(etiqueta_window, 'load_products'):
            etiqueta_window.load_products()

    def set_return_index(self, index):
        self.return_index = index

    def go_back(self):
        self.stacked_widget.setCurrentIndex(self.return_index)

# =============================================================================
# NOVA CLASSE LogomarcaWidget
# =============================================================================

class LogomarcaWidget(QWidget):
    def __init__(self, db_handler, parent=None):
        super().__init__(parent)
        self.db_handler = db_handler
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(PADDING, PADDING, PADDING, PADDING)
        main_layout.setSpacing(SPACING)

        # Frame principal
        frame = QGroupBox("Gerenciamento da Logomarca")
        frame.setStyleSheet(f"""
            QGroupBox {{
                background-color: {COLOR_WIDGET_BG};
                border: 1px solid #ccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: {COLOR_HEADER};
                font-weight: bold;
            }}
        """)
        frame_layout = QVBoxLayout(frame)

        # Seção: Visualização da Logomarca Atual
        preview_group = QGroupBox("Logomarca Atual")
        preview_group.setStyleSheet(f"""
            QGroupBox {{
                background-color: {COLOR_WIDGET_BG};
                border: 1px solid #ccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }}
        """)
        preview_layout = QVBoxLayout(preview_group)

        # Label para exibir a logomarca atual
        self.logo_preview_label = QLabel()
        self.logo_preview_label.setFixedSize(200, 200)
        self.logo_preview_label.setStyleSheet(f"""
            border: 2px dashed {COLOR_BORDER};
            background-color: {COLOR_BACKGROUND};
            border-radius: 10px;
        """)
        self.logo_preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_preview_label.setText("Logomarca não configurada")
        
        # Label para mostrar o caminho atual
        self.path_label = StyledLabel("Caminho: Não configurado")
        self.path_label.setWordWrap(True)

        preview_layout.addWidget(self.logo_preview_label, alignment=Qt.AlignmentFlag.AlignCenter)
        preview_layout.addWidget(self.path_label)

        # Seção: Atualizar Logomarca
        update_group = QGroupBox("Atualizar Logomarca")
        update_group.setStyleSheet(f"""
            QGroupBox {{
                background-color: {COLOR_WIDGET_BG};
                border: 1px solid #ccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }}
        """)
        update_layout = QVBoxLayout(update_group)

        # Botão para selecionar nova imagem
        self.select_btn = PrimaryButton('Selecionar Nova Logomarca', rounded=True)
        self.select_btn.setFixedSize(200, BUTTON_HEIGHT)
        self.select_btn.clicked.connect(self.selecionar_logomarca)
        
        # Informações sobre formatos suportados
        format_info = StyledLabel(
            "Formatos suportados: PNG, JPG, JPEG, BMP, GIF\n"
            "A imagem será convertida para PNG e redimensionada para 256x256 pixels."
        )
        format_info.setStyleSheet(f"color: {COLOR_SECONDARY}; font-size: 10px;")

        update_layout.addWidget(self.select_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        update_layout.addWidget(format_info)

        # Adicionar grupos ao frame
        frame_layout.addWidget(preview_group)
        frame_layout.addWidget(update_group)
        
        # Adicionar frame ao layout principal
        main_layout.addWidget(frame)
        main_layout.addStretch()

        # Carregar a logomarca atual
        self.carregar_logomarca_atual()

    def carregar_logomarca_atual(self):
        """Carrega e exibe a logomarca atual"""
        path_logomarca = self.db_handler.ler_dados_request_json('logomarca')
        
        if path_logomarca == 'logomarca':  # Placeholder - não configurada
            self.logo_preview_label.setText("Logomarca\nnão configurada")
            self.path_label.setText("Caminho: Não configurado")
        else:
            # Tentar carregar a imagem
            try:
                if os.path.exists(path_logomarca):
                    pixmap = QPixmap(path_logomarca)
                    if not pixmap.isNull():
                        scaled_pixmap = pixmap.scaled(
                            self.logo_preview_label.size(),
                            Qt.AspectRatioMode.KeepAspectRatio,
                            Qt.TransformationMode.SmoothTransformation
                        )
                        self.logo_preview_label.setPixmap(scaled_pixmap)
                        self.path_label.setText(f"Caminho: {path_logomarca}")
                    else:
                        self.logo_preview_label.setText("Erro ao\ncarregar imagem")
                        self.path_label.setText(f"Caminho: {path_logomarca} (inválido)")
                else:
                    self.logo_preview_label.setText("Arquivo\nnão encontrado")
                    self.path_label.setText(f"Caminho: {path_logomarca} (não existe)")
            except Exception as e:
                self.logo_preview_label.setText("Erro ao\ncarregar")
                self.path_label.setText(f"Erro: {str(e)}")

    def selecionar_logomarca(self):
        """Abre diálogo para selecionar nova logomarca"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar Logomarca",
            "",
            "Imagens (*.png *.jpg *.jpeg *.bmp *.gif);;Todos os arquivos (*)"
        )
        
        if file_path:
            # Processar a imagem selecionada
            sucesso, mensagem = self.db_handler._converter_e_salvar_imagem(file_path)
            
            if sucesso:
                QMessageBox.information(self, "Sucesso", mensagem)
                # Recarregar a visualização
                self.carregar_logomarca_atual()
                
                # Notificar outras partes da aplicação sobre a atualização
                self.notificar_atualizacao_logomarca()
            else:
                QMessageBox.warning(self, "Erro", mensagem)

    def notificar_atualizacao_logomarca(self):
        """Notifica outras partes da aplicação sobre a atualização da logomarca"""
        print("Logomarca atualizada - notificando outras janelas...")

# =============================================================================
# SETTINGS WINDOW (ATUALIZADA)
# =============================================================================
# =============================================================================
# CLASSES PARA AS ABAS DE GESTÃO (CRUD)
# =============================================================================

class GestaoProdutosWidget(QWidget):
    def __init__(self, db_handler, parent=None):
        super().__init__(parent)
        self.db_handler = db_handler
        self.setup_ui()
        self.carregar_produtos()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(PADDING, PADDING, PADDING, PADDING)
        layout.setSpacing(SPACING)

        # Header
        header_label = StyledLabel('Gestão de Produtos', is_header=True)
        layout.addWidget(header_label)

        # Barra de ferramentas
        toolbar_layout = QHBoxLayout()
        
        self.btn_novo = PrimaryButton('Novo Produto', rounded=True)
        self.btn_novo.clicked.connect(self.novo_produto)
        toolbar_layout.addWidget(self.btn_novo)
        
        self.btn_editar = SecondaryButton('Editar', rounded=True)
        self.btn_editar.clicked.connect(self.editar_produto)
        toolbar_layout.addWidget(self.btn_editar)
        
        self.btn_excluir = SecondaryButton('Excluir', rounded=True)
        self.btn_excluir.clicked.connect(self.excluir_produto)
        toolbar_layout.addWidget(self.btn_excluir)
        
        toolbar_layout.addStretch()
        
        # Campo de busca
        self.busca_input = StyledLineEdit('Buscar produto...')
        self.busca_input.textChanged.connect(self.filtrar_produtos)
        toolbar_layout.addWidget(self.busca_input)
        
        layout.addLayout(toolbar_layout)

        # Tabela de produtos
        self.tabela_produtos = QTableWidget()
        self.tabela_produtos.setColumnCount(5)
        self.tabela_produtos.setHorizontalHeaderLabels(['ID', 'Nome', 'Porção', 'Código Barras', 'Valor Energético'])
        self.tabela_produtos.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabela_produtos.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        # Ajustar largura das colunas
        header = self.tabela_produtos.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        
        layout.addWidget(self.tabela_produtos)

        self.setLayout(layout)

    def carregar_produtos(self, filtro=None):
        """Carrega produtos na tabela"""
        self.tabela_produtos.setRowCount(0)
        
        if not self.db_handler.dados or 'Produtos' not in self.db_handler.dados:
            return

        produtos = self.db_handler.dados['Produtos']
        row = 0
        
        for key, produto in produtos.items():
            if key == 'Proxima ID Novo Registro':
                continue
                
            nome = produto.get('nome', '')
            
            # Aplicar filtro se existir
            if filtro and filtro.lower() not in nome.lower():
                continue
            
            self.tabela_produtos.insertRow(row)
            
            # ID
            self.tabela_produtos.setItem(row, 0, QTableWidgetItem(key))
            
            # Nome
            self.tabela_produtos.setItem(row, 1, QTableWidgetItem(nome))
            
            # Porção
            self.tabela_produtos.setItem(row, 2, QTableWidgetItem(produto.get('porcao', '')))
            
            # Código de Barras
            self.tabela_produtos.setItem(row, 3, QTableWidgetItem(produto.get('codigoBarras12', '')))
            
            # Valor Energético
            valor_energetico = produto.get('tabelaNutricional', {}).get('Valor energético', '')
            self.tabela_produtos.setItem(row, 4, QTableWidgetItem(valor_energetico))
            
            row += 1

    def filtrar_produtos(self):
        """Filtra produtos baseado no texto de busca"""
        filtro = self.busca_input.text()
        self.carregar_produtos(filtro)

    def novo_produto(self):
        """Abre diálogo para criar novo produto"""
        dialog = ProdutoDialog(self.db_handler, self)
        if dialog.exec():
            self.carregar_produtos()
            self.db_handler.dados_modificados = True

    def editar_produto(self):
        """Abre diálogo para editar produto selecionado"""
        selected_items = self.tabela_produtos.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, 'Aviso', 'Selecione um produto para editar.')
            return
        
        row = selected_items[0].row()
        produto_id = self.tabela_produtos.item(row, 0).text()
        
        dialog = ProdutoDialog(self.db_handler, self, produto_id)
        if dialog.exec():
            self.carregar_produtos()
            self.db_handler.dados_modificados = True

    def excluir_produto(self):
        """Exclui produto selecionado"""
        selected_items = self.tabela_produtos.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, 'Aviso', 'Selecione um produto para excluir.')
            return
        
        row = selected_items[0].row()
        produto_id = self.tabela_produtos.item(row, 0).text()
        produto_nome = self.tabela_produtos.item(row, 1).text()
        
        resposta = QMessageBox.question(
            self,
            'Confirmar Exclusão',
            f'Tem certeza que deseja excluir o produto "{produto_nome}"?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if resposta == QMessageBox.StandardButton.Yes:
            if 'Produtos' in self.db_handler.dados and produto_id in self.db_handler.dados['Produtos']:
                del self.db_handler.dados['Produtos'][produto_id]
                self.carregar_produtos()
                self.db_handler.dados_modificados = True
                QMessageBox.information(self, 'Sucesso', 'Produto excluído com sucesso!')


class GestaoClientesWidget(QWidget):
    def __init__(self, db_handler, parent=None):
        super().__init__(parent)
        self.db_handler = db_handler
        self.setup_ui()
        self.carregar_clientes()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(PADDING, PADDING, PADDING, PADDING)
        layout.setSpacing(SPACING)

        # Header
        header_label = StyledLabel('Gestão de Clientes', is_header=True)
        layout.addWidget(header_label)

        # Barra de ferramentas
        toolbar_layout = QHBoxLayout()
        
        self.btn_novo = PrimaryButton('Novo Cliente', rounded=True)
        self.btn_novo.clicked.connect(self.novo_cliente)
        toolbar_layout.addWidget(self.btn_novo)
        
        self.btn_editar = SecondaryButton('Editar', rounded=True)
        self.btn_editar.clicked.connect(self.editar_cliente)
        toolbar_layout.addWidget(self.btn_editar)
        
        self.btn_excluir = SecondaryButton('Excluir', rounded=True)
        self.btn_excluir.clicked.connect(self.excluir_cliente)
        toolbar_layout.addWidget(self.btn_excluir)
        
        toolbar_layout.addStretch()
        
        # Campo de busca
        self.busca_input = StyledLineEdit('Buscar cliente...')
        self.busca_input.textChanged.connect(self.filtrar_clientes)
        toolbar_layout.addWidget(self.busca_input)
        
        layout.addLayout(toolbar_layout)

        # Tabela de clientes
        self.tabela_clientes = QTableWidget()
        self.tabela_clientes.setColumnCount(4)
        self.tabela_clientes.setHorizontalHeaderLabels(['ID', 'Nome Comercial', 'Razão Social', 'CNPJ'])
        self.tabela_clientes.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabela_clientes.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        # Ajustar largura das colunas
        header = self.tabela_clientes.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        
        layout.addWidget(self.tabela_clientes)

        self.setLayout(layout)

    def carregar_clientes(self, filtro=None):
        """Carrega clientes na tabela"""
        self.tabela_clientes.setRowCount(0)
        
        if not self.db_handler.dados or 'Clientes' not in self.db_handler.dados:
            return

        clientes = self.db_handler.dados['Clientes']
        row = 0
        
        for key, cliente in clientes.items():
            if key == 'Proxima ID Novo Registro':
                continue
                
            nome_comercial = cliente.get('Nome Comercial', '')
            razao_social = cliente.get('Razão Social', '')
            
            # Aplicar filtro se existir
            if filtro and filtro.lower() not in nome_comercial.lower() and filtro.lower() not in razao_social.lower():
                continue
            
            self.tabela_clientes.insertRow(row)
            
            # ID
            self.tabela_clientes.setItem(row, 0, QTableWidgetItem(key))
            
            # Nome Comercial
            self.tabela_clientes.setItem(row, 1, QTableWidgetItem(nome_comercial))
            
            # Razão Social
            self.tabela_clientes.setItem(row, 2, QTableWidgetItem(razao_social))
            
            # CNPJ
            self.tabela_clientes.setItem(row, 3, QTableWidgetItem(cliente.get('CNPJ', '')))
            
            row += 1

    def filtrar_clientes(self):
        """Filtra clientes baseado no texto de busca"""
        filtro = self.busca_input.text()
        self.carregar_clientes(filtro)

    def novo_cliente(self):
        """Abre diálogo para criar novo cliente"""
        dialog = ClienteDialog(self.db_handler, self)
        if dialog.exec():
            self.carregar_clientes()
            self.db_handler.dados_modificados = True

    def editar_cliente(self):
        """Abre diálogo para editar cliente selecionado"""
        selected_items = self.tabela_clientes.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, 'Aviso', 'Selecione um cliente para editar.')
            return
        
        row = selected_items[0].row()
        cliente_id = self.tabela_clientes.item(row, 0).text()
        
        dialog = ClienteDialog(self.db_handler, self, cliente_id)
        if dialog.exec():
            self.carregar_clientes()
            self.db_handler.dados_modificados = True

    def excluir_cliente(self):
        """Exclui cliente selecionado"""
        selected_items = self.tabela_clientes.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, 'Aviso', 'Selecione um cliente para excluir.')
            return
        
        row = selected_items[0].row()
        cliente_id = self.tabela_clientes.item(row, 0).text()
        cliente_nome = self.tabela_clientes.item(row, 1).text()
        
        resposta = QMessageBox.question(
            self,
            'Confirmar Exclusão',
            f'Tem certeza que deseja excluir o cliente "{cliente_nome}"?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if resposta == QMessageBox.StandardButton.Yes:
            if 'Clientes' in self.db_handler.dados and cliente_id in self.db_handler.dados['Clientes']:
                del self.db_handler.dados['Clientes'][cliente_id]
                self.carregar_clientes()
                self.db_handler.dados_modificados = True
                QMessageBox.information(self, 'Sucesso', 'Cliente excluído com sucesso!')


class GestaoPedidosWidget(QWidget):
    def __init__(self, db_handler, parent=None):
        super().__init__(parent)
        self.db_handler = db_handler
        self.setup_ui()
        self.carregar_pedidos()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(PADDING, PADDING, PADDING, PADDING)
        layout.setSpacing(SPACING)

        # Header
        header_label = StyledLabel('Gestão de Pedidos', is_header=True)
        layout.addWidget(header_label)

        # Barra de ferramentas
        toolbar_layout = QHBoxLayout()
        
        self.btn_novo = PrimaryButton('Novo Pedido', rounded=True)
        self.btn_novo.clicked.connect(self.novo_pedido)
        toolbar_layout.addWidget(self.btn_novo)
        
        self.btn_editar = SecondaryButton('Editar', rounded=True)
        self.btn_editar.clicked.connect(self.editar_pedido)
        toolbar_layout.addWidget(self.btn_editar)
        
        self.btn_excluir = SecondaryButton('Excluir', rounded=True)
        self.btn_excluir.clicked.connect(self.excluir_pedido)
        toolbar_layout.addWidget(self.btn_excluir)
        
        toolbar_layout.addStretch()
        
        # Filtro de status
        self.filtro_status = QComboBox()
        self.filtro_status.addItems(['Todos', 'Pendente', 'Processando', 'Concluído', 'Cancelado'])
        self.filtro_status.currentTextChanged.connect(self.filtrar_pedidos)
        toolbar_layout.addWidget(QLabel('Status:'))
        toolbar_layout.addWidget(self.filtro_status)
        
        layout.addLayout(toolbar_layout)

        # Tabela de pedidos
        self.tabela_pedidos = QTableWidget()
        self.tabela_pedidos.setColumnCount(6)
        self.tabela_pedidos.setHorizontalHeaderLabels(['ID', 'Cliente', 'Produto', 'Quantidade', 'Valor', 'Status'])
        self.tabela_pedidos.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabela_pedidos.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        
        # Ajustar largura das colunas
        header = self.tabela_pedidos.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        
        layout.addWidget(self.tabela_pedidos)

        self.setLayout(layout)

    def carregar_pedidos(self, status_filtro='Todos'):
        """Carrega pedidos na tabela"""
        self.tabela_pedidos.setRowCount(0)
        
        if not self.db_handler.dados or 'Pedidos' not in self.db_handler.dados:
            return

        pedidos = self.db_handler.dados['Pedidos']
        row = 0
        
        for key, pedido in pedidos.items():
            if key == 'Proxima ID Novo Registro':
                continue
            
            pedido_status = pedido.get('Status', '')
            
            # Aplicar filtro de status
            if status_filtro != 'Todos' and pedido_status != status_filtro:
                continue
            
            self.tabela_pedidos.insertRow(row)
            
            # ID
            self.tabela_pedidos.setItem(row, 0, QTableWidgetItem(key))
            
            # Cliente (buscar nome do cliente)
            cliente_id = pedido.get('ID Cliente', '')
            cliente_nome = self.obter_nome_cliente(cliente_id)
            self.tabela_pedidos.setItem(row, 1, QTableWidgetItem(cliente_nome))
            
            # Produto (buscar nome do produto)
            lote_id = pedido.get('ID Lote', '')
            produto_nome = self.obter_nome_produto(lote_id)
            self.tabela_pedidos.setItem(row, 2, QTableWidgetItem(produto_nome))
            
            # Quantidade
            self.tabela_pedidos.setItem(row, 3, QTableWidgetItem(str(pedido.get('Quantidade', ''))))
            
            # Valor
            valor = pedido.get('Valor', '')
            self.tabela_pedidos.setItem(row, 4, QTableWidgetItem(f"R$ {valor}" if valor else ""))
            
            # Status com cor
            status_item = QTableWidgetItem(pedido_status)
            if pedido_status == 'Concluído':
                status_item.setBackground(Qt.GlobalColor.green)
            elif pedido_status == 'Cancelado':
                status_item.setBackground(Qt.GlobalColor.red)
            elif pedido_status == 'Processando':
                status_item.setBackground(Qt.GlobalColor.yellow)
            self.tabela_pedidos.setItem(row, 5, status_item)
            
            row += 1

    def obter_nome_cliente(self, cliente_id):
        """Obtém nome do cliente pelo ID"""
        if not cliente_id or 'Clientes' not in self.db_handler.dados:
            return "N/A"
        
        cliente = self.db_handler.dados['Clientes'].get(cliente_id, {})
        return cliente.get('Nome Comercial', cliente.get('Razão Social', 'N/A'))

    def obter_nome_produto(self, lote_id):
        """Obtém nome do produto pelo ID do lote"""
        if not lote_id or 'Lotes' not in self.db_handler.dados:
            return "N/A"
        
        lote = self.db_handler.dados['Lotes'].get(lote_id, {})
        produto_id = lote.get('ID Produto', '')
        
        if produto_id and 'Produtos' in self.db_handler.dados:
            produto = self.db_handler.dados['Produtos'].get(produto_id, {})
            return produto.get('nome', 'N/A')
        
        return "N/A"

    def filtrar_pedidos(self):
        """Filtra pedidos baseado no status"""
        status_filtro = self.filtro_status.currentText()
        self.carregar_pedidos(status_filtro)

    def novo_pedido(self):
        """Abre diálogo para criar novo pedido"""
        dialog = PedidoDialog(self.db_handler, self)
        if dialog.exec():
            self.carregar_pedidos()
            self.db_handler.dados_modificados = True

    def editar_pedido(self):
        """Abre diálogo para editar pedido selecionado"""
        selected_items = self.tabela_pedidos.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, 'Aviso', 'Selecione um pedido para editar.')
            return
        
        row = selected_items[0].row()
        pedido_id = self.tabela_pedidos.item(row, 0).text()
        
        dialog = PedidoDialog(self.db_handler, self, pedido_id)
        if dialog.exec():
            self.carregar_pedidos()
            self.db_handler.dados_modificados = True

    def excluir_pedido(self):
        """Exclui pedido selecionado"""
        selected_items = self.tabela_pedidos.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, 'Aviso', 'Selecione um pedido para excluir.')
            return
        
        row = selected_items[0].row()
        pedido_id = self.tabela_pedidos.item(row, 0).text()
        cliente_nome = self.tabela_pedidos.item(row, 1).text()
        
        resposta = QMessageBox.question(
            self,
            'Confirmar Exclusão',
            f'Tem certeza que deseja excluir o pedido #{pedido_id} do cliente "{cliente_nome}"?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if resposta == QMessageBox.StandardButton.Yes:
            if 'Pedidos' in self.db_handler.dados and pedido_id in self.db_handler.dados['Pedidos']:
                del self.db_handler.dados['Pedidos'][pedido_id]
                self.carregar_pedidos()
                self.db_handler.dados_modificados = True
                QMessageBox.information(self, 'Sucesso', 'Pedido excluído com sucesso!')


# =============================================================================
# DIÁLOGOS PARA CRIAÇÃO/EDIÇÃO
# =============================================================================

class ProdutoDialog(QDialog):
    def __init__(self, db_handler, parent=None, produto_id=None):
        super().__init__(parent)
        self.db_handler = db_handler
        self.produto_id = produto_id
        self.is_edit = produto_id is not None
        self.setup_ui()
        self.carregar_dados()

    def setup_ui(self):
        self.setWindowTitle('Editar Produto' if self.is_edit else 'Novo Produto')
        self.setModal(True)
        self.resize(500, 600)
        
        layout = QVBoxLayout()
        
        # Formulário
        form_layout = QFormLayout()
        
        self.nome_input = StyledLineEdit()
        form_layout.addRow('Nome:', self.nome_input)
        
        self.porcao_input = StyledLineEdit()
        form_layout.addRow('Porção:', self.porcao_input)
        
        self.codigo_barras_input = StyledLineEdit()
        form_layout.addRow('Código Barras (12 dígitos):', self.codigo_barras_input)
        
        # Tabela nutricional
        nutri_group = QGroupBox('Tabela Nutricional')
        nutri_layout = QFormLayout()
        
        self.energia_input = StyledLineEdit()
        nutri_layout.addRow('Valor energético (kcal):', self.energia_input)
        
        self.carboidratos_input = StyledLineEdit()
        nutri_layout.addRow('Carboidratos (g):', self.carboidratos_input)
        
        self.proteinas_input = StyledLineEdit()
        nutri_layout.addRow('Proteínas (g):', self.proteinas_input)
        
        self.gorduras_input = StyledLineEdit()
        nutri_layout.addRow('Gorduras totais (g):', self.gorduras_input)
        
        self.fibra_input = StyledLineEdit()
        nutri_layout.addRow('Fibra alimentar (g):', self.fibra_input)
        
        self.sodio_input = StyledLineEdit()
        nutri_layout.addRow('Sódio (mg):', self.sodio_input)
        
        nutri_group.setLayout(nuti_layout)
        
        # Botões
        btn_layout = QHBoxLayout()
        self.btn_salvar = PrimaryButton('Salvar')
        self.btn_salvar.clicked.connect(self.salvar)
        btn_layout.addWidget(self.btn_salvar)
        
        self.btn_cancelar = SecondaryButton('Cancelar')
        self.btn_cancelar.clicked.connect(self.reject)
        btn_layout.addWidget(self.btn_cancelar)
        
        layout.addLayout(form_layout)
        layout.addWidget(nutri_group)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)

    def carregar_dados(self):
        if self.is_edit and self.produto_id in self.db_handler.dados['Produtos']:
            produto = self.db_handler.dados['Produtos'][self.produto_id]
            self.nome_input.setText(produto.get('nome', ''))
            self.porcao_input.setText(produto.get('porcao', ''))
            self.codigo_barras_input.setText(produto.get('codigoBarras12', ''))
            
            tabela = produto.get('tabelaNutricional', {})
            self.energia_input.setText(tabela.get('Valor energético', ''))
            self.carboidratos_input.setText(tabela.get('Carboidratos', ''))
            self.proteinas_input.setText(tabela.get('Proteínas', ''))
            self.gorduras_input.setText(tabela.get('Gorduras totais', ''))
            self.fibra_input.setText(tabela.get('Fibra alimentar', ''))
            self.sodio_input.setText(tabela.get('Sódio', ''))

    def salvar(self):
        # Validação básica
        if not self.nome_input.text().strip():
            QMessageBox.warning(self, 'Erro', 'O nome do produto é obrigatório.')
            return
        
        # Preparar dados
        produto_data = {
            'nome': self.nome_input.text().strip(),
            'porcao': self.porcao_input.text().strip(),
            'codigoBarras12': self.codigo_barras_input.text().strip(),
            'Pesos': [],
            'Valores': [],
            'tabelaNutricional': {
                'Valor energético': self.energia_input.text().strip(),
                'Carboidratos': self.carboidratos_input.text().strip(),
                'Proteínas': self.proteinas_input.text().strip(),
                'Gorduras totais': self.gorduras_input.text().strip(),
                'Fibra alimentar': self.fibra_input.text().strip(),
                'Sódio': self.sodio_input.text().strip()
            }
        }
        
        # Salvar no JSON
        if self.is_edit:
            self.db_handler.dados['Produtos'][self.produto_id] = produto_data
        else:
            # Criar novo ID
            next_id = str(self.db_handler.dados['Produtos']['Proxima ID Novo Registro'])
            self.db_handler.dados['Produtos'][next_id] = produto_data
            self.db_handler.dados['Produtos']['Proxima ID Novo Registro'] += 1
        
        self.accept()


class ClienteDialog(QDialog):
    def __init__(self, db_handler, parent=None, cliente_id=None):
        super().__init__(parent)
        self.db_handler = db_handler
        self.cliente_id = cliente_id
        self.is_edit = cliente_id is not None
        self.setup_ui()
        self.carregar_dados()

    def setup_ui(self):
        self.setWindowTitle('Editar Cliente' if self.is_edit else 'Novo Cliente')
        self.setModal(True)
        self.resize(500, 400)
        
        layout = QVBoxLayout()
        
        # Formulário
        form_layout = QFormLayout()
        
        self.nome_comercial_input = StyledLineEdit()
        form_layout.addRow('Nome Comercial:', self.nome_comercial_input)
        
        self.razao_social_input = StyledLineEdit()
        form_layout.addRow('Razão Social:', self.razao_social_input)
        
        self.cnpj_input = StyledLineEdit()
        form_layout.addRow('CNPJ:', self.cnpj_input)
        
        # Endereço
        endereco_group = QGroupBox('Endereço')
        endereco_layout = QFormLayout()
        
        self.rua_input = StyledLineEdit()
        endereco_layout.addRow('Rua:', self.rua_input)
        
        self.numero_input = StyledLineEdit()
        endereco_layout.addRow('Número:', self.numero_input)
        
        self.bairro_input = StyledLineEdit()
        endereco_layout.addRow('Bairro:', self.bairro_input)
        
        self.cidade_input = StyledLineEdit()
        endereco_layout.addRow('Cidade:', self.cidade_input)
        
        self.estado_input = StyledLineEdit()
        endereco_layout.addRow('Estado:', self.estado_input)
        
        self.cep_input = StyledLineEdit()
        endereco_layout.addRow('CEP:', self.cep_input)
        
        endereco_group.setLayout(endereco_layout)
        
        # Botões
        btn_layout = QHBoxLayout()
        self.btn_salvar = PrimaryButton('Salvar')
        self.btn_salvar.clicked.connect(self.salvar)
        btn_layout.addWidget(self.btn_salvar)
        
        self.btn_cancelar = SecondaryButton('Cancelar')
        self.btn_cancelar.clicked.connect(self.reject)
        btn_layout.addWidget(self.btn_cancelar)
        
        layout.addLayout(form_layout)
        layout.addWidget(endereco_group)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)

    def carregar_dados(self):
        if self.is_edit and self.cliente_id in self.db_handler.dados['Clientes']:
            cliente = self.db_handler.dados['Clientes'][self.cliente_id]
            self.nome_comercial_input.setText(cliente.get('Nome Comercial', ''))
            self.razao_social_input.setText(cliente.get('Razão Social', ''))
            self.cnpj_input.setText(cliente.get('CNPJ', ''))
            
            endereco = cliente.get('Endereço', {})
            self.rua_input.setText(endereco.get('Rua', ''))
            self.numero_input.setText(endereco.get('Numero', ''))
            self.bairro_input.setText(endereco.get('Bairro', ''))
            self.cidade_input.setText(endereco.get('Cidade', ''))
            self.estado_input.setText(endereco.get('Estado/Província', ''))
            self.cep_input.setText(endereco.get('CEP', ''))

    def salvar(self):
        # Validação básica
        if not self.nome_comercial_input.text().strip():
            QMessageBox.warning(self, 'Erro', 'O nome comercial é obrigatório.')
            return
        
        # Preparar dados
        cliente_data = {
            'Nome Comercial': self.nome_comercial_input.text().strip(),
            'Razão Social': self.razao_social_input.text().strip(),
            'CNPJ': self.cnpj_input.text().strip(),
            'Endereço': {
                'Rua': self.rua_input.text().strip(),
                'Numero': self.numero_input.text().strip(),
                'Complemento': '',
                'Bairro': self.bairro_input.text().strip(),
                'Cidade': self.cidade_input.text().strip(),
                'Municipalidade': '',
                'Estado/Província': self.estado_input.text().strip(),
                'País': 'Brasil',
                'CEP': self.cep_input.text().strip()
            },
            'Telefone': [],
            'Email': []
        }
        
        # Salvar no JSON
        if self.is_edit:
            self.db_handler.dados['Clientes'][self.cliente_id] = cliente_data
        else:
            # Criar novo ID
            next_id = str(self.db_handler.dados['Clientes']['Proxima ID Novo Registro'])
            self.db_handler.dados['Clientes'][next_id] = cliente_data
            self.db_handler.dados['Clientes']['Proxima ID Novo Registro'] += 1
        
        self.accept()


class PedidoDialog(QDialog):
    def __init__(self, db_handler, parent=None, pedido_id=None):
        super().__init__(parent)
        self.db_handler = db_handler
        self.pedido_id = pedido_id
        self.is_edit = pedido_id is not None
        self.setup_ui()
        self.carregar_dados()

    def setup_ui(self):
        self.setWindowTitle('Editar Pedido' if self.is_edit else 'Novo Pedido')
        self.setModal(True)
        self.resize(400, 300)
        
        layout = QVBoxLayout()
        
        # Formulário
        form_layout = QFormLayout()
        
        # Cliente
        self.cliente_combo = QComboBox()
        self.carregar_clientes()
        form_layout.addRow('Cliente:', self.cliente_combo)
        
        # Produto
        self.produto_combo = QComboBox()
        self.carregar_produtos()
        form_layout.addRow('Produto:', self.produto_combo)
        
        self.quantidade_input = StyledLineEdit()
        form_layout.addRow('Quantidade:', self.quantidade_input)
        
        self.valor_input = StyledLineEdit()
        form_layout.addRow('Valor (R$):', self.valor_input)
        
        self.status_combo = QComboBox()
        self.status_combo.addItems(['Pendente', 'Processando', 'Concluído', 'Cancelado'])
        form_layout.addRow('Status:', self.status_combo)
        
        # Botões
        btn_layout = QHBoxLayout()
        self.btn_salvar = PrimaryButton('Salvar')
        self.btn_salvar.clicked.connect(self.salvar)
        btn_layout.addWidget(self.btn_salvar)
        
        self.btn_cancelar = SecondaryButton('Cancelar')
        self.btn_cancelar.clicked.connect(self.reject)
        btn_layout.addWidget(self.btn_cancelar)
        
        layout.addLayout(form_layout)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)

    def carregar_clientes(self):
        self.cliente_combo.clear()
        if 'Clientes' in self.db_handler.dados:
            for key, cliente in self.db_handler.dados['Clientes'].items():
                if key != 'Proxima ID Novo Registro':
                    nome = cliente.get('Nome Comercial', f'Cliente {key}')
                    self.cliente_combo.addItem(nome, key)

    def carregar_produtos(self):
        self.produto_combo.clear()
        if 'Produtos' in self.db_handler.dados:
            for key, produto in self.db_handler.dados['Produtos'].items():
                if key != 'Proxima ID Novo Registro':
                    self.produto_combo.addItem(produto.get('nome', ''), key)

    def carregar_dados(self):
        if self.is_edit and self.pedido_id in self.db_handler.dados['Pedidos']:
            pedido = self.db_handler.dados['Pedidos'][self.pedido_id]
            
            # Cliente
            cliente_id = pedido.get('ID Cliente', '')
            index = self.cliente_combo.findData(cliente_id)
            if index >= 0:
                self.cliente_combo.setCurrentIndex(index)
            
            # Produto (via lote)
            lote_id = pedido.get('ID Lote', '')
            if lote_id and 'Lotes' in self.db_handler.dados:
                lote = self.db_handler.dados['Lotes'].get(lote_id, {})
                produto_id = lote.get('ID Produto', '')
                index = self.produto_combo.findData(produto_id)
                if index >= 0:
                    self.produto_combo.setCurrentIndex(index)
            
            self.quantidade_input.setText(str(pedido.get('Quantidade', '')))
            self.valor_input.setText(str(pedido.get('Valor', '')))
            
            status = pedido.get('Status', 'Pendente')
            index = self.status_combo.findText(status)
            if index >= 0:
                self.status_combo.setCurrentIndex(index)

    def salvar(self):
        # Validação básica
        if not self.quantidade_input.text().strip():
            QMessageBox.warning(self, 'Erro', 'A quantidade é obrigatória.')
            return
        
        # Criar lote para o produto selecionado
        produto_id = self.produto_combo.currentData()
        if not produto_id:
            QMessageBox.warning(self, 'Erro', 'Selecione um produto.')
            return
        
        # Criar novo lote
        lote_id = str(self.db_handler.dados['Lotes']['Proxima ID Novo Registro'])
        self.db_handler.dados['Lotes'][lote_id] = {
            'ID Produto': produto_id,
            'Numero do Lote': f"LOTE_{lote_id}",
            'Fabricação do Lote': date.today().strftime('%d/%m/%Y'),
            'Validade do Lote': (date.today() + timedelta(days=30)).strftime('%d/%m/%Y')
        }
        self.db_handler.dados['Lotes']['Proxima ID Novo Registro'] += 1
        
        # Preparar dados do pedido
        pedido_data = {
            'ID Cliente': self.cliente_combo.currentData(),
            'ID Lote': lote_id,
            'Quantidade': self.quantidade_input.text().strip(),
            'Valor': self.valor_input.text().strip(),
            'Status': self.status_combo.currentText(),
            'Data de Pagamento': date.today().strftime('%d/%m/%Y') if self.status_combo.currentText() == 'Concluído' else ''
        }
        
        # Salvar no JSON
        if self.is_edit:
            self.db_handler.dados['Pedidos'][self.pedido_id] = pedido_data
        else:
            # Criar novo ID
            next_id = str(self.db_handler.dados['Pedidos']['Proxima ID Novo Registro'])
            self.db_handler.dados['Pedidos'][next_id] = pedido_data
            self.db_handler.dados['Pedidos']['Proxima ID Novo Registro'] += 1
        
        self.accept()

class EmpresaWidget(QWidget):
    def __init__(self, db_handler, parent=None):
        super().__init__(parent)
        self.db_handler = db_handler
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(PADDING, PADDING, PADDING, PADDING)
        main_layout.setSpacing(SPACING)

        frame = QGroupBox("Dados da Empresa")
        frame.setStyleSheet(f"""
            QGroupBox {{
                background-color: {COLOR_WIDGET_BG};
                border: 1px solid #ccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: {COLOR_HEADER};
                font-weight: bold;
            }}
        """)
        frame_layout = QVBoxLayout(frame)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid #ccc;
                background-color: {COLOR_WIDGET_BG};
            }}
            QTabBar::tab {{
                background: {COLOR_SECONDARY};
                color: white;
                padding: 8px 15px;
                border: 1px solid #ccc;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                margin-right: 2px;
            }}
            QTabBar::tab:selected {{
                background: {COLOR_PRIMARY};
                color: white;
                border-color: {COLOR_PRIMARY};
                border-bottom-color: {COLOR_WIDGET_BG};
            }}
            QTabBar::tab:hover {{
                background: {COLOR_SECONDARY_HOVER};
            }}
        """)

        empresa_data = self.db_handler.dados.get('Empresa', {})

        # 1. Aba: Informações Básicas
        basic_info_tab = QWidget()
        basic_info_layout = QVBoxLayout(basic_info_tab)
        
        scroll_basic = QScrollArea()
        scroll_basic.setWidgetResizable(True)
        scroll_basic_content = QWidget()
        scroll_basic.setWidget(scroll_basic_content)
        
        basic_form_layout = QFormLayout(scroll_basic_content)
        basic_form_layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)
        basic_form_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        basic_form_layout.setHorizontalSpacing(SPACING * 2)
        basic_form_layout.setVerticalSpacing(SPACING)

        def add_field(form_layout, label_text, data_key, is_address=False):
            if is_address:
                data = empresa_data.get('Endereço', {})
            else:
                data = empresa_data
            
            value = data.get(data_key, '')
            
            label = StyledLabel(label_text)
            line_edit = StyledLineEdit(value)
            line_edit.setText(value)
            line_edit.setReadOnly(False)
            form_layout.addRow(label, line_edit)

        add_field(basic_form_layout, "Nome Comercial:", "Nome Comercial")
        add_field(basic_form_layout, "Slogan:", "Slogan")
        add_field(basic_form_layout, "Razão Social:", "Razão Social")
        add_field(basic_form_layout, "CNPJ:", "CNPJ")
        
        basic_info_layout.addWidget(scroll_basic)
        self.tabs.addTab(basic_info_tab, 'Informações Básicas')

        # 2. Aba: Endereço
        address_tab = QWidget()
        address_layout = QVBoxLayout(address_tab)
        
        scroll_address = QScrollArea()
        scroll_address.setWidgetResizable(True)
        scroll_address_content = QWidget()
        scroll_address.setWidget(scroll_address_content)
        
        address_form_layout = QFormLayout(scroll_address_content)
        address_form_layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)
        address_form_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        address_form_layout.setHorizontalSpacing(SPACING * 2)
        address_form_layout.setVerticalSpacing(SPACING)

        add_field(address_form_layout, "Rua:", "Rua", is_address=True)
        
        numero_complemento_layout = QHBoxLayout()

        numero_label = StyledLabel("Número:")
        numero_edit = StyledLineEdit(empresa_data.get('Endereço', {}).get('Numero', ''))
        numero_edit.setReadOnly(False)

        complemento_label = StyledLabel("Complemento:")
        complemento_edit = StyledLineEdit(empresa_data.get('Endereço', {}).get('Complemento', ''))
        complemento_edit.setReadOnly(False)

        numero_complemento_layout.addWidget(numero_label)
        numero_complemento_layout.addWidget(numero_edit)
        numero_complemento_layout.addWidget(complemento_label)
        numero_complemento_layout.addWidget(complemento_edit)

        address_form_layout.addRow("", numero_complemento_layout)
        
        bairro_cidade_layout = QHBoxLayout()
        
        bairro_label = StyledLabel("Bairro:")
        bairro_edit = StyledLineEdit(empresa_data.get('Endereço', {}).get('Bairro', ''))
        bairro_edit.setReadOnly(False)

        cidade_label = StyledLabel("Cidade:")
        cidade_edit = StyledLineEdit(empresa_data.get('Endereço', {}).get('Cidade', ''))
        cidade_edit.setReadOnly(False)

        bairro_cidade_layout.addWidget(bairro_label)
        bairro_cidade_layout.addWidget(bairro_edit)
        bairro_cidade_layout.addWidget(cidade_label)
        bairro_cidade_layout.addWidget(cidade_edit)

        address_form_layout.addRow("", bairro_cidade_layout)

        estado_pais_cep_layout = QHBoxLayout()

        estado_label = StyledLabel("Estado/Província:")
        estado_edit = StyledLineEdit(empresa_data.get('Endereço', {}).get('Estado/Província', ''))
        estado_edit.setReadOnly(False)

        country_label = StyledLabel("País:")
        country_edit = StyledLineEdit(empresa_data.get('Endereço', {}).get('País', ''))
        country_edit.setReadOnly(False)

        cep_label = StyledLabel("CEP:")
        cep_edit = StyledLineEdit(empresa_data.get('Endereço', {}).get('CEP', ''))
        cep_edit.setReadOnly(False)

        estado_pais_cep_layout.addWidget(estado_label)
        estado_pais_cep_layout.addWidget(estado_edit)
        estado_pais_cep_layout.addWidget(country_label)
        estado_pais_cep_layout.addWidget(country_edit)
        estado_pais_cep_layout.addWidget(cep_label)
        estado_pais_cep_layout.addWidget(cep_edit)

        address_form_layout.addRow("", estado_pais_cep_layout)
        
        address_layout.addWidget(scroll_address)
        self.tabs.addTab(address_tab, 'Endereço')

        # 3. Aba: Contato
        contact_tab = QWidget()
        contact_layout = QVBoxLayout(contact_tab)
        
        scroll_contact = QScrollArea()
        scroll_contact.setWidgetResizable(True)
        scroll_contact_content = QWidget()
        scroll_contact.setWidget(scroll_contact_content)
        
        contact_form_layout = QFormLayout(scroll_contact_content)
        contact_form_layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)
        contact_form_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        contact_form_layout.setHorizontalSpacing(SPACING * 2)
        contact_form_layout.setVerticalSpacing(SPACING)

        telefones = ", ".join(empresa_data.get('Telefone', []))
        emails = ", ".join(empresa_data.get('Email', []))
        
        label_tel = StyledLabel("Telefones:")
        line_edit_tel = StyledLineEdit(telefones)
        line_edit_tel.setText(telefones)
        line_edit_tel.setReadOnly(False)
        contact_form_layout.addRow(label_tel, line_edit_tel)
        
        label_email = StyledLabel("E-mails:")
        line_edit_email = StyledLineEdit(emails)
        line_edit_email.setText(emails)
        line_edit_email.setReadOnly(False)
        contact_form_layout.addRow(label_email, line_edit_email)
        
        contact_layout.addWidget(scroll_contact)
        self.tabs.addTab(contact_tab, 'Contato')

        frame_layout.addWidget(self.tabs)
        main_layout.addWidget(frame)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.edit_btn = PrimaryButton('Editar Dados da Empresa', rounded=True)
        self.edit_btn.setFixedSize(200, BUTTON_HEIGHT)
        button_layout.addWidget(self.edit_btn)
        
        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)
        main_layout.addStretch()

class UsersWidget(QWidget):
    def __init__(self, db_handler, parent=None):
        super().__init__(parent)
        self.db_handler = db_handler
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(PADDING, PADDING, PADDING, PADDING)
        main_layout.setSpacing(SPACING)

        frame = QGroupBox("Gestão de Usuários")
        frame.setStyleSheet(f"""
            QGroupBox {{
                background-color: {COLOR_WIDGET_BG};
                border: 1px solid #ccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: {COLOR_HEADER};
                font-weight: bold;
            }}
        """)
        frame_layout = QVBoxLayout(frame)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid #ccc;
                background-color: {COLOR_WIDGET_BG};
            }}
            QTabBar::tab {{
                background: {COLOR_SECONDARY};
                color: white;
                padding: 8px 15px;
                border: 1px solid #ccc;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                margin-right: 2px;
            }}
            QTabBar::tab:selected {{
                background: {COLOR_PRIMARY};
                color: white;
                border-color: {COLOR_PRIMARY};
                border-bottom-color: {COLOR_WIDGET_BG};
            }}
            QTabBar::tab:hover {{
                background: {COLOR_SECONDARY_HOVER};
            }}
        """)

        usuarios_data = self.db_handler.dados.get('Usuários', {})

        def create_user_form(user_data, user_type):
            tab = QWidget()
            layout = QVBoxLayout(tab)
            
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll_content = QWidget()
            scroll.setWidget(scroll_content)
            
            form_layout = QFormLayout(scroll_content)
            form_layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)
            form_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
            form_layout.setHorizontalSpacing(SPACING * 2)
            form_layout.setVerticalSpacing(SPACING)

            def add_user_field(label_text, field_key, value=""):
                label = StyledLabel(label_text)
                line_edit = StyledLineEdit(value)
                line_edit.setText(value)
                line_edit.setReadOnly(False)
                form_layout.addRow(label, line_edit)

            if user_data:
                add_user_field("ID:", "Id", str(user_data.get('Id', '')))
                add_user_field("Nome Completo:", "Nome Completo", user_data.get('Nome Completo', ''))
                add_user_field("Nome de Usuário:", "Nome de Usuário", user_data.get('Nome de Usuário', ''))
                add_user_field("Senha:", "Senha de Usuário", user_data.get('Senha de Usuário', ''))
                add_user_field("Nível de Acesso:", "Nível de Acesso", user_data.get('Nível de Acesso', user_type))
            else:
                add_user_field("Nome Completo:", "Nome Completo", "")
                add_user_field("Nome de Usuário:", "Nome de Usuário", "")
                add_user_field("Senha:", "Senha de Usuário", "")
                add_user_field("Nível de Acesso:", "Nível de Acesso", user_type)

            layout.addWidget(scroll)
            return tab

        admin_data = usuarios_data.get('Administrator', {})
        admin_tab = create_user_form(admin_data, "Administrador")
        self.tabs.addTab(admin_tab, 'Administradores')

        tecnico_data = usuarios_data.get('Tecnico', {})
        tecnico_tab = create_user_form(tecnico_data, "Tecnico")
        self.tabs.addTab(tecnico_tab, 'Técnicos')

        gerente_data = usuarios_data.get('Gerente', {})
        gerente_tab = create_user_form(gerente_data, "Gerencia")
        self.tabs.addTab(gerente_tab, 'Gerentes')

        funcionario_data = usuarios_data.get('Funcionários', {})
        funcionario_tab = create_user_form(funcionario_data, "Comum")
        self.tabs.addTab(funcionario_tab, 'Funcionários')

        frame_layout.addWidget(self.tabs)
        main_layout.addWidget(frame)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.save_btn = PrimaryButton('Salvar Alterações', rounded=True)
        self.save_btn.setFixedSize(180, BUTTON_HEIGHT)
        button_layout.addWidget(self.save_btn)
        
        self.add_user_btn = SecondaryButton('Adicionar Usuário', rounded=True)
        self.add_user_btn.setFixedSize(150, BUTTON_HEIGHT)
        button_layout.addWidget(self.add_user_btn)
        
        self.reset_btn = SecondaryButton('Redefinir Senhas', rounded=True)
        self.reset_btn.setFixedSize(150, BUTTON_HEIGHT)
        button_layout.addWidget(self.reset_btn)
        
        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)
        main_layout.addStretch()
        
class SettingsWindow(BaseWidget):
    def __init__(self, stacked_widget, db_handler):
        super().__init__(stacked_widget, db_handler)
        self.current_user = None
        self.user_status = False

    def setup_ui(self):
        tab_style = f"""
            QTabWidget::pane {{
                border: 1px solid #ccc;
                background-color: {COLOR_WIDGET_BG};
            }}
            QTabBar::tab {{
                background: {COLOR_SECONDARY};
                color: white;
                padding: 8px 15px;
                border: 1px solid #ccc;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                margin-right: 2px;
            }}
            QTabBar::tab:selected {{
                background: {COLOR_PRIMARY};
                color: white;
                border-color: {COLOR_PRIMARY};
                border-bottom-color: {COLOR_WIDGET_BG};
            }}
            QTabBar::tab:hover {{
                background: {COLOR_SECONDARY_HOVER};
            }}
        """
        self.setStyleSheet(self.styleSheet() + tab_style)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(PADDING, PADDING, PADDING, PADDING)
        layout.setSpacing(SPACING)

        top_bar_layout = QHBoxLayout()
        
        self.back_btn = SecondaryButton('← Voltar para Home', rounded=True)
        self.back_btn.clicked.connect(self.go_back)
        top_bar_layout.addWidget(self.back_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        
        top_bar_layout.addStretch()
        
        title_label = StyledLabel('Configurações', is_header=True)
        title_label.setStyleSheet(f"color: {COLOR_HEADER};")
        top_bar_layout.addWidget(title_label)
        
        top_bar_layout.addStretch()
        
        self.backup_btn = PrimaryButton('Backup do Sistema', rounded=True)
        self.backup_btn.setFixedSize(200, BUTTON_HEIGHT)
        self.backup_btn.clicked.connect(self.backup)
        top_bar_layout.addWidget(self.backup_btn, alignment=Qt.AlignmentFlag.AlignRight)
        
        layout.addLayout(top_bar_layout)
        
        self.tabs = QTabWidget()
        
        # 1. Dados da Empresa
        empresa_widget = EmpresaWidget(self.db_handler)
        self.tabs.addTab(empresa_widget, 'Dados da Empresa')
        
        # 2. Logomarca (NOVA ABA)
        logomarca_widget = LogomarcaWidget(self.db_handler)
        self.tabs.addTab(logomarca_widget, 'Logomarca')
        
        # 3. Usuários
        users_widget = UsersWidget(self.db_handler)
        self.tabs.addTab(users_widget, 'Gestão de Usuários')
        
        # 4. Configurações de Etiqueta
        self.tabs.addTab(QLabel('Conteúdo das Configurações de Etiqueta'), 'Configurações de Etiqueta')
        
        # 5. Configurações de Tabela Nutricional
        self.tabs.addTab(QLabel('Conteúdo das Configurações de Tabela Nutricional'), 'Configurações de Tabela Nutricional')
        
        # 6. Outras Configurações
        self.tabs.addTab(QLabel('Conteúdo de Outras Configurações'), 'Outras Configurações')

        layout.addWidget(self.tabs)
        
        self.setLayout(layout)

    def showEvent(self, event):
        super().showEvent(event)
        self.collect_user_info()
        
    def collect_user_info(self):
        home_window = self.stacked_widget.widget(1)
        if hasattr(home_window, 'get_current_user'):
            self.current_user = home_window.get_current_user()
        
        if self.current_user and isinstance(self.current_user, str) and self.current_user.strip():
            self.user_status = True
            print(f"SettingsWindow: Usuário logado - '{self.current_user}'")
        else:
            self.user_status = False
            self.current_user = None
            print("SettingsWindow: Nenhum usuário logado")
        
        if self.user_status:
            self.back_btn.setText('← Voltar para Home')
        else:
            self.back_btn.setText('← Voltar para Login')

    def backup(self):
        home_window = self.stacked_widget.widget(1)
        if hasattr(home_window, 'get_current_user') and home_window.get_current_user():
            backup_window = self.stacked_widget.widget(4)
            if hasattr(backup_window, 'set_return_index'):
                backup_window.set_return_index(2)
            self.stacked_widget.setCurrentIndex(4)
        else:
            QMessageBox.warning(self, 'Acesso Negado', 'É necessário fazer login para acessar o backup.')
            self.stacked_widget.setCurrentIndex(0)

    def go_back(self):
        if self.user_status:
            self.stacked_widget.setCurrentIndex(1)
        else:
            self.stacked_widget.setCurrentIndex(0)

# =============================================================================
# CLASSE PRINCIPAL DA APLICAÇÃO (ATUALIZADA)
# =============================================================================

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Confeitaria - Sistema de Gestão')
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setStyleSheet(f"background-color: {COLOR_BACKGROUND};")

        self.db_handler = DatabaseHandler()
        self.db_handler.criar_ou_validar_backup()
        
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.login_window = LoginWindow(self.stacked_widget, self.db_handler)
        self.home_window = HomeWindow(self.stacked_widget, self.db_handler)
        self.settings_window = SettingsWindow(self.stacked_widget, self.db_handler)
        self.etiqueta_window = EtiquetaWindow(self.stacked_widget, self.db_handler)
        self.backup_window = BackupWindow(self.stacked_widget, self.db_handler)
        
        self.stacked_widget.addWidget(self.login_window)
        self.stacked_widget.addWidget(self.home_window)
        self.stacked_widget.addWidget(self.settings_window)
        self.stacked_widget.addWidget(self.etiqueta_window)
        self.stacked_widget.addWidget(self.backup_window)

    def showEvent(self, event):
        super().showEvent(event)
        self.verificar_estado_inicial()
    
    def verificar_estado_inicial(self):
        print("Verificando estado inicial dos dados...")
        
        resultado = self.db_handler.verificar_estado_inicial()
        
        print(f"Resultado da verificação: {resultado}")
        print(f"LIST_BASE: {LIST_BASE}")
        
        if resultado == list(LIST_BASE):
            print("Dados estão no estado inicial. Redirecionando para SettingsWindow...")
            self.stacked_widget.setCurrentIndex(2)
            
            QMessageBox.information(
                self, 
                'Configuração Inicial Necessária',
                'É necessário configurar os dados da empresa antes de usar o sistema.\n\n'
                'Por favor, preencha todas as informações na tela de Configurações.'
            )
        else:
            print("Dados já configurados. Mantendo na tela de Login.")
            self.stacked_widget.setCurrentIndex(0)

# =============================================================================
# PONTO DE ENTRADA DA APLICAÇÃO
# =============================================================================

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
