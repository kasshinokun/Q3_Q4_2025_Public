## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](https://github.com/kasshinokun/Q3_Q4_2025_Public/blob/main/LICENSE.md) para detalhes.

# 📦 Problemas de Otimização 3D - PyQt5

Este projeto implementa uma aplicação gráfica interativa para visualizar e resolver três problemas clássicos de otimização 3D usando **PyQt5** e **OpenGL**.

## 🚀 Funcionalidades

A aplicação inclui três tipos de problemas de otimização:

1. **Bin Packing 3D** - Empacotamento estático de caixas em um container
2. **Dynamic Bin Packing 3D** - Empacotamento dinâmico com chegada e saída de itens
3. **Knapsack 3D** - Problema da mochila tridimensional com programação dinâmica

## 📋 Pré-requisitos

### Python 3.7 ou superior
Verifique sua versão:
```bash
python --version
```

### Dependências do sistema (Linux/Ubuntu)
```bash
sudo apt-get update
sudo apt-get install python3-pip python3-pyqt5 python3-opengl
```

### Dependências do sistema (Windows)
- Instale o Python 3.7+ do [python.org](https://www.python.org/)
- Certifique-se de marcar "Add Python to PATH" durante a instalação

## 📦 Instalação das Dependências Python

### Método 1: Usando requirements.txt (Recomendado)

1. Crie um arquivo `requirements.txt` com o seguinte conteúdo:
```txt
PyQt5==5.15.9
numpy==1.24.3
pyopengl==3.1.7
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

### Método 2: Instalação manual
```bash
pip install PyQt5 numpy pyopengl
```

## 🎮 Como Executar

### 1. Clone ou baixe o projeto
```bash
git clone [seu-repositorio]
cd [pasta-do-projeto]
```

### 2. Execute o script principal
```bash
python Quadrado_PyQt5_v6.py
```

### 3. Ou execute diretamente (se já estiver na pasta)
```bash
python3 Quadrado_PyQt5_v6.py
```

## 🖥️ Estrutura da Interface

A aplicação possui uma interface dividida em duas partes principais:

### **Painel Esquerdo** - Controles
- **Seletor de Problema**: Abas para escolher entre os três problemas
- **Configurações**: Parâmetros específicos de cada problema
- **Controles de Câmera**: Rotação e zoom da visualização 3D
- **Dicas de Navegação**: Instruções para interagir com a cena

### **Painel Direito** - Visualização 3D
- Renderização OpenGL dos objetos e containers
- Navegação interativa com mouse
- Cores diferenciadas para cada item

## 🎯 Como Usar

### Para Bin Packing 3D:
1. Selecione a aba "Bin Packing"
2. Configure as dimensões do container
3. Defina a quantidade e tamanho dos objetos
4. Clique em "Gerar Objetos Aleatórios"
5. Arraste com o mouse para rotacionar a cena

### Para Dynamic Bin Packing:
1. Selecione a aba "Dynamic Packing"
2. Configure as durações mínima e máxima
3. Ajuste a velocidade da simulação
4. Clique em "Iniciar Simulação"
5. Observe os itens chegando e saindo dinamicamente

### Para Knapsack 3D:
1. Selecione a aba "Knapsack"
2. Defina a capacidade da mochila
3. Configure o número e valor dos itens
4. Clique em "Resolver Knapsack"
5. Veja os itens selecionados otimamente

## 🎮 Controles de Câmera

- **Arraste com o botão esquerdo**: Rotacionar a cena
- **Roda do mouse**: Zoom in/out
- **Checkboxes**: Ativar rotação automática nos eixos X/Y
- **Sliders**: Ajuste manual da rotação e zoom

## 🔧 Solução de Problemas

### Erro: "No module named 'PyQt5'"
```bash
pip install --upgrade pip
pip install PyQt5
```

### Erro: "OpenGL.GL not found"
```bash
pip install PyOpenGL PyOpenGL_accelerate
```

### Erro: "Could not find Qt platform plugin"
(Windows) Instale os pacotes de runtime do Visual Studio:
- Baixe e instale o [Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)

### Performance lenta
- Reduza o número de objetos nas configurações
- Feche outros aplicativos pesados
- Use valores menores para as dimensões do container

## 🎨 Paleta de Cores

O projeto utiliza uma paleta de 34 cores pré-definidas para diferenciar os itens, incluindo:
- **Preto (#000000)**: Para as linhas do container
- **Branco (#FFFFFF)**: Para o fundo
- 32 cores vibrantes para os objetos 3D

## 📊 Algoritmos Implementados

1. **Bin Packing**: First-Fit algorithm para colocação de itens
2. **Dynamic Packing**: Sistema de chegada/saída com First-Fit
3. **Knapsack**: Programação dinâmica 4D para otimização

## 🗂️ Estrutura do Código

```
Quadrado_PyQt5_v6.py
├── Classes principais
│   ├── BinPacking3D (empacotamento estático)
│   ├── DynamicBinPacking3D (empacotamento dinâmico)
│   ├── Knapsack3D (problema da mochila)
│   └── OpenGL3DViewer (visualizador OpenGL)
├── Funções auxiliares
│   └── hex_to_rgb (conversão de cores)
├── Interface gráfica
│   └── MainWindow (janela principal PyQt5)
└── Execução principal
```

## 💡 Dicas para Desenvolvedores

### Modificando as cores:
- A paleta de cores está definida em `vector_cores_hex`
- Use a função `hex_to_rgb()` para converter cores hexadecimais

### Adicionando novos algoritmos:
1. Crie uma nova classe herdando de `BinPacking3D`
2. Implemente o método de colocação específico
3. Adicione uma nova aba na interface
4. Implemente a função de desenho no visualizador

### Testando com dados específicos:
```python
# Exemplo: Adicionar item manualmente no Bin Packing
packer = BinPacking3D(20, 20, 20)
packer.add_item(5, 3, 4)  # Largura, Altura, Profundidade
```

## 📝 Licença

Este projeto é para fins educacionais. Sinta-se à vontade para modificar e distribuir.

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📧 Suporte

Para problemas ou dúvidas:
1. Verifique a seção "Solução de Problemas"
2. Consulte a documentação do PyQt5 e OpenGL
3. Abra uma issue no repositório do projeto

---

**Divirta-se explorando os problemas de otimização 3D!** 🎮📦
