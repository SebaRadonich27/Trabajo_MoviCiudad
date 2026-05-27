import pandas as pd
import numpy as np
import os

def ejecutar_analisis_operacional(ruta_csv):
    # Cargar el dataset
    df = pd.read_csv(ruta_csv)
    
    # Eliminar duplicados por ID de formulario para asegurar datos limpios
    df = df.drop_duplicates(subset=['id_formulario'], keep='first')
    
    # Estandarización y limpieza de columnas numéricas clave
    columnas_numericas = ['tiempo_viaje_min', 'retraso_min', 'pasajeros_reportados']
    for col in columnas_numericas:
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str).str.replace(' min', '', case=False)
            df[col] = df[col].astype(str).str.replace(',', '.')
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    print("--- 1. ESTADÍSTICA DESCRIPTIVA (CON VALORES EXTREMOS) ---")
    print(df[columnas_numericas].describe().round(2))
    print("\n" + "="*50 + "\n")
    
    print("--- 2. DETECCIÓN DE VALORES ATÍPICOS (MÉTODO IQR) ---")
    df_filtrado = df.copy()
    
    for col in columnas_numericas:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        
        limite_inferior = q1 - 1.5 * iqr
        limite_superior = q3 + 1.5 * iqr
        
        # Identificar registros atípicos
        atipicos = df[(df[col] < limite_inferior) | (df[col] > limite_superior)]
        print(f"Variable '{col}':")
        print(f"  -> Umbrales IQR normales: [{limite_inferior:.2f} a {limite_superior:.2f}]")
        print(f"  -> Registros atípicos detectados: {len(atipicos)}")
        if len(atipicos) > 0:
            print(f"  -> Valores extremos identificados: {atipicos[col].dropna().unique()[:5]}")
            
        # Filtrar el dataframe para quedarnos solo con los datos normales
        df_filtrado = df_filtrado[(df_filtrado[col] >= limite_inferior) & (df_filtrado[col] <= limite_superior)]
        
    print("\n" + "="*50 + "\n")
    
    print("--- 3. MATRIZ DE CORRELACIÓN DE PEARSON (DATOS DEPURADOS) ---")
    print(df_filtrado[columnas_numericas].corr().round(4))

if __name__ == "__main__":
    # Truco para que Python encuentre el CSV en la misma carpeta del script
    carpeta_actual = os.path.dirname(os.path.abspath(__file__))
    archivo_bruto = os.path.join(carpeta_actual, "moviciudad_operaciones_bruto_SET_A.csv")
    
    ejecutar_analisis_operacional(archivo_bruto)