# 🚌 Proyecto de Optimización Analítica - MoviCiudad SpA

Este repositorio contiene el desarrollo del pipeline de datos automatizado para el diagnóstico operacional, limpieza estadística, modelamiento predictivo y reportabilidad de la flota de transporte de **MoviCiudad SpA**.

## 📁 Estructura del Repositorio

El proyecto se organiza de forma modular para garantizar la reproducibilidad y el orden del software:

* `main.py`: Script orquestador central. Ejecuta todo el flujo con un solo clic.
* `limpieza.py`: Módulo de estandarización de tipos de datos y eliminación de duplicados.
* `analisis_operacional.py`: Diagnóstico estadístico y depuración de outliers mediante el método IQR.
* `modelo_predictivo.py`: Entrenamiento de modelo de regresión lineal y cálculo de métricas (MAE, RMSE, R²).
* `dashboard_y_exportacion.py`: Generación del tablero visual y persistencia en Excel.
* `moviciudad_operaciones_bruto_SET_A.csv`: Base de datos original en bruto.

## 🚀 Cómo Ejecutar el Proyecto

Para replicar el análisis completo y generar los entregables, asegúrese de tener instaladas las librerías necesarias (`pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`, `openpyxl`) y ejecute desde la terminal:

```bash
python main.py
