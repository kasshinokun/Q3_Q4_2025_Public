# Sistema de Apresentações Flask - Versão Refatorada

Sistema modularizado para gerenciamento de múltiplas apresentações com Reveal.js e Flask.

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](https://github.com/kasshinokun/Q3_Q4_2025_Public/blob/main/LICENSE.md) para detalhes.

## 👥 Autores

- [**Gabriel da Silva Cassino**](https://github.com/kasshinokun)

- [**Welbert Junio Afonso de Almeida** ](https://github.com/welbertalmeida)

**Professor:** Marco Rodrigo Costa  
**Instituição:** PUC Minas  
**Curso:** Engenharia de Computação / Ciência da Computação

## 🏗️ Arquitetura

O sistema utiliza uma arquitetura orientada a objetos com herança e separação de responsabilidades:

### 1. **Presentation** (Classe Base)
- Define a estrutura comum para todas as apresentações
- Gerencia contexto e renderização de templates
- Localização: `core/presentation.py`

### 2. **Orchestrator** (Classe Seletora de Views)
- Registra e gerencia apresentações disponíveis
- Fornece lista de apresentações para UI
- Localização: `core/presentation.py`

### 3. **Maestro_TTP e Maestro_Artigo** (Classes Subordinadas)
- Herdam de `Presentation`
- Implementam estrutura de navegação específica
- Definem título, template e conteúdo
- Localização: `core/maestro.py`

### 4. **Musician_TTP e Musician_Artigo** (Classes Seletoras de Rotas)
- Fazem request do render através do Orchestrator
- Servem como camada entre rotas Flask e apresentações
- Localização: `core/musician.py`

## 📁 Estrutura de Diretórios

```
flask_presentation_refactored/
├── app.py                          # Aplicação Flask principal
├── requirements.txt                # Dependências Python
├── README.md                       # Documentação
├── core/                           # Módulo principal
│   ├── __init__.py
│   ├── presentation.py             # Presentation + Orchestrator
│   ├── maestro.py                  # Maestro_TTP + Maestro_Artigo
│   └── musician.py                 # Musician_TTP + Musician_Artigo
├── routes/                         # Rotas Flask
│   ├── __init__.py
│   └── routes.py                   # Blueprint com rotas
├── templates/                      # Templates Jinja2
│   ├── base/
│   │   └── layout.html             # Template base com sidebar e dropdown
│   ├── ttp/
│   │   └── python_presentation.html
│   └── artigo/
│       └── article_presentation.html
└── static/                         # Arquivos estáticos
    ├── css/
    │   └── style.css               # CSS otimizado
    ├── js/
    │   └── script.js               # JavaScript otimizado
    └── images/                     # Imagens das apresentações
```

## 🚀 Instalação e Execução

### 1. Instalar Dependências

```bash
cd flask_presentation_refactored
pip install -r requirements.txt
```

### 2. Executar Aplicação

```bash
python app.py
```

### 3. Acessar no Navegador

- **URL Principal:** http://localhost:5000
- **Health Check:** http://localhost:5000/health

## 🎯 Funcionalidades Implementadas

### ✅ Correções Realizadas

1. **Menu Sidebar com Subtópicos**
   - Estrutura hierárquica dinâmica
   - Submenus expansíveis com animação
   - Sincronização com slides do Reveal.js

2. **Troca de Apresentações**
   - Dropdown funcional com links dinâmicos
   - Integração com rotas Flask via `url_for()`
   - Marcação visual da apresentação ativa

3. **CSS Modularizado**
   - Removido CSS inline dos templates
   - Design system com variáveis CSS
   - Responsivo e acessível

4. **JavaScript Otimizado**
   - Lógica centralizada em arquivo único
   - Event listeners eficientes
   - Sincronização automática de navegação

### 🎨 Melhorias de UI/UX

1. **Design Moderno**
   - Gradientes e sombras suaves
   - Animações e transições fluidas
   - Paleta de cores consistente

2. **Responsividade**
   - Adaptação para mobile, tablet e desktop
   - Sidebar colapsável em telas pequenas
   - Layout flexível com Grid CSS

3. **Acessibilidade**
   - Focus visible para navegação por teclado
   - Suporte a `prefers-reduced-motion`
   - Contraste adequado de cores

4. **Interatividade**
   - Hover effects em cards e links
   - Feedback visual em todas as ações
   - Atalhos de teclado (pressione 'S' para toggle da sidebar)

## 🔧 Rotas Disponíveis

| Rota | Descrição | Classe Responsável |
|------|-----------|-------------------|
| `/` | Redireciona para apresentação TTP | - |
| `/python_presentation` | Apresentação sobre Python | Musician_TTP |
| `/python_r_comparative` | Apresentação Python vs R | Musician_Artigo |
| `/health` | Health check da aplicação | - |

## 📝 Como Adicionar Nova Apresentação

### 1. Criar Classe Maestro

```python
# core/maestro.py
class Maestro_NovaApresentacao(Presentation):
    KEY = 'nova'
    TITLE = '🎯 Nova Apresentação'
    TEMPLATE_PATH = 'nova/apresentacao.html'
    
    def get_navigation_structure(self):
        return [
            {'id': 'intro', 'title': '1. Introdução', 'has_submenu': False},
            # ... mais itens
        ]

# Registrar no Orchestrator
Orchestrator.register_presentation(Maestro_NovaApresentacao)
```

### 2. Criar Classe Musician

```python
# core/musician.py
class Musician_NovaApresentacao:
    @staticmethod
    def render_presentation():
        maestro = Orchestrator.get_presentation('nova')
        if maestro:
            return maestro.render()
        return Response("Apresentação não encontrada", status=404)
```

### 3. Adicionar Rota

```python
# routes/routes.py
@main_bp.route('/nova_apresentacao')
def nova_apresentacao():
    return Musician_NovaApresentacao.render_presentation()
```

### 4. Criar Template

```html
<!-- templates/nova/apresentacao.html -->
{% extends "base/layout.html" %}

{% block slides %}
<section id="intro">
    <h2>Introdução</h2>
    <p>Conteúdo da apresentação...</p>
</section>
{% endblock %}
```

## 🎓 Tecnologias Utilizadas

- **Backend:** Flask 3.0
- **Frontend:** Reveal.js 4.5
- **Template Engine:** Jinja2
- **CSS:** CSS3 com variáveis e Grid Layout
- **JavaScript:** ES6+ com event listeners modernos

## 📊 Apresentações Disponíveis

### 1. 🐍 Relatório sobre Python
- História e evolução do Python
- Características e paradigmas
- Aplicações e ecossistema
- Exemplos práticos

### 2. 📈 Python e R na Análise de Precipitação
- Análise climática em Rondônia
- Comparação Python vs R
- Metodologia e resultados
- Referências científicas

## 🔑 Atalhos de Teclado

| Tecla | Ação |
|-------|------|
| `S` | Toggle da sidebar |
| `←` `→` | Navegar entre slides |
| `ESC` | Visão geral dos slides |
| `F` | Fullscreen |
| `?` | Ajuda do Reveal.js |


