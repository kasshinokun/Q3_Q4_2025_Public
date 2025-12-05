# --- main.r: Aplicação Principal Shiny ---

# Instale os pacotes necessários se ainda não estiverem instalados
# install.packages(c("shiny", "dplyr", "ggplot2", "reshape2", "corrplot", "DT", "rsample", "readr", "shinythemes", "shinycssloaders"))

library(shiny)
library(dplyr)
library(ggplot2)
library(reshape2)
library(corrplot)
library(DT)
library(rsample)
library(readr)
library(shinythemes)
library(shinycssloaders)

# --- Configurações Iniciais ---
DATA_DIR <- "r_climatica_data"
ZIP_URL <- "http://www.dpi.inpe.br/amb_data/AmericaSul/SAmerica_WCLIM.zip"
ZIP_FILENAME <- "SAmerica_WCLIM.zip"
LOG_FILE <- file.path(DATA_DIR, "model_creation.log")
DOWNLOAD_TIMEOUT_SECONDS <- 300

# --- Importação dos Módulos ---
source("data_processing.r")
source("modeling.r")
source("visualization.r")

# --- UI da Aplicação ---

ui <- fluidPage(
  theme = shinytheme("flatly"),
  titlePanel("🌎 Análise Climática da América do Sul"),
  sidebarLayout(
    sidebarPanel(
      width = 3,
      h4("Navegação"),
      radioButtons(
        "menu_selecao",
        "Selecione a seção:",
        choices = c(
          "1. Administração - Download e Processamento",
          "2. Análise Estatística Exploratória", 
          "3. Modelagem Simples: Regressão Linear",
          "4. Visualização de Dados e Modelo",
          "5. Referências"
        ),
        selected = "1. Administração - Download e Processamento"
      ),
      br(),
      hr(),
      h4("Status do Sistema"),
      uiOutput("status_sistema")
    ),
    mainPanel(
      width = 9,
      # UI 1: Administração
      conditionalPanel(
        condition = "input.menu_selecao == '1. Administração - Download e Processamento'",
        uiOutput("ui_administracao")
      ),
      # UI 2: Análise Estatística
      conditionalPanel(
        condition = "input.menu_selecao == '2. Análise Estatística Exploratória'",
        uiOutput("ui_analise_estatistica")
      ),
      # UI 3: Modelagem
      conditionalPanel(
        condition = "input.menu_selecao == '3. Modelagem Simples: Regressão Linear'",
        uiOutput("ui_modelagem")
      ),
      # UI 4: Visualização
      conditionalPanel(
        condition = "input.menu_selecao == '4. Visualização de Dados e Modelo'",
        uiOutput("ui_visualizacao")
      ),
      # UI 5: Referências
      conditionalPanel(
        condition = "input.menu_selecao == '5. Referências'",
        uiOutput("ui_referencias")
      )
    )
  )
)

# --- Servidor da Aplicação ---

server <- function(input, output, session) {
  
  # Reactive values para armazenar dados
  rv <- reactiveValues(
    df_clean = NULL,
    model = NULL,
    predictions = NULL,
    test_data = NULL,
    metrics = NULL,
    dados_processados = FALSE
  )
  
  # Status do sistema
  output$status_sistema <- renderUI({
    if (rv$dados_processados) {
      tagList(
        div(style = "color: green;", "✅ Dados Processados"),
        div(style = "font-size: 12px;", paste("📊", format(nrow(rv$df_clean), big.mark = ","), "pontos de dados"))
      )
    } else {
      div(style = "color: orange;", "⚠️ Aguardando Processamento")
    }
  })
  
  # UI 1: Administração
  output$ui_administracao <- renderUI({
    status <- check_data_status(DATA_DIR, ZIP_FILENAME, LOG_FILE)
    
    tagList(
      h2("📊 Administração - Download e Processamento de Dados"),
      p("Esta seção gerencia o download e processamento dos dados climáticos do WorldClim para a América do Sul."),
      p("Os dados serão baixados do INPE e processados para análise."),
      br(),
      
      if (status$model_created && validate_existing_model(DATA_DIR, LOG_FILE)) {
        tagList(
          div(style = "color: green; font-weight: bold;", "✅ Modelo e dados prontos para serem visualizados"),
          p("Os dados já foram processados e estão disponíveis para análise nas outras seções."),
          br(),
          actionButton("reprocessar_btn", "🔄 Reprocessar Dados", class = "btn-warning")
        )
      } else {
        tagList(
          div(style = "color: orange; font-weight: bold;", "⚠️ Dados não encontrados. É necessário processar os dados para continuar."),
          br(),
          actionButton("processar_btn", "🚀 Processar Dados", class = "btn-primary")
        )
      }
    )
  })
  
  # Processar dados quando botão for clicado
  observeEvent(input$processar_btn, {
    withProgress({
      setProgress(message = "Iniciando processamento...", value = 0.1)
      
      if (download_and_process_data(ZIP_URL, DATA_DIR, ZIP_FILENAME, LOG_FILE, DOWNLOAD_TIMEOUT_SECONDS)) {
        setProgress(message = "Processando dados climáticos...", value = 0.8)
        rv$df_clean <- process_worldclim_data(DATA_DIR)
        
        if (!is.null(rv$df_clean)) {
          rv$dados_processados <- TRUE
          showNotification("Dados processados com sucesso!", type = "message")
        } else {
          showNotification("Falha ao processar dados", type = "error")
        }
      }
    })
  })
  
  # Reprocessar dados
  observeEvent(input$reprocessar_btn, {
    # Remove diretório existente para forçar novo processamento
    if (dir.exists(DATA_DIR)) {
      unlink(DATA_DIR, recursive = TRUE)
    }
    rv$dados_processados <- FALSE
    rv$df_clean <- NULL
    rv$model <- NULL
    rv$predictions <- NULL
    rv$test_data <- NULL
    rv$metrics <- NULL
    
    # Força o re-render da UI de administração
    output$ui_administracao <- renderUI({
      status <- check_data_status(DATA_DIR, ZIP_FILENAME, LOG_FILE)
      
      tagList(
        h2("📊 Administração - Download e Processamento de Dados"),
        p("Esta seção gerencia o download e processamento dos dados climáticos do WorldClim para a América do Sul."),
        p("Os dados serão baixados do INPE e processados para análise."),
        br(),
        
        if (status$model_created && validate_existing_model(DATA_DIR, LOG_FILE)) {
          tagList(
            div(style = "color: green; font-weight: bold;", "✅ Modelo e dados prontos para serem visualizados"),
            p("Os dados já foram processados e estão disponíveis para análise nas outras seções."),
            br(),
            actionButton("reprocessar_btn", "🔄 Reprocessar Dados", class = "btn-warning")
          )
        } else {
          tagList(
            div(style = "color: orange; font-weight: bold;", "⚠️ Dados não encontrados. É necessário processar os dados para continuar."),
            br(),
            actionButton("processar_btn", "🚀 Processar Dados", class = "btn-primary")
          )
        }
      )
    })
  })
  
  # --- Lógica de Análise Estatística ---
  
  # Estatísticas Descritivas
  output$desc_stats <- DT::renderDataTable({
    req(rv$df_clean)
    render_desc_stats(rv$df_clean)
  })
  
  # Matriz de Correlação
  output$corr_plot <- renderPlot({
    req(rv$df_clean)
    render_corr_plot(rv$df_clean)
  })
  
  # UI 2: Análise Estatística
  output$ui_analise_estatistica <- renderUI({
    if (is.null(rv$df_clean)) {
      return(tags$div(
        style = "color: orange; font-weight: bold;",
        "⚠️ Por favor, processe os dados primeiro na seção 'Administração'."
      ))
    }
    
    tagList(
      h2("📈 Análise Estatística Exploratória"),
      
      h3("Visão Geral dos Dados"),
      p("Número total de pontos de grade válidos:", strong(format(nrow(rv$df_clean), big.mark = ","))),
      
      h3("Estatísticas Descritivas"),
      withSpinner(DT::dataTableOutput("desc_stats"), type = 4),
      
      h3("Análise de Correlação"),
      withSpinner(plotOutput("corr_plot", height = "600px"), type = 4)
    )
  })
  
  # --- Lógica de Modelagem ---
  
  # Treinamento do Modelo
  observeEvent(input$treinar_modelo_btn, {
    req(rv$df_clean)
    
    withProgress(message = 'Treinando modelo...', value = 0.1, {
      
      setProgress(detail = "Dividindo dados e ajustando o modelo...", value = 0.5)
      
      model_results <- train_linear_model(rv$df_clean)
      
      rv$model <- model_results$model
      rv$predictions <- model_results$predictions
      rv$test_data <- model_results$test_data
      rv$metrics <- model_results$metrics
      
      setProgress(detail = "Avaliação concluída.", value = 1.0)
      showNotification("Modelo treinado e avaliado com sucesso!", type = "message")
    })
  })
  
  # Resumo do Modelo
  output$model_summary <- renderPrint({
    req(rv$model)
    render_model_summary(rv$model)
  })
  
  # Métricas de Avaliação
  output$model_metrics <- renderUI({
    req(rv$metrics)
    render_model_metrics(rv$metrics)
  })
  
  # UI 3: Modelagem
  output$ui_modelagem <- renderUI({
    if (is.null(rv$df_clean)) {
      return(tags$div(
        style = "color: orange; font-weight: bold;",
        "⚠️ Por favor, processe os dados primeiro na seção 'Administração'."
      ))
    }
    
    tagList(
      h2("🔬 Modelagem Simples: Regressão Linear"),
      p("Esta seção treina um modelo de regressão linear simples para prever a Temperatura Média Anual (BIO1) com base na Precipitação Anual (BIO12)."),
      
      actionButton("treinar_modelo_btn", "⚙️ Treinar Modelo (BIO1 ~ BIO12)", class = "btn-success"),
      br(),
      br(),
      
      if (!is.null(rv$model)) {
        tagList(
          h3("Resumo do Modelo"),
          verbatimTextOutput("model_summary"),
          uiOutput("model_metrics")
        )
      } else {
        p("Clique no botão acima para treinar o modelo.")
      }
    )
  })
  
  # --- Lógica de Visualização ---
  
  # Histograma BIO1
  output$bio1_hist <- renderPlot({
    req(rv$df_clean)
    plot_bio1_hist(rv$df_clean)
  })
  
  # Dispersão BIO1 vs BIO12
  output$bio1_bio12_scatter <- renderPlot({
    req(rv$df_clean)
    plot_bio1_bio12_scatter(rv$df_clean)
  })
  
  # Gráfico de resíduos
  output$residuals_plot <- renderPlot({
    req(rv$model, rv$predictions, rv$test_data)
    plot_residuals(rv$predictions, rv$test_data)
  })
  
  # Valores reais vs preditos
  output$pred_vs_actual <- renderPlot({
    req(rv$model, rv$predictions, rv$test_data)
    plot_pred_vs_actual(rv$predictions, rv$test_data)
  })
  
  # UI 4: Visualização
  output$ui_visualizacao <- renderUI({
    if (is.null(rv$df_clean)) {
      return(tags$div(
        style = "color: orange; font-weight: bold;",
        "⚠️ Por favor, processe os dados primeiro na seção 'Administração'."
      ))
    }
    
    tagList(
      h2("🖼️ Visualização de Dados e Modelo"),
      
      h3("Visualização dos Dados"),
      fluidRow(
        column(6,
               h4("Distribuição de BIO1"),
               withSpinner(plotOutput("bio1_hist"), type = 4)
        ),
        column(6,
               h4("Relação entre BIO1 e BIO12"),
               withSpinner(plotOutput("bio1_bio12_scatter"), type = 4)
        )
      ),
      
      if (!is.null(rv$model)) {
        tagList(
          h3("Visualização do Modelo"),
          fluidRow(
            column(6,
                   h4("Distribuição dos Resíduos do Modelo"),
                   withSpinner(plotOutput("residuals_plot"), type = 4)
            ),
            column(6,
                   h4("Valores Reais vs Preditos"),
                   withSpinner(plotOutput("pred_vs_actual"), type = 4)
            )
          )
        )
      } else {
        p("Treine o modelo na seção 'Modelagem' para visualizar os resultados.")
      }
    )
  })
  
  # UI 5: Referências
  output$ui_referencias <- renderUI({
    tagList(
      h2("📚 Referências Bibliográficas"),
      
      h3("Base de Dados Utilizada"),
      
      p(strong("WorldClim - South America Climate Data")),
      p(strong("Fonte:"), "INPE (Instituto Nacional de Pesquisas Espaciais)"),
      p(strong("URL:"), a(ZIP_URL, href = ZIP_URL)),
      p(strong("Descrição:"), "Conjunto de dados bioclimáticos de alta resolução (1km) para a América do Sul, contendo 19 variáveis bioclimáticas derivadas de dados de temperatura e precipitação."),
      
      h3("Referências Bibliográficas"),
      
      tags$ol(
        tags$li(
          strong("Fick, S.E. & Hijmans, R.J. (2017)"),
          br(),
          em("WorldClim 2: new 1km spatial resolution climate surfaces for global land areas"),
          br(),
          "International Journal of Climatology"
        ),
        tags$li(
          strong("Wickham, H. & Grolemund, G. (2016)"),
          br(),
          em("R for Data Science"),
          br(),
          "O'Reilly Media"
        ),
        tags$li(
          strong("McKinney, W. (2017)"),
          br(),
          em("Python for Data Analysis"),
          br(),
          "O'Reilly Media"
        ),
        tags$li(
          strong("Chang, W. et al. (2023)"),
          br(),
          em("Shiny: Web Application Framework for R"),
          br(),
          a("https://shiny.rstudio.com", href = "https://shiny.rstudio.com")
        ),
        tags$li(
          strong("Van Rossum, G. (1995)"),
          br(),
          em("Python Tutorial"),
          br(),
          "Technical Report CS-R9526"
        ),
        tags$li(
          strong("Ihaka, R. & Gentleman, R. (1996)"),
          br(),
          em("R: A Language for Data Analysis and Graphics"),
          br(),
          "Journal of Computational and Graphical Statistics"
        )
      ),
      
      h3("Variáveis Bioclimáticas (BIO1-BIO19)"),
      
      p("As 19 variáveis bioclimáticas representam aspectos anuais e sazonais do clima:"),
      tags$ul(
        tags$li(strong("BIO1:"), "Temperatura média anual"),
        tags$li(strong("BIO2:"), "Variação média diurna"),
        tags$li(strong("BIO3:"), "Isotermalidade"),
        tags$li(strong("BIO4:"), "Sazonalidade da temperatura"),
        tags$li(strong("BIO5:"), "Temperatura máxima do mês mais quente"),
        tags$li(strong("BIO6:"), "Temperatura mínima do mês mais frio"),
        tags$li(strong("BIO7:"), "Amplitude térmica anual"),
        tags$li(strong("BIO12:"), "Precipitação anual"),
        tags$li(strong("BIO13:"), "Precipitação do mês mais úmido"),
        tags$li(strong("BIO14:"), "Precipitação do mês mais seco")
      )
    )
  })
}

# Executar aplicação
shinyApp(ui = ui, server = server)
