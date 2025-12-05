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
DATA_DIR <- "streamlit_data"
ZIP_URL <- "http://www.dpi.inpe.br/amb_data/AmericaSul/SAmerica_WCLIM.zip"
ZIP_FILENAME <- "SAmerica_WCLIM.zip"
LOG_FILE <- file.path(DATA_DIR, "model_creation.log")

# --- Funções de Processamento de Dados (Atualizadas e Refatoradas) ---

# Função auxiliar para o operador %||% (se não for nulo, use o valor, senão use o padrão)
`%||%` <- function(a, b) {
  if (!is.null(a)) a else b
}

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
    log_content <- readLines(LOG_FILE)
    status$model_created <- any(grepl("CREATED:\\s*TRUE", log_content, ignore.case = TRUE))
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
      if (length(asc_files) > 10) { # Espera-se mais de 10 arquivos climáticos
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

# Função de leitura de arquivos ASC (do v3.r)
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

# Função de processamento de dados WorldClim (do v3.r)
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

# --- UI da Aplicação (do v3.r) ---

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

# --- Servidor da Aplicação (統合と更新) ---

server <- function(input, output, session) {
  
  # Reactive values para armazenar dados
  rv <- reactiveValues(
    df_clean = NULL,
    model = NULL,
    predictions = NULL,
    test_data = NULL,
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
    status <- check_data_status(DATA_DIR, ZIP_FILENAME)
    
    tagList(
      h2("📊 Administração - Download e Processamento de Dados"),
      p("Esta seção gerencia o download e processamento dos dados climáticos do WorldClim para a América do Sul."),
      p("Os dados serão baixados do INPE e processados para análise."),
      br(),
      
      if (status$model_created && validate_existing_model(DATA_DIR)) {
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
  
  # Processar dados quando botão for clicado (USANDO A NOVA FUNÇÃO)
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
    
    # Simula clique no botão processar
    # Nota: A lógica de reprocessamento no v3.r era complexa e usava shinyjs::click. 
    # Simplificamos para que o próximo clique no botão "Processar Dados" (que aparecerá após o unlink) 
    # execute a nova lógica de download_and_process_data.
    # Para forçar o re-render da UI de administração:
    output$ui_administracao <- renderUI({
      status <- check_data_status(DATA_DIR, ZIP_FILENAME)
      
      tagList(
        h2("📊 Administração - Download e Processamento de Dados"),
        p("Esta seção gerencia o download e processamento dos dados climáticos do WorldClim para a América do Sul."),
        p("Os dados serão baixados do INPE e processados para análise."),
        br(),
        
        if (status$model_created && validate_existing_model(DATA_DIR)) {
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
  
  # --- Lógica de Análise Estatística (do v3.r) ---
  
  # Estatísticas Descritivas
  output$desc_stats <- DT::renderDataTable({
    req(rv$df_clean)
    
    # Selecionar apenas as colunas bioclimáticas (excluindo row e col)
    bio_cols <- names(rv$df_clean)[!names(rv$df_clean) %in% c("row", "col")]
    
    stats <- rv$df_clean %>%
      select(all_of(bio_cols)) %>%
      summarise_all(list(
        Média = ~mean(., na.rm = TRUE),
        Mediana = ~median(., na.rm = TRUE),
        DP = ~sd(., na.rm = TRUE),
        Mín = ~min(., na.rm = TRUE),
        Máx = ~max(., na.rm = TRUE),
        NAs = ~sum(is.na(.))
      )) %>%
      t() %>%
      as.data.frame()
    
    names(stats) <- c("Média", "Mediana", "DP", "Mín", "Máx", "NAs")
    stats$Variável <- rownames(stats)
    stats <- stats %>% select(Variável, everything())
    
    DT::datatable(stats, options = list(pageLength = 10))
  })
  
  # Matriz de Correlação
  output$corr_plot <- renderPlot({
    req(rv$df_clean)
    
    bio_cols <- names(rv$df_clean)[!names(rv$df_clean) %in% c("row", "col")]
    corr_matrix <- cor(rv$df_clean %>% select(all_of(bio_cols)), use = "complete.obs")
    
    corrplot(corr_matrix, method = "color", type = "upper", 
             tl.col = "black", tl.srt = 45, addCoef.col = "black", 
             title = "Matriz de Correlação das Variáveis Bioclimáticas", 
             mar = c(0,0,1,0))
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
  
  # --- Lógica de Modelagem (do v3.r) ---
  
  # Treinamento do Modelo
  observeEvent(input$treinar_modelo_btn, {
    req(rv$df_clean)
    
    withProgress(message = 'Treinando modelo...', value = 0.1, {
      
      # 1. Preparação dos dados
      setProgress(detail = "Dividindo dados em treino e teste...", value = 0.3)
      
      # Usar BIO1 (Temperatura Média Anual) como variável dependente
      # Usar BIO12 (Precipitação Anual) como variável independente
      data_model <- rv$df_clean %>% select(bio1, bio12) %>% na.omit()
      
      # Divisão dos dados (70% treino, 30% teste)
      set.seed(42) # Para reprodutibilidade
      split <- initial_split(data_model, prop = 0.7)
      train_data <- training(split)
      test_data <- testing(split)
      
      rv$test_data <- test_data
      
      # 2. Treinamento do Modelo de Regressão Linear
      setProgress(detail = "Ajustando o modelo de regressão linear...", value = 0.6)
      model <- lm(bio1 ~ bio12, data = train_data)
      rv$model <- model
      
      # 3. Previsões e Avaliação
      setProgress(detail = "Realizando previsões e avaliando...", value = 0.8)
      predictions <- predict(model, newdata = test_data)
      rv$predictions <- predictions
      
      # Cálculo do R-quadrado
      r_squared <- summary(model)$r.squared
      
      # Cálculo do RMSE (Root Mean Squared Error)
      rmse <- sqrt(mean((test_data$bio1 - predictions)^2))
      
      # Armazenar métricas para exibição
      rv$metrics <- list(
        r_squared = r_squared,
        rmse = rmse,
        n_train = nrow(train_data),
        n_test = nrow(test_data)
      )
      
      showNotification("Modelo treinado e avaliado com sucesso!", type = "message")
    })
  })
  
  # Resumo do Modelo
  output$model_summary <- renderPrint({
    req(rv$model)
    summary(rv$model)
  })
  
  # Métricas de Avaliação
  output$model_metrics <- renderUI({
    req(rv$metrics)
    
    tagList(
      h4("Métricas de Avaliação (Conjunto de Teste)"),
      tags$ul(
        tags$li(strong("R-quadrado:"), round(rv$metrics$r_squared, 4)),
        tags$li(strong("RMSE (Erro Quadrático Médio):"), round(rv$metrics$rmse, 4)),
        tags$li(strong("Tamanho do Conjunto de Treino:"), rv$metrics$n_train),
        tags$li(strong("Tamanho do Conjunto de Teste:"), rv$metrics$n_test)
      )
    )
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
        p(strong("Aguardando treinamento do modelo..."))
      }
    )
  })
  
  # --- Lógica de Visualização (do v3.r) ---
  
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
    
    ggplot(rv$df_clean, aes(x = bio1)) +
      geom_histogram(aes(y = after_stat(density)), bins = 30, fill = "skyblue", alpha = 0.7) +
      geom_density(color = "darkblue", linewidth = 1) +
      labs(title = "Distribuição de BIO1 (Temperatura Média Anual)",
           x = "BIO1 (x 10 °C)", y = "Densidade") +
      theme_minimal()
  })
  
  # Dispersão BIO1 vs BIO12
  output$bio1_bio12_scatter <- renderPlot({
    req(rv$df_clean)
    
    sample_data <- rv$df_clean %>% sample_n(min(5000, nrow(rv$df_clean)))
    
    ggplot(sample_data, aes(x = bio12, y = bio1)) +
      geom_point(alpha = 0.5, color = "darkred") +
      labs(title = "BIO1 vs BIO12 (Amostra)",
           x = "BIO12 (mm)", y = "BIO1 (x 10 °C)") +
      theme_minimal()
  })
  
  # Gráfico de resíduos
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
  
  # Valores reais vs preditos
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
  
  # UI 5: Referências (do v3.r)
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
