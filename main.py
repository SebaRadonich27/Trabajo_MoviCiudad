#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MoviCiudad SpA - Data Pipeline Orquestador Central
Autor: Consultor de Analítica de Datos
Fecha: Mayo 2026
Descripción: Script maestro que automatiza el flujo completo de datos,
             desde la limpieza y el análisis descriptivo, hasta el modelamiento
             predictivo y la generación de dashboards visuales.
"""

import os
import sys

# =====================================================================
# CONFIGURACIÓN DE RUTAS Y ENTORNO
# =====================================================================
# Definimos de forma dinámica la carpeta raíz del proyecto para evitar errores de ruta
CARPETA_RAIZ = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_INPUT = os.path.join(CARPETA_RAIZ, "moviciudad_operaciones_bruto_SET_A.csv")

def verificar_entorno():
    """Valida que el archivo de datos bruto exista antes de iniciar el pipeline."""
    if not os.path.exists(ARCHIVO_INPUT):
        print(f"❌ ERROR CRÍTICO: No se encuentra el archivo base en: {ARCHIVO_INPUT}")
        print("Asegúrese de colocar el archivo CSV en la misma carpeta que este script.")
        sys.exit(1)
    print("✔️ Entorno verificado con éxito. Iniciando Data Pipeline...\n" + "="*60)

# =====================================================================
# EJECUCIÓN SECUENCIAL DEL FLUJO DE TRABAJO (PIPELINE)
# =====================================================================
def ejecutar_pipeline_completo():
    # Paso 0: Verificación inicial
    verificar_entorno()
    
    try:
        # PASO 1: Análisis Operacional y Detección de Outliers (IQR)
        print("[FASE 1]: Ejecutando Análisis Estadístico y Diagnóstico de Outliers...")
        # Importamos la función directamente desde el archivo que creaste previamente
        from analisis_operacional import ejecutar_analisis_operacional
        ejecutar_analisis_operacional(ARCHIVO_INPUT)
        print("✔️ FASE 1 Finalizada con éxito.\n" + "-"*60)
        
        # PASO 2: Modelamiento Predictivo con Machine Learning
        print("[FASE 2]: Entrenando Modelo de Regresión y Evaluando Métricas (MAE, R²)...")
        # Importamos la lógica predictiva para analizar el rendimiento lineal
        from modelo_predictivo import entrenar_modelo_predictivo
        entrenar_modelo_predictivo(ARCHIVO_INPUT)
        print("✔️ FASE 2 Finalizada con éxito.\n" + "-"*60)
        
        # PASO 3: Generación de Dashboards Visuales y Exportación a Excel
        print("[FASE 3]: Construyendo Dashboard estático y exportando reportes multicapa...")
        # Invocamos el generador de gráficos de Matplotlib/Seaborn y la persistencia en Excel
        from dashboard_y_exportacion import generar_dashboard_y_excel
        generar_dashboard_y_excel(ARCHIVO_INPUT)
        print("✔️ FASE 3 Finalizada con éxito.\n" + "="*60)
        
        print("\n🚀 ¡PIPELINE EJECUTADO CORRECTAMENTE!")
        print("Resultados generados en tu carpeta:")
        print(" └─> Imagen del Tablero: 'dashboard_operacional.png'")
        print(" └─> Reporte Final Excel: 'moviciudad_datos_procesados.xlsx'")

    except ImportError as e:
        print(f"❌ ERROR DE IMPORTACIÓN: Asegúrese de que todos los archivos .py estén en la misma carpeta.")
        print(f"Detalle: {e}")
    except Exception as e:
        print(f"❌ ERROR INESPERADO durante la ejecución del flujo: {e}")

# Punto de entrada oficial de la aplicación en Python
if __name__ == "__main__":
    ejecutar_pipeline_completo()