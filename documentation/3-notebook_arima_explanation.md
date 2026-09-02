# Modelo ARIMA y notebook

El proyecto ofrece dos formas de ejecutar el pronóstico: el notebook histórico `notebooks/ARIMA (KAKEBIA).ipynb` y el script reproducible `models/ARIMA.py`. Ambos usan un modelo ARIMA(1,1,1), pero el script es el punto de entrada actual para ejecución directa.

## Datos de entrada

El script carga `data/processed/kakebo_merged.csv` con separador `;`. El archivo debe contener al menos `MES`, `MONTO` y `AÑO`; si existe `TIPO_DATO`, solo los registros con valor `REAL` se usan para entrenar.

El script resuelve las rutas a partir de su propia ubicación, por lo que puede ejecutarse desde cualquier directorio:

```powershell
python models\ARIMA.py
```

## Preparación

1. Normaliza los nombres de columnas a mayúsculas.
2. Convierte montos colombianos, eliminando puntos de miles y cambiando la coma decimal por punto.
3. Convierte nombres de meses a números, incluyendo `SEPTIEMBRE` y `SETIEMBRE`.
4. Crea `FECHA` usando el primer día de cada mes y ordena cronológicamente.
5. Construye una serie mensual con frecuencia `MS`.

## Entrenamiento y pronóstico

El modelo se configura como:

```python
ARIMA(y, order=(1, 1, 1),
      enforce_stationarity=False,
      enforce_invertibility=False)
```

La configuración actual pronostica **3 meses** (`steps = 3`) y calcula intervalos de confianza del 95 %. No debe describirse como un pronóstico de 12 meses: ese valor aparece únicamente en metadatos antiguos del notebook.

## Archivos generados

El script escribe `data/processed/kakebo_pred_hist.csv`, con `fecha`, `monto`, `tipo_dato`, `lower_95` y `upper_95`, y `dashboards/HTML/arima_forecast.html`, un gráfico Plotly con histórico, predicción e intervalo de confianza.

También intenta copiar el HTML a `C:\xampp\htdocs\REDOHIS\modules\dashboard\arima_forecast.html` cuando esa instalación local de REDOHIS existe. Esta copia es opcional y no reemplaza el archivo generado en `dashboards/HTML/`.

## Notebook

Para trabajar de forma interactiva:

1. Seleccionar el intérprete `.venv` en VS Code.
2. Abrir `notebooks/ARIMA (KAKEBIA).ipynb`.
3. Ejecutar las celdas en orden.
4. Comprobar la creación de `kakebo_pred_hist.csv` y `kakebo_pred_pbix.csv` en `data/processed/`.

El notebook conserva referencias históricas de Deepnote a `kakebo_pred2.csv` y a rutas relativas de ese entorno. Si se ejecuta localmente, usar como entrada `../data/processed/kakebo_merged.csv` y mantener las salidas dentro de `../data/processed/`.

## Salida para Power BI

La última parte del notebook lee `kakebo_pred_hist.csv`, elimina `lower_95` y `upper_95`, renombra las columnas a `FECHA`, `MONTO` y `TIPO_DATO`, redondea `MONTO` y crea `MONTO_COP` con separador de miles mediante puntos. El resultado es `data/processed/kakebo_pred_pbix.csv`.

*Actualizado: 2 de septiembre de 2026.*