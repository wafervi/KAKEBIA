# Configuración del entorno virtual

## Requisitos

- Windows con PowerShell o CMD.
- Python 3.13.0, que es la versión usada por el entorno actual.
- El repositorio clonado localmente.

Los datos de `data/raw/`, el archivo `.env` y otros archivos locales no se versionan. Una clonación limpia requiere restaurarlos por separado, mediante DVC cuando corresponda.

## Crear y activar `.venv`

Desde la raíz de `KAKEBIA`:

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

En CMD:

```cmd
.venv\Scripts\activate.bat
```

Para salir del entorno:

```powershell
deactivate
```

## Instalar dependencias

```powershell
python -m pip install --upgrade pip
python -m pip install -r documentation\requirements.txt
```

Las dependencias fijadas incluyen pandas 2.2.3, numpy 2.2.0, plotly 5.24.1, statsmodels 0.14.4, openai 1.90.0, openpyxl 3.1.5 y python-dotenv 1.1.0. La aplicación Streamlit requiere instalar adicionalmente `streamlit`, porque todavía no está incluido en `documentation/requirements.txt`.

```powershell
python -m pip install streamlit
```

Verificar la instalación:

```powershell
python --version
python -m pip list
```

## Variables de entorno

Crear `.env` en la raíz del repositorio:

```text
OPENAI_API_KEY=tu_clave_de_openai
```

No incluir la clave en Git, documentación, notebooks ni capturas. `pipelines/functions.py` carga `.env` usando una ruta relativa, por lo que el pipeline ETL debe ejecutarse desde la raíz del proyecto.

## Comandos principales

Pipeline ETL:

```powershell
python pipelines\combinator.py
```

Modelo ARIMA y dashboard:

```powershell
python models\ARIMA.py
```

Aplicación interactiva Streamlit:

```powershell
streamlit run app\KAKEBIA.py
```

La aplicación lee `data/processed/kakebo_pred_hist.csv`; ese archivo debe existir antes de iniciarla.

Notebook: abrir `notebooks/ARIMA (KAKEBIA).ipynb` con el intérprete `.venv` y ejecutar las celdas en orden.

## Actualizar dependencias

```powershell
python -m pip install nombre-paquete
python -m pip freeze | Out-File -Encoding utf8 documentation\requirements.txt
```

*Actualizado: 9 de septiembre de 2026.*