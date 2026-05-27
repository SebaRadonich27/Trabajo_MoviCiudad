import pandas as pd
import numpy as np

def pipeline_limpieza_moviciudad(ruta_input, ruta_output=None):
    """
    Carga, limpia, imputa y estructura de forma reproducible los datos 
    operacionales brutos de MoviCiudad SpA.
    """
    print("Iniciando proceso de estructuración de datos...")
    
    # 1. Extracción
    df = pd.read_csv(ruta_input)
    print(f"-> Registros iniciales cargados: {len(df)}")
    
    # 2. Eliminación de duplicados basados en el identificador del formulario
    df = df.drop_duplicates(subset=['id_formulario'], keep='first')
    
    # 3. Conversión y estandarización de formatos
    df['fecha_registro'] = pd.to_datetime(df['fecha_registro'], errors='coerce')
    
    # Forzar conversión a numérico (errores de digitación de texto pasarán a NaN)
    columnas_numericas = ['tiempo_viaje_min', 'retraso_min', 'pasajeros_reportados']
    for col in columnas_numericas:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    # 4. Imputación inteligente de datos faltantes (NaN)
    # Se utiliza la mediana agrupada por Ruta y Turno para no distorsionar el comportamiento real
    df['tiempo_viaje_min'] = df.groupby(['ruta', 'turno'])['tiempo_viaje_min']\
                               .transform(lambda x: x.fillna(x.median()))
                               
    df['retraso_min'] = df.groupby(['ruta', 'turno'])['retraso_min']\
                          .transform(lambda x: x.fillna(x.median()))
                          
    df['pasajeros_reportados'] = df.groupby(['ruta', 'turno'])['pasajeros_reportados']\
                                   .transform(lambda x: x.fillna(x.median()))
    
    # 5. Estructuración final y formateo de tipos
    # Usamos 'Int64' (entero extendido de pandas) para permitir consistencia en datos de conteo
    df['pasajeros_reportados'] = df['pasajeros_reportados'].round().astype('Int64')
    
    # Ordenar cronológicamente por fecha y hora de salida de servicio
    df = df.sort_values(by=['fecha_registro', 'hora_salida']).reset_index(drop=True)
    
    print(f"-> Registros limpios y estructurados finales: {len(df)}")
    print(f"-> Valores nulos remanentes en el dataset: {df.isnull().sum().sum()}")
    
    # 6. Exportación reproducible
    if ruta_output:
        df.to_csv(ruta_output, index=False)
        print(f" Archivo guardado exitosamente en: {ruta_output}")
        
    return df

# --- Ejecución del script ---
import os

# Este truco encuentra automáticamente la carpeta exacta donde está guardado 'limpieza.py'
carpeta_actual = os.path.dirname(os.path.abspath(__file__))

# Unimos la carpeta con el nombre de los archivos
archivo_bruto = os.path.join(carpeta_actual, "moviciudad_operaciones_bruto_SET_A.csv")
archivo_limpio = os.path.join(carpeta_actual, "moviciudad_operaciones_estructurado.csv")

# Llamada al pipeline
df_estructurado = pipeline_limpieza_moviciudad(archivo_bruto, archivo_limpio)

# Mostrar previsualización del resultado estructurado
print("\nEstructura final del DataFrame:")
print(df_estructurado.info())
print("\nPrimeros registros limpios:")
print(df_estructurado.head())