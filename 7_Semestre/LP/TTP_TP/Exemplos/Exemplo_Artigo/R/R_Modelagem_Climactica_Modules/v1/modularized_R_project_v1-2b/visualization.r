# --- Funções de Visualização ---

# Histograma BIO1
plot_bio1_hist <- function(df_clean) {
  ggplot(df_clean, aes(x = bio1)) +
    geom_histogram(aes(y = after_stat(density)), bins = 30, fill = "skyblue", alpha = 0.7) +
    geom_density(color = "darkblue", linewidth = 1) +
    labs(title = "Distribuição de BIO1 (Temperatura Média Anual)",
         x = "BIO1 (x 10 °C)", y = "Densidade") +
    theme_minimal()
}

# Dispersão BIO1 vs BIO12
plot_bio1_bio12_scatter <- function(df_clean) {
  # Amostra para evitar sobrecarga de plotagem
  sample_data <- df_clean %>% dplyr::sample_n(min(5000, nrow(df_clean)))
  
  ggplot(sample_data, aes(x = bio12, y = bio1)) +
    geom_point(alpha = 0.5, color = "darkred") +
    labs(title = "BIO1 vs BIO12 (Amostra)",
         x = "BIO12 (mm)", y = "BIO1 (x 10 °C)") +
    theme_minimal()
}

# Gráfico de resíduos
plot_residuals <- function(predictions, test_data) {
  residuals <- test_data$bio1 - predictions
  
  ggplot(data.frame(residuals = residuals), aes(x = residuals)) +
    geom_histogram(aes(y = after_stat(density)), bins = 30, fill = "lightgreen", alpha = 0.7) +
    geom_density(color = "darkgreen", linewidth = 1) +
    labs(title = "Distribuição dos Resíduos",
         x = "Resíduos (y_test - y_pred)", y = "Densidade") +
    theme_minimal()
}

# Valores reais vs preditos
plot_pred_vs_actual <- function(predictions, test_data) {
  plot_data <- data.frame(
    Actual = test_data$bio1,
    Predicted = predictions
  )
  
  ggplot(plot_data, aes(x = Actual, y = Predicted)) +
    geom_point(alpha = 0.5, color = "purple") +
    geom_abline(slope = 1, intercept = 0, color = "red", linetype = "dashed", linewidth = 1) +
    labs(title = "Valores Reais vs Preditos",
         x = "Valores Reais", y = "Valores Preditos") +
    theme_minimal()
}
