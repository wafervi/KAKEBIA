# KAKEBIA — Analítica de gastos y predicción

Proyecto de ciencia de datos y analítica para estructurar gastos mensuales en CSV y generar predicciones simples de egresos con regresión lineal.

## 📌 Objetivos
- Estandarizar información de gastos en formato CSV.
- Transformar montos a formatos numéricos para análisis.
- Generar proyecciones de egresos con un modelo base.

## 🧱 Estructura del proyecto
- **Código fuente**: [src/funciones.py](src/funciones.py), [src/prompt.py](src/prompt.py)
- **Datos**: [data/outputs/KAKEBO2025.csv](data/outputs/KAKEBO2025.csv), [data/outputs/kakebo2025_wrangled.csv](data/outputs/kakebo2025_wrangled.csv)
- **Notebook de análisis y predicción**: [notebooks/PREDICCIONES_KAKEBO.ipynb](notebooks/PREDICCIONES_KAKEBO.ipynb)

## 🔧 Flujo de trabajo
1. **Extracción y estructuración**  
   - La extracción desde Excel se realiza con [`extraer_texto_excel`](src/funciones.py) y el prompt definido en [`prompt`](src/prompt.py).
2. **Normalización**  
   - Conversión a DataFrame con [`csv_a_dataframe`](src/funciones.py), normalizando el campo `monto`.
3. **Modelado**  
   - Predicciones con regresión lineal en [notebooks/PREDICCIONES_KAKEBO.ipynb](notebooks/PREDICCIONES_KAKEBO.ipynb).

## ▶️ Ejecución rápida
1. Asegura que el entorno tenga las dependencias necesarias.
2. Ejecuta el notebook [notebooks/PREDICCIONES_KAKEBO.ipynb](notebooks/PREDICCIONES_KAKEBO.ipynb) para reproducir el análisis y la predicción.

## 📊 Salidas esperadas
- CSV estructurado: [data/outputs/kakebo2025_wrangled.csv](data/outputs/kakebo2025_wrangled.csv)
- Resultados de predicción exportados desde el notebook.

## ✅ Notas de calidad
- Los montos se convierten a numéricos usando `,` como separador decimal.
- El modelo actual es una línea base; se recomienda validar con más datos y evaluar métricas como RMSE.

## 📎 Referencias internas
- Prompt de extracción: [`prompt`](src/prompt.py) en [src/prompt.py](src/prompt.py)
- Funciones de procesamiento: [`extraer_texto_excel`](src/funciones.py), [`estructurar_texto`](src/funciones.py), [`csv_a_dataframe`](src/funciones.py) en [src/funciones.py](src/funciones.py)