# Pipeline ETL de KAKEBIA

El pipeline de `pipelines/` transforma archivos Excel del método Kakebo en CSV listos para análisis y pronóstico. El punto de entrada actual es `pipelines/combinator.py`; no existe `pipelines/main.py`.

## Estado actual y limitación conocida

En el estado actual del repositorio, `data/raw/` contiene `KAKEBO2025.xlsx` y `KAKEBO2026.xlsx` directamente, sin subcarpetas de facturas. Además, `pipelines/functions.py` devuelve las columnas `mes`, `no_de_mes` y `monto`, mientras que `combinator.py` intenta aplicar una conversión sobre `moneda` e `importe` antes de cargar `KAKEBO2025.xlsx`. Por estas dos razones, la ejecución actual puede terminar con `KeyError` y no debe considerarse un flujo ETL reproducible hasta que se corrija el código o se prepare una entrada compatible.

## Módulos

### `pipelines/functions.py`

- `extraer_texto_excel(ruta_excel)`: lee el primer esquema del Excel con pandas y lo convierte a texto.
- `estructurar_texto(texto)`: envía el texto a `gpt-4o-mini` usando `OPENAI_API_KEY` y solicita únicamente CSV separado por `;`.
- `csv_a_dataframe(csv)`: lee las columnas `mes`, `no_de_mes` y `monto`, y convierte `monto` a número.

### `pipelines/prompt.py`

Define el formato esperado por el modelo: `mes;no_de_mes;monto`, meses en español y mayúsculas, y montos en pesos colombianos.

## Entrada requerida

El script recorre únicamente directorios dentro de `data/raw/`; los archivos Excel sueltos en la raíz de `data/raw/` se ignoran en la primera fase. La estructura que el código espera es:

```text
data/raw/
├── <carpeta-de-facturas>/
│   └── <archivo>.xlsx
├── KAKEBO2025.xlsx
└── KAKEBO2026.xlsx
```

Además, deben existir `KAKEBO2025.xlsx` con la hoja `3-TOTAL GASTOS Y SSPP`, `KAKEBO2026.xlsx` con la hoja `KAKEBO 2026` y `.env` en la raíz con `OPENAI_API_KEY`.

## Fases de `combinator.py`

### 1. Extracción y consolidación

1. Recorre las subcarpetas de `data/raw/` en orden.
2. Lee cada archivo y solicita a OpenAI una tabla CSV estructurada.
3. Convierte la respuesta a DataFrame y concatena los resultados.
4. Intenta convertir a euros los registros cuya moneda sea `pesos`, usando `0.00024`. Esta operación requiere columnas `moneda` e `importe`, que no son producidas actualmente por `functions.py`.
5. Agrega la hoja `3-TOTAL GASTOS Y SSPP` de `KAKEBO2025.xlsx`.
6. Escribe `data/processed/KAKEBO2025.csv` con separador `;`.

### 2. Preparación analítica

1. Limpia columnas y filas de encabezado del CSV 2025.
2. Renombra las columnas de mes y monto y elimina filas nulas.
3. Escribe `data/processed/kakebo2025_wrangled.csv`.
4. Lee los datos 2026 y elimina filas compuestas únicamente por ceros.
5. Añade `año = 2025` y `año = 2026`.
6. Concatena ambos años y elimina el índice residual.
7. Escribe `data/processed/kakebo_merged.csv` con separador `;`.

La variable `kakebo_merged` también se construye temporalmente mediante un `merge` por `MES`, pero el resultado que se exporta es la concatenación vertical de ambos años.

## Ejecución

Desde la raíz del repositorio y con `.venv` activo:

```powershell
python pipelines\combinator.py
```

El proceso requiere acceso a la API de OpenAI para la fase de extracción. Con el estado actual del código, la ejecución puede fallar antes de generar los CSV; verificar y corregir la incompatibilidad indicada arriba antes de usar estas salidas.

## Relación con el modelo

`models/ARIMA.py` consume `data/processed/kakebo_merged.csv`, entrena un ARIMA(1,1,1) con los registros reales y genera las predicciones y el HTML descritos en la documentación del modelo.

*Actualizado: 9 de septiembre de 2026.*