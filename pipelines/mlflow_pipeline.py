import mlflow
import funciones
import pandas as pd
import os

# Configurar MLflow
mlflow.set_experiment("KAKEBIA-ARIMA")

def pipeline_kakebia():
    """Pipeline principal de KAKEBIA con rastreo MLflow"""
    
    with mlflow.start_run(run_name="procesamiento_datos_kakebia"):
        
        print("🔄 Iniciando procesamiento de datos...")
        df = pd.DataFrame()
        
        # 1. Procesar archivos Excel
        for carpeta in sorted(os.listdir("./data/raw")):
            ruta_carpeta = os.path.join("./data/raw", carpeta)
            
            if not os.path.isdir(ruta_carpeta):
                continue
            
            for archivo in os.listdir(ruta_carpeta):
                ruta_excel = os.path.join(ruta_carpeta, archivo)
                
                if not os.path.isfile(ruta_excel):
                    continue
                
                print(f"📄 Procesando: {ruta_excel}")
                
                try:
                    texto_no_estructurado = funciones.extraer_texto_excel(ruta_excel)
                    texto_estructurado = funciones.estructurar_texto(texto_no_estructurado)
                    df_book = funciones.csv_a_dataframe(texto_estructurado)
                    df = pd.concat([df, df_book], ignore_index=True)
                except Exception as e:
                    print(f"⚠️ Error procesando {ruta_excel}: {e}")
                    continue
        
        # 2. Conversión de moneda
        df.loc[df["moneda"] == "pesos", "importe"] *= 0.00024
        df = df.iloc[:, 0:4]
        
        # 3. Leer KAKEBO2025
        df_kakebo = pd.read_excel("./data/raw/KAKEBO2025.xlsx", 
                                  sheet_name="3-TOTAL GASTOS Y SSPP")
        df = pd.concat([df, df_kakebo], ignore_index=True)
        
        # 4. Registrar parámetros en MLflow
        mlflow.log_param("total_registros", len(df))
        mlflow.log_param("total_columnas", len(df.columns))
        mlflow.log_param("columnas_utilizadas", str(list(df.columns)))
        
        # 5. Guardar datos procesados
        output_path = "./data/processed/kakebo_merged.csv"
        df.to_csv(output_path, index=False)
        mlflow.log_artifact(output_path)
        
        # 6. Registrar métricas del dataset
        mlflow.log_metric("null_values", int(df.isnull().sum().sum()))
        mlflow.log_metric("duplicate_rows", int(df.duplicated().sum()))
        
        print(f"✅ Datos procesados: {len(df)} registros")
        print(f"✅ Datos guardados en: {output_path}")
        print("✅ Información registrada en MLflow")

if __name__ == "__main__":
    pipeline_kakebia()
