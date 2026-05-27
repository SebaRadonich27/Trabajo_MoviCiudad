import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def entrenar_modelo_predictivo(ruta_csv):
    # 1. Carga y Limpieza Básica (Mismo estándar previo)
    df = pd.read_csv(ruta_csv)
    df = df.drop_duplicates(subset=['id_formulario'], keep='first')
    
    columnas_numericas = ['tiempo_viaje_min', 'retraso_min', 'pasajeros_reportados']
    for col in columnas_numericas:
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str).str.replace(' min', '', case=False).str.replace(',', '.')
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # 2. Filtrado de Outliers por IQR
    for col in columnas_numericas:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        df = df[(df[col] >= q1 - 1.5*iqr) & (df[col] <= q3 + 1.5*iqr)]
    
    # Seleccionar características (Variables X) y objetivo (Variable y)
    df_ml = df[['tiempo_viaje_min', 'retraso_min', 'pasajeros_reportados', 'ruta', 'turno', 'tipo_dia']].dropna()
    
    # 3. Ingeniería de Características: Convertir variables categóricas a numéricas (One-Hot Encoding)
    X = pd.get_dummies(df_ml[['retraso_min', 'pasajeros_reportados', 'ruta', 'turno', 'tipo_dia']], drop_first=True)
    y = df_ml['tiempo_viaje_min']
    
    # 4. División del dataset (80% Entrenamiento, 20% Prueba)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 5. Entrenamiento del Modelo
    modelo = LinearRegression()
    modelo.fit(X_train, y_train)
    
    # 6. Predicción y Evaluación
    predicciones = modelo.predict(X_test)
    
    mae = mean_absolute_error(y_test, predicciones)
    mse = mean_squared_error(y_test, predicciones)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, predicciones)
    
    print("--- EVALUACIÓN DEL MODELO DE REGRESIÓN ---")
    print(f"Error Absoluto Medio (MAE): {mae:.2f} minutos")
    print(f"Error Cuadrático Medio (MSE): {mse:.2f}")
    print(f"Raíz del Error Cuadrático Medio (RMSE): {rmse:.2f} minutos")
    print(f"Coeficiente de Determinación (R²): {r2:.4f}")

if __name__ == "__main__":
    carpeta_actual = os.path.dirname(os.path.abspath(__file__))
    archivo_bruto = os.path.join(carpeta_actual, "moviciudad_operaciones_bruto_SET_A.csv")
    entrenar_modelo_predictivo(archivo_bruto)