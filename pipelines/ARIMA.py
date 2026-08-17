import os
from pathlib import Path
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import plotly.graph_objects as go
import shutil

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data" / "processed"
path = DATA_DIR / "kakebo_merged.csv"

# Condicional 'if' para leer archivo .csv

if path.exists():
    df = pd.read_csv(path, sep=";", encoding="utf-8")
    print(f"Nota: El archivo '{path}' fue cargado exitosamente.")
else:
    raise FileNotFoundError(f"Error: No se encontró el archivo '{path}'.")

df.columns = [c.strip().upper() for c in df.columns]

def parse_monto(x):
    if pd.isna(x):
        return np.nan
    s = str(x).strip()
    s = s.replace(".", "")      # miles
    s = s.replace(",", ".")     # decimal
    return float(s)

df["MONTO"] = df["MONTO"].apply(parse_monto)

df["MES_NOMBRE"] = df["MES"].astype(str).str.replace("MES", "", regex=False).str.strip().str.upper()

mes_map = {
    "ENERO": 1, "FEBRERO": 2, "MARZO": 3, "ABRIL": 4, "MAYO": 5, "JUNIO": 6,
    "JULIO": 7, "AGOSTO": 8, "SEPTIEMBRE": 9, "SETIEMBRE": 9, "OCTUBRE": 10,
    "NOVIEMBRE": 11, "DICIEMBRE": 12
}
df["MES_NUM"] = df["MES_NOMBRE"].map(mes_map)
df["FECHA"] = pd.to_datetime(dict(year=df["AÑO"], month=df["MES_NUM"], day=1))
df = df.sort_values("FECHA")

# Entrenar SOLO con datos reales
if "TIPO_DATO" in df.columns:
    train_df = df[df["TIPO_DATO"].astype(str).str.upper() == "REAL"].copy()
    if train_df.empty:
        train_df = df.copy()
else:
    train_df = df.copy()
y = train_df.set_index("FECHA")["MONTO"].asfreq("MS")

order = (1, 1, 1)
model = ARIMA(y, order=order, enforce_stationarity=False, enforce_invertibility=False)
res = model.fit()

steps = 3
forecast_res = res.get_forecast(steps=steps)

yhat = forecast_res.predicted_mean #uso de la media para hacer las predicciones
ci = forecast_res.conf_int(alpha=0.05)  # uso del 95% en el rango Intervalo de Confianza

# Histórico
hist_out = (
    y.reset_index()
    .rename(columns={"FECHA": "fecha", "MONTO": "monto"})
)
hist_out["tipo_dato"] = "REAL"
hist_out["lower_95"] = np.nan
hist_out["upper_95"] = np.nan

# Pronóstico
pred_out = pd.DataFrame({
    "fecha": yhat.index,
    "monto": yhat.values,
    "tipo_dato": "PREDICCION",
    "lower_95": ci.iloc[:, 0].values,
    "upper_95": ci.iloc[:, 1].values
})

out = pd.concat([hist_out, pred_out], ignore_index=True).sort_values("fecha")

# Opcional: formatear fecha YYYY-MM-DD
out["fecha"] = out["fecha"].dt.strftime("%Y-%m-%d")

out_path = DATA_DIR / "kakebo_pred_hist.csv"
out.to_csv(out_path, index=False, encoding="utf-8")

print(f"Archivo exportado: {out_path}")
print(out.tail(15).to_string(index=False))

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=pd.to_datetime(hist_out["fecha"]),
    y=hist_out["monto"].values,
    mode="lines+markers",
    name="Datos Históricos (REALES)"
))

fig.add_trace(go.Scatter(
    x=yhat.index, y=yhat.values,
    mode="lines+markers",
    name="Predicción"
))

fig.add_trace(go.Scatter(
    x=ci.index,
    y=ci.iloc[:, 0].values,
    mode="lines",
    line=dict(width=0),
    showlegend=False
))
fig.add_trace(go.Scatter(
    x=ci.index,
    y=ci.iloc[:, 1].values,
    mode="lines",
    fill="tonexty",
    line=dict(width=0),
    name="Rango de Predicción - (IC 95%)"
))

fig.update_layout(
    title=f"Predicciones de gastos KAKEBO ",
    title_x=0.5,
    title_xanchor="center",
    xaxis_title="Fecha",
    yaxis_title="Monto",
    template="plotly_white",
    hovermode="x unified"
)
fig.show()


