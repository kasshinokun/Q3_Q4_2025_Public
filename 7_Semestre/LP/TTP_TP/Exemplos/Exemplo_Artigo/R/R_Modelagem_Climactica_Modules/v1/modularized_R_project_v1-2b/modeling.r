# --- Funções de Modelagem ---

# Função para treinar e avaliar o modelo de regressão linear
train_linear_model <- function(df_clean) {
  
  # 1. Preparação dos dados
  # Usar BIO1 (Temperatura Média Anual) como variável dependente
  # Usar BIO12 (Precipitação Anual) como variável independente
  data_model <- df_clean %>% select(bio1, bio12) %>% na.omit()
  
  # Divisão dos dados (70% treino, 30% teste)
  set.seed(42) # Para reprodutibilidade
  split <- rsample::initial_split(data_model, prop = 0.7)
  train_data <- rsample::training(split)
  test_data <- rsample::testing(split)
  
  # 2. Treinamento do Modelo de Regressão Linear
  model <- lm(bio1 ~ bio12, data = train_data)
  
  # 3. Previsões e Avaliação
  predictions <- predict(model, newdata = test_data)
  
  # Cálculo do R-quadrado
  r_squared <- summary(model)$r.squared
  
  # Cálculo do RMSE (Root Mean Squared Error)
  rmse <- sqrt(mean((test_data$bio1 - predictions)^2))
  
  # Armazenar métricas para exibição
  metrics <- list(
    r_squared = r_squared,
    rmse = rmse,
    n_train = nrow(train_data),
    n_test = nrow(test_data)
  )
  
  return(list(
    model = model,
    predictions = predictions,
    test_data = test_data,
    metrics = metrics
  ))
}

# Função para renderizar o resumo do modelo
render_model_summary <- function(model) {
  summary(model)
}

# Função para renderizar as métricas de avaliação
render_model_metrics <- function(metrics) {
  tagList(
    h4("Métricas de Avaliação (Conjunto de Teste)"),
    tags$ul(
      tags$li(strong("R-quadrado:"), round(metrics$r_squared, 4)),
      tags$li(strong("RMSE (Erro Quadrático Médio):"), round(metrics$rmse, 4)),
      tags$li(strong("Tamanho do Conjunto de Treino:"), metrics$n_train),
      tags$li(strong("Tamanho do Conjunto de Teste:"), metrics$n_test)
    )
  )
}
