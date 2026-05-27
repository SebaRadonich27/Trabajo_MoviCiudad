import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def generar_dashboard_y_excel(ruta_csv):
    # 1. Carga y Limpieza Base
    df = pd.read_csv(ruta_csv)
    df = df.drop_duplicates(subset=['id_formulario'], keep='first')
    
    columnas_numericas = ['tiempo_viaje_min', 'retraso_min', 'pasajeros_reportados']
    for col in columnas_numericas:
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str).str.replace(' min', '', case=False).str.replace(',', '.')
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # 2. Filtrado de Outliers mediante IQR (para no distorsionar los gráficos)
    df_filtrado = df.copy()
    for col in columnas_numericas:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        limite_inferior = q1 - 1.5 * iqr
        limite_superior = q3 + 1.5 * iqr
        df_filtrado = df_filtrado[(df_filtrado[col] >= limite_inferior) & (df_filtrado[col] <= limite_superior)]
    
    # 3. Configuración del Estilo del Dashboard
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Dashboard Operacional: Diagnóstico de MoviCiudad SpA', fontsize=20, fontweight='bold', color='#1a365d')
    
    # Gráfico 1: Distribución de Tiempos de Viaje (Histograma + KDE)
    sns.histplot(df_filtrado['tiempo_viaje_min'], kde=True, ax=axes[0, 0], color='#3182ce', bins=15)
    axes[0, 0].set_title('Distribución de Tiempos de Viaje', fontsize=14, fontweight='bold')
    axes[0, 0].set_xlabel('Minutos por trayecto')
    axes[0, 0].set_ylabel('Frecuencia de viajes')
    
    # Gráfico 2: Análisis de Retrasos y Adelantos por Tipo de Día (Boxplot)
    sns.boxplot(x='tipo_dia', y='retraso_min', data=df_filtrado, ax=axes[0, 1], palette='Set2')
    axes[0, 1].axhline(0, color='red', linestyle='--', linewidth=1.2, label='Horario Programado')
    axes[0, 1].set_title('Comportamiento del Retraso según Tipo de Día', fontsize=14, fontweight='bold')
    axes[0, 1].set_xlabel('Tipo de Día')
    axes[0, 1].set_ylabel('Minutos de Desviación (Negativo = Adelanto)')
    axes[0, 1].legend()
    
    # Gráfico 3: Relación Pasajeros vs. Tiempo de Viaje (Scatter Plot)
    sns.scatterplot(x='pasajeros_reportados', y='tiempo_viaje_min', data=df_filtrado, ax=axes[1, 0], color='#e53e3e', alpha=0.7)
    axes[1, 0].set_title('Relación: Carga de Pasajeros vs. Duración del Viaje', fontsize=14, fontweight='bold')
    axes[1, 0].set_xlabel('Cantidad de Pasajeros')
    axes[1, 0].set_ylabel('Tiempo de Viaje (Min)')
    
    # Gráfico 4: Matriz de Correlación de Pearson (Heatmap)
    matriz_corr = df_filtrado[columnas_numericas].corr()
    sns.heatmap(matriz_corr, annot=True, cmap='coolwarm', fmt=".3f", linewidths=.5, ax=axes[1, 1], vmin=-1, vmax=1)
    axes[1, 1].set_title('Mapa de Calor: Correlaciones Lineales', fontsize=14, fontweight='bold')
    
    # Ajustar espaciado y guardar la imagen del Dashboard
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    carpeta_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_dashboard = os.path.join(carpeta_actual, "dashboard_operacional.png")
    plt.savefig(ruta_dashboard, dpi=300)
    plt.close()
    print(f"✔️ Dashboard guardado exitosamente como imagen en: {ruta_dashboard}")
    
    # 4. Exportación a archivo Excel estructurado para operaciones posteriores
    ruta_excel = os.path.join(carpeta_actual, "moviciudad_datos_procesados.xlsx")
    with pd.ExcelWriter(ruta_excel, engine='openpyxl') as writer:
        df_filtrado.to_excel(writer, sheet_name='Datos_Limpios_Sin_Outliers', index=False)
        df.to_excel(writer, sheet_name='Datos_Originales_Históricos', index=False)
    print(f"✔️ Dataset procesado exportado exitosamente a Excel en: {ruta_excel}")

if __name__ == "__main__":
    carpeta_actual = os.path.dirname(os.path.abspath(__file__))
    archivo_bruto = os.path.join(carpeta_actual, "moviciudad_operaciones_bruto_SET_A.csv")
    generar_dashboard_y_excel(archivo_bruto)