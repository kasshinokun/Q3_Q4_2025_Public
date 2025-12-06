# 📚 Repositório de Aplicações Flask – Python & JavaScript

Este repositório contém uma série de aplicações Flask desenvolvidas para demonstrar, na prática, os principais paradigmas e características avançadas do Python, bem como a integração com JavaScript em interfaces web modernas.

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](https://github.com/kasshinokun/Q3_Q4_2025_Public/blob/main/LICENSE.md) para detalhes.

## 👥 Autores

- [**Gabriel da Silva Cassino**](https://github.com/kasshinokun)

- [**Welbert Junio Afonso de Almeida** ](https://github.com/welbertalmeida)

**Professor:** Marco Rodrigo Costa  
**Instituição:** PUC Minas  
**Curso:** Engenharia de Computação / Ciência da Computação


## 🎯 Objetivo

Transformar relatórios técnicos em apresentações web interativas, aplicando conceitos como:

- **Programação Orientada a Objetos** (classes, herança, polimorfismo)
- **Programação Funcional** (decoradores, higher-order functions)
- **Características Avançadas do Python** (context managers, metaclasses, type hints, dataclasses)
- **Desenvolvimento Web com Flask** (APIs REST, templates Jinja2, design responsivo)

---

## 🚀 Aplicações Disponíveis

### 1. Apresentação Python & JavaScript

Uma aplicação monolítica em Flask que apresenta o conteúdo de um relatório sobre Python e JavaScript, com:

- Páginas interativas sobre histórico, paradigmas e exemplos de Python
- APIs JSON demonstrando funcionalidades avançadas
- Design responsivo com tema azul/amarelo (Python/JavaScript)

**🔗 Deploy:** [https://praticagraduacao.pythonanywhere.com/python](https://praticagraduacao.pythonanywhere.com/python)

### 2. Sistema de Apresentações Refatorado

Sistema modularizado para gerenciar múltiplas apresentações com Reveal.js:

- Arquitetura OO com classes base (`Presentation`, `Orchestrator`)
- Sidebar dinâmica com subtópicos sincronizados com os slides
- Suporte a múltiplas apresentações (ex.: Python vs R, Relatório TTP)
- CSS e JavaScript otimizados e centralizados

**🛠️ Estrutura:** Baseada em `Maestro` (conteúdo) e `Musician` (rotas), com templates reutilizáveis.

---

## ✅ Testes e Validações

Todos os endpoints foram testados com sucesso:

- ✅ Página inicial e navegação
- ✅ APIs JSON funcionais (`/api/python-features`, `/api/demo`)
- ✅ Design responsivo (mobile, tablet, desktop)
- ✅ Carregamento de templates e assets estáticos
- ✅ CORS habilitado para integração frontend/backend

---

## 🧠 Tecnologias Utilizadas

| Backend         | Frontend          | Ferramentas           |
|-----------------|-------------------|-----------------------|
| Flask           | HTML5 / CSS3      | Virtual Environment   |
| Jinja2          | JavaScript ES6+   | Type Hints            |
| Flask-CORS      | Reveal.js         | Git                   |
| Python 3.11+    | Prism.js          | PythonAnyWhere (Deploy)|

---

## 📁 Estrutura de Pastas (Projeto Principal)

```text
python_js_presentation/
├── src/
│   ├── models/           # Classes Python (POO)
│   ├── templates/        # Jinja2 com herança
│   ├── static/           # CSS, JS, imagens
│   └── main.py          # App Flask
├── requirements.txt
└── README.md
```
---

As aplicações demonstram na prática como Python pode ser utilizado de forma moderna e eficiente no desenvolvimento web, unindo backend robusto com frontend interativo e acessível.