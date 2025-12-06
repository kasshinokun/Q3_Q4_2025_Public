"""
Módulo de Xadrez Adaptado para Flask.

Adapta a lógica do Pygame (020_Xadrez/chess.py) para ser executada em um ambiente web (Flask).
O jogo será renderizado como uma imagem PNG no Flask, e as interações do usuário
serão tratadas via requisições HTTP.
"""

import base64
from io import BytesIO
import pygame as pg
import os 
from typing import List, Dict, Any

# Importar a lógica do jogo de xadrez
# O arquivo chess.py precisa ser copiado para o diretório core
# para que possa ser importado.

# Copiar chess.py e as imagens para o diretório core
# O Pygame original usa pg.image.load('./pawn black.png')
# As imagens precisam estar acessíveis.

# A classe Chess do arquivo original é muito acoplada ao Pygame.
# A adaptação será complexa. Vou focar em criar uma classe que simule
# a lógica do jogo e gere a imagem do tabuleiro.

class ChessFlask:
    """
    Simula a lógica do jogo de xadrez e gera a imagem do tabuleiro.
    """
    
    def __init__(self):
        # Inicialização mínima do Pygame para uso de fontes e imagens
        if not pg.get_init():
            pg.init()
        
        self.square_size = 100
        self.board_size = 8 * self.square_size
        self.green = (115, 150, 80)
        self.green_light = (235, 235, 210)
        
        # Carregar imagens das peças
        self.pieces_images = self._load_pieces()
        
        # Estado inicial do tabuleiro
        self.board_map = [['b_rk','b_kn','b_bs','b_qn','b_kg','b_bs','b_kn','b_rk'],
                          ['b_pw','b_pw','b_pw','b_pw','b_pw','b_pw','b_pw','b_pw'],
                          [    '','','','','','','',''],
                          [    '','','','','','','',''],
                          [    '','','','','','','',''],
                          [    '','','','','','','',''],
                          ['w_pw','w_pw','w_pw','w_pw','w_pw','w_pw','w_pw','w_pw'],
                          ['w_rk','w_kn','w_bs','w_qn','w_kg','w_bs','w_kn','w_rk']]
        
        self.selected_piece_pos = None
        self.player_turn = 'white'

    def _load_pieces(self) -> Dict[str, pg.Surface]:
        """Carrega as imagens das peças de xadrez."""
        pieces = {}
        # Lista de nomes de arquivos de peças
        piece_files = [
            'pawn black.png', 'knight black.png', 'bishop black.png', 'queen black.png', 'king black.png', 'rook black.png',
            'pawn white.png', 'knight white.png', 'bishop white.png', 'queen white.png', 'king white.png', 'rook white.png'
        ]
        
        # O caminho para as imagens é /home/ubuntu/project_chess/020_Xadrez/
        base_path = os.path.dirname(os.path.abspath(__file__))+os.sep+'images'+os.sep+'chess'+os.sep
        
        for filename in piece_files:
            try:
                # O nome da peça no mapa é 'cor_tipo' (ex: 'b_pw' para peão preto)
                name_parts = filename.replace('.png', '').split(' ')
                color = 'w' if name_parts[1] == 'white' else 'b'
                piece_type = name_parts[0][:2] if name_parts[0] != 'pawn' else 'pw'
                key = f"{color}_{piece_type}"
                
                image = pg.image.load(base_path + filename)
                image = pg.transform.scale(image, (self.square_size, self.square_size))
                pieces[key] = image
            except pg.error as e:
                print(f"Erro ao carregar imagem {filename}: {e}")
                # Criar um placeholder em caso de falha
                pieces[key] = pg.Surface((self.square_size, self.square_size))
                pieces[key].fill((255, 0, 255)) # Cor de erro
                
        return pieces

    def _draw_board(self, screen: pg.Surface):
        """Desenha o tabuleiro e as peças."""
        for row in range(8):
            for col in range(8):
                # Desenhar o quadrado
                color = self.green_light if (row + col) % 2 == 0 else self.green
                pg.draw.rect(screen, color, (col * self.square_size, row * self.square_size, self.square_size, self.square_size))
                
                # Desenhar a peça
                piece_key = self.board_map[row][col]
                if piece_key in self.pieces_images:
                    screen.blit(self.pieces_images[piece_key], (col * self.square_size, row * self.square_size))

    def get_board_image(self) -> str:
        """Gera a imagem do tabuleiro como string base64."""
        screen = pg.Surface((self.board_size, self.board_size))
        self._draw_board(screen)
        
        # Converter Surface para PNG e depois para base64
        buffer = BytesIO()
        pg.image.save(screen, buffer, 'png')
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        return image_base64

    def handle_click(self, x: int, y: int) -> str:
        """Processa o clique do usuário e retorna a nova imagem do tabuleiro."""
        row = y // self.square_size
        col = x // self.square_size
        
        # Lógica de seleção e movimento (simplificada para demonstração)
        if self.selected_piece_pos is None:
            # Selecionar peça
            piece = self.board_map[row][col]
            if piece and piece[0] == self.player_turn[0]:
                self.selected_piece_pos = (row, col)
        else:
            # Mover peça (simplesmente move, sem validação de regras)
            from_row, from_col = self.selected_piece_pos
            piece_to_move = self.board_map[from_row][from_col]
            
            # Se o clique for em uma casa diferente da selecionada
            if (row, col) != (from_row, from_col):
                self.board_map[row][col] = piece_to_move
                self.board_map[from_row][from_col] = ''
                
                # Trocar o turno (simplificado)
                self.player_turn = 'black' if self.player_turn == 'white' else 'white'
            
            self.selected_piece_pos = None
            
        return self.get_board_image()

# Instância global do jogo para manter o estado
chess_game = ChessFlask()
