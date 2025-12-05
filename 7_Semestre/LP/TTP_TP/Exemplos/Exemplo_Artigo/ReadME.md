# 🌎 Projeto de Modelagem Climática e Aplicações Interativas

Este repositório contém o código-fonte e os dados de exemplo para um projeto de análise e modelagem climática, com foco na modularização do código em diferentes linguagens (R e Python/Streamlit) para fins de comparação e melhoria da manutenibilidade. O projeto utiliza dados bioclimáticos do WorldClim para a região da América do Sul.

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](https://github.com/kasshinokun/Q3_Q4_2025_Public/blob/main/LICENSE.md) para detalhes.

## 🌟 Destaques do Projeto

O projeto é dividido em duas grandes seções, cada uma com abordagens distintas para a modelagem climática:

1.  **Modelagem Climática em R (Shiny):** Uma aplicação interativa desenvolvida em R com o framework Shiny, destinada à análise exploratória e modelagem climática. O código foi modularizado para melhor organização e legibilidade.
2.  **Modelagem Climática em Python (Streamlit):** Uma implementação equivalente em Python, utilizando o framework Streamlit para a criação de uma aplicação web interativa.

## 📂 Estrutura do Repositório

O repositório está organizado da seguinte forma:

| Diretório | Descrição |
| :--- | :--- |
| `R/` | Contém o código-fonte em R, incluindo versões monolíticas e modularizadas da aplicação Shiny. |
| `Streamlit/` | Contém o código-fonte em Python, incluindo a aplicação Streamlit modularizada e monolítica. |

### 🔬 Modelagem em R (Shiny)

A versão em R utiliza o framework Shiny para criar uma aplicação web interativa. A estrutura modularizada (`R/R_Modelagem_Climactica_Modules/v2/`) é composta por:

| Arquivo | Responsabilidade |
| :--- | :--- |
| `main.r` | **Aplicação Principal (Shiny)**: Interface de usuário (`ui`), lógica do servidor (`server`) e execução. |
| `data_processing.r` | **Processamento de Dados**: Funções para download, limpeza e análise estatística exploratória. |
| `modeling.r` | **Modelagem Estatística**: Funções para divisão de dados e treinamento de modelo de regressão linear (`lm(bio1 ~ bio12)`). |
| `visualization.r` | **Visualização de Dados**: Funções para geração de gráficos (`ggplot2`). |

### 🐍 Modelagem em Python (Streamlit)

A versão em Python utiliza o Streamlit para a aplicação web. A estrutura modularizada (`Streamlit/ST_Modelagem_Climatica_Python_Modules/`) é composta por:

| Arquivo | Responsabilidade |
| :--- | :--- |
| `main.py` | **Aplicação Principal (Streamlit)**: Ponto de entrada e orquestração dos módulos. |
| `data_processing.py` | **Processamento de Dados**: Funções de manipulação e limpeza de dados. |
| `modeling.py` | **Modelagem Estatística**: Funções de treinamento e avaliação de modelos. |
| `visualization.py` | **Visualização de Dados**: Funções para geração de gráficos. |
| `requirements.txt` | Lista de dependências Python necessárias. |

## 🛠️ Pré-requisitos e Instalação

### Para a Aplicação R (Shiny)

1.  Instale o **R** e o **RStudio** (recomendado).
2.  Instale os pacotes R necessários no console:
    ```R
    install.packages(c("shiny", "dplyr", "ggplot2", "reshape2", "corrplot", "DT", "rsample", "readr", "shinythemes", "shinycssloaders"))
    ```
3.  Execute a aplicação abrindo o arquivo `R/R_Modelagem_Climactica_Modules/v2/main.r` no RStudio e clicando em **"Run App"**.

### Para a Aplicação Python (Streamlit)

1.  Instale o **Python 3.x**.
2.  Instale as dependências usando o arquivo `requirements.txt`:
    ```bash
    pip install -r Streamlit/ST_Modelagem_Climatica_Python_Modules/requirements.txt
    ```
3.  Execute a aplicação Streamlit:
    ```bash
    streamlit run Streamlit/ST_Modelagem_Climatica_Python_Modules/main.py
    ```




