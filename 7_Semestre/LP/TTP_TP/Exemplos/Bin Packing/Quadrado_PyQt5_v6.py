import sys
import random
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QSlider, QLabel, 
                             QGroupBox, QSpinBox, QDoubleSpinBox, QTabWidget,
                             QMessageBox, QProgressBar, QCheckBox, QScrollArea)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtOpenGL import QGLWidget
import OpenGL.GL as gl
import OpenGL.GLU as glu


vector_cores_hex = [
    "#000000",  # Preto (linhas)
    "#FFFFFF",  # Branco (fundo)
    "#FF6B6B",  # Vermelho coral
    "#4ECDC4",  # Turquesa
    "#45B7D1",  # Azul claro
    "#96CEB4",  # Verde menta
    "#FFEAA7",  # Amarelo claro
    "#DDA0DD",  # Ameixa
    "#98D8C8",  # Verde água
    "#F7DC6F",  # Amarelo dourado
    "#BB8FCE",  # Lavanda
    "#85C1E9",  # Azul céu
    "#F8C471",  # Laranja claro
    "#82E0AA",  # Verde primavera
    "#F1948A",  # Rosa salmão
    "#7FB3D5",  # Azul pólvora
    "#F9E79F",  # Amarelo creme
    "#D7BDE2",  # Lilás
    "#A9DFBF",  # Verde pastel
    "#F5B7B1",  # Rosa claro
    "#AED6F1",  # Azul bebê
    "#FAD7A0",  # Pêssego
    "#ABEBC6",  # Verde maná
    "#E8DAEF",  # Lavanda claro
    "#FDEBD0",  # Amêndoa
    "#D1F2EB",  # Azul gelo
    "#FDEDEC",  # Rosa muito claro
    "#EAF2F8",  # Azul alice
    "#FEF9E7",  # Amarelo floral
    "#EAEDED",  # Cinza muito claro
    "#2E4053",  # Azul petróleo
    "#1A5276",  # Azul marinho
    "#186A3B",  # Verde floresta
    "#6C3483"   # Roxo profundo
]


def hex_to_rgb(hex_color):
    """Converte cor hexadecimal para RGB normalizado (0-1)"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))


class BinPacking3D:
    def __init__(self, container_width=10, container_height=10, container_depth=10):
        self.container_width = container_width
        self.container_height = container_height
        self.container_depth = container_depth
        self.items = []
        self.positions = []
        
    def add_item(self, width, height, depth):
        """Adiciona um item 3D usando algoritmo First Fit"""
        item = {'width': width, 'height': height, 'depth': depth, 'placed': False}
        
        # Tentar encontrar posição no container existente
        for z in range(0, self.container_depth - depth + 1):
            for y in range(0, self.container_height - height + 1):
                for x in range(0, self.container_width - width + 1):
                    if self.can_place_at(x, y, z, width, height, depth):
                        item['x'] = x
                        item['y'] = y
                        item['z'] = z
                        item['placed'] = True
                        self.items.append(item)
                        return True
        
        item['placed'] = False
        self.items.append(item)
        return False
    
    def can_place_at(self, x, y, z, width, height, depth):
        """Verifica se pode colocar o item na posição (x,y,z)"""
        if (x + width > self.container_width or 
            y + height > self.container_height or 
            z + depth > self.container_depth):
            return False
        
        for item in self.items:
            if item['placed']:
                if (x < item['x'] + item['width'] and
                    x + width > item['x'] and
                    y < item['y'] + item['height'] and
                    y + height > item['y'] and
                    z < item['z'] + item['depth'] and
                    z + depth > item['z']):
                    return False
        return True
    
    def clear_items(self):
        self.items = []

class DynamicBinPacking3D(BinPacking3D):
    def __init__(self, container_width=10, container_height=10, container_depth=10):
        super().__init__(container_width, container_height, container_depth)
        self.arrival_sequence = []
        self.departure_times = {}
        self.current_time = 0
        
    def add_item_with_duration(self, width, height, depth, duration):
        """Adiciona item com duração específica"""
        item_id = len(self.items)
        self.arrival_sequence.append(('arrival', item_id, self.current_time))
        self.departure_times[item_id] = self.current_time + duration
        
        success = self.add_item(width, height, depth)
        if success:
            self.items[-1]['id'] = item_id
            self.items[-1]['duration'] = duration
            self.items[-1]['arrival_time'] = self.current_time
        return success
    
    def update_time(self, time_step=1):
        """Atualiza o tempo e remove itens expirados"""
        self.current_time += time_step
        items_to_remove = []
        
        for i, item in enumerate(self.items):
            if item.get('placed', False) and item['id'] in self.departure_times:
                if self.current_time >= self.departure_times[item['id']]:
                    items_to_remove.append(i)
                    self.arrival_sequence.append(('departure', item['id'], self.current_time))
        
        # Remover itens em ordem reversa para não afetar índices
        for i in sorted(items_to_remove, reverse=True):
            if i < len(self.items):
                self.items.pop(i)
        
        return len(items_to_remove)

class Knapsack3D:
    def __init__(self, capacity_width=10, capacity_height=10, capacity_depth=10):
        self.capacity_width = capacity_width
        self.capacity_height = capacity_height
        self.capacity_depth = capacity_depth
        self.items = []
        self.selected_items = []
        self.max_value = 0
        
    def add_item(self, width, height, depth, value):
        self.items.append({
            'width': width, 'height': height, 'depth': depth, 
            'value': value, 'volume': width * height * depth
        })
    
    def solve_knapsack(self):
        """Algoritmo de programação dinâmica para knapsack 3D"""
        n = len(self.items)
        if n == 0:
            return 0
            
        # Criar matriz DP 4D
        dp = np.zeros((n + 1, self.capacity_width + 1, 
                      self.capacity_height + 1, self.capacity_depth + 1))
        
        for i in range(1, n + 1):
            item = self.items[i-1]
            for w in range(self.capacity_width + 1):
                for h in range(self.capacity_height + 1):
                    for d in range(self.capacity_depth + 1):
                        if (item['width'] <= w and item['height'] <= h and item['depth'] <= d):
                            dp[i][w][h][d] = max(
                                dp[i-1][w][h][d],
                                dp[i-1][w-item['width']][h-item['height']][d-item['depth']] + item['value']
                            )
                        else:
                            dp[i][w][h][d] = dp[i-1][w][h][d]
        
        # Reconstruir solução
        self.max_value = dp[n][self.capacity_width][self.capacity_height][self.capacity_depth]
        self.selected_items = []
        
        w, h, d = self.capacity_width, self.capacity_height, self.capacity_depth
        for i in range(n, 0, -1):
            if dp[i][w][h][d] != dp[i-1][w][h][d]:
                self.selected_items.append(i-1)
                w -= self.items[i-1]['width']
                h -= self.items[i-1]['height']
                d -= self.items[i-1]['depth']
        
        self.selected_items.reverse()
        return self.max_value

class OpenGL3DViewer(QGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.rotation_x = 0
        self.rotation_y = 0
        self.zoom = -40
        self.last_pos = None
        
        # Problemas
        self.bin_packer = None
        self.dynamic_packer = None
        self.knapsack = None
        self.current_problem = "bin_packing"
        
        # Rotação automática
        self.auto_rotate_x = False
        self.auto_rotate_y = False
        self.rotation_timer = QTimer()
        self.rotation_timer.timeout.connect(self.auto_rotate)
        self.rotation_timer.start(50)  # 20 FPS
        
        # Centro do objeto para focar a câmera
        self.focus_point = [0, 0, 0]
        
        # Cores pré-definidas
        self.background_color = hex_to_rgb(vector_cores_hex[1]) + (1.0,)  # Branco
        self.line_color = hex_to_rgb(vector_cores_hex[0]) + (1.0,)  # Preto
        self.container_color = hex_to_rgb(vector_cores_hex[1]) + (0.2,)  # Branco transparente
        
        # Cores para os itens (excluindo preto e branco)
        self.item_colors = [hex_to_rgb(color) + (0.8,) for color in vector_cores_hex[2:]]
        
    def initializeGL(self):
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_LIGHTING)
        gl.glEnable(gl.GL_LIGHT0)
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, [1, 1, 1, 0])
        gl.glEnable(gl.GL_COLOR_MATERIAL)
        gl.glColorMaterial(gl.GL_FRONT_AND_BACK, gl.GL_AMBIENT_AND_DIFFUSE)
        
    def resizeGL(self, w, h):
        gl.glViewport(0, 0, w, h)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluPerspective(45, w/h, 0.1, 200.0)  # Aumentado o far plane
        gl.glMatrixMode(gl.GL_MODELVIEW)
        
    def paintGL(self):
        # Definir cor de fundo como branco
        gl.glClearColor(*self.background_color)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glLoadIdentity()
        
        # Calcular ponto de foco baseado no problema atual
        self.calculate_focus_point()
        
        # Configurar câmera para focar no centro do objeto
        gl.glTranslatef(0, 0, self.zoom)
        gl.glRotatef(self.rotation_x, 1, 0, 0)
        gl.glRotatef(self.rotation_y, 0, 1, 0)
        gl.glTranslatef(-self.focus_point[0], -self.focus_point[1], -self.focus_point[2])
        
        if self.current_problem == "bin_packing" and self.bin_packer:
            self.draw_bin_packing()
        elif self.current_problem == "dynamic_packing" and self.dynamic_packer:
            self.draw_dynamic_packing()
        elif self.current_problem == "knapsack" and self.knapsack:
            self.draw_knapsack()
            
    def calculate_focus_point(self):
        """Calcula o ponto central para focar a câmera"""
        if self.current_problem == "bin_packing" and self.bin_packer:
            self.focus_point = [
                self.bin_packer.container_width / 2,
                self.bin_packer.container_height / 2, 
                self.bin_packer.container_depth / 2
            ]
        elif self.current_problem == "dynamic_packing" and self.dynamic_packer:
            self.focus_point = [
                self.dynamic_packer.container_width / 2,
                self.dynamic_packer.container_height / 2,
                self.dynamic_packer.container_depth / 2
            ]
        elif self.current_problem == "knapsack" and self.knapsack:
            self.focus_point = [
                self.knapsack.capacity_width / 2,
                self.knapsack.capacity_height / 2,
                self.knapsack.capacity_depth / 2
            ]
        else:
            self.focus_point = [0, 0, 0]
    
    def draw_bin_packing(self):
        # Desenhar container (transparente)
        self.draw_cube_wireframe(0, 0, 0, 
                               self.bin_packer.container_width,
                               self.bin_packer.container_height,
                               self.bin_packer.container_depth,
                               self.line_color)
        
        # Desenhar itens
        for i, item in enumerate(self.bin_packer.items):
            if item.get('placed', False):
                color = self.get_color_for_item(item, i)
                self.draw_cube_solid(item['x'], item['y'], item['z'],
                                   item['width'], item['height'], item['depth'],
                                   color)
    
    def draw_dynamic_packing(self):
        # Desenhar container (transparente)
        self.draw_cube_wireframe(0, 0, 0,
                               self.dynamic_packer.container_width,
                               self.dynamic_packer.container_height,
                               self.dynamic_packer.container_depth,
                               self.line_color)
        
        # Desenhar itens
        for i, item in enumerate(self.dynamic_packer.items):
            if item.get('placed', False):
                # Cor baseada no tempo restante
                time_left = self.dynamic_packer.departure_times[item['id']] - self.dynamic_packer.current_time
                total_time = item['duration']
                ratio = time_left / total_time if total_time > 0 else 1
                
                r = max(0.2, ratio)
                g = max(0.2, 1 - ratio)
                b = 0.5
                
                self.draw_cube_solid(item['x'], item['y'], item['z'],
                                   item['width'], item['height'], item['depth'],
                                   (r, g, b, 0.8))
    
    def draw_knapsack(self):
        # Desenhar container da mochila (transparente)
        self.draw_cube_wireframe(0, 0, 0,
                               self.knapsack.capacity_width,
                               self.knapsack.capacity_height,
                               self.knapsack.capacity_depth,
                               self.line_color)
        
        # Desenhar itens selecionados
        x_offset = 0
        for idx in self.knapsack.selected_items:
            item = self.knapsack.items[idx]
            color = self.get_color_for_item(item, idx)
            self.draw_cube_solid(x_offset, 0, 0,
                               item['width'], item['height'], item['depth'],
                               color)
            x_offset += item['width'] + 1
    
    def draw_cube_solid(self, x, y, z, width, height, depth, color):
        gl.glPushMatrix()
        gl.glTranslatef(x + width/2, y + height/2, z + depth/2)
        gl.glScalef(width, height, depth)
        
        gl.glColor4f(*color)
        
        gl.glBegin(gl.GL_QUADS)
        # Frente
        gl.glNormal3f(0, 0, 1)
        gl.glVertex3f(-0.5, -0.5, 0.5)
        gl.glVertex3f(0.5, -0.5, 0.5)
        gl.glVertex3f(0.5, 0.5, 0.5)
        gl.glVertex3f(-0.5, 0.5, 0.5)
        
        # Trás
        gl.glNormal3f(0, 0, -1)
        gl.glVertex3f(-0.5, -0.5, -0.5)
        gl.glVertex3f(-0.5, 0.5, -0.5)
        gl.glVertex3f(0.5, 0.5, -0.5)
        gl.glVertex3f(0.5, -0.5, -0.5)
        
        # Esquerda
        gl.glNormal3f(-1, 0, 0)
        gl.glVertex3f(-0.5, -0.5, -0.5)
        gl.glVertex3f(-0.5, -0.5, 0.5)
        gl.glVertex3f(-0.5, 0.5, 0.5)
        gl.glVertex3f(-0.5, 0.5, -0.5)
        
        # Direita
        gl.glNormal3f(1, 0, 0)
        gl.glVertex3f(0.5, -0.5, -0.5)
        gl.glVertex3f(0.5, 0.5, -0.5)
        gl.glVertex3f(0.5, 0.5, 0.5)
        gl.glVertex3f(0.5, -0.5, 0.5)
        
        # Topo
        gl.glNormal3f(0, 1, 0)
        gl.glVertex3f(-0.5, 0.5, -0.5)
        gl.glVertex3f(-0.5, 0.5, 0.5)
        gl.glVertex3f(0.5, 0.5, 0.5)
        gl.glVertex3f(0.5, 0.5, -0.5)
        
        # Base
        gl.glNormal3f(0, -1, 0)
        gl.glVertex3f(-0.5, -0.5, -0.5)
        gl.glVertex3f(0.5, -0.5, -0.5)
        gl.glVertex3f(0.5, -0.5, 0.5)
        gl.glVertex3f(-0.5, -0.5, 0.5)
        gl.glEnd()
        
        gl.glPopMatrix()
    
    def draw_cube_wireframe(self, x, y, z, width, height, depth, color):
        gl.glPushMatrix()
        gl.glTranslatef(x + width/2, y + height/2, z + depth/2)
        gl.glScalef(width, height, depth)
        
        gl.glColor4f(*color)
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
        gl.glLineWidth(2.0)  # Linhas mais grossas para melhor visibilidade
        
        gl.glBegin(gl.GL_QUADS)
        vertices = [
            [-0.5, -0.5, 0.5], [0.5, -0.5, 0.5], [0.5, 0.5, 0.5], [-0.5, 0.5, 0.5],
            [-0.5, -0.5, -0.5], [-0.5, 0.5, -0.5], [0.5, 0.5, -0.5], [0.5, -0.5, -0.5],
            [-0.5, -0.5, -0.5], [-0.5, -0.5, 0.5], [-0.5, 0.5, 0.5], [-0.5, 0.5, -0.5],
            [0.5, -0.5, -0.5], [0.5, 0.5, -0.5], [0.5, 0.5, 0.5], [0.5, -0.5, 0.5],
            [-0.5, 0.5, -0.5], [-0.5, 0.5, 0.5], [0.5, 0.5, 0.5], [0.5, 0.5, -0.5],
            [-0.5, -0.5, -0.5], [0.5, -0.5, -0.5], [0.5, -0.5, 0.5], [-0.5, -0.5, 0.5]
        ]
        
        for vertex in vertices:
            gl.glVertex3f(*vertex)
        
        gl.glEnd()
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)
        gl.glPopMatrix()
    
    def get_color_for_item(self, item, index):
        """Seleciona uma cor aleatória da paleta para cada item"""
        if hasattr(self, 'item_colors') and self.item_colors:
            return random.choice(self.item_colors)
        else:
            # Fallback para cores geradas proceduralmente
            r = (item['width'] / 10.0) % 1.0
            g = (item['height'] / 10.0) % 1.0
            b = (item['depth'] / 10.0) % 1.0
            return (r, g, b, 0.8)
    
    def auto_rotate(self):
        """Rotação automática baseada nas configurações"""
        if self.auto_rotate_x:
            self.rotation_x += 1
            if self.rotation_x > 360:
                self.rotation_x = 0
                
        if self.auto_rotate_y:
            self.rotation_y += 1
            if self.rotation_y > 360:
                self.rotation_y = 0
                
        if self.auto_rotate_x or self.auto_rotate_y:
            self.update()
    
    def mousePressEvent(self, event):
        self.last_pos = event.pos()
    
    def mouseMoveEvent(self, event):
        dx = event.x() - self.last_pos.x()
        dy = event.y() - self.last_pos.y()
        
        if event.buttons() & Qt.LeftButton:
            self.rotation_x += dy * 0.5
            self.rotation_y += dx * 0.5
            self.update()
        
        self.last_pos = event.pos()
    
    def wheelEvent(self, event):
        self.zoom += event.angleDelta().y() * 0.01
        self.update()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Problemas de Otimização 3D - Bin Packing, Dynamic Packing e Knapsack")
        self.setGeometry(100, 100, 1400, 900)
        
        # Inicializar problemas
        self.bin_packer = BinPacking3D()
        self.dynamic_packer = DynamicBinPacking3D()
        self.knapsack = Knapsack3D()
        
        # Timer para animação dinâmica
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_dynamic_packing)
        
        self.init_ui()
        
    def init_ui(self):
        central_widget = QWidget()
        main_layout = QHBoxLayout()
        
        # Painel de controle
        control_panel = self.create_control_panel()
        control_panel.setFixedWidth(350)  # Ligeiramente maior para novos controles
        
        # Visualizador 3D
        self.viewer = OpenGL3DViewer()
        self.viewer.bin_packer = self.bin_packer
        self.viewer.dynamic_packer = self.dynamic_packer
        self.viewer.knapsack = self.knapsack
        
        main_layout.addWidget(control_panel)
        main_layout.addWidget(self.viewer)
        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
    
    def create_control_panel(self):
        # O widget que contém todo o conteúdo do painel de controle
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setSpacing(10) # Ajuste de espaçamento
        layout.setContentsMargins(10, 10, 10, 10) # Margens internas

        # Seletor de problema
        problem_group = QGroupBox("Selecionar Problema")
        problem_layout = QVBoxLayout()
        
        self.problem_tabs = QTabWidget()
        
        # Tab Bin Packing
        bin_tab = self.create_bin_packing_tab()
        self.problem_tabs.addTab(bin_tab, "Bin Packing")
        
        # Tab Dynamic Packing
        dynamic_tab = self.create_dynamic_packing_tab()
        self.problem_tabs.addTab(dynamic_tab, "Dynamic Packing")
        
        # Tab Knapsack
        knapsack_tab = self.create_knapsack_tab()
        self.problem_tabs.addTab(knapsack_tab, "Knapsack")
        
        self.problem_tabs.currentChanged.connect(self.on_problem_changed)
        
        problem_layout.addWidget(self.problem_tabs)
        problem_group.setLayout(problem_layout)
        
        # Controles de visualização
        viz_group = QGroupBox("Controles de Câmera")
        viz_layout = QVBoxLayout()
        
        # Rotação automática
        rotation_group = QGroupBox("Rotação Automática")
        rotation_layout = QVBoxLayout()
        
        self.auto_rotate_x = QCheckBox("Rotação Automática Eixo X")
        self.auto_rotate_x.stateChanged.connect(self.toggle_auto_rotate_x)
        rotation_layout.addWidget(self.auto_rotate_x)
        
        self.auto_rotate_y = QCheckBox("Rotação Automática Eixo Y")
        self.auto_rotate_y.stateChanged.connect(self.toggle_auto_rotate_y)
        rotation_layout.addWidget(self.auto_rotate_y)
        
        rotation_group.setLayout(rotation_layout)
        viz_layout.addWidget(rotation_group)
        
        # Controles manuais
        manual_group = QGroupBox("Controles Manuais")
        manual_layout = QVBoxLayout()
        
        manual_layout.addWidget(QLabel("Rotação X:"))
        self.rotation_x_slider = QSlider(Qt.Horizontal)
        self.rotation_x_slider.setRange(0, 360)
        self.rotation_x_slider.valueChanged.connect(self.update_rotation_x)
        manual_layout.addWidget(self.rotation_x_slider)
        
        manual_layout.addWidget(QLabel("Rotação Y:"))
        self.rotation_y_slider = QSlider(Qt.Horizontal)
        self.rotation_y_slider.setRange(0, 360)
        self.rotation_y_slider.valueChanged.connect(self.update_rotation_y)
        manual_layout.addWidget(self.rotation_y_slider)
        
        manual_layout.addWidget(QLabel("Zoom:"))
        self.zoom_slider = QSlider(Qt.Horizontal)
        self.zoom_slider.setRange(-80, -20)
        self.zoom_slider.setValue(-40)
        self.zoom_slider.valueChanged.connect(self.update_zoom)
        manual_layout.addWidget(self.zoom_slider)
        
        manual_group.setLayout(manual_layout)
        viz_layout.addWidget(manual_group)
        
        # Dicas de uso
        tips_group = QGroupBox("Dicas de Navegação")
        tips_layout = QVBoxLayout()
        tips_layout.addWidget(QLabel("• Arraste: Rotacionar"))
        tips_layout.addWidget(QLabel("• Roda do mouse: Zoom"))
        tips_layout.addWidget(QLabel("• Checkboxes: Rotação automática"))
        tips_group.setLayout(tips_layout)
        viz_layout.addWidget(tips_group)
        
        viz_group.setLayout(viz_layout)
        
        layout.addWidget(problem_group)
        layout.addWidget(viz_group)
        layout.addStretch()
        
        # Cria o QScrollArea e define o content_widget como seu widget
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(content_widget)
        
        return scroll_area
    
    def create_bin_packing_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(10) # Ajuste de espaçamento para a aba

        # Configurações do container
        container_group = QGroupBox("Configurações do Container")
        container_layout = QVBoxLayout(container_group)
        container_layout.setSpacing(5) # Espaçamento menor dentro do grupo
        
        container_layout.addWidget(QLabel("Largura:"))
        self.bin_width = QSpinBox()
        self.bin_width.setRange(10, 300)
        self.bin_width.setValue(20)
        container_layout.addWidget(self.bin_width)
        
        container_layout.addWidget(QLabel("Altura:"))
        self.bin_height = QSpinBox()
        self.bin_height.setRange(10, 300)
        self.bin_height.setValue(20)
        container_layout.addWidget(self.bin_height)
        
        container_layout.addWidget(QLabel("Profundidade:"))
        self.bin_depth = QSpinBox()
        self.bin_depth.setRange(10, 300)
        self.bin_depth.setValue(20)
        container_layout.addWidget(self.bin_depth)
        
        container_group.setLayout(container_layout)
        
        # Configurações dos objetos
        objects_group = QGroupBox("Configurações dos Objetos")
        objects_layout = QVBoxLayout()
        
        objects_layout.addWidget(QLabel("Quantidade:"))
        self.num_objects = QSpinBox()
        self.num_objects.setRange(1, 100)
        self.num_objects.setValue(15)
        objects_layout.addWidget(self.num_objects)
        
        objects_layout.addWidget(QLabel("Tamanho Mínimo:"))
        self.min_size = QSpinBox()
        self.min_size.setRange(1, 10)
        self.min_size.setValue(2)
        objects_layout.addWidget(self.min_size)
        
        objects_layout.addWidget(QLabel("Tamanho Máximo:"))
        self.max_size = QSpinBox()
        self.max_size.setRange(5, 30)
        self.max_size.setValue(8)
        objects_layout.addWidget(self.max_size)
        
        objects_group.setLayout(objects_layout)
        
        # Botões
        self.generate_bin_btn = QPushButton("Gerar Objetos Aleatórios")
        self.generate_bin_btn.clicked.connect(self.generate_bin_packing)
        
        self.clear_bin_btn = QPushButton("Limpar")
        self.clear_bin_btn.clicked.connect(self.clear_bin_packing)
        
        # Estatísticas
        self.bin_stats = QLabel("Estatísticas aparecerão aqui")
        self.bin_stats.setStyleSheet("background-color: #f0f0f0; padding: 8px; border-radius: 4px;")
        self.bin_stats.setWordWrap(True)
        
        layout.addWidget(container_group)
        layout.addWidget(objects_group)
        layout.addWidget(self.generate_bin_btn)
        layout.addWidget(self.clear_bin_btn)
        layout.addWidget(self.bin_stats)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def create_dynamic_packing_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(10) # Ajuste de espaçamento para a aba

        # Configurações similares ao bin packing
        container_group = QGroupBox("Configurações do Container")
        container_layout = QVBoxLayout(container_group)
        container_layout.setSpacing(5) # Espaçamento menor dentro do grupo
        
        container_layout.addWidget(QLabel("Largura:"))
        self.dynamic_width = QSpinBox()
        self.dynamic_width.setRange(10, 300)
        self.dynamic_width.setValue(25)
        container_layout.addWidget(self.dynamic_width)
        
        container_layout.addWidget(QLabel("Altura:"))
        self.dynamic_height = QSpinBox()
        self.dynamic_height.setRange(10, 300)
        self.dynamic_height.setValue(25)
        container_layout.addWidget(self.dynamic_height)
        
        container_layout.addWidget(QLabel("Profundidade:"))
        self.dynamic_depth = QSpinBox()
        self.dynamic_depth.setRange(10, 300)
        self.dynamic_depth.setValue(25)
        container_layout.addWidget(self.dynamic_depth)
        
        container_group.setLayout(container_layout)
        
        # Configurações dinâmicas
        dynamic_group = QGroupBox("Configurações Dinâmicas")
        dynamic_layout = QVBoxLayout()
        
        dynamic_layout.addWidget(QLabel("Duração Mínima:"))
        self.min_duration = QSpinBox()
        self.min_duration.setRange(1, 50)
        self.min_duration.setValue(10)
        dynamic_layout.addWidget(self.min_duration)
        
        dynamic_layout.addWidget(QLabel("Duração Máxima:"))
        self.max_duration = QSpinBox()
        self.max_duration.setRange(10, 100)
        self.max_duration.setValue(30)
        dynamic_layout.addWidget(self.max_duration)
        
        dynamic_layout.addWidget(QLabel("Velocidade:"))
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(1, 10)
        self.speed_slider.setValue(5)
        dynamic_layout.addWidget(self.speed_slider)
        
        dynamic_group.setLayout(dynamic_layout)
        
        # Botões
        self.start_dynamic_btn = QPushButton("Iniciar Simulação")
        self.start_dynamic_btn.clicked.connect(self.start_dynamic_packing)
        
        self.stop_dynamic_btn = QPushButton("Parar Simulação")
        self.stop_dynamic_btn.clicked.connect(self.stop_dynamic_packing)
        
        # Estatísticas
        self.dynamic_stats = QLabel("Simulação parada")
        self.dynamic_stats.setStyleSheet("background-color: #f0f0f0; padding: 8px; border-radius: 4px;")
        self.dynamic_stats.setWordWrap(True)
        
        layout.addWidget(container_group)
        layout.addWidget(dynamic_group)
        layout.addWidget(self.start_dynamic_btn)
        layout.addWidget(self.stop_dynamic_btn)
        layout.addWidget(self.dynamic_stats)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def create_knapsack_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(10) # Ajuste de espaçamento para a aba

        # Configurações da mochila
        knapsack_group = QGroupBox("Configurações da Mochila")
        knapsack_layout = QVBoxLayout(knapsack_group)
        knapsack_layout.setSpacing(5) # Espaçamento menor dentro do grupo
        
        knapsack_layout.addWidget(QLabel("Capacidade Largura:"))
        self.knapsack_width = QSpinBox()
        self.knapsack_width.setRange(10, 100)
        self.knapsack_width.setValue(15)
        knapsack_layout.addWidget(self.knapsack_width)
        
        knapsack_layout.addWidget(QLabel("Capacidade Altura:"))
        self.knapsack_height = QSpinBox()
        self.knapsack_height.setRange(10, 100)
        self.knapsack_height.setValue(15)
        knapsack_layout.addWidget(self.knapsack_height)
        
        knapsack_layout.addWidget(QLabel("Capacidade Profundidade:"))
        self.knapsack_depth = QSpinBox()
        self.knapsack_depth.setRange(10, 100)
        self.knapsack_depth.setValue(15)
        knapsack_layout.addWidget(self.knapsack_depth)
        
        knapsack_group.setLayout(knapsack_layout)
        
        # Configurações dos itens
        items_group = QGroupBox("Configurações dos Itens")
        items_layout = QVBoxLayout()
        
        items_layout.addWidget(QLabel("Número de Itens:"))
        self.knapsack_num_items = QSpinBox()
        self.knapsack_num_items.setRange(5, 50)
        self.knapsack_num_items.setValue(20)
        items_layout.addWidget(self.knapsack_num_items)
        
        items_layout.addWidget(QLabel("Valor Máximo:"))
        self.max_value = QSpinBox()
        self.max_value.setRange(10, 200)
        self.max_value.setValue(100)
        items_layout.addWidget(self.max_value)
        
        items_group.setLayout(items_layout)
        
        # Botões
        self.solve_knapsack_btn = QPushButton("Resolver Knapsack")
        self.solve_knapsack_btn.clicked.connect(self.solve_knapsack)
        
        # Resultados
        self.knapsack_results = QLabel("Resolva o problema para ver resultados")
        self.knapsack_results.setStyleSheet("background-color: #f0f0f0; padding: 8px; border-radius: 4px;")
        self.knapsack_results.setWordWrap(True)
        
        layout.addWidget(knapsack_group)
        layout.addWidget(items_group)
        layout.addWidget(self.solve_knapsack_btn)
        layout.addWidget(self.knapsack_results)
        layout.addStretch()
        
        widget.setLayout(layout)
        return widget
    
    def on_problem_changed(self, index):
        problems = ["bin_packing", "dynamic_packing", "knapsack"]
        self.viewer.current_problem = problems[index]
        self.viewer.update()
    
    def toggle_auto_rotate_x(self, state):
        self.viewer.auto_rotate_x = (state == Qt.Checked)
    
    def toggle_auto_rotate_y(self, state):
        self.viewer.auto_rotate_y = (state == Qt.Checked)
    
    def generate_bin_packing(self):
        # Atualizar container
        self.bin_packer = BinPacking3D(
            self.bin_width.value(),
            self.bin_height.value(),
            self.bin_depth.value()
        )
        self.viewer.bin_packer = self.bin_packer
        
        # Gerar objetos aleatórios
        placed_count = 0
        for i in range(self.num_objects.value()):
            width = random.randint(self.min_size.value(), self.max_size.value())
            height = random.randint(self.min_size.value(), self.max_size.value())
            depth = random.randint(self.min_size.value(), self.max_size.value())
            
            if self.bin_packer.add_item(width, height, depth):
                placed_count += 1
        
        # Atualizar estatísticas
        total_volume = self.bin_packer.container_width * self.bin_packer.container_height * self.bin_packer.container_depth
        used_volume = sum(item['width'] * item['height'] * item['depth'] 
                         for item in self.bin_packer.items if item['placed'])
        utilization = (used_volume / total_volume) * 100
        
        self.bin_stats.setText(
            f"Objetos colocados: {placed_count}/{self.num_objects.value()}\n"
            f"Utilização: {utilization:.1f}%\n"
            f"Volume usado: {used_volume}/{total_volume}"
        )
        
        self.viewer.update()
    
    def clear_bin_packing(self):
        self.bin_packer.clear_items()
        self.bin_stats.setText("Container limpo")
        self.viewer.update()
    
    def start_dynamic_packing(self):
        self.dynamic_packer = DynamicBinPacking3D(
            self.dynamic_width.value(),
            self.dynamic_height.value(),
            self.dynamic_depth.value()
        )
        self.viewer.dynamic_packer = self.dynamic_packer
        
        # Gerar objetos iniciais
        for i in range(10):
            width = random.randint(2, 8)
            height = random.randint(2, 8)
            depth = random.randint(2, 8)
            duration = random.randint(self.min_duration.value(), self.max_duration.value())
            self.dynamic_packer.add_item_with_duration(width, height, depth, duration)
        
        self.animation_timer.start(1000 // self.speed_slider.value())
        self.dynamic_stats.setText("Simulação em andamento...")
    
    def stop_dynamic_packing(self):
        self.animation_timer.stop()
        self.dynamic_stats.setText("Simulação parada")
    
    def update_dynamic_packing(self):
        # Adicionar novo item ocasionalmente
        if random.random() < 0.3:  # 30% de chance por tick
            width = random.randint(2, 8)
            height = random.randint(2, 8)
            depth = random.randint(2, 8)
            duration = random.randint(self.min_duration.value(), self.max_duration.value())
            self.dynamic_packer.add_item_with_duration(width, height, depth, duration)
        
        # Atualizar tempo
        removed_count = self.dynamic_packer.update_time()
        
        # Atualizar estatísticas
        placed_count = sum(1 for item in self.dynamic_packer.items if item['placed'])
        total_volume = (self.dynamic_packer.container_width * 
                       self.dynamic_packer.container_height * 
                       self.dynamic_packer.container_depth)
        used_volume = sum(item['width'] * item['height'] * item['depth'] 
                         for item in self.dynamic_packer.items if item['placed'])
        utilization = (used_volume / total_volume) * 100
        
        self.dynamic_stats.setText(
            f"Tempo: {self.dynamic_packer.current_time}\n"
            f"Objetos ativos: {placed_count}\n"
            f"Utilização: {utilization:.1f}%\n"
            f"Removidos neste tick: {removed_count}"
        )
        
        self.viewer.update()
    
    def solve_knapsack(self):
        self.knapsack = Knapsack3D(
            self.knapsack_width.value(),
            self.knapsack_height.value(),
            self.knapsack_depth.value()
        )
        self.viewer.knapsack = self.knapsack
        
        # Gerar itens aleatórios
        for i in range(self.knapsack_num_items.value()):
            width = random.randint(2, 8)
            height = random.randint(2, 8)
            depth = random.randint(2, 8)
            value = random.randint(10, self.max_value.value())
            self.knapsack.add_item(width, height, depth, value)
        
        # Resolver
        max_value = self.knapsack.solve_knapsack()
        
        # Mostrar resultados
        total_volume = sum(self.knapsack.items[i]['volume'] for i in self.knapsack.selected_items)
        max_volume = (self.knapsack.capacity_width * 
                     self.knapsack.capacity_height * 
                     self.knapsack.capacity_depth)
        
        self.knapsack_results.setText(
            f"Valor máximo: {max_value}\n"
            f"Itens selecionados: {len(self.knapsack.selected_items)}/{self.knapsack_num_items.value()}\n"
            f"Volume usado: {total_volume}/{max_volume}\n"
            f"Eficiência: {(total_volume/max_volume)*100:.1f}%"
        )
        
        self.viewer.update()
    
    def update_rotation_x(self, value):
        self.viewer.rotation_x = value
        self.viewer.update()
    
    def update_rotation_y(self, value):
        self.viewer.rotation_y = value
        self.viewer.update()
    
    def update_zoom(self, value):
        self.viewer.zoom = value
        self.viewer.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())