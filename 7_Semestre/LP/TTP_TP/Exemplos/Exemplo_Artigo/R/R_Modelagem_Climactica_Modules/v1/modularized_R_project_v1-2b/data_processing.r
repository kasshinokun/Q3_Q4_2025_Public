# --- Variavel de TimeOut
DOWNLOAD_TIMEOUT <- 300 # 5 minutos

# --- Funções de Processamento de Dados ---

# Função auxiliar para o operador %||% (se não for nulo, use o valor, senão use o padrão)
`%||%` <- function(a, b) {
  if (!is.null(a)) a else b
}

# Função 1: Verificar existência do diretório e arquivo .zip
check_data_status <- function(data_dir, zip_filename, log_file) {
  dir_exists <- dir.exists(data_dir)
  zip_exists <- file.exists(file.path(data_dir, zip_filename))
  log_exists <- file.exists(log_file)
  
  status <- list(
    dir_exists = dir_exists,
    zip_exists = zip_exists,
    log_exists = log_exists
  )
  
  # Verificar se o modelo já foi criado
  if (log_exists) {
    log_content <- readLines(log_file)
    status$model_created <- any(grepl("CREATED:\\s*TRUE", log_content, ignore.case = TRUE))
  } else {
    status$model_created <- FALSE
  }
  
  return(status)
}

# Função 2: Download do arquivo .zip
download_zip_file <- function(url, target_dir, zip_filename, download_timeout_seconds) {
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
      # Configura o timeout para o download
      options(timeout = download_timeout_seconds)
      download.file(url, temp_zip, mode = "wb", quiet = TRUE)
      # Restaura o timeout padrão (geralmente 60 segundos)
      options(timeout = DOWNLOAD_TIMEOUT)
      
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
create_model_log <- function(log_file, data_dir, status = TRUE) {
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
validate_existing_model <- function(data_dir, log_file) {
  
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
download_and_process_data <- function(url, target_dir, zip_filename, log_file, download_timeout_seconds) {
  # Verificar status atual
  status <- check_data_status(target_dir, zip_filename, log_file)
  
  # Se modelo já foi criado e validado, retornar TRUE
  if (status$model_created && validate_existing_model(target_dir, log_file)) {
    return(TRUE)
  }
  
  # Barra de progresso principal
  withProgress({
    # Etapa 1: Verificar e baixar dados se necessário
    setProgress(message = "Verificando dados existentes...", value = 0.1)
    
    if (!status$zip_exists || !status$dir_exists) {
      setProgress(message = "Download necessário. Baixando dados...", value = 0.2)
      download_success <- download_zip_file(url, target_dir, zip_filename, download_timeout_seconds)
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
    log_success <- create_model_log(log_file, target_dir, TRUE)
    
    setProgress(message = "Processamento concluído!", value = 1.0)
    return(TRUE)
  })
}

# Função de leitura de arquivos ASC
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

# Função de processamento de dados WorldClim
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

# --- Funções de Análise Estatística (movidas para data_processing.r para manter coesão com o processamento) ---

# Estatísticas Descritivas
render_desc_stats <- function(df_clean) {
  # Selecionar apenas as colunas bioclimáticas (excluindo row e col)
  bio_cols <- names(df_clean)[!names(df_clean) %in% c("row", "col")]
  
  stats <- df_clean %>%
    select(all_of(bio_cols)) %>%
    summarise(across(everything(), list(
      Média = ~mean(., na.rm = TRUE),
      Mediana = ~median(., na.rm = TRUE),
      DP = ~sd(., na.rm = TRUE),
      Mín = ~min(., na.rm = TRUE),
      Máx = ~max(., na.rm = TRUE),
      NAs = ~sum(is.na(.))
    ))) %>%
    pivot_longer(cols = everything(), names_to = "Variável_Estatistica", values_to = "Valor") %>%
    separate(Variável_Estatistica, into = c("Variável", "Estatistica"), sep = "_") %>%
    pivot_wider(names_from = Estatistica, values_from = Valor) %>%
    as.data.frame()
  
  return(DT::datatable(stats, options = list(pageLength = 10)))
}

# Matriz de Correlação
render_corr_plot <- function(df_clean) {
  bio_cols <- names(df_clean)[!names(df_clean) %in% c("row", "col")]
  corr_matrix <- cor(df_clean %>% select(all_of(bio_cols)), use = "complete.obs")
  
  # Salvar parâmetros gráficos originais
  op <- par(mar = c(0, 0, 3, 0), oma = c(2, 2, 5, 2))
  
  # Configurar layout com título e legenda dedicados
  layout(matrix(c(1, 2), nrow = 2), heights = c(0.9, 0.1))
  
  # Plot principal da matriz de correlação
  corrplot(corr_matrix, 
           method = "color", 
           type = "full",  # Mostrar triângulo completo
           order = "hclust",  # Ordenar por cluster hierárquico
           tl.col = "black", 
           tl.srt = 45, 
           tl.cex = 0.8,
           tl.pos = "lt",  # Posicionar labels top e left
           cl.pos = "r",  # Legenda à direita
           addrect = 3,  # Adicionar retângulos agrupando clusters
           rect.col = "blue", 
           rect.lwd = 2,
           addCoef.col = "black", 
           number.cex = 0.7,
           number.digits = 2,
           title = "",  # Título será adicionado separadamente
           mar = c(0, 0, 0, 0))
  
  # Título
  title(main = "Matriz de Correlação das Variáveis Bioclimáticas", 
        line = 1, cex.main = 1.2, font.main = 2)
  
  # Segunda parte do layout: legenda
  par(mar = c(1, 4, 1, 4))
  plot.new()
  
  # Legenda explicativa
  legend("center", 
         legend = c("-1.0 Correlação Negativa Perfeita", 
                    "0.0 Sem Correlação", 
                    "+1.0 Correlação Positiva Perfeita"),
         fill = colorRampPalette(c("blue", "white", "red"))(3),
         border = NA,
         bty = "n",
         horiz = TRUE,
         cex = 0.8,
         xpd = TRUE)
  
  # Restaurar parâmetros gráficos originais
  par(op)
  
  # Adicionar informação adicional
  mtext(paste("Número de variáveis:", ncol(corr_matrix), 
              "| Número de observações:", nrow(df_clean)), 
        side = 1, line = 0, cex = 0.7, outer = TRUE)
}