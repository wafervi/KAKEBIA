import openai
import openpyxl
from dotenv import load_dotenv
import os
import pandas as pd
from io import StringIO
from prompt import prompt

# Cargar variables de entorno desde el archivo .env
load_dotenv(".env")

# Obtener la clave de API de OpenAI desde las variables de entorno
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def extraer_texto_excel(ruta_excel):
    """Extrae el texto de un archivo Excel y lo retorna como una cadena."""
    
    df = pd.read_excel(ruta_excel)
    text = df.to_string()
    return text


def estructurar_texto(texto):
    """Envía el texto a OpenAI y obtiene la respuesta estructurada en CSV,
    asegurando que solo devuelva datos válidos o 'error' en caso de problema."""

    cliente = openai.OpenAI(api_key=OPENAI_API_KEY)

    respuesta = cliente.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Eres un experto en extracción de datos de excel. Devuelve solo el CSV sin explicaciones ni mensajes adicionales. Si no puedes extraer datos, devuelve exactamente la palabra 'Error: NO SE PUEDEN EXTRAER LOS DATOS' sin comillas.",
            },
            {
                "role": "user",
                "content": prompt + "\n Este es el texto a parsear:\n" + texto,
            },
        ],
    )

    csv_respuesta = respuesta.choices[0].message.content.strip()
    return csv_respuesta


def csv_a_dataframe(csv):
    """Convierte el texto CSV en un DataFrame de pandas, asegurando que 'importe' sea numérico."""

    # Definir los tipos de datos para cada columna
    dtype_cols = {
        "mes": str,
        "no_de_mes": int,
        "monto": str,  # Se leerá primero como str para poder limpiar comas
    }

    # Leer el CSV en un DataFrame con los tipos especificados
    df_temp = pd.read_csv(StringIO(csv), delimiter=";", dtype=dtype_cols)

    # Convertir 'monto' a float, asegurando que los valores con coma se conviertan correctamente
    df_temp["monto"] = pd.to_numeric(
        df_temp["monto"].str.replace(",", "."), errors="coerce"
    )

    return df_temp
