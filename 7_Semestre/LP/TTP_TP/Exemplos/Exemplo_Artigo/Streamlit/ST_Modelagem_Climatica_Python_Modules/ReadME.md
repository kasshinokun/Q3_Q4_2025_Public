# Análise Climática da América do Sul - Versão Modularizada (Streamlit)

Este projeto é uma aplicação Streamlit para análise de dados bioclimáticos do WorldClim para a América do Sul. O código original foi modularizado em classes para melhor organização, manutenibilidade e reutilização, seguindo as melhores práticas de desenvolvimento Python.

## Estrutura do Projeto

O projeto é composto pelos seguintes arquivos Python, cada um com uma responsabilidade clara:

| Arquivo | Descrição | Classe Principal |
| :--- | :--- | :--- |
| `main.py` | Ponto de entrada da aplicação Streamlit. Orquestra a interface do usuário e a interação entre as classes. | N/A |
| `data_processing.py` | Contém a lógica para download, descompactação, leitura de arquivos `.asc` e processamento dos dados WorldClim em um DataFrame. | `DataProcessor` |
| `modeling.py` | Contém a lógica para treinamento do modelo de Regressão Linear Múltipla e cálculo das métricas de avaliação. | `ClimateModel` |
| `visualization.py` | Contém as funções para gerar e exibir os gráficos (histogramas, dispersão, resíduos) e as métricas no Streamlit. | `Visualizer` |
| `requirements.txt` | Lista de dependências Python necessárias. | N/A |

## Estrutura de Classes

A modularização foi baseada nas seguintes classes, que encapsulam a lógica de negócio da aplicação:

### `DataProcessor` (em `data_processing.py`)

Gerencia todo o ciclo de vida dos dados, desde a aquisição até a preparação para a modelagem.

*   **Métodos Principais:**
    *   `download_and_process_data()`: Orquestra o download e a descompactação do arquivo ZIP do WorldClim.
    *   `process_worldclim_data()`: Converte os arquivos `.asc` em um `pandas.DataFrame` limpo, pronto para análise.

### `ClimateModel` (em `modeling.py`)

Responsável pela criação e avaliação do modelo estatístico.

*   **Método Principal:**
    *   `train_model(df_clean)`: Divide o DataFrame em conjuntos de treino e teste, treina um modelo de Regressão Linear Múltipla para prever a **Temperatura Média Anual (BIO1)** com base em **Precipitação Anual (BIO12)** e **Sazonalidade da Temperatura (BIO4)**, e retorna as métricas de avaliação.

### `Visualizer` (em `visualization.py`)

Trata da apresentação dos resultados e diagnósticos do modelo na interface do Streamlit.

*   **Métodos Principais:**
    *   `plot_data_distribution(df_clean)`: Gera visualizações exploratórias dos dados.
    *   `plot_model_diagnostics(y_test, predictions)`: Gera gráficos de diagnóstico do modelo (resíduos, real vs. predito).
    *   `display_metrics(metrics)`: Exibe as métricas de avaliação e a interpretação do modelo.

## Como Executar o Projeto

### Pré-requisitos

Você precisará ter o Python (versão 3.6+) instalado em seu sistema.

### 1. Instalação das Dependências

Após descompactar o arquivo, navegue até o diretório do projeto e instale as bibliotecas necessárias usando o `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 2. Execução da Aplicação

O projeto é uma aplicação Streamlit. Para iniciá-la, execute o seguinte comando no terminal:

```bash
streamlit run main.py
```

A aplicação será aberta automaticamente no seu navegador padrão.

### 3. Uso da Aplicação

1.  **Administração - Download e Processamento**: Comece nesta seção. Clique em **"Iniciar/Verificar Processamento de Dados"**. A aplicação fará o download dos dados climáticos do WorldClim (cerca de 100MB) e os processará.
2.  **Análise Estatística Exploratória**: Após o processamento, você pode visualizar uma amostra dos dados, estatísticas descritivas e a matriz de correlação.
3.  **Modelagem: Regressão Linear Múltipla**: Clique em **"Treinar Modelo"** para executar o modelo de regressão e ver as métricas de avaliação.
4.  **Visualização de Dados e Modelo**: Visualize os gráficos exploratórios e os diagnósticos do modelo treinado.
