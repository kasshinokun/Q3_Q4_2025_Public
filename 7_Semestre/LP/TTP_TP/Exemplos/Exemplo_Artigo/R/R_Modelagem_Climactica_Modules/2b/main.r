# main.R

#' @title Aplicação Principal de Análise Climática
#' @description Interface Shiny para análise de dados climáticos da América do Sul

# Carregar bibliotecas
library(shiny)
library(shinythemes)
library(shinycssloaders)
library(DT)

# Carregar módulos
source("data_processing.R")
source("modeling.R")
source("visualization.R")

# UI da Aplicação
ui <- fluidPage(
  theme = shinytheme("flatly"),
  titlePanel("🌎 Análise Climática da América do Sul - Versão Modularizada"),
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
          "3. Modelagem: Regressão Linear",
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
        condition = "input.menu_selecao == '3. Modelagem: Regressão Linear'",
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

# Servidor da Aplicação
server <- function(input, output, session) {
  
  # Reactive values para armazenar dados
  rv <- reactiveValues(
    df_clean = NULL,
    model_result = NULL,
    dados_processados = FALSE,
    stats = NULL,
    corr_matrix = NULL,
    download_timeout = DOWNLOAD_TIMEOUT
  )
  
  # Status do sistema
  output$status_sistema <- renderUI({
    if (rv$dados_processados) {
      tagList(
        div(style = "color: green;", "✅ Dados Processados"),
        div(style = "font-size: 12px;", 
            paste("📊", format(nrow(rv$df_clean), big.mark = ","), "pontos de dados")),
        div(style = "font-size: 12px;", 
            paste("📁 Diretório:", DATA_DIR)),
        div(style = "font-size: 12px; color: gray;", 
            paste("⏱️ Timeout:", rv$download_timeout, "segundos"))
      )
    } else {
      tagList(
        div(style = "color: orange;", "⚠️ Aguardando Processamento"),
        div(style = "font-size: 12px;", 
            paste("📁 Diretório:", DATA_DIR)),
        div(style = "font-size: 12px; color: gray;", 
            paste("⏱️ Timeout configurado:", rv$download_timeout, "segundos"))
      )
    }
  })
  
  # UI 1: Administração
  output$ui_administracao <- renderUI({
    status <- check_data_status()
    
    tagList(
      h2("📊 Administração - Download e Processamento de Dados"),
      p("Esta seção gerencia o download e processamento dos dados climáticos do WorldClim para a América do Sul."),
      p("Os dados serão baixados do INPE e processados para análise."),
      
      fluidRow(
        column(6,
               div(class = "well",
                   h4("📋 Status do Sistema"),
                   tags$ul(
                     tags$li(paste("Diretório:", DATA_DIR)),
                     tags$li(paste("Arquivo ZIP:", ifelse(status$zip_exists, "✅ Existe", "❌ Não existe"))),
                     tags$li(paste("Modelo processado:", ifelse(status$model_created, "✅ Sim", "❌ Não"))),
                     tags$li(paste("Timeout download:", rv$download_timeout, "segundos")),
                     tags$li(paste("URL fonte:", ZIP_URL))
                   )
               )
        ),
        column(6,
               div(class = "well",
                   h4("⚙️ Configurações"),
                   numericInput("timeout_input", "Timeout (segundos):", 
                               value = rv$download_timeout, min = 30, max = 600, step = 30),
                   actionButton("update_timeout", "🔄 Atualizar Timeout", class = "btn-info btn-sm"),
                   hr(),
                   p(strong("Instruções:")),
                   tags$ul(
                     tags$li("1. O sistema verificará se o arquivo ZIP já existe em", tags$code(DATA_DIR)),
                     tags$li("2. Se não existir, fará o download automaticamente"),
                     tags$li("3. O timeout padrão é de 5 minutos (300 segundos)"),
                     tags$li("4. Ajuste o timeout se sua conexão for lenta")
                   )
               )
        )
      ),
      
      br(),
      
      if (status$model_created && validate_existing_model()) {
        tagList(
          div(style = "color: green; font-weight: bold; padding: 15px; border: 2px solid green; border-radius: 5px; background-color: #f0fff0;", 
              icon("check-circle"), 
              "✅ Dados já processados e válidos!"),
          p("Os dados climáticos já estão disponíveis para análise nas outras seções."),
          br(),
          actionButton("reprocessar_btn", "🔄 Reprocessar Dados", 
                      class = "btn-warning", width = "100%",
                      onclick = "return confirm('Isso removerá os dados existentes. Continuar?')")
        )
      } else {
        tagList(
          div(style = "color: orange; font-weight: bold; padding: 15px; border: 2px solid orange; border-radius: 5px; background-color: #fffaf0;", 
              icon("exclamation-triangle"), 
              "⚠️ Dados não encontrados ou incompletos"),
          p("É necessário processar os dados para continuar com a análise."),
          br(),
          actionButton("processar_btn", "🚀 Iniciar Processamento", 
                      class = "btn-primary btn-lg", width = "100%")
        )
      }
    )
  })
  
  # Atualizar timeout
  observeEvent(input$update_timeout, {
    new_timeout <- input$timeout_input
    if (new_timeout >= 30 && new_timeout <= 600) {
      rv$download_timeout <- new_timeout
      showNotification(paste("Timeout atualizado para", new_timeout, "segundos"), 
                      type = "success", duration = 3)
    } else {
      showNotification("Timeout deve estar entre 30 e 600 segundos", 
                      type = "warning", duration = 5)
    }
  })
  
  # Processar dados quando botão for clicado
  observeEvent(input$processar_btn, {
    
    # Mostrar informações sobre o processamento
    showModal(modalDialog(
      title = tags$h3(icon("gears"), "Processamento em Andamento"),
      tags$div(
        tags$p(icon("info-circle"), "Por favor, aguarde enquanto o sistema:"),
        tags$ol(
          tags$li("Verifica se o arquivo ZIP existe em", tags$code(DATA_DIR)),
          tags$li("Faz o download se necessário (pode levar alguns minutos)"),
          tags$li("Descompacta os arquivos"),
          tags$li("Processa os dados climáticos")
        ),
        tags$hr(),
        tags$p(strong("Configurações atuais:")),
        tags$ul(
          tags$li(paste("Timeout:", rv$download_timeout, "segundos")),
          tags$li(paste("Diretório:", DATA_DIR)),
          tags$li(paste("URL:", ZIP_URL))
        ),
        tags$p(em("Esta janela fechará automaticamente quando o processamento concluir."))
      ),
      footer = NULL,
      size = "m",
      easyClose = FALSE
    ))
    
    withProgress({
      setProgress(message = "Verificando dados existentes...", value = 0.1)
      
      # Passar o timeout atualizado para a função
      current_timeout <- rv$download_timeout
      
      setProgress(message = paste("Processando com timeout de", current_timeout, "segundos..."), 
                 value = 0.2)
      
      # Download e processamento
      download_success <- download_and_process_data(timeout = current_timeout)
      
      if (download_success) {
        setProgress(message = "Processando dados climáticos...", value = 0.7)
        rv$df_clean <- process_worldclim_data()
        
        if (!is.null(rv$df_clean)) {
          rv$dados_processados <- TRUE
          
          # Calcular estatísticas e correlação
          setProgress(message = "Calculando estatísticas...", value = 0.85)
          rv$stats <- calculate_descriptive_stats(rv$df_clean)
          rv$corr_matrix <- calculate_correlation_matrix(rv$df_clean)
          
          setProgress(value = 1.0)
          
          removeModal()
          showNotification(
            tags$div(
              icon("check-circle"), 
              tags$span(style = "font-weight: bold;", "✅ Processamento concluído com sucesso!"),
              tags$br(),
              tags$span(paste("📊", format(nrow(rv$df_clean), big.mark = ","), 
                             "pontos de dados processados"))
            ),
            type = "success", 
            duration = 10
          )
        } else {
          removeModal()
          showNotification(
            tags$div(
              icon("exclamation-triangle"),
              tags$span(style = "font-weight: bold;", "❌ Falha ao processar dados")
            ),
            type = "error",
            duration = 10
          )
        }
      } else {
        removeModal()
        showNotification(
          tags$div(
            icon("exclamation-triangle"),
            tags$span(style = "font-weight: bold;", "❌ Falha no download/processamento"),
            tags$br(),
            tags$span("Verifique sua conexão com a internet e tente novamente.")
          ),
          type = "error",
          duration = 10
        )
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
    rv$model_result <- NULL
    rv$stats <- NULL
    rv$corr_matrix <- NULL
    
    showNotification("Dados removidos. Clique em 'Iniciar Processamento' para recomeçar.", 
                    type = "warning", duration = 5)
  })
  
  # --- UI 2: Análise Estatística ---
  output$ui_analise_estatistica <- renderUI({
    if (is.null(rv$df_clean)) {
      return(tags$div(
        style = "color: orange; font-weight: bold; padding: 20px; border: 1px solid orange; border-radius: 5px;",
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
  
  # Tabela de estatísticas
  output$desc_stats <- DT::renderDataTable({
    req(rv$stats)
    DT::datatable(rv$stats, 
                  options = list(pageLength = 10, scrollX = TRUE),
                  rownames = FALSE)
  })
  
  # Gráfico de correlação
  output$corr_plot <- renderPlot({
    req(rv$corr_matrix)
    create_correlation_plot(rv$corr_matrix)
  })
  
  # --- UI 3: Modelagem ---
  output$ui_modelagem <- renderUI({
    if (is.null(rv$df_clean)) {
      return(tags$div(
        style = "color: orange; font-weight: bold; padding: 20px; border: 1px solid orange; border-radius: 5px;",
        "⚠️ Por favor, processe os dados primeiro na seção 'Administração'."
      ))
    }
    
    tagList(
      h2("🔬 Modelagem: Regressão Linear"),
      p("Esta seção treina um modelo de regressão linear para prever a Temperatura Média Anual (BIO1) com base na Precipitação Anual (BIO12)."),
      
      fluidRow(
        column(6,
               selectInput("target_var", "Variável Alvo (Y):",
                           choices = names(rv$df_clean)[!names(rv$df_clean) %in% c("row", "col")],
                           selected = "bio1")
        ),
        column(6,
               selectInput("predictor_var", "Variável Preditora (X):",
                           choices = names(rv$df_clean)[!names(rv$df_clean) %in% c("row", "col")],
                           selected = "bio12")
        )
      ),
      
      actionButton("treinar_modelo_btn", "⚙️ Treinar Modelo", class = "btn-success"),
      br(),
      br(),
      
      if (!is.null(rv$model_result)) {
        tagList(
          h3("Resumo do Modelo"),
          verbatimTextOutput("model_summary"),
          uiOutput("model_metrics")
        )
      } else {
        p(strong("Aguardando treinamento do modelo..."))
      }
    )
  })
  
  # Treinar modelo
  observeEvent(input$treinar_modelo_btn, {
    req(rv$df_clean, input$target_var, input$predictor_var)
    
    withProgress(message = 'Treinando modelo...', value = 0.3, {
      rv$model_result <- train_linear_regression(
        rv$df_clean, 
        target_var = input$target_var,
        predictor_var = input$predictor_var
      )
      setProgress(value = 1.0)
    })
    
    showNotification("Modelo treinado e avaliado com sucesso!", type = "message")
  })
  
  # Resumo do modelo
  output$model_summary <- renderPrint({
    req(rv$model_result)
    summary(rv$model_result$model)
  })
  
  # Métricas do modelo
  output$model_metrics <- renderUI({
    req(rv$model_result)
    display_model_metrics(rv$model_result$metrics)
  })
  
  # --- UI 4: Visualização ---
  output$ui_visualizacao <- renderUI({
    if (is.null(rv$df_clean)) {
      return(tags$div(
        style = "color: orange; font-weight: bold; padding: 20px; border: 1px solid orange; border-radius: 5px;",
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
      
      conditionalPanel(
        condition = "output.model_summary != null",
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
    )
  })
  
  # Histograma BIO1
  output$bio1_hist <- renderPlot({
    req(rv$df_clean)
    create_histogram(rv$df_clean, "bio1")
  })
  
  # Dispersão BIO1 vs BIO12
  output$bio1_bio12_scatter <- renderPlot({
    req(rv$df_clean)
    create_scatterplot(rv$df_clean, "bio12", "bio1")
  })
  
  # Gráfico de resíduos
  output$residuals_plot <- renderPlot({
    req(rv$model_result)
    create_residuals_plot(
      rv$model_result$test_data[[input$target_var %||% "bio1"]],
      rv$model_result$predictions
    )
  })
  
  # Valores reais vs preditos
  output$pred_vs_actual <- renderPlot({
    req(rv$model_result)
    create_pred_vs_actual_plot(
      rv$model_result$test_data[[input$target_var %||% "bio1"]],
      rv$model_result$predictions
    )
  })
  
  # --- UI 5: Referências ---
  output$ui_referencias <- renderUI({
    tagList(
      h2("📚 Referências Bibliográficas"),
      
      h3("Base de Dados Utilizada"),
      tags$div(class = "well",
               p(strong("WorldClim - South America Climate Data")),
               p(strong("Fonte:"), "INPE (Instituto Nacional de Pesquisas Espaciais)"),
               p(strong("URL:"), tags$a(href = ZIP_URL, ZIP_URL, target = "_blank")),
               p(strong("Descrição:"), "Conjunto de dados bioclimáticos de alta resolução (1km) para a América do Sul, contendo 19 variáveis bioclimáticas derivadas de dados de temperatura e precipitação.")
      ),
      
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
          tags$a(href = "https://shiny.rstudio.com", "https://shiny.rstudio.com", target = "_blank")
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