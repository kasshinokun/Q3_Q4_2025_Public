# data_processing.R

#' @title Funções de Processamento de Dados Climáticos
#' @description Módulo responsável pelo download, extração e processamento dos dados WorldClim

# Configurações iniciais
DATA_DIR <- "r_climatica_data"  # Diretório alterado para /r_climatica_data
ZIP_URL <- "http://www.dpi.inpe.br/amb_data/AmericaSul/SAmerica_WCLIM.zip"
ZIP_FILENAME <- "SAmerica_WCLIM.zip"
LOG_FILE <- file.path(DATA_DIR, "model_creation.log")

# Configurações de timeout (5 minutos = 300 segundos)
DOWNLOAD_TIMEOUT <- 300  # 5 minutos em segundos

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

#' Download robusto do arquivo ZIP com timeout configurável
#' @param url URL do arquivo ZIP
#' @param target_dir Diretório de destino
#' @param zip_filename Nome do arquivo ZIP
#' @param timeout Timeout em segundos (usa DOWNLOAD_TIMEOUT por padrão)
#' @param max_retries Número máximo de tentativas (padrão: 3)
#' @return TRUE se bem-sucedido, FALSE caso contrário
download_zip_file <- function(url = ZIP_URL, target_dir = DATA_DIR, 
                             zip_filename = ZIP_FILENAME, 
                             timeout = DOWNLOAD_TIMEOUT, 
                             max_retries = 3) {
  
  # Criar diretório se não existir
  if (!dir.exists(target_dir)) {
    dir.create(target_dir, recursive = TRUE, showWarnings = FALSE)
  }
  
  target_zip <- file.path(target_dir, zip_filename)
  
  for (attempt in 1:max_retries) {
    tryCatch({
      # Configurar timeout
      old_timeout <- getOption("timeout")
      options(timeout = timeout)
      
      message(paste("Tentativa", attempt, "/", max_retries, 
                    "- Timeout:", timeout, "segundos"))
      
      # Método 1: Tentar com download.file primeiro
      if (attempt == 1) {
        message("Método: download.file")
        download.file(url, target_zip, mode = "wb", quiet = FALSE)
      }
      # Método 2: Tentar com curl se disponível
      else if (attempt == 2) {
        if (requireNamespace("curl", quietly = TRUE)) {
          message("Método: curl")
          curl::curl_download(url, target_zip, quiet = FALSE)
        } else {
          message("curl não disponível. Tentando download.file novamente...")
          download.file(url, target_zip, mode = "wb", quiet = FALSE)
        }
      }
      # Método 3: Tentar com httr
      else if (attempt == 3) {
        if (requireNamespace("httr", quietly = TRUE)) {
          message("Método: httr")
          response <- httr::GET(url, 
                               httr::write_disk(target_zip, overwrite = TRUE), 
                               httr::progress(),
                               httr::timeout(timeout))
          if (httr::http_error(response)) {
            stop("Erro HTTP: ", httr::status_code(response))
          }
        } else {
          message("httr não disponível. Tentando download.file novamente...")
          download.file(url, target_zip, mode = "wb", quiet = FALSE)
        }
      }
      
      # Verificar se o arquivo foi baixado completamente
      if (file.exists(target_zip)) {
        file_size <- file.info(target_zip)$size
        message(paste("Arquivo baixado. Tamanho:", 
                      format(file_size, big.mark = ","), "bytes"))
        
        # Tamanho mínimo esperado (ajuste conforme necessário)
        expected_min_size <- 30000000  # 30MB
        if (file_size >= expected_min_size) {
          message("Download concluído com sucesso!")
          options(timeout = old_timeout)
          return(TRUE)
        } else {
          message(paste("Arquivo muito pequeno. Esperado:", 
                        format(expected_min_size, big.mark = ","), 
                        "bytes, Obtido:", format(file_size, big.mark = ","), "bytes"))
          file.remove(target_zip)
        }
      }
      
    }, error = function(e) {
      message(paste("Erro na tentativa", attempt, ":", e$message))
      # Limpar arquivo parcial em caso de erro
      if (file.exists(target_zip)) {
        file.remove(target_zip)
      }
    }, finally = {
      options(timeout = old_timeout)
    })
    
    # Aguardar antes de tentar novamente (com aumento exponencial)
    if (attempt < max_retries) {
      wait_time <- 2 ^ attempt  # 2, 4, 8... segundos
      message(paste("Aguardando", wait_time, "segundos antes da próxima tentativa..."))
      Sys.sleep(wait_time)
    }
  }
  
  message("Falha em todas as tentativas de download")
  return(FALSE)
}

#' Verificar se o arquivo ZIP já existe no diretório
#' @param target_dir Diretório de destino
#' @param zip_filename Nome do arquivo ZIP
#' @param min_size Tamanho mínimo esperado em bytes
#' @return TRUE se arquivo existe e tem tamanho adequado, FALSE caso contrário
check_zip_exists <- function(target_dir = DATA_DIR, 
                            zip_filename = ZIP_FILENAME, 
                            min_size = 30000000) {
  
  zip_path <- file.path(target_dir, zip_filename)
  
  if (!file.exists(zip_path)) {
    message(paste("Arquivo ZIP não encontrado em:", zip_path))
    return(FALSE)
  }
  
  file_size <- file.info(zip_path)$size
  message(paste("Arquivo ZIP encontrado. Tamanho:", 
                format(file_size, big.mark = ","), "bytes"))
  
  if (file_size >= min_size) {
    message("Arquivo ZIP parece completo")
    return(TRUE)
  } else {
    message(paste("Arquivo ZIP muito pequeno. Necessário:", 
                  format(min_size, big.mark = ","),
                  "bytes, Obtido:", format(file_size, big.mark = ","), "bytes"))
    return(FALSE)
  }
}

#' Descompactar arquivo ZIP
#' @param zip_path Caminho do arquivo ZIP
#' @param target_dir Diretório de destino
#' @return TRUE se bem-sucedido, FALSE caso contrário
unzip_data_file <- function(zip_path, target_dir = DATA_DIR) {
  tryCatch({
    # Verificar se o arquivo ZIP é válido
    if (!file.exists(zip_path)) {
      stop("Arquivo ZIP não encontrado: ", zip_path)
    }
    
    message("Descompactando arquivos...")
    
    # Listar arquivos no ZIP
    zip_info <- unzip(zip_path, list = TRUE)
    file_list <- zip_info$Name
    message(paste("Encontrados", length(file_list), "arquivos no ZIP"))
    
    # Mostrar alguns arquivos como exemplo
    if (length(file_list) > 0) {
      message("Primeiros 5 arquivos:")
      for (i in 1:min(5, length(file_list))) {
        message(paste("  ", file_list[i]))
      }
      if (length(file_list) > 5) {
        message(paste("  ... e mais", length(file_list) - 5, "arquivos"))
      }
    }
    
    # Descompactar arquivos
    message("Extraindo arquivos...")
    unzip(zip_path, exdir = target_dir)
    
    # Verificar se os arquivos foram extraídos
    extracted_files <- list.files(target_dir, recursive = TRUE, full.names = TRUE)
    asc_files <- list.files(target_dir, pattern = "\\.asc$", recursive = TRUE, full.names = TRUE)
    
    message(paste("Extraídos", length(extracted_files), "arquivos no total"))
    message(paste("Arquivos .asc:", length(asc_files)))
    
    if (length(asc_files) > 0) {
      message("Arquivos .asc encontrados:")
      for (i in 1:min(5, length(asc_files))) {
        message(paste("  ", basename(asc_files[i])))
      }
      if (length(asc_files) > 5) {
        message(paste("  ... e mais", length(asc_files) - 5, "arquivos .asc"))
      }
    }
    
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
    "\nTIMESTAMP:", as.integer(Sys.time()),
    "\nDOWNLOAD_TIMEOUT:", DOWNLOAD_TIMEOUT
  )
  
  tryCatch({
    writeLines(log_content, log_file)
    message("Log criado com sucesso")
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
    message("Log não encontrado")
    return(FALSE)
  }
  
  tryCatch({
    log_content <- readLines(log_file)
    model_created <- any(grepl("CREATED:\\s*TRUE", log_content, ignore.case = TRUE))
    
    if (model_created) {
      # Verificar se os arquivos ASC existem
      asc_files <- list.files(data_dir, pattern = "\\.asc$", full.names = TRUE)
      message(paste("Validando modelo existente..."))
      message(paste("Arquivos .asc encontrados:", length(asc_files)))
      
      # Filtrar apenas arquivos climáticos
      clim_files <- asc_files[!basename(asc_files) %in% 
                               c('alt.asc', 'decl.asc', 
                                 '110914_DadosWorldClim_SouthAmerica_25.txt')]
      
      message(paste("Arquivos climáticos:", length(clim_files)))
      
      if (length(clim_files) >= 10) { # Espera-se pelo menos 10 arquivos climáticos
        message("Modelo existente validado com sucesso")
        return(TRUE)
      } else {
        message(paste("Modelo incompleto. Apenas", length(clim_files), 
                      "arquivos climáticos encontrados (mínimo: 10)"))
        return(FALSE)
      }
    } else {
      message("Log indica que modelo não foi criado")
      return(FALSE)
    }
  }, error = function(e) {
    warning(paste("Erro ao validar modelo existente:", e$message))
    return(FALSE)
  })
}

#' Função principal: Orquestrar download e processamento
#' @param url URL do arquivo ZIP
#' @param target_dir Diretório de destino
#' @param zip_filename Nome do arquivo ZIP
#' @param timeout Timeout para download
#' @return TRUE se bem-sucedido, FALSE caso contrário
download_and_process_data <- function(url = ZIP_URL, target_dir = DATA_DIR, 
                                     zip_filename = ZIP_FILENAME,
                                     timeout = DOWNLOAD_TIMEOUT) {
  
  message("==================================================")
  message("PROCESSAMENTO DE DADOS CLIMÁTICOS")
  message("==================================================")
  
  # Verificar status atual
  status <- check_data_status(target_dir, zip_filename)
  
  message(paste("Status inicial:"))
  message(paste("  • Diretório:", ifelse(status$dir_exists, "Existe", "Não existe")))
  message(paste("  • Arquivo ZIP:", ifelse(status$zip_exists, "Existe", "Não existe")))
  message(paste("  • Log:", ifelse(status$log_exists, "Existe", "Não existe")))
  message(paste("  • Modelo criado:", ifelse(status$model_created, "Sim", "Não")))
  
  # Se modelo já foi criado e validado, retornar TRUE
  if (status$model_created) {
    message("\nValidando modelo existente...")
    if (validate_existing_model(target_dir)) {
      message("Usando dados existentes do diretório:", target_dir)
      return(TRUE)
    } else {
      message("Modelo existente não é válido. Processando novamente...")
    }
  }
  
  # Verificar se o arquivo ZIP já existe e é válido
  zip_path <- file.path(target_dir, zip_filename)
  if (status$zip_exists && check_zip_exists(target_dir, zip_filename)) {
    message("\nUsando arquivo ZIP existente:", zip_path)
  } else {
    message(paste("\nArquivo ZIP não encontrado ou inválido em:", target_dir))
    message(paste("Baixando de:", url))
    message(paste("Timeout configurado:", timeout, "segundos"))
    
    # Instalar pacotes necessários se não estiverem instalados
    message("\nVerificando pacotes necessários...")
    required_packages <- c("curl", "httr")
    for (pkg in required_packages) {
      if (!requireNamespace(pkg, quietly = TRUE)) {
        message(paste("  • Instalando", pkg, "..."))
        install.packages(pkg, quiet = TRUE, repos = "https://cloud.r-project.org")
      } else {
        message(paste("  •", pkg, "já instalado"))
      }
    }
    
    # Realizar download
    download_success <- download_zip_file(url, target_dir, zip_filename, timeout)
    if (!download_success) {
      message("Falha no download do arquivo ZIP")
      return(FALSE)
    }
  }
  
  # Descompactar dados
  message("\nDescompactando arquivos...")
  unzip_success <- unzip_data_file(zip_path, target_dir)
  if (!unzip_success) {
    message("Falha na descompactação")
    return(FALSE)
  }
  
  # Criar log do modelo
  message("\nCriando log do processamento...")
  log_success <- create_model_log(target_dir, TRUE)
  
  message("\n==================================================")
  message("PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
  message(paste("Dados disponíveis em:", target_dir))
  message("==================================================")
  
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
#' @param show_progress Mostrar progresso (padrão: TRUE)
#' @return DataFrame com dados processados
process_worldclim_data <- function(data_dir = DATA_DIR, show_progress = TRUE) {
  
  message("Processando dados WorldClim...")
  
  # Processa todos os arquivos WorldClim (.asc) no diretório
  if (!dir.exists(data_dir)) {
    warning(paste("Diretório não encontrado:", data_dir))
    return(NULL)
  }
  
  # Listar arquivos .asc, excluindo arquivos não climáticos
  asc_files <- list.files(data_dir, pattern = "\\.asc$", full.names = TRUE)
  files_to_process <- asc_files[!basename(asc_files) %in% 
                                 c('alt.asc', 'decl.asc', 
                                   '110914_DadosWorldClim_SouthAmerica_25.txt')]
  
  if (length(files_to_process) == 0) {
    warning("Nenhum arquivo .asc de variáveis climáticas encontrado")
    return(NULL)
  }
  
  message(paste("Encontrados", length(files_to_process), "arquivos para processar"))
  
  all_data <- list()
  
  # Processar primeiro arquivo para obter estrutura
  first_file <- files_to_process[1]
  message(paste("Arquivo de referência:", basename(first_file)))
  
  first_result <- read_asc_file(first_file)
  if (is.null(first_result)) return(NULL)
  
  rows <- first_result$header$nrows
  cols <- first_result$header$ncols
  nodata_value <- first_result$header$NODATA_value %||% -9999
  
  message(paste("Dimensões da grade:", rows, "x", cols))
  message(paste("Valor NODATA:", nodata_value))
  
  # Adicionar primeiro conjunto de dados
  var_name <- tools::file_path_sans_ext(basename(first_file))
  all_data[[var_name]] <- as.vector(first_result$data)
  
  # Processar arquivos restantes
  if (length(files_to_process) > 1) {
    for (i in 2:length(files_to_process)) {
      filepath <- files_to_process[i]
      
      if (show_progress && i %% 5 == 0) {
        message(paste("Processando", i, "de", length(files_to_process), 
                      "arquivos..."))
      }
      
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
  }
  
  # Criar DataFrame
  message("Criando DataFrame...")
  df <- as.data.frame(all_data)
  
  # Adicionar coordenadas
  df$row <- rep(1:rows, each = cols)
  df$col <- rep(1:cols, times = rows)
  
  # Reordenar colunas
  df <- df %>% dplyr::select(row, col, everything())
  
  # Remover valores NODATA
  message("Removendo valores NODATA...")
  df_clean <- df[!rowSums(df == nodata_value, na.rm = TRUE) > 0, ]
  
  message(paste("Processamento concluído."))
  message(paste("Pontos de dados válidos:", nrow(df_clean)))
  message(paste("Variáveis:", ncol(df_clean) - 2, "variáveis climáticas"))
  
  return(df_clean)
}