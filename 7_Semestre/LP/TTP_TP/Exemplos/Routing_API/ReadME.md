# 🗺️ API de Roteamento e Otimização Geográfica

Este repositório contém o código-fonte para uma API de roteamento e otimização geográfica desenvolvida em **Python** utilizando o framework **Flask**. A API oferece endpoints para gerenciamento de dados geográficos (cidades) e para a execução de algoritmos de otimização de rotas, como o algoritmo de Dijkstra, K-means para agrupamento e o problema do Caixeiro Viajante (TSP) usando o algoritmo do vizinho mais próximo.

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](https://github.com/kasshinokun/Q3_Q4_2025_Public/blob/main/LICENSE.md) para detalhes.

## ✨ Funcionalidades Principais

A API é estruturada em torno de dois conjuntos principais de funcionalidades:

1.  **Gerenciamento de Cidades:** Permite a listagem de todas as cidades e a busca por cidades dentro de uma região delimitada (bounding box) utilizando uma estrutura de dados **Quadtree** para otimização espacial.
2.  **Otimização de Rotas:** Implementa algoritmos clássicos de otimização para resolver problemas de caminho mais curto e agrupamento geográfico.

## ⚙️ Estrutura do Projeto

O projeto é composto pela API Flask de roteamento e por uma aplicação Streamlit para roteamento hierárquico global.

| Arquivo/Diretório | Descrição |
| :--- | :--- |
| `Flask/v2a/` | Contém o código-fonte da API de Roteamento (Flask). |
| `app_graphos_alpha.py` | Aplicação Streamlit para Roteamento Hierárquico Global Otimizado. |

### 🌐 Aplicação Interativa Streamlit: Roteamento Hierárquico Global

A aplicação `app_graphos_alpha.py` é um sistema de roteamento global otimizado, desenvolvido em Streamlit, que implementa uma lógica de busca de caminho hierárquica e eficiente.

**Título:** 🌍 Sistema de Roteamento Hierárquico Global Otimizado
**Complexidade:** O(log m * n) → O(1) - 7 Níveis Hierárquicos com Cache e Índices

**Funcionalidades:**
*   **Roteamento Hierárquico:** Utiliza 7 níveis de hierarquia (cidade, município, estado, país, bloco regional, continente, global) para otimizar a busca de rotas.
*   **Otimização de Performance:** Implementa cache (`lru_cache`) para distâncias e rotas, além de pré-computação de distâncias entre cidades próximas, visando uma complexidade de busca próxima a O(1).
*   **Estrutura de Dados:** Utiliza um banco de dados SQLite (`global_hierarchical_router_optimized.db`) com tabelas e índices otimizados para a estrutura hierárquica.
*   **Visualização:** Integração com Plotly para visualização interativa de dados e rotas.

## 🚀 Endpoints da API

O projeto está organizado na seguinte estrutura:

```
Flask/
└── v2a/
    ├── main.py
    ├── quadtree_logic.py
    ├── routing_algorithms.py
    ├── models/
    │   └── user.py
    ├── routes/
    │   ├── routing.py
    │   └── user.py
    └── database/
        └── app.db
```

| Arquivo/Diretório | Descrição |
| :--- | :--- |
| `main.py` | Ponto de entrada da aplicação Flask. Configura a aplicação, o banco de dados (SQLite) e registra os *blueprints* de rotas. |
| `routes/routing.py` | Define os endpoints da API de roteamento e otimização. |
| `routing_algorithms.py` | Contém as implementações dos algoritmos de roteamento (Dijkstra, K-means, TSP). |
| `quadtree_logic.py` | Implementa a lógica da estrutura de dados Quadtree para consultas espaciais eficientes. |
| `models/user.py` | Define o modelo de dados para o usuário (embora o foco principal seja o roteamento). |
| `database/app.db` | Arquivo do banco de dados SQLite utilizado pela aplicação. |

## 🚀 Endpoints da API

A API expõe os seguintes endpoints principais sob o prefixo `/api`:

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `GET` | `/api/routing/cities` | Retorna a lista de todas as cidades disponíveis no banco de dados. |
| `POST` | `/api/routing/cities/search` | Busca cidades dentro de uma caixa delimitadora (`min_lat`, `max_lat`, `min_lon`, `max_lon`) usando Quadtree. |
| `POST` | `/api/routing/route/dijkstra` | Calcula a rota mais curta entre duas cidades (`start_city_id`, `end_city_id`) usando o algoritmo de Dijkstra. |
| `POST` | `/api/routing/route/kmeans` | Agrupa um conjunto de cidades (`city_ids`) em `num_clusters` usando o algoritmo K-means. |
| `POST` | `/api/routing/route/tsp` | Calcula uma rota otimizada para o problema do Caixeiro Viajante (TSP) para um conjunto de cidades (`city_ids`) usando o algoritmo do vizinho mais próximo. |

## 🛠️ Pré-requisitos e Instalação

### Pré-requisitos

*   Python 3.x
*   **Para a API Flask:** Flask, Flask-SQLAlchemy, e bibliotecas para algoritmos de roteamento (inferidas pelo código).
*   **Para a Aplicação Streamlit:** streamlit, pandas, sqlite3, plotly, numpy, requests, pygwalker (inferidas pelo código).

### Instalação

1.  **Clone o repositório** (ou descompacte o arquivo fornecido).

#### 1. API de Roteamento (Flask)

1.  **Navegue até o diretório da API** (`Flask/v2a/`).
2.  **Instale as dependências** (as dependências exatas devem ser verificadas, mas as principais são):
    ```bash
    pip install Flask Flask-SQLAlchemy
    ```
3.  **Execute a API:**
    ```bash
    python main.py
    ```
    A API será iniciada em `http://0.0.0.0:5000`.

#### 2. Aplicação Streamlit (Roteamento Hierárquico)

1.  **Instale as dependências** (as dependências exatas devem ser verificadas, mas as principais são):
    ```bash
    pip install streamlit pandas plotly numpy requests pygwalker
    ```
2.  **Execute a aplicação:**
    ```bash
    streamlit run app_graphos_alpha.py
    ```
    A aplicação será aberta no seu navegador. Na primeira execução, ela fará o download dos dados globais e construirá o banco de dados hierárquico otimizado.

A aplicação será iniciada em `http://0.0.0.0:8501`.


---

