# modeling.R

#' @title Funções de Modelagem Climática
#' @description Módulo responsável pela modelagem estatística dos dados climáticos

library(dplyr)
library(rsample)

#' Treinar modelo de regressão linear
#' @param df DataFrame com dados processados
#' @param target_var Variável alvo (padrão: bio1)
#' @param predictor_var Variável preditora (padrão: bio12)
#' @param prop Proporção para divisão treino/teste (padrão: 0.7)
#' @param seed Semente para reprodutibilidade (padrão: 42)
#' @return Lista com modelo, previsões, dados de teste e métricas
train_linear_regression <- function(df, target_var = "bio1", predictor_var = "bio12", prop = 0.7, seed = 42) {
  # Preparação dos dados
  data_model <- df %>% 
    dplyr::select(!!sym(target_var), !!sym(predictor_var)) %>% 
    na.omit()
  
  # Divisão dos dados
  set.seed(seed)
  split <- rsample::initial_split(data_model, prop = prop)
  train_data <- rsample::training(split)
  test_data <- rsample::testing(split)
  
  # Treinamento do Modelo de Regressão Linear
  formula <- as.formula(paste(target_var, "~", predictor_var))
  model <- lm(formula, data = train_data)
  
  # Previsões
  predictions <- predict(model, newdata = test_data)
  
  # Cálculo das métricas
  r_squared <- summary(model)$r.squared
  rmse <- sqrt(mean((test_data[[target_var]] - predictions)^2))
  
  # Cálculo do MAE (Mean Absolute Error)
  mae <- mean(abs(test_data[[target_var]] - predictions))
  
  # Coeficientes do modelo
  coefficients <- coef(model)
  
  metrics <- list(
    r_squared = r_squared,
    rmse = rmse,
    mae = mae,
    n_train = nrow(train_data),
    n_test = nrow(test_data),
    coefficients = coefficients
  )
  
  return(list(
    model = model,
    predictions = predictions,
    test_data = test_data,
    metrics = metrics
  ))
}

#' Gerar resumo do modelo formatado para UI
#' @param model_result Resultado do modelo de train_linear_regression
#' @return Lista com resumos formatados
get_model_summary <- function(model_result) {
  model <- model_result$model
  metrics <- model_result$metrics
  
  # Resumo estatístico
  model_summary <- summary(model)
  
  # Texto interpretativo
  interpretation <- paste(
    "O modelo explica", round(metrics$r_squared * 100, 2), 
    "% da variância na variável alvo.",
    "\n\nPara cada unidade de aumento na variável preditora,",
    "a variável alvo muda em", round(metrics$coefficients[2], 4), "unidades.",
    "\n\nO erro médio de previsão (RMSE) é de", round(metrics$rmse, 2), "unidades."
  )
  
  return(list(
    summary = model_summary,
    metrics = metrics,
    interpretation = interpretation
  ))
}

#' Calcular estatísticas descritivas
#' @param df DataFrame com dados
#' @param exclude_cols Colunas a excluir da análise
#' @return DataFrame com estatísticas
calculate_descriptive_stats <- function(df, exclude_cols = c("row", "col")) {
  # Selecionar apenas as colunas bioclimáticas
  bio_cols <- names(df)[!names(df) %in% exclude_cols]
  
  stats <- df %>%
    dplyr::select(dplyr::all_of(bio_cols)) %>%
    dplyr::summarise_all(list(
      Média = ~mean(., na.rm = TRUE),
      Mediana = ~median(., na.rm = TRUE),
      DP = ~sd(., na.rm = TRUE),
      Mín = ~min(., na.rm = TRUE),
      Máx = ~max(., na.rm = TRUE),
      Q1 = ~quantile(., 0.25, na.rm = TRUE),
      Q3 = ~quantile(., 0.75, na.rm = TRUE),
      NAs = ~sum(is.na(.))
    )) %>%
    t() %>%
    as.data.frame()
  
  colnames(stats) <- "Valor"
  stats$Variável <- rownames(stats)
  stats <- stats %>% dplyr::select(Variável, Valor)
  
  return(stats)
}

#' Calcular matriz de correlação
#' @param df DataFrame com dados
#' @param exclude_cols Colunas a excluir
#' @return Matriz de correlação
calculate_correlation_matrix <- function(df, exclude_cols = c("row", "col")) {
  bio_cols <- names(df)[!names(df) %in% exclude_cols]
  corr_matrix <- cor(df %>% dplyr::select(dplyr::all_of(bio_cols)), use = "complete.obs")
  return(corr_matrix)
}