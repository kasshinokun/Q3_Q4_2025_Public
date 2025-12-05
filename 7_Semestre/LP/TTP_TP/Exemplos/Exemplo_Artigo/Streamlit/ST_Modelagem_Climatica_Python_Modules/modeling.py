import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import numpy as np

class ClimateModel:
    def __init__(self, target_col='bio1', feature_cols=['bio12', 'bio4'], test_size=0.3, random_state=42):
        self.target_col = target_col
        self.feature_cols = feature_cols
        self.test_size = test_size
        self.random_state = random_state
        self.model = None
        self.metrics = None
        self.predictions = None
        self.test_data = None

    def train_model(self, df_clean: pd.DataFrame):
        """
        Treina o modelo de Regressão Linear Múltipla e calcula as métricas.
        """
        if df_clean is None or df_clean.empty:
            raise ValueError("DataFrame de entrada não pode ser nulo ou vazio.")

        # Preparação dos dados
        X = df_clean[self.feature_cols]
        y = df_clean[self.target_col]

        # Divisão em treino e teste
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=self.test_size, random_state=self.random_state
        )

        # Treinamento do modelo
        self.model = LinearRegression()
        self.model.fit(X_train, y_train)

        # Previsões
        self.predictions = self.model.predict(X_test)
        
        # Armazenar dados de teste para visualização
        self.test_data = {'X': X_test, 'y': y_test}

        # Cálculo das métricas
        r_squared = r2_score(y_test, self.predictions)
        rmse = np.sqrt(mean_squared_error(y_test, self.predictions))
        mae = mean_absolute_error(y_test, self.predictions)

        # Coeficientes
        coefficients = {
            'intercept': self.model.intercept_,
        }
        for feature, coef in zip(self.feature_cols, self.model.coef_):
            coefficients[feature] = coef

        self.metrics = {
            'r_squared': r_squared,
            'rmse': rmse,
            'mae': mae,
            'coefficients': coefficients
        }
        
        return self.model, self.metrics, self.predictions, self.test_data

    def get_metrics(self):
        return self.metrics

    def get_predictions(self):
        return self.predictions

    def get_test_data(self):
        return self.test_data
