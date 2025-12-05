import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

class Visualizer:
    def __init__(self):
        pass

    def plot_data_distribution(self, df_clean: pd.DataFrame):
        """
        Gera e exibe o histograma da distribuição da Temperatura Média Anual (BIO1)
        e o gráfico de dispersão BIO1 vs BIO12.
        """
        st.subheader("Visualização dos Dados Climáticos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Histograma BIO1
            st.markdown("**Distribuição da Temperatura Média Anual (BIO1)**")
            fig1, ax1 = plt.subplots()
            sns.histplot(df_clean['bio1'], kde=True, ax=ax1, color='skyblue')
            ax1.set_title('Distribuição de BIO1 (Temperatura Média Anual)')
            ax1.set_xlabel('BIO1 (x 10 °C)')
            ax1.set_ylabel('Densidade')
            st.pyplot(fig1)
        
        with col2:
            # Dispersão BIO1 vs BIO12
            st.markdown("**Relação entre BIO1 e BIO12**")
            # Amostra para evitar sobrecarga de plotagem
            sample_data = df_clean.sample(n=min(5000, len(df_clean)), random_state=42)
            fig2, ax2 = plt.subplots()
            sns.scatterplot(x='bio12', y='bio1', data=sample_data, alpha=0.5, ax=ax2, color='darkred')
            ax2.set_title('BIO1 vs BIO12 (Amostra)')
            ax2.set_xlabel('BIO12 (mm)')
            ax2.set_ylabel('BIO1 (x 10 °C)')
            st.pyplot(fig2)

    def plot_model_diagnostics(self, y_test: pd.Series, predictions: np.ndarray):
        """
        Gera e exibe os gráficos de diagnóstico do modelo:
        - Distribuição dos resíduos
        - Valores reais vs preditos
        """
        st.subheader("Visualização do Modelo")
        
        col1, col2 = st.columns(2)
        
        residuals = y_test - predictions
        
        with col1:
            # Distribuição dos resíduos
            st.markdown("**Distribuição dos Resíduos do Modelo**")
            fig3, ax3 = plt.subplots()
            sns.histplot(residuals, kde=True, ax=ax3, color='lightgreen')
            ax3.set_title('Distribuição dos Resíduos')
            ax3.set_xlabel('Resíduos (y_test - y_pred)')
            ax3.set_ylabel('Densidade')
            st.pyplot(fig3)
        
        with col2:
            # Valores reais vs preditos
            st.markdown("**Valores Reais vs Preditos**")
            fig4, ax4 = plt.subplots()
            ax4.scatter(y_test, predictions, alpha=0.5, color='purple')
            # Linha 45 graus (y=x)
            min_val = min(y_test.min(), predictions.min())
            max_val = max(y_test.max(), predictions.max())
            ax4.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2)
            ax4.set_xlabel('Valores Reais')
            ax4.set_ylabel('Valores Preditos')
            ax4.set_title('Valores Reais vs Preditos')
            st.pyplot(fig4)

    def display_metrics(self, metrics: dict):
        """Exibe as métricas do modelo em formato de colunas no Streamlit."""
        st.subheader("📈 Métricas de Avaliação do Modelo")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("R² (R-Squared)", f"{metrics['r_squared']:.4f}", 
                     help="Coeficiente de Determinação")
        with col2:
            st.metric("RMSE (Root Mean Squared Error)", f"{metrics['rmse']:.4f}", 
                     help="Raiz do Erro Quadrático Médio")
        with col3:
            st.metric("MAE (Mean Absolute Error)", f"{metrics['mae']:.4f}", 
                     help="Erro Absoluto Médio")

        st.subheader("📊 Coeficientes do Modelo")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("BIO12 (Precipitação Anual)", f"{metrics['coefficients']['bio12']:.4f}", 
                     help="Coeficiente para BIO12")
        with col2:
            st.metric("BIO4 (Sazonalidade da Temperatura)", f"{metrics['coefficients']['bio4']:.4f}", 
                     help="Coeficiente para BIO4")
        with col3:
            st.metric("Intercepto", f"{metrics['coefficients']['intercept']:.4f}", 
                     help="Termo constante")
        
        # Interpretação do Modelo
        st.subheader("📋 Interpretação do Modelo")
        
        interpretation_text = f"""
        O modelo explica **{metrics['r_squared']*100:.2f}%** da variância na Temperatura Média Anual (BIO1).
        
        📈 Um aumento de 1 unidade em BIO12 (Precipitação Anual) está associado a uma mudança de **{metrics['coefficients']['bio12']:.4f}** na BIO1.
        
        🌡️ Um aumento de 1 unidade em BIO4 (Sazonalidade da Temperatura) está associado a uma mudança de **{metrics['coefficients']['bio4']:.4f}** na BIO1.
        
        🎯 O RMSE de **{metrics['rmse']:.2f}** indica o erro médio de previsão do modelo.
        """
        
        st.info(interpretation_text)
