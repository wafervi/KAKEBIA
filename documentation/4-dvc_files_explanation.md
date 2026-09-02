# Archivos DVC del proyecto

## Qué es DVC

DVC (Data Version Control) mantiene en Git pequeños descriptores `.dvc` y almacena el contenido de los datos en un remoto o caché direccionado por hash MD5. El hash permite detectar si el archivo recuperado coincide con la versión registrada.

## Descriptores actuales

### `data/processed/kakebo_merged.csv.dvc`

```yaml
outs:
- md5: 54cffeb0fd093df6fae3239444b3c179
  size: 516
  hash: md5
  path: kakebo_merged.csv
```

Rastrea el CSV combinado que consume el modelo ARIMA.

### `data/processed/kakebo_pred_pbix.csv.dvc`

```yaml
outs:
- md5: e9e58fc31d2ed9a1563b491984e270ca
  size: 904
  hash: md5
  path: kakebo_pred_pbix.csv
```

Rastrea el CSV preparado para Power BI.

Los archivos `kakebo_pred.csv.dvc` y `kakebo_pred2.csv.dvc` descritos en versiones anteriores ya no forman parte del inventario actual. Tampoco existe un descriptor para `kakebo_pred_hist.csv`.

## Remoto configurado

La configuración versionada en `.dvc/config` contiene un remoto DVC de Google Drive y actualmente apunta a:

```text
../data versions
```

La carpeta local `data versions/` contiene objetos organizados por los primeros dos caracteres del MD5:

```text
data versions/files/md5/<primeros-2-caracteres>/<resto-del-hash>
```

No confundir esta ubicación con `data/processed/`, que contiene las copias de trabajo usadas por los scripts.

## Flujo operativo

Instalar DVC en el entorno activo si aún no está disponible:

```powershell
python -m pip install dvc dvc-gdrive
```

Recuperar los datos rastreados:

```powershell
dvc pull
```

Actualizar un archivo rastreado después de regenerarlo:

```powershell
dvc add data/processed/kakebo_merged.csv
dvc add data/processed/kakebo_pred_pbix.csv
```

Luego revisar los cambios en los `.dvc` y registrarlos en Git según el flujo del proyecto. `dvc add` actualiza el descriptor y el caché; no sustituye la confirmación de los cambios en Git.

## Consideraciones

- MD5 se usa para integridad y detección de cambios, no para seguridad criptográfica.
- `data/raw/` y `.env` son recursos locales sensibles o no versionados; DVC no reemplaza la configuración de la API de OpenAI.
- Tras `dvc pull`, verificar que `data/processed/kakebo_merged.csv` exista antes de ejecutar `models/ARIMA.py`.

*Actualizado: 2 de septiembre de 2026.*