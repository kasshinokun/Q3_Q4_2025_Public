# ♟️ Xadrez - Implementação com Pygame

Este projeto é uma implementação do clássico jogo de xadrez desenvolvida em Python utilizando a biblioteca Pygame para a interface gráfica e a lógica do jogo.

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](https://github.com/kasshinokun/Q3_Q4_2025_Public/blob/main/LICENSE.md) para detalhes.

## ✨ Funcionalidades

*   **Interface Gráfica:** Tabuleiro de xadrez interativo com peças carregadas a partir de arquivos PNG.
*   **Movimentação de Peças:** Lógica de movimentação para todas as peças (Peão, Torre, Cavalo, Bispo, Rainha e Rei).
*   **Regras Especiais:** Suporte para movimentos especiais como:
    *   Roque (Castling).
    *   Captura En Passant.
    *   Promoção de Peão (para Rainha).
*   **Controle de Turnos:** Alternância entre os turnos das peças brancas e pretas.
*   **Seleção e Destaque:** Destaque visual das casas para onde a peça selecionada pode se mover.

## 🛠️ Tecnologias Utilizadas

*   **Python 3.x**
*   **Pygame:** Biblioteca para desenvolvimento de jogos em Python, utilizada para renderização gráfica, manipulação de eventos e lógica do jogo.

## 🚀 Instalação

Para rodar este projeto, você precisará ter o Python instalado em seu sistema.

1.  **Baixe o Projeto:**
    Descompacte o arquivo `Xadrez.zip` em um diretório de sua preferência.

2.  **Instale a Dependência:**
    O projeto requer a biblioteca `pygame`. Instale-a usando o `pip`:
    ```bash
    pip install pygame
    ```

## 💻 Uso

Para iniciar o jogo, navegue até o diretório onde o arquivo `chess.py` está localizado e execute-o:

```bash
python Xadrez/chess.py
```
*(Nota: O arquivo principal do jogo está localizado dentro da pasta `Xadrez` que foi criada ao descompactar o ZIP.)*

## 📂 Estrutura do Projeto

O projeto é organizado da seguinte forma:

```
Xadrez/
├── chess.py            # Lógica principal do jogo e interface Pygame
├── bishop black.png    # Imagem do Bispo Preto
├── bishop white.png    # Imagem do Bispo Branco
├── king black.png      # Imagem do Rei Preto
├── king white.png      # Imagem do Rei Branco
├── knight black.png    # Imagem do Cavalo Preto
├── knight white.png    # Imagem do Cavalo Branco
├── pawn black.png      # Imagem do Peão Preto
├── pawn white.png      # Imagem do Peão Branco
├── queen black.png     # Imagem da Rainha Preta
├── queen white.png     # Imagem da Rainha Branca
├── rook black.png      # Imagem da Torre Preta
└── rook white.png      # Imagem da Torre Branca
```

---


