# visualization.R

#' @title Funções de Visualização de Dados Climáticos
#' @description Módulo responsável por gráficos e visualizações

library(ggplot2)
library(corrplot)

#' Criar histograma de distribuição
#' @param df DataFrame com dados
#' @param var Nome da variável
#' @param bins Número de bins (padrão: 30)
#' @param fill_color Cor do preenchimento (padrão: "skyblue")
#' @param line_color Cor da linha (padrão: "darkblue")
#' @return Objeto ggplot
create_histogram <- function(df, var, bins = 30, fill_color = "skyblue", line_color = "darkblue") {
  ggplot(df, aes(x = !!sym(var))) +
    geom_histogram(aes(y = after_stat(density)), bins = bins, fill = fill_color, alpha = 0.7) +
    geom_density(color = line_color, linewidth = 1) +
    labs(title = paste("Distribuição de", toupper(var)),
         x = paste(var, "(unidades originais)"), y = "Densidade") +
    theme_minimal()
}

#' Criar gráfico de dispersão
#' @param df DataFrame com dados
#' @param x_var Variável no eixo X
#' @param y_var Variável no eixo Y
#' @param max_points Número máximo de pontos (padrão: 5000)
#' @param point_color Cor dos pontos (padrão: "darkred")
#' @param alpha Transparência (padrão: 0.5)
#' @return Objeto ggplot
create_scatterplot <- function(df, x_var, y_var, max_points = 5000, point_color = "darkred", alpha = 0.5) {
  # Amostrar dados se necessário
  if (nrow(df) > max_points) {
    plot_data <- df %>% dplyr::sample_n(min(max_points, nrow(df)))
  } else {
    plot_data <- df
  }
  
  ggplot(plot_data, aes(x = !!sym(x_var), y = !!sym(y_var))) +
    geom_point(alpha = alpha, color = point_color) +
    labs(title = paste(toupper(y_var), "vs", toupper(x_var)),
         x = paste(x_var, "(unidades originais)"), 
         y = paste(y_var, "(unidades originais)")) +
    theme_minimal()
}

#' Criar gráfico de resíduos
#' @param actual Valores reais
#' @param predicted Valores preditos
#' @param bins Número de bins (padrão: 30)
#' @param fill_color Cor do preenchimento (padrão: "lightgreen")
#' @param line_color Cor da linha (padrão: "darkgreen")
#' @return Objeto ggplot
create_residuals_plot <- function(actual, predicted, bins = 30, fill_color = "lightgreen", line_color = "darkgreen") {
  residuals <- actual - predicted
  
  ggplot(data.frame(residuals = residuals), aes(x = residuals)) +
    geom_histogram(aes(y = after_stat(density)), bins = bins, fill = fill_color, alpha = 0.7) +
    geom_density(color = line_color, linewidth = 1) +
    labs(title = "Distribuição dos Resíduos",
         x = "Resíduos (y_test - y_pred)", y = "Densidade") +
    theme_minimal() +
    geom_vline(xintercept = 0, linetype = "dashed", color = "red")
}

#' Criar gráfico de valores reais vs preditos
#' @param actual Valores reais
#' @param predicted Valores preditos
#' @param point_color Cor dos pontos (padrão: "purple")
#' @param alpha Transparência (padrão: 0.5)
#' @return Objeto ggplot
create_pred_vs_actual_plot <- function(actual, predicted, point_color = "purple", alpha = 0.5) {
  plot_data <- data.frame(Actual = actual, Predicted = predicted)
  
  ggplot(plot_data, aes(x = Actual, y = Predicted)) +
    geom_point(alpha = alpha, color = point_color) +
    geom_abline(slope = 1, intercept = 0, color = "red", linetype = "dashed", linewidth = 1) +
    labs(title = "Valores Reais vs Preditos",
         x = "Valores Reais", y = "Valores Preditos") +
    theme_minimal()
}

#' Criar matriz de correlação
#' @param corr_matrix Matriz de correlação
#' @param method Método de visualização (padrão: "color")
#' @param type Tipo de visualização (padrão: "upper")
#' @param tl_col Cor dos rótulos (padrão: "black")
#' @param tl_srt Ângulo dos rótulos (padrão: 45)
#' @param title Título do gráfico
#' @return Objeto de plot corrplot
create_correlation_plot <- function(corr_matrix, method = "color", type = "upper", 
                                   tl_col = "black", tl_srt = 45, 
                                   title = "Matriz de Correlação das Variáveis Bioclimáticas") {
  corrplot(corr_matrix, method = method, type = type, 
           tl.col = tl_col, tl.srt = tl_srt, addCoef.col = "black", 
           title = title, mar = c(0, 0, 1, 0))
}

#' Exibir métricas do modelo formatadas
#' @param metrics Lista com métricas do modelo
#' @return Lista HTML formatada
display_model_metrics <- function(metrics) {
  tagList(
    h4("Métricas de Avaliação (Conjunto de Teste)"),
    tags$ul(
      tags$li(strong("R-quadrado:"), round(metrics$r_squared, 4)),
      tags$li(strong("RMSE (Erro Quadrático Médio):"), round(metrics$rmse, 4)),
      tags$li(strong("MAE (Erro Absoluto Médio):"), round(metrics$mae, 4)),
      tags$li(strong("Tamanho do Conjunto de Treino:"), metrics$n_train),
      tags$li(strong("Tamanho do Conjunto de Teste:"), metrics$n_test)
    ),
    h4("Coeficientes do Modelo"),
    tags$ul(
      tags$li(strong("Intercepto:"), round(metrics$coefficients[1], 4)),
      tags$li(strong("Coeficiente:"), round(metrics$coefficients[2], 4))
    )
  )
}