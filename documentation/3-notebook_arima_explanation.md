# Explicación del Notebook ARIMA (KAKEBIA)

## Descripción General

Este notebook implementa un modelo **ARIMA** (AutoRegressive Integrated Moving Average) para pronosticar gastos mensuales basados en el método **Kakebo** (sistema japonés de control de gastos personales).

## Estructura del Notebook

### 1. Importación de Librerías

**Celdas:** 1-3

**Librerías utilizadas:**
- `pandas` y `numpy`: para manejo y procesamiento de datos
- `statsmodels.tsa.arima.model`: para la implementación del modelo ARIMA
- `plotly.graph_objects`: para visualizaciones interactivas

### 2. Carga y Limpieza de Datos

**Celdas:** 4-8

**Proceso:**
- **Carga de datos:** Lee el archivo `../data/processed/kakebo_pred2.csv` con datos históricos de gastos
- **Limpieza de columnas:** Normaliza nombres de columnas a mayúsculas
- **Parseo de montos:** Maneja formato colombiano (puntos para miles, comas para decimales)
  - Ejemplo: "1.500.000,50" → 1500000.50
- **Conversión de fechas:** 
  - Mapea nombres de meses a números
  - Crea columna `FECHA` en formato datetime
- **Filtrado de datos:** Selecciona solo registros con `TIPO_DATO == "REAL"` para el entrenamiento (excluye predicciones previas)

### 3. Entrenamiento del Modelo ARIMA

**Celdas:** 9-10

**Modelo implementado:** ARIMA(1,1,1)

**Parámetros:**
- **p = 1**: Componente autoregresivo (usa 1 valor anterior)
- **d = 1**: Diferenciación de primer orden (para lograr estacionaridad)
- **q = 1**: Media móvil (considera 1 error anterior)

**Configuración adicional:**
- `enforce_stationarity=False`: No fuerza estacionaridad estricta
- `enforce_invertibility=False`: No fuerza invertibilidad estricta

### 4. Pronóstico a 12 Meses

**Celdas:** 11-12

**Generación de predicciones:**
- **Horizonte:** 12 meses futuros
- **Método:** `get_forecast(steps=12)`
- **Salidas:**
  - `yhat`: Valores predichos (media)
  - `ci`: Intervalo de confianza al 95% (límites inferior y superior)

### 5. Exportación de Resultados

**Celdas:** 13-15

**Archivo generado:** `../data/processed/kakebo_pred_hist.csv`

**Estructura del archivo:**
- `fecha`: Fecha en formato YYYY-MM-DD
- `monto`: Valor histórico o predicho
- `tipo_dato`: "REAL" o "PREDICCION"
- `lower_95`: Límite inferior del IC 95% (solo predicciones)
- `upper_95`: Límite superior del IC 95% (solo predicciones)

**Contenido:** Combina datos históricos reales con las predicciones futuras

### 6. Visualización de Resultados

**Celdas:** 16-18

**Tipo de gráfica:** Gráfica interactiva con Plotly

**Elementos visuales:**
- **Línea azul con marcadores:** Datos históricos reales
- **Línea roja con marcadores:** Predicciones futuras
- **Área morada (relleno):** Rango de incertidumbre - Intervalo de Confianza al 95%

**Características:**
- Título: "Predicciones de gastos KAKEBO 2026-2027"
- Ejes: Fecha (X) vs Monto (Y)
- Template: plotly_white
- Modo hover: x unified (muestra todos los valores al pasar el cursor)

**Interpretación del Intervalo de Confianza:**

El área morada representa el rango donde se espera que estén los valores verdaderos con un 95% de confianza. El punto rojo es el valor estimado de gasto para cada mes.

### 7. Formato para PowerBI

**Celdas:** 19-21

**Archivo generado:** `../data/processed/kakebo_pred_pbix.csv`

**Transformaciones:**
- Elimina columnas `lower_95` y `upper_95`
- Renombra columnas a mayúsculas: `FECHA`, `MONTO`, `TIPO_DATO`
- Redondea `MONTO` a enteros
- Crea columna `MONTO_COP` con formato de pesos colombianos:
  - Ejemplo: `$ 1.500.000` (sin la palabra "COP")
  - Usa punto como separador de miles

**Propósito:** Datos optimizados para visualización en dashboard de PowerBI

## Objetivo Final

Predecir los gastos mensuales futuros (2026-2027) basándose en patrones históricos del método Kakebo, proporcionando:
- Estimaciones puntuales de gasto mensual
- Rangos de confianza que cuantifican la incertidumbre
- Datos formateados para análisis y visualización

## Referencias

- Fuente de apoyo: https://github.com/copilot/share/0a1e4036-40a0-84f6-b900-260a20a209e2
- Notebook original creado en Deepnote

---

**Elaborado por**: Wagner Fernández V.  
**Especialista en Ciencia de Datos y Analítica**
---

*Documentación generada en marzo de 2026*