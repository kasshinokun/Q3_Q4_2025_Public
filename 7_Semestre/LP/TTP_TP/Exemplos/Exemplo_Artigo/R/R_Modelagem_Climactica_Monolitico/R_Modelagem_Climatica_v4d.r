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

# Configurações iniciais
DATA_DIR <- "r_files_data"
ZIP_URL <- "http://www.dpi.inpe.br/amb_data/AmericaSul/SAmerica_WCLIM.zip"
ZIP_FILENAME <- "SAmerica_WCLIM.zip"
LOG_FILE <- file.path(DATA_DIR, "model_creation.log")

# --- Operador Auxiliar ---
`%||%` <- function(a, b) {
  if (!is.null(a)) a else b
}

# --- Sistema de Download e Processamento (v4 melhorado) ---

# Função 1: Verificar existência do diretório e arquivo .zip
check_data_status <- function(data_dir, zip_filename) {
  dir_exists <- dir.exists(data_dir)
  zip_exists <- file.exists(file.path(data_dir, zip_filename))
  log_exists <- file.exists(LOG_FILE)
  
  status <- list(
    dir_exists = dir_exists,
    zip_exists = zip_exists,
    log_exists = log_exists
  )
  
  # Verificar se o modelo já foi criado
  if (log_exists) {
    tryCatch({
      log_content <- readLines(LOG_FILE)
      status$model_created <- any(grepl("CREATED:\\s*TRUE", log_content, ignore.case = TRUE))
    }, error = function(e) {
      status$model_created <- FALSE
    })
  } else {
    status$model_created <- FALSE
  }
  
  return(status)
}

# Função 2: Download do arquivo .zip
download_zip_file <- function(url, target_dir, zip_filename) {
  tryCatch({
    showNotification("Iniciando download dos dados...", type = "message")
    
    # Criar diretório se não existir
    if (!dir.exists(target_dir)) {
      dir.create(target_dir, recursive = TRUE, showWarnings = FALSE)
    }
    
    temp_zip <- tempfile(fileext = ".zip")
    
    # Download com barra de progresso
    withProgress({
      setProgress(message = "Baixando dados climáticos...", value = 0.3)
      options(timeout = 300)
      download.file(url, temp_zip, mode = "wb", quiet = TRUE)
      
      # Mover arquivo para o diretório destino
      target_zip <- file.path(target_dir, zip_filename)
      file.copy(temp_zip, target_zip, overwrite = TRUE)
      file.remove(temp_zip)
      
      setProgress(message = "Download concluído!", value = 1.0)
    })
    
    showNotification("Download realizado com sucesso!", type = "message")
    return(TRUE)
  }, error = function(e) {
    showNotification(paste("Erro durante o download:", e$message), type = "error")
    return(FALSE)
  })
}

# Função 3: Descompactar arquivo .zip
unzip_data_file <- function(zip_path, target_dir) {
  tryCatch({
    showNotification("Iniciando descompactação dos dados...", type = "message")
    
    withProgress({
      setProgress(message = "Descompactando arquivos...", value = 0.6)
      
      # Descompactar arquivos
      unzip(zip_path, exdir = target_dir)
      
      setProgress(message = "Descompactação concluída!", value = 1.0)
    })
    
    showNotification("Dados descompactados com sucesso!", type = "message")
    return(TRUE)
  }, error = function(e) {
    showNotification(paste("Erro durante descompactação:", e$message), type = "error")
    return(FALSE)
  })
}

# Função 4: Criar arquivo de log
create_model_log <- function(data_dir, status = TRUE) {
  log_file <- file.path(data_dir, "model_creation.log")
  log_content <- paste(
    "CREATED:", toupper(as.character(status)),
    "\nDATE:", Sys.time(),
    "\nDATA_DIR:", data_dir,
    "\nTIMESTAMP:", as.integer(Sys.time())
  )
  
  tryCatch({
    writeLines(log_content, log_file)
    return(TRUE)
  }, error = function(e) {
    showNotification(paste("Erro ao criar arquivo de log:", e$message), type = "warning")
    return(FALSE)
  })
}

# Função 5: Validar modelo existente
validate_existing_model <- function(data_dir) {
  log_file <- file.path(data_dir, "model_creation.log")
  
  if (!file.exists(log_file)) {
    return(FALSE)
  }
  
  tryCatch({
    log_content <- readLines(log_file)
    model_created <- any(grepl("CREATED:\\s*TRUE", log_content, ignore.case = TRUE))
    
    if (model_created) {
      # Verificar se os arquivos ASC existem (validação mais robusta)
      asc_files <- list.files(data_dir, pattern = "\\.asc$", full.names = TRUE)
      files_to_process <- asc_files[!basename(asc_files) %in% c('alt.asc', 'decl.asc', '110914_DadosWorldClim_SouthAmerica_25.txt')]
      
      if (length(files_to_process) > 10) { # Espera-se mais de 10 arquivos climáticos
        showNotification("Modelo existente validado. Utilizando dados pré-processados.", type = "info")
        return(TRUE)
      } else {
        showNotification("Log encontrado, mas arquivos de dados incompletos. Reprocessando.", type = "warning")
        return(FALSE)
      }
    } else {
      return(FALSE)
    }
  }, error = function(e) {
    showNotification("Erro ao validar modelo existente. Reprocessando dados...", type = "warning")
    return(FALSE)
  })
}

# Função principal: Orquestrar download e processamento
download_and_process_data <- function(url, target_dir, zip_filename) {
  # Verificar status atual
  status <- check_data_status(target_dir, zip_filename)
  
  # Se modelo já foi criado e validado, retornar TRUE
  if (status$model_created && validate_existing_model(target_dir)) {
    return(TRUE)
  }
  
  # Barra de progresso principal
  withProgress({
    # Etapa 1: Verificar e baixar dados se necessário
    setProgress(message = "Verificando dados existentes...", value = 0.1)
    
    if (!status$zip_exists || !status$dir_exists) {
      setProgress(message = "Download necessário. Baixando dados...", value = 0.2)
      download_success <- download_zip_file(url, target_dir, zip_filename)
      if (!download_success) return(FALSE)
      status$zip_exists <- TRUE # Atualiza status
    }
    
    # Etapa 2: Descompactar dados
    setProgress(message = "Preparando para descompactar...", value = 0.5)
    zip_path <- file.path(target_dir, zip_filename)
    unzip_success <- unzip_data_file(zip_path, target_dir)
    if (!unzip_success) return(FALSE)
    
    # Etapa 3: Criar log do modelo
    setProgress(message = "Finalizando processamento...", value = 0.9)
    log_success <- create_model_log(target_dir, TRUE)
    
    setProgress(message = "Processamento concluído!", value = 1.0)
    return(TRUE)
  })
}

# --- Funções de Processamento de Dados Climáticos (v3 mantidas) ---

read_asc_file <- function(filepath) {
  # Lê um arquivo ASCII Grid (.asc) e retorna os metadados e os dados
  tryCatch({
    # Ler cabeçalho (6 linhas)
    con <- file(filepath, "r")
    header_lines <- readLines(con, 6)
    close(con)
    
    header <- list()
    for(line in header_lines) {
      parts <- strsplit(trimws(line), "\\s+")[[1]]
      key <- parts[1]
      value <- if(key %in% c("ncols", "nrows")) as.integer(parts[2]) else as.numeric(parts[2])
      header[[key]] <- value
    }
    
    # Ler dados
    data <- as.matrix(read.table(filepath, skip = 6))
    
    return(list(header = header, data = data))
  }, error = function(e) {
    showNotification(paste("Erro ao ler arquivo", basename(filepath), ":", e$message), type = "error")
    return(NULL)
  })
}

process_worldclim_data <- function(data_dir) {
  # Processa todos os arquivos WorldClim (.asc) no diretório
  if (!dir.exists(data_dir)) {
    showNotification(paste("Diretório não encontrado:", data_dir), type = "error")
    return(NULL)
  }
  
  # Listar arquivos .asc, excluindo arquivos não climáticos
  asc_files <- list.files(data_dir, pattern = "\\.asc$", full.names = TRUE)
  files_to_process <- asc_files[!basename(asc_files) %in% c('alt.asc', 'decl.asc', '110914_DadosWorldClim_SouthAmerica_25.txt')]
  
  if (length(files_to_process) == 0) {
    showNotification("Nenhum arquivo .asc de variáveis climáticas encontrado", type = "warning")
    return(NULL)
  }
  
  all_data <- list()
  
  # Processar primeiro arquivo para obter estrutura
  first_file <- files_to_process[1]
  first_result <- read_asc_file(first_file)
  if (is.null(first_result)) return(NULL)
  
  rows <- first_result$header$nrows
  cols <- first_result$header$ncols
  nodata_value <- first_result$header$NODATA_value %||% -9999
  
  # Adicionar primeiro conjunto de dados
  var_name <- tools::file_path_sans_ext(basename(first_file))
  all_data[[var_name]] <- as.vector(first_result$data)
  
  # Processar arquivos restantes
  for (filepath in files_to_process[-1]) {
    result <- read_asc_file(filepath)
    if (is.null(result)) next
    
    # Verificar dimensões
    if (result$header$nrows != rows || result$header$ncols != cols) {
      showNotification(paste("Dimensões não correspondem para", basename(filepath)), type = "warning")
      next
    }
    
    var_name <- tools::file_path_sans_ext(basename(filepath))
    all_data[[var_name]] <- as.vector(result$data)
  }
  
  # Criar DataFrame
  df <- as.data.frame(all_data)
  
  # Adicionar coordenadas
  df$row <- rep(1:rows, each = cols)
  df$col <- rep(1:cols, times = rows)
  
  # Reordenar colunas
  df <- df %>% select(row, col, everything())
  
  # Remover valores NODATA
  df_clean <- df[!rowSums(df == nodata_value, na.rm = TRUE) > 0, ]
  
  return(df_clean)
}

# --- UI da Aplicação (v3 com sistema de status da v4) ---

ui <- fluidPage(
  theme = shinytheme("flatly"),
  titlePanel("🌎 Análise Climática da América do Sul - Versão Integrada"),
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
          "3. Modelagem: Regressão Linear Múltipla",
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
        condition = "input.menu_selecao == '3. Modelagem: Regressão Linear Múltipla'",
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

# --- Servidor da Aplicação (Integrado) ---

server <- function(input, output, session) {
  
  # Reactive values para armazenar dados
  rv <- reactiveValues(
    df_clean = NULL,
    model = NULL,
    predictions = NULL,
    test_data = NULL,
    train_data = NULL,
    dados_processados = FALSE,
    metrics = NULL
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
    status <- check_data_status(DATA_DIR, ZIP_FILENAME)
    
    tagList(
      h2("📊 Administração - Download e Processamento de Dados"),
      p("Esta seção gerencia o download e processamento dos dados climáticos do WorldClim para a América do Sul."),
      p("Os dados serão baixados do INPE e processados para análise."),
      br(),
      
      if (rv$dados_processados) {
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
      
      # Usar a nova função refatorada para download/unzip/log
      if (download_and_process_data(ZIP_URL, DATA_DIR, ZIP_FILENAME)) {
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
    rv$train_data <- NULL
    
    showNotification("Dados removidos. Clique em 'Processar Dados' para recriar.", type = "warning")
  })
  
  # UI 2: Análise Estatística (v3) - ATUALIZADA com NAs
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
      
      h3("Estatísticas Descritivas (Completas)"),
      p("Estatísticas descritivas para todas as variáveis bioclimáticas incluindo valores NA:"),
      withSpinner(DT::dataTableOutput("desc_stats_complete"), type = 4),
      
      h3("Análise de Correlação"),
      h4("Correlação de BIO1 (Temperatura Média Anual) com Outras Variáveis:"),
      withSpinner(DT::dataTableOutput("corr_bio1"), type = 4),
      
      h4("Mapa de Calor de Correlações:"),
      withSpinner(plotOutput("corr_heatmap", height = "600px"), type = 4)
    )
  })
  
  # Estatísticas descritivas COMPLETAS com NAs
  output$desc_stats_complete <- DT::renderDataTable({
    req(rv$df_clean)
    
    bio_cols <- grep("^bio", names(rv$df_clean), value = TRUE)
    desc_stats <- rv$df_clean[bio_cols] %>% 
      summarise(across(everything(), list(
        N = ~sum(!is.na(.)),
        N_NA = ~sum(is.na(.)),
        Porcentagem_NA = ~round(mean(is.na(.)) * 100, 2),
        Média = ~mean(., na.rm = TRUE),
        Mediana = ~median(., na.rm = TRUE),
        SD = ~sd(., na.rm = TRUE),
        Min = ~min(., na.rm = TRUE),
        Q1 = ~quantile(., 0.25, na.rm = TRUE),
        Q3 = ~quantile(., 0.75, na.rm = TRUE),
        Max = ~max(., na.rm = TRUE)
      ))) %>% 
      t() %>% 
      as.data.frame() %>% 
      round(3)
    
    # Adicionar nomes das linhas como coluna
    desc_stats$Estatística <- rownames(desc_stats)
    desc_stats <- desc_stats %>% select(Estatística, everything())
    names(desc_stats)[2] <- "Valor"
    
    DT::datatable(desc_stats, 
                  options = list(
                    scrollX = TRUE,
                    pageLength = 25,
                    dom = 'tip'
                  ),
                  rownames = FALSE) %>%
      formatStyle('Estatística', fontWeight = 'bold')
  })
  
  # Correlação com BIO1 (v3)
  output$corr_bio1 <- DT::renderDataTable({
    req(rv$df_clean)
    
    bio_cols <- grep("^bio", names(rv$df_clean), value = TRUE)
    cor_matrix <- cor(rv$df_clean[bio_cols], use = "complete.obs")
    
    corr_bio1 <- as.data.frame(cor_matrix['bio1', , drop = FALSE])
    corr_bio1 <- corr_bio1[order(-corr_bio1$bio1), , drop = FALSE]
    corr_bio1 <- corr_bio1[rownames(corr_bio1) != 'bio1', , drop = FALSE]
    
    DT::datatable(corr_bio1, 
                  options = list(scrollX = TRUE),
                  caption = "Correlação com BIO1 (Temperatura Média Anual)") %>%
      formatRound(columns = 'bio1', digits = 4) %>%
      formatStyle('bio1',
                  backgroundColor = styleInterval(
                    c(-0.5, 0, 0.5),
                    c('#ff6b6b', '#ffe66d', '#90ee90', '#4ecdc4')
                  ))
  })
  
  # Heatmap de correlação (v3)
  output$corr_heatmap <- renderPlot({
    req(rv$df_clean)
    
    bio_cols <- grep("^bio", names(rv$df_clean), value = TRUE)
    cor_matrix <- cor(rv$df_clean[bio_cols], use = "complete.obs")
    
    corrplot(cor_matrix, method = "color", type = "upper", 
             order = "hclust", tl.cex = 0.8, tl.col = "black",
             addCoef.col = "black", number.cex = 0.7,
             title = "Matriz de Correlação - Variáveis Bioclimáticas",
             mar = c(0,0,2,0))
  })
  
  # UI 3: Modelagem (v3 - Regressão Múltipla) - ATUALIZADA
  output$ui_modelagem <- renderUI({
    if (is.null(rv$df_clean)) {
      return(tags$div(
        style = "color: orange; font-weight: bold;",
        "⚠️ Por favor, processe os dados primeiro na seção 'Administração'."
      ))
    }
    
    tagList(
      h2("🤖 Modelagem: Regressão Linear Múltipla"),
      p(strong("Modelo:"), "BIO1 (Temperatura Média Anual) ~ BIO12 (Precipitação Anual) + BIO4 (Sazonalidade da Temperatura)"),
      
      actionButton("treinar_modelo_btn", "🎯 Treinar Modelo", class = "btn-success"),
      br(), br(),
      
      conditionalPanel(
        condition = "input.treinar_modelo_btn > 0",
        tagList(
          withSpinner(verbatimTextOutput("model_summary"), type = 4),
          
          h3("Métricas de Avaliação do Modelo"),
          uiOutput("model_metrics"),
          
          h3("Estatísticas dos Conjuntos de Dados"),
          uiOutput("dataset_stats"),
          
          h3("Coeficientes do Modelo"),
          uiOutput("model_coefficients"),
          
          h3("Interpretação do Modelo"),
          uiOutput("model_interpretation")
        )
      )
    )
  })
  
  # Treinar modelo quando botão for clicado
  observeEvent(input$treinar_modelo_btn, {
    req(rv$df_clean)
    
    withProgress({
      setProgress(message = "Treinando modelo...", value = 0.3)
      
      # Preparar dados (v3 - regressão múltipla)
      model_df <- rv$df_clean %>% 
        select(bio1, bio12, bio4) %>% 
        na.omit()
      
      # Dividir dados
      set.seed(42)
      split <- initial_split(model_df, prop = 0.7)
      train_data <- training(split)
      test_data <- testing(split)
      
      # Armazenar conjuntos
      rv$train_data <- train_data
      rv$test_data <- test_data
      
      # Treinar modelo
      setProgress(message = "Ajustando modelo...", value = 0.7)
      model <- lm(bio1 ~ bio12 + bio4, data = train_data)
      
      # Fazer previsões
      predictions <- predict(model, newdata = test_data)
      
      # Armazenar resultados
      rv$model <- model
      rv$predictions <- predictions
      
      # Calcular métricas avançadas
      r_squared <- summary(model)$r.squared
      mse <- mean((predictions - test_data$bio1)^2)
      rmse <- sqrt(mse)
      mae <- mean(abs(predictions - test_data$bio1))
      
      rv$metrics <- list(
        r_squared = r_squared,
        mse = mse,
        rmse = rmse,
        mae = mae,
        coefficients = coef(model),
        n_train = nrow(train_data),
        n_test = nrow(test_data),
        n_total = nrow(model_df)
      )
      
      setProgress(message = "Modelo treinado com sucesso!", value = 1.0)
    })
    
    showNotification("Modelo treinado com sucesso!", type = "message")
  })
  
  # Sumário do modelo (v3)
  output$model_summary <- renderPrint({
    req(rv$model)
    summary(rv$model)
  })
  
  # Métricas do modelo - NOVA SEÇÃO
  output$model_metrics <- renderUI({
    req(rv$model, rv$metrics)
    
    fluidRow(
      column(6,
             div(style = "background-color: #e8f5e8; padding: 15px; border-radius: 5px; margin-bottom: 10px;",
                 h4("R² (Coeficiente de Determinação)"),
                 h3(style = "color: #28a745;", sprintf("%.4f", rv$metrics$r_squared)),
                 p("Proporção da variância explicada pelo modelo")
             )
      ),
      column(6,
             div(style = "background-color: #ffe6e6; padding: 15px; border-radius: 5px; margin-bottom: 10px;",
                 h4("MSE (Erro Quadrático Médio)"),
                 h3(style = "color: #dc3545;", sprintf("%.2f", rv$metrics$mse)),
                 p("Média dos quadrados dos erros")
             )
      ),
      column(6,
             div(style = "background-color: #fff3cd; padding: 15px; border-radius: 5px; margin-bottom: 10px;",
                 h4("RMSE (Raiz do Erro Quadrático Médio)"),
                 h3(style = "color: #ffc107;", sprintf("%.2f", rv$metrics$rmse)),
                 p("Raiz quadrada do MSE - na mesma unidade da variável resposta")
             )
      ),
      column(6,
             div(style = "background-color: #d1ecf1; padding: 15px; border-radius: 5px; margin-bottom: 10px;",
                 h4("MAE (Erro Absoluto Médio)"),
                 h3(style = "color: #17a2b8;", sprintf("%.2f", rv$metrics$mae)),
                 p("Média dos valores absolutos dos erros")
             )
      )
    )
  })
  
  # Estatísticas dos conjuntos de dados - NOVA SEÇÃO
  output$dataset_stats <- renderUI({
    req(rv$train_data, rv$test_data)
    
    tagList(
      fluidRow(
        column(4,
               div(style = "background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 10px;",
                   h4("Conjunto de Treino"),
                   h3(style = "color: #007bff;", sprintf("%d", rv$metrics$n_train)),
                   p("Observações para treinamento")
               )
        ),
        column(4,
               div(style = "background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 10px;",
                   h4("Conjunto de Teste"),
                   h3(style = "color: #6c757d;", sprintf("%d", rv$metrics$n_test)),
                   p("Observações para teste")
               )
        ),
        column(4,
               div(style = "background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 10px;",
                   h4("Total (Após Limpeza)"),
                   h3(style = "color: #28a745;", sprintf("%d", rv$metrics$n_total)),
                   p("Observações válidas para modelagem")
               )
        )
      ),
      
      h4("Estatísticas Descritivas dos Conjuntos"),
      p("Estatísticas básicas para as variáveis nos conjuntos de treino e teste:"),
      withSpinner(DT::dataTableOutput("train_test_stats"), type = 4)
    )
  })
  
  # Tabela de estatísticas treino/teste
  output$train_test_stats <- DT::renderDataTable({
    req(rv$train_data, rv$test_data)
    
    # Função para calcular estatísticas
    calculate_stats <- function(data, dataset_name) {
      data %>% 
        summarise(across(everything(), list(
          Média = ~mean(., na.rm = TRUE),
          DP = ~sd(., na.rm = TRUE),
          Min = ~min(., na.rm = TRUE),
          Máx = ~max(., na.rm = TRUE)
        ))) %>%
        t() %>%
        as.data.frame() %>%
        mutate(Estatística = rownames(.),
               Conjunto = dataset_name) %>%
        select(Conjunto, Estatística, Valor = V1)
    }
    
    train_stats <- calculate_stats(rv$train_data, "Treino")
    test_stats <- calculate_stats(rv$test_data, "Teste")
    
    stats_combined <- bind_rows(train_stats, test_stats) %>%
      mutate(Valor = round(Valor, 3))
    
    DT::datatable(stats_combined, 
                  options = list(
                    pageLength = 20,
                    dom = 'tip'
                  ),
                  rownames = FALSE) %>%
      formatStyle('Conjunto', fontWeight = 'bold')
  })
  
  # Coeficientes do modelo - SEPARADO
  output$model_coefficients <- renderUI({
    req(rv$model, rv$metrics)
    
    fluidRow(
      column(4,
             div(style = "background-color: #e3f2fd; padding: 15px; border-radius: 5px; margin-bottom: 10px;",
                 h4("Coeficiente BIO12"),
                 h3(style = "color: #1976d2;", sprintf("%.4f", rv$metrics$coefficients["bio12"])),
                 p("Precipitação Anual")
             )
      ),
      column(4,
             div(style = "background-color: #e8f5e8; padding: 15px; border-radius: 5px; margin-bottom: 10px;",
                 h4("Coeficiente BIO4"),
                 h3(style = "color: #388e3c;", sprintf("%.4f", rv$metrics$coefficients["bio4"])),
                 p("Sazonalidade da Temperatura")
             )
      ),
      column(4,
             div(style = "background-color: #f3e5f5; padding: 15px; border-radius: 5px; margin-bottom: 10px;",
                 h4("Intercepto"),
                 h3(style = "color: #7b1fa2;", sprintf("%.4f", rv$metrics$coefficients["(Intercept)"])),
                 p("Termo constante")
             )
      )
    )
  })
  
  # Interpretação do modelo (v3)
  output$model_interpretation <- renderUI({
    req(rv$model, rv$metrics)
    
    tagList(
      div(style = "background-color: #fff3cd; padding: 15px; border-radius: 5px;",
          h4("📊 Interpretação do Modelo"),
          p("O modelo explica", strong(sprintf("%.2f%%", rv$metrics$r_squared * 100)), 
            "da variância na Temperatura Média Anual (BIO1)."),
          p("📈 Um aumento de 1 unidade em BIO12 (Precipitação Anual) está associado a uma mudança de",
            strong(sprintf("%.4f", rv$metrics$coefficients["bio12"])), "na BIO1."),
          p("🌡️ Um aumento de 1 unidade em BIO4 (Sazonalidade da Temperatura) está associado a uma mudança de",
            strong(sprintf("%.4f", rv$metrics$coefficients["bio4"])), "na BIO1."),
          p("🎯 O RMSE de", strong(sprintf("%.2f", rv$metrics$rmse)), "indica o erro médio de previsão do modelo.")
      )
    )
  })
  
  # UI 4: Visualização (v3)
  output$ui_visualizacao <- renderUI({
    if (is.null(rv$df_clean)) {
      return(tags$div(
        style = "color: orange; font-weight: bold;",
        "⚠️ Por favor, processe os dados primeiro na seção 'Administração'."
      ))
    }
    
    tagList(
      h2("📊 Visualização de Dados e Modelo"),
      
      h3("Visualização dos Dados Climáticos"),
      
      fluidRow(
        column(6,
               h4("Distribuição da Temperatura Média Anual (BIO1)"),
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
  
  # Histograma BIO1 (v3)
  output$bio1_hist <- renderPlot({
    req(rv$df_clean)
    
    ggplot(rv$df_clean, aes(x = bio1)) +
      geom_histogram(aes(y = after_stat(density)), bins = 30, fill = "skyblue", alpha = 0.7) +
      geom_density(color = "darkblue", linewidth = 1) +
      labs(title = "Distribuição de BIO1 (Temperatura Média Anual)",
           x = "BIO1 (x 10 °C)", y = "Densidade") +
      theme_minimal()
  })
  
  # Dispersão BIO1 vs BIO12 (v3)
  output$bio1_bio12_scatter <- renderPlot({
    req(rv$df_clean)
    
    sample_data <- rv$df_clean %>% sample_n(min(5000, nrow(rv$df_clean)))
    
    ggplot(sample_data, aes(x = bio12, y = bio1)) +
      geom_point(alpha = 0.5, color = "darkred") +
      geom_smooth(method = "lm", color = "blue", se = FALSE) +
      labs(title = "BIO1 vs BIO12 (Amostra)",
           x = "BIO12 (mm)", y = "BIO1 (x 10 °C)") +
      theme_minimal()
  })
  
  # Gráfico de resíduos (v3)
  output$residuals_plot <- renderPlot({
    req(rv$model, rv$predictions, rv$test_data)
    
    residuals <- rv$test_data$bio1 - rv$predictions
    
    ggplot(data.frame(residuals = residuals), aes(x = residuals)) +
      geom_histogram(aes(y = after_stat(density)), bins = 30, fill = "lightgreen", alpha = 0.7) +
      geom_density(color = "darkgreen", linewidth = 1) +
      labs(title = "Distribuição dos Resíduos",
           x = "Resíduos (y_test - y_pred)", y = "Densidade") +
      theme_minimal()
  })
  
  # Valores reais vs preditos (v3)
  output$pred_vs_actual <- renderPlot({
    req(rv$model, rv$predictions, rv$test_data)
    
    plot_data <- data.frame(
      Actual = rv$test_data$bio1,
      Predicted = rv$predictions
    )
    
    ggplot(plot_data, aes(x = Actual, y = Predicted)) +
      geom_point(alpha = 0.5, color = "purple") +
      geom_abline(slope = 1, intercept = 0, color = "red", linetype = "dashed", linewidth = 1) +
      labs(title = "Valores Reais vs Preditos",
           x = "Valores Reais", y = "Valores Preditos") +
      theme_minimal()
  })
  
  # UI 5: Referências (v3)
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