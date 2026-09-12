# Ejecución del aplicativo

## Requisitos

- Windows con PowerShell.
- Python instalado.
- El proyecto KAKEBIA descargado localmente.
- El entorno virtual `.venv` creado.
- El archivo `data/processed/kakebo_pred_hist.csv` disponible.

## Ubicación del aplicativo

El archivo principal de la aplicación es:

```text
app\KAKEBIA.py
```

La aplicación obtiene los datos desde:

```text
data\processed\kakebo_pred_hist.csv
```

## Iniciar la aplicación

Abrir PowerShell y ubicarse en la carpeta raíz del proyecto:

```powershell
cd "C:\UBICACIÓN DEL ARCHIVO EN TU PC\KAKEBIA"
```

Ejecutar Streamlit usando el intérprete del entorno virtual:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app\KAKEBIA.py
```

También es posible activar primero el entorno virtual:

```powershell
.\.venv\Scripts\Activate.ps1
streamlit run app\KAKEBIA.py
```

## Visualizar el dashboard

Después de ejecutar el comando, abrir en el navegador:

```text
http://localhost:8501
```

La terminal debe permanecer abierta mientras se utiliza el aplicativo.

## Detener el aplicativo

En la terminal donde se está ejecutando Streamlit, presionar:

```text
Ctrl + C
```

## Solución de problemas

### El comando `streamlit` no se reconoce

Ejecutar Streamlit mediante el intérprete del entorno virtual:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app\KAKEBIA.py
```

Si Streamlit no está instalado, instalarlo con:

```powershell
.\.venv\Scripts\python.exe -m pip install streamlit
```

### No se encuentra el archivo CSV

Verificar que exista el archivo:

```text
data\processed\kakebo_pred_hist.csv
```

La ruta se construye automáticamente a partir de la ubicación de `app\KAKEBIA.py`, por lo que la aplicación puede iniciarse desde la raíz del proyecto.

### El puerto 8501 está ocupado

Iniciar la aplicación en otro puerto:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app\KAKEBIA.py --server.port 8502
```

En ese caso, abrir:

```text
http://localhost:8502
```

## Resumen rápido (Ejemplo)

Para iniciar desde la consola de comandos:

```powershell
cd "C:\Users\WAGNER FERNÁNDEZ\OneDrive - POLICIA NACIONAL DE COLOMBIA\Documents\Ciencia de Datos\PROYECTOS\KAKEBIA"
.\.venv\Scripts\python.exe -m streamlit run app\KAKEBIA.py
```

Luego abrir `http://localhost:8501` en el navegador.
