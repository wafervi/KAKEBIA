# Explicación de Archivos Python - Carpeta `pipelines/`

## Descripción General

La carpeta `pipelines/` contiene los scripts que implementan un pipeline ETL (Extracción, Transformación y Carga) automatizado para procesar datos de gastos personales del método KAKEBO. Este pipeline utiliza la API de OpenAI GPT-4o-mini para extraer y estructurar información de archivos Excel con formato variable.

---

## 📄 funciones.py

### Propósito
Módulo de funciones auxiliares para extraer y estructurar datos de archivos Excel usando inteligencia artificial (OpenAI GPT-4o-mini).

### Dependencias
```python
import openai          # Cliente para API de OpenAI
import openpyxl        # Para leer archivos Excel
from dotenv import load_dotenv  # Para cargar variables de entorno
import os              # Operaciones del sistema
import pandas as pd    # Manipulación de datos
from io import StringIO  # Conversión de strings a archivos
from prompt import prompt  # Importa el prompt desde prompt.py
```

### Variables de Entorno
```python
load_dotenv(".env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
```
Carga la clave de API de OpenAI desde un archivo `.env` para mantener la seguridad.

### Funciones Principales

#### 1. `extraer_texto_excel(ruta_excel)`

**Descripción:** Extrae el contenido completo de un archivo Excel y lo convierte a texto plano.

**Parámetros:**
- `ruta_excel` (str): Ruta absoluta o relativa al archivo Excel

**Retorna:**
- `text` (str): Contenido del Excel en formato de texto plano

**Proceso:**
1. Lee el archivo Excel usando `pd.read_excel()`
2. Convierte el DataFrame a string usando `.to_string()`
3. Retorna el texto para procesamiento posterior

**Ejemplo de uso:**
```python
texto = extraer_texto_excel("./data/raw/KAKEBO2025.xlsx")
```

---

#### 2. `estructurar_texto(texto)`

**Descripción:** Envía el texto extraído a OpenAI y obtiene una respuesta estructurada en formato CSV.

**Parámetros:**
- `texto` (str): Texto sin estructurar extraído del Excel

**Retorna:**
- `csv_respuesta` (str): Datos estructurados en formato CSV o mensaje de error

**Proceso:**
1. Crea cliente de OpenAI con la API key
2. Envía solicitud al modelo `gpt-4o-mini` con dos mensajes:
   - **System:** Define el rol como "experto en extracción de datos de excel"
   - **User:** Combina el prompt de instrucciones + texto a parsear
3. Extrae la respuesta del modelo
4. Retorna el CSV limpio o mensaje de error

**Configuración del modelo:**
- Modelo utilizado: `gpt-4o-mini`
- Instrucción: Devolver solo CSV sin explicaciones
- Manejo de errores: Si no puede extraer, retorna "Error: NO SE PUEDEN EXTRAER LOS DATOS"

**Ejemplo de uso:**
```python
csv_estructurado = estructurar_texto(texto_bruto)
```

---

#### 3. `csv_a_dataframe(csv)`

**Descripción:** Convierte el texto CSV generado por OpenAI en un DataFrame de pandas con tipos de datos correctos.

**Parámetros:**
- `csv` (str): Texto en formato CSV con separador `;`

**Retorna:**
- `df_temp` (DataFrame): DataFrame de pandas con columnas tipadas correctamente

**Proceso:**
1. Define tipos de datos para cada columna:
   ```python
   dtype_cols = {
       "mes": str,           # Nombre del mes
       "no_de_mes": int,     # Número del mes (1-12)
       "monto": str,         # Inicialmente string para limpieza
   }
   ```
2. Lee el CSV usando `pd.read_csv()` con delimitador `;`
3. Limpia la columna `monto`:
   - Reemplaza comas por puntos (formato decimal)
   - Convierte a tipo numérico float
   - Maneja errores con `errors='coerce'` (valores inválidos → NaN)

**Ejemplo de transformación:**
- Entrada: `"1.500.000,50"` → Salida: `1500000.50`
- Entrada: `"200000"` → Salida: `200000.0`

**Ejemplo de uso:**
```python
df = csv_a_dataframe(csv_text)
```

---

## 📄 main.py

### Propósito
Script principal que ejecuta el pipeline completo de extracción, transformación y carga (ETL) de datos KAKEBO.

### Dependencias
```python
import funciones       # Módulo local con funciones auxiliares
import pandas as pd    # Manipulación de datos
import os              # Operaciones del sistema
```

### Estructura del Pipeline

El script se divide en **2 fases principales**:

---

### FASE 1: Extracción y Estructuración de Datos Brutos

**Objetivo:** Procesar archivos Excel brutos y consolidarlos en un único archivo CSV estructurado.

#### Proceso Paso a Paso

**1.1 Inicialización**
```python
df = pd.DataFrame()  # DataFrame vacío para acumular datos
```

**1.2 Recorrido de Carpetas y Archivos**
```python
for carpeta in sorted(os.listdir("./data/raw")):
    ruta_carpeta = os.path.join("./data/raw", carpeta)
```
- Itera sobre todas las carpetas en `./data/raw`
- Ordena alfabéticamente para procesamiento consistente
- Salta archivos que no sean directorios

**1.3 Procesamiento de Archivos Excel**
```python
for archivo in os.listdir(ruta_carpeta):
    ruta_excel = os.path.join(ruta_carpeta, archivo)
```
Para cada archivo Excel:
1. **Extrae texto:** `funciones.extraer_texto_excel(ruta_excel)`
2. **Estructura con IA:** `funciones.estructurar_texto(texto_no_estructurado)`
3. **Convierte a DataFrame:** `funciones.csv_a_dataframe(texto_estructurado)`
4. **Consolida:** Agrega al DataFrame principal con `pd.concat()`

**1.4 Conversión de Moneda**
```python
df.loc[df["moneda"] == "pesos", "importe"] *= 0.00024
```
- Convierte pesos colombianos a euros
- Factor de conversión: 0.00024 (aproximado)

**1.5 Limpieza de Columnas**
```python
df = df.iloc[:, 0:4]  # Mantiene solo las primeras 4 columnas
```

**1.6 Integración de KAKEBO2025**
```python
df_kakebo = pd.read_excel("./data/raw/KAKEBO2025.xlsx", 
                          sheet_name="3-TOTAL GASTOS Y SSPP")
df = pd.concat([df, df_kakebo], ignore_index=True)
```

**1.7 Exportación**
```python
df.to_csv("data/processed/KAKEBO2025.csv", index=False, sep=";")
```
**Archivo generado:** `data/processed/KAKEBO2025.csv`

---

### FASE 2: Organización y Preparación para Análisis

**Objetivo:** Limpiar, organizar y combinar datos de múltiples años.

#### Proceso Paso a Paso

**2.1 Carga de Datos**
```python
kakebo = pd.read_csv("data/processed/KAKEBO2025.csv", sep=";")
```

**2.2 Eliminación de Columnas Innecesarias**
```python
kakebo.drop(columns=["ITEM", "MONTO", "Unnamed: 2", "Unnamed: 3"], inplace=True)
```
- Remueve columnas duplicadas o irrelevantes
- Limpia columnas sin nombre (`Unnamed`)

**2.3 Limpieza de Filas**
```python
kakebo = kakebo.iloc[2:].reset_index(drop=True)
if pd.isna(kakebo.iloc[0, 0]) or kakebo.iloc[0, 0] == "MES":
    kakebo = kakebo.drop(kakebo.index[:2]).reset_index(drop=True)
```
- Elimina las primeras 2 filas (headers/metadatos)
- Verifica y elimina headers duplicados
- Reinicia índices para mantener secuencia correcta

**2.4 Renombramiento de Columnas**
```python
kakebo.rename(columns={"Unnamed: 4": "MES", "Unnamed: 5": "MONTO"}, inplace=True)
```

**2.5 Eliminación de Valores Nulos**
```python
kakebo = kakebo.dropna()
```

**2.6 Exportación de Datos Limpios**
```python
kakebo.to_csv('data/processed/kakebo2025_wrangled.csv', sep=";")
```
**Archivo generado:** `data/processed/kakebo2025_wrangled.csv`

**2.7 Carga de Datos 2026**
```python
kakebo_2026 = pd.read_excel("data/raw/KAKEBO2026.xlsx", sheet_name="KAKEBO 2026")
kakebo_2026 = kakebo_2026[(kakebo_2026 != 0).all(axis=1)]
```
- Lee datos del año 2026
- Filtra filas que contengan al menos un cero

**2.8 Combinación de Años**
```python
kakebo_2025['año'] = 2025
kakebo_2026['año'] = 2026
kakebo_merged = pd.concat([kakebo_2025, kakebo_2026], ignore_index=True)
kakebo_merged = kakebo_merged.drop(columns=["Unnamed: 0"])
```
- Agrega columna `año` a cada dataset
- Concatena verticalmente ambos DataFrames
- Elimina columnas de índice residuales

**2.9 Exportación Final**
```python
kakebo_merged.to_csv('data/processed/kakebo_merged.csv', sep=";", index=False)
```
**Archivo generado:** `data/processed/kakebo_merged.csv`

**2.10 Verificación**
```python
if os.path.exists('data/processed/kakebo_merged.csv'):
    print("Archivo 'kakebo_merged.csv' creado exitosamente.")
else: 
    print("Error: El archivo 'kakebo_merged.csv' no se ha creado.")
```

---

## 📄 prompt.py

### Propósito
Define el prompt de instrucciones detalladas para el modelo GPT-4o-mini, especificando exactamente cómo debe extraer y estructurar los datos.

### Contenido del Prompt

```python
prompt = """
Eres un asistente especializado en estructurar información de en formato .csv
...
"""
```

### Instrucciones Específicas al Modelo

#### 📍 Ubicación de Datos en Excel
- **Hoja:** `3-TOTAL GASTOS Y SSPP`
- **Columna MES:** Celdas E3:E15
- **Columna MONTO:** Celdas F3:F15

#### 📋 Requerimientos de Extracción

**1. MES**
- Extraer el nombre del mes
- Formato: MAYÚSCULAS
- Idioma: Español

**2. No. DE MES**
- Número correspondiente al mes
- Rango: 1 (enero) a 12 (diciembre)

**3. MONTO**
- Extraer el valor monetario
- Moneda: Pesos Colombianos (COP)

#### 📤 Formato de Salida Obligatorio

**Header (primera línea):**
```csv
mes;no_de_mes;monto
```

**Características:**
- Separador: punto y coma (`;`)
- Header incluido **solo una vez**
- Sin líneas vacías
- Sin encabezados repetidos
- Sin explicaciones ni comentarios

#### 📊 Ejemplo de Salida Esperada

```csv
mes;no_de_mes;monto
ENERO;1;200000
FEBRERO;2;150000
MARZO;3;180000
```

#### ⚠️ Manejo de Errores

Si el modelo no puede extraer datos correctamente:
```
error
```
(Retorna exactamente la palabra "error" sin comillas)

---

## 🔄 Flujo de Trabajo Completo del Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                     INICIO DEL PIPELINE                         │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  FASE 1: EXTRACCIÓN Y ESTRUCTURACIÓN                            │
├─────────────────────────────────────────────────────────────────┤
│  1. Escanea carpetas en data/raw/                               │
│  2. Lee archivos Excel → extraer_texto_excel()                  │
│  3. Envía texto a OpenAI GPT-4o-mini → estructurar_texto()      │
│  4. Modelo retorna CSV estructurado según prompt.py             │
│  5. Convierte CSV a DataFrame → csv_a_dataframe()               │
│  6. Consolida todos los DataFrames                              │
│  7. Convierte pesos a euros (si aplica)                         │
│  8. Lee KAKEBO2025.xlsx y agrega al consolidado                 │
│  9. Exporta → data/processed/KAKEBO2025.csv                     │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  FASE 2: ORGANIZACIÓN Y PREPARACIÓN                             │
├─────────────────────────────────────────────────────────────────┤
│  1. Lee KAKEBO2025.csv                                          │
│  2. Elimina columnas innecesarias                               │
│  3. Limpia filas con headers duplicados                         │
│  4. Renombra columnas a nombres estándar                        │
│  5. Elimina valores nulos                                       │
│  6. Exporta → data/processed/kakebo2025_wrangled.csv            │
│  7. Lee KAKEBO2026.xlsx                                         │
│  8. Filtra filas válidas                                        │
│  9. Agrega columna 'año' a ambos datasets                       │
│  10. Combina 2025 y 2026 verticalmente                          │
│  11. Exporta → data/processed/kakebo_merged.csv                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                     ARCHIVOS GENERADOS                          │
├─────────────────────────────────────────────────────────────────┤
│  ✅ KAKEBO2025.csv - Datos consolidados brutos 2025             │
│  ✅ kakebo2025_wrangled.csv - Datos limpios 2025                │
│  ✅ kakebo_merged.csv - Datos combinados 2025-2026              │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Propósito del Pipeline

Este pipeline automatiza completamente el proceso de:

1. **Extracción:** Obtener datos de múltiples archivos Excel con formatos variables
2. **Estructuración:** Usar IA para identificar y organizar información relevante
3. **Limpieza:** Eliminar duplicados, valores nulos y columnas innecesarias
4. **Consolidación:** Combinar datos de múltiples fuentes y períodos
5. **Preparación:** Generar archivos listos para análisis y modelado (ARIMA, visualizaciones, etc.)

**Ventaja clave:** Utiliza inteligencia artificial (GPT-4o-mini) para manejar archivos Excel con estructuras inconsistentes, eliminando la necesidad de programar lógicas de extracción específicas para cada formato.

---

## 📦 Archivos de Salida

| Archivo | Descripción | Uso |
|---------|-------------|-----|
| `KAKEBO2025.csv` | Datos consolidados de 2025 sin procesar | Archivo intermedio |
| `kakebo2025_wrangled.csv` | Datos de 2025 limpios y organizados | Análisis individual de 2025 |
| `kakebo_merged.csv` | Datos combinados 2025-2026 | Análisis temporal y predicciones |

---

## 🔐 Requisitos de Configuración

### Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:
```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Estructura de Carpetas Requerida

```
KAKEBIA/
├── data/
│   ├── raw/              # Archivos Excel de entrada
│   │   ├── KAKEBO2025.xlsx
│   │   └── KAKEBO2026.xlsx
│   └── processed/        # Archivos CSV de salida (generados automáticamente)
├── pipelines/
│   ├── funciones.py
│   ├── main.py
│   └── prompt.py
└── .env                  # Variables de entorno (no versionar)
```

---

## 🚀 Ejecución del Pipeline

```bash
# Activar entorno virtual
.venv\Scripts\Activate.ps1

# Ejecutar pipeline completo
python pipelines/main.py
```

---
**Proyecto:** KAKEBIA - Control de Gastos Familiares  
**Tecnologías:** Python, Pandas, OpenAI GPT-4o-mini
---

Elaborado por**: Wagner Fernández V.  
Especialista en Ciencia de Datos y Analítica**
---

*Documentación generada en marzo de 2026*