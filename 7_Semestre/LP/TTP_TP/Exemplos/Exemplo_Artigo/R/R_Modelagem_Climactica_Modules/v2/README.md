# Projeto de Modelagem Climática Modularizada em R

## 🌎 Análise Climática da América do Sul com Shiny

Este projeto consiste em uma aplicação interativa desenvolvida em R com o framework Shiny, destinada à análise exploratória e modelagem climática da América do Sul, utilizando dados bioclimáticos do WorldClim. O código original foi modularizado para melhorar a organização, manutenção e legibilidade.

### 📂 Estrutura do Projeto Modularizado

O projeto foi dividido em quatro arquivos principais, cada um com responsabilidades bem definidas:

| Arquivo | Responsabilidade | Conteúdo Principal |
| :--- | :--- | :--- |
| `main.r` | **Aplicação Principal (Shiny)** | Contém a interface de usuário (`ui`), a lógica do servidor (`server`) e a execução da aplicação (`shinyApp`). Importa todas as funções dos outros módulos. |
| `data_processing.r` | **Processamento de Dados** | Funções para download, descompactação, leitura de arquivos `.asc`, limpeza de dados (remoção de valores `NODATA`) e funções de análise estatística exploratória (estatísticas descritivas e matriz de correlação). |
| `modeling.r` | **Modelagem Estatística** | Funções para divisão de dados (treino/teste), treinamento do modelo de regressão linear (`lm(bio1 ~ bio12)`) e cálculo das métricas de avaliação (R-quadrado, RMSE). |
| `visualization.r` | **Visualização de Dados** | Funções para geração de gráficos utilizando `ggplot2`, incluindo histogramas, gráficos de dispersão e gráficos de diagnóstico do modelo (resíduos e valores preditos vs. reais). |

### 🛠️ Pré-requisitos

Para executar a aplicação, você precisará ter o R instalado e os seguintes pacotes:

| Pacote | Função |
| :--- | :--- |
| `shiny` | Framework para a aplicação web interativa. |
| `dplyr` | Manipulação e transformação de dados. |
| `ggplot2` | Geração de gráficos. |
| `reshape2` | Transformação de dados (não essencial, mas usado internamente). |
| `corrplot` | Visualização da matriz de correlação. |
| `DT` | Exibição de tabelas interativas. |
| `rsample` | Divisão de dados em conjuntos de treino e teste. |
| `readr` | Leitura de dados (não essencial, mas usado internamente). |
| `shinythemes` | Temas visuais para a aplicação Shiny. |
| `shinycssloaders` | Indicadores de carregamento para elementos da UI. |

#### 1. Instalação dos Pacotes (Comum a todos os métodos)

Abra o console do R (ou o RStudio) e execute o seguinte comando para instalar todas as dependências:

```R
install.packages(c("shiny", "dplyr", "ggplot2", "reshape2", "corrplot", "DT", "rsample", "readr", "shinythemes", "shinycssloaders"))
```

### 🚀 Guia de Execução

Após a instalação dos pacotes, você pode executar o projeto de duas maneiras:

#### A. Execução via RStudio (Windows)

Este é o método mais simples e recomendado para usuários do RStudio.

1.  **Abra o RStudio.**
2.  **Abra o arquivo `main.r`** (File -> Open File...).
3.  **Clique no botão "Run App"** (localizado no canto superior direito da janela do editor de código).

A aplicação Shiny será iniciada em uma nova janela ou no painel de visualização do RStudio.

#### B. Execução via Linha de Comando (Windows/Linux)

Este método é útil para execução em servidores ou ambientes sem interface gráfica.

1.  **Navegue até o diretório do projeto** (onde estão os arquivos `.r`).

    ```bash
    cd /caminho/para/o/projeto
    ```

2.  **Execute o script `main.r`** usando o comando `Rscript`.

    ```bash
    # No Linux/macOS
    Rscript main.r
    
    # No Windows (pode ser necessário especificar o caminho completo para o Rscript.exe)
    "C:\Program Files\R\R-x.x.x\bin\Rscript.exe" main.r
    ```

    **Nota:** A execução de aplicações Shiny via `Rscript` na linha de comando pode exigir que o ambiente tenha as bibliotecas gráficas necessárias e pode não ser ideal para ambientes sem interface gráfica. Para execução em servidores, é mais comum usar o **Shiny Server**. No entanto, para um teste local simples, o `Rscript` deve funcionar.

### 📝 Observações

*   A primeira execução da aplicação exigirá o download de um arquivo ZIP de aproximadamente 100 MB do INPE (`http://www.dpi.inpe.br/amb_data/AmericaSul/SAmerica_WCLIM.zip`).
*   O download e o processamento dos dados são gerenciados na seção **"1. Administração - Download e Processamento"** da aplicação.
*   O modelo de regressão linear é simples (`BIO1 ~ BIO12`) e serve apenas como um exemplo didático de modelagem dentro do contexto da aplicação Shiny.

---
*Documento gerado por **Manus AI***
