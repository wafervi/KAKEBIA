import functions
import pandas as pd
import os
#from sqlalchemy import create_engine

# 1- EXTRAER Y ESTRUCTURAR LOS DATOS DE LOS ARCHIVOS EXCEL QUE ESTÁN EN BRUTO EN LA CARPETA "data/raw" Y GUARDARLOS EN UN ARCHIVO CSV

# Crear un DataFrame vacío para almacenar todas las facturas
df = pd.DataFrame()

# Recorrer todas las carpetas dentro de la carpeta "facturas"
for carpeta in sorted(os.listdir("./data/raw")):
    ruta_carpeta = os.path.join("./data/raw", carpeta)
    
    # Skip if it's a file, not a directory
    if not os.path.isdir(ruta_carpeta):
        continue

    # Recorrer todos los archivos dentro de la carpeta
    for archivo in os.listdir(ruta_carpeta):
        ruta_excel = os.path.join(ruta_carpeta, archivo)
        
        # Skip if it's a directory
        if not os.path.isfile(ruta_excel):
            continue

        print(f"📄 Procesando archivo: {ruta_excel}")

        # Extraer texto del archivo excel
        texto_no_estructurado = functions.extraer_texto_excel(ruta_excel)

        # Estructurar el texto del archivo excel
        texto_estructurado = functions.estructurar_texto(texto_no_estructurado)

        # Convertir texto estructurado en dataframe
        df_book = functions.csv_a_dataframe(texto_estructurado)

        # Anexar el dataframe del archivo excel al dataframe general
        df = pd.concat([df, df_book], ignore_index=True)

    # Si la moneda es "pesos" convertir a euros multiplicando por 0,00024
    df.loc[df["moneda"] == "pesos", "importe"] *= 0.00024

    # Eliminar las columnas no esenciales
    df = df.iloc[:, 0:4]

# Leer el archivo Excel KAKEBO.xlsx
df_kakebo = pd.read_excel("./data/raw/KAKEBO2025.xlsx", sheet_name="3-TOTAL GASTOS Y SSPP")
df = pd.concat([df, df_kakebo], ignore_index=True)

# Guardar el DataFrame final en una bbdd sqlite
# Crear una conexión a la base de datos SQLite
#engine = create_engine("sqlite:///facturas.db")

# Guardar el DataFrame final en una bbdd sqlite, añadiendo los datos en lugar de reemplazarlos
df.to_csv("data/processed/KAKEBO2025.csv", index=False, sep=";")
#df.to_sql("facturas", engine, if_exists="append", index=False)

# Cerrar la conexión a la base de datos
#engine.dispose()

print("Proceso de extracción y estructuración del archivo 'KAKEBO2025.csv' ha sido completado exitosamente.")
print("Datos guardados en el archivo 'data/processed/KAKEBO2025.csv'.")

# 2- ORGANIZAR EL ARCHIVO PARA PROCESO DE ANALÍTICA DE DATOS

kakebo = pd.read_csv("data/processed/KAKEBO2025.csv", sep=";")

kakebo.drop(columns=["ITEM", "MONTO", "Unnamed: 2", "Unnamed: 3"], inplace=True)

kakebo = kakebo.iloc[2:].reset_index(drop=True)
if pd.isna(kakebo.iloc[0, 0]) or kakebo.iloc[0, 0] == "MES":
    kakebo = kakebo.drop(kakebo.index[:2]).reset_index(drop=True)

kakebo.rename(columns={"Unnamed: 4": "MES", "Unnamed: 5": "MONTO"}, inplace=True)

kakebo = kakebo.dropna()

kakebo.to_csv('data/processed/kakebo2025_wrangled.csv', sep=";")

kakebo_2025 = pd.read_csv("data/processed/kakebo2025_wrangled.csv", sep=";")
kakebo_2026 = pd.read_excel("data/raw/KAKEBO2026.xlsx", sheet_name="KAKEBO 2026")
kakebo_2026 = kakebo_2026[(kakebo_2026 != 0).all(axis=1)]

kakebo_merged = pd.merge(kakebo_2025, kakebo_2026, on="MES", how="outer", suffixes=("_2025", "_2026"))
kakebo_2025['año'] = 2025
kakebo_2026['año'] = 2026
kakebo_merged = pd.concat([kakebo_2025, kakebo_2026], ignore_index=True)
kakebo_merged = kakebo_merged.drop(columns=["Unnamed: 0"])
kakebo_merged.to_csv('data/processed/kakebo_merged.csv', sep=";", index=False)

if os.path.exists('data/processed/kakebo_merged.csv'):
    print("Archivo 'kakebo_merged.csv' creado exitosamente.")
else: 
    print("Error: El archivo 'kakebo_merged.csv' no se ha creado.")
