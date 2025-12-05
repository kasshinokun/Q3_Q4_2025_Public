# data_processing.R

#' @title Funções de Processamento de Dados Climáticos
#' @description Módulo responsável pelo download, extração e processamento dos dados WorldClim

# Configurações iniciais
DATA_DIR <- "r_climatica_data"
ZIP_URL <- "http://www.dpi.inpe.br/amb_data/AmericaSul/SAmerica_WCLIM.zip"
ZIP_FILENAME <- "SAmerica_WCLIM.zip"
LOG_FILE <- file.path(DATA_DIR, "model_creation.log")

# Função auxiliar para o operador %||% (se não for nulo, use o valor, senão use o padrão)
`%||%` <- function(a, b) {
  if (!is.null(a)) a else b
}

#' Verificar status dos dados
#' @param data_dir Diretório dos dados
#' @param zip_filename Nome do arquivo ZIP
#' @return Lista com status dos arquivos
check_data_status <- function(data_dir = DATA_DIR, zip_filename = ZIP_FILENAME) {
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

#' Download do arquivo ZIP
#' @param url URL do arquivo ZIP
#' @param target_dir Diretório de destino
#' @param zip_filename Nome do arquivo ZIP
#' @return TRUE se bem-sucedido, FALSE caso contrário
download_zip_file <- function(url = ZIP_URL, target_dir = DATA_DIR, zip_filename = ZIP_FILENAME) {
  tryCatch({
    # Criar diretório se não existir
    if (!dir.exists(target_dir)) {
      dir.create(target_dir, recursive = TRUE, showWarnings = FALSE)
    }
    
    temp_zip <- tempfile(fileext = ".zip")
    
    # Download com barra de progresso
    download.file(url, temp_zip, mode = "wb", quiet = TRUE)
    
    # Mover arquivo para o diretório destino
    target_zip <- file.path(target_dir, zip_filename)
    file.copy(temp_zip, target_zip, overwrite = TRUE)
    file.remove(temp_zip)
    
    return(TRUE)
  }, error = function(e) {
    warning(paste("Erro durante o download:", e$message))
    return(FALSE)
  })
}

#' Descompactar arquivo ZIP
#' @param zip_path Caminho do arquivo ZIP
#' @param target_dir Diretório de destino
#' @return TRUE se bem-sucedido, FALSE caso contrário
unzip_data_file <- function(zip_path, target_dir = DATA_DIR) {
  tryCatch({
    # Descompactar arquivos
    unzip(zip_path, exdir = target_dir)
    return(TRUE)
  }, error = function(e) {
    warning(paste("Erro durante descompactação:", e$message))
    return(FALSE)
  })
}

#' Criar arquivo de log
#' @param data_dir Diretório dos dados
#' @param status Status do processamento
#' @return TRUE se bem-sucedido, FALSE caso contrário
create_model_log <- function(data_dir = DATA_DIR, status = TRUE) {
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
    warning(paste("Erro ao criar arquivo de log:", e$message))
    return(FALSE)
  })
}

#' Validar modelo existente
#' @param data_dir Diretório dos dados
#' @return TRUE se válido, FALSE caso contrário
validate_existing_model <- function(data_dir = DATA_DIR) {
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
        return(TRUE)
      } else {
        return(FALSE)
      }
    } else {
      return(FALSE)
    }
  }, error = function(e) {
    warning("Erro ao validar modelo existente")
    return(FALSE)
  })
}

#' Função principal: Orquestrar download e processamento
#' @param url URL do arquivo ZIP
#' @param target_dir Diretório de destino
#' @param zip_filename Nome do arquivo ZIP
#' @return TRUE se bem-sucedido, FALSE caso contrário
download_and_process_data <- function(url = ZIP_URL, target_dir = DATA_DIR, zip_filename = ZIP_FILENAME) {
  # Verificar status atual
  status <- check_data_status(target_dir, zip_filename)
  
  # Se modelo já foi criado e validado, retornar TRUE
  if (status$model_created && validate_existing_model(target_dir)) {
    return(TRUE)
  }
  
  if (!status$zip_exists || !status$dir_exists) {
    download_success <- download_zip_file(url, target_dir, zip_filename)
    if (!download_success) return(FALSE)
    status$zip_exists <- TRUE # Atualiza status
  }
  
  # Descompactar dados
  zip_path <- file.path(target_dir, zip_filename)
  unzip_success <- unzip_data_file(zip_path, target_dir)
  if (!unzip_success) return(FALSE)
  
  # Criar log do modelo
  log_success <- create_model_log(target_dir, TRUE)
  
  return(TRUE)
}

#' Ler arquivo ASCII Grid (.asc)
#' @param filepath Caminho do arquivo
#' @return Lista com cabeçalho e dados
read_asc_file <- function(filepath) {
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
    warning(paste("Erro ao ler arquivo", basename(filepath), ":", e$message))
    return(NULL)
  })
}

#' Processar dados WorldClim
#' @param data_dir Diretório dos dados
#' @return DataFrame com dados processados
process_worldclim_data <- function(data_dir = DATA_DIR) {
  # Processa todos os arquivos WorldClim (.asc) no diretório
  if (!dir.exists(data_dir)) {
    warning(paste("Diretório não encontrado:", data_dir))
    return(NULL)
  }
  
  # Listar arquivos .asc, excluindo arquivos não climáticos
  asc_files <- list.files(data_dir, pattern = "\\.asc$", full.names = TRUE)
  files_to_process <- asc_files[!basename(asc_files) %in% c('alt.asc', 'decl.asc', '110914_DadosWorldClim_SouthAmerica_25.txt')]
  
  if (length(files_to_process) == 0) {
    warning("Nenhum arquivo .asc de variáveis climáticas encontrado")
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
      warning(paste("Dimensões não correspondem para", basename(filepath)))
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
  df <- df %>% dplyr::select(row, col, everything())
  
  # Remover valores NODATA
  df_clean <- df[!rowSums(df == nodata_value, na.rm = TRUE) > 0, ]
  
  return(df_clean)
}