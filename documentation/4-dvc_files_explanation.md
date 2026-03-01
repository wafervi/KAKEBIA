# Archivos .dvc - Documentación Técnica

## Descripción General

Los archivos con extensión `.dvc` son archivos de metadatos generados por **DVC (Data Version Control)**, una herramienta de control de versiones diseñada específicamente para gestionar datasets y modelos de machine learning. Estos archivos actúan como punteros ligeros hacia los archivos de datos reales, permitiendo versionar datos de gran tamaño sin almacenarlos directamente en Git.

## Arquitectura y Funcionamiento

DVC implementa un sistema de almacenamiento basado en contenido direccionable (content-addressable storage) utilizando hashes MD5. Los archivos de datos reales se almacenan en la carpeta `.dvc/cache` o en un almacenamiento remoto configurado, mientras que los archivos `.dvc` contienen únicamente los metadatos necesarios para recuperarlos.

## Estructura de Archivos .dvc

Cada archivo `.dvc` es un descriptor YAML con la siguiente estructura:

```yaml
outs:
  - md5: <hash_md5_del_archivo>
    size: <tamaño_en_bytes>
    hash: md5
    path: <ruta_relativa_al_archivo>
```

## Inventario de Archivos en el Proyecto

### 1. `kakebo_pred.csv.dvc`

```yaml
outs:
  - md5: 8392d0a11035bae6d7d7e3f42253040b
    size: 491
    hash: md5
    path: kakebo_pred.csv
```

**Propósito**: Rastrea el archivo de predicciones en formato simple que contiene datos históricos reales y una predicción para el siguiente mes.

**Ubicación del contenido real**: `data versions/files/md5/83/92d0a11035bae6d7d7e3f42253040b`

**Tamaño**: 491 bytes

---

### 2. `kakebo_pred2.csv.dvc`

```yaml
outs:
  - md5: 8d113f045bf9b6ee7c6d9dbe9d792d03
    size: 517
    hash: md5
    path: kakebo_pred2.csv
```

**Propósito**: Rastrea el archivo de predicciones con formato colombiano (separadores de miles).

**Ubicación del contenido real**: `data versions/files/md5/8d/113f045bf9b6ee7c6d9dbe9d792d03`

**Tamaño**: 517 bytes

---

### 3. `kakebo_pred_pbix.csv.dvc`

```yaml
outs:
  - md5: 73b29be7cba18fb1dc24698c27de26aa
    size: 1069
    hash: md5
    path: kakebo_pred_pbix.csv
```

**Propósito**: Rastrea el archivo optimizado para visualización en Power BI, que incluye una columna adicional con formato de moneda colombiana.

**Ubicación del contenido real**: `data versions/files/md5/73/b29be7cba18fb1dc24698c27de26aa`

**Tamaño**: 1,069 bytes

---

## Almacenamiento en Caché

Los archivos de datos rastreados por DVC se almacenan en la estructura de directorios `data versions/files/md5/`, organizados jerárquicamente utilizando los primeros dos caracteres del hash MD5 como subdirectorio. Esta estructura optimiza el acceso y previene la saturación de un único directorio con miles de archivos.

**Patrón de almacenamiento**:
```
data versions/files/md5/<primeros_2_chars>/<resto_del_hash>
```

## Ventajas del Sistema de Versionado

1. **Eficiencia en Git**: Los archivos `.dvc` (≈100 bytes) se versionan en Git en lugar de los archivos de datos completos, reduciendo significativamente el tamaño del repositorio.

2. **Integridad de Datos**: El hash MD5 garantiza la integridad del contenido. Cualquier modificación en el archivo de datos generará un hash diferente.

3. **Trazabilidad**: Cada versión del modelo o dataset queda registrada con su hash único, permitiendo reproducibilidad total del pipeline.

4. **Compatibilidad con CI/CD**: Los archivos `.dvc` permiten integrar pipelines de datos en flujos de integración continua sin transferir grandes volúmenes de información.

## Workflows Operativos

**Para recuperar los archivos de datos**:
```bash
dvc pull
```

**Para actualizar el tracking después de modificar un archivo**:
```bash
dvc add data/processed/kakebo_pred.csv
```

**Para versionar cambios**:
```bash
git add data/processed/kakebo_pred.csv.dvc
git commit -m "Update predictions dataset"
```

## Consideraciones Técnicas

- **Algoritmo de hash**: MD5 (suficiente para detección de cambios, no recomendado para seguridad criptográfica)
- **Formato**: YAML
- **Compatibilidad**: DVC 2.x o superior
- **Dependencias**: Requiere DVC instalado en el entorno de desarrollo

---

*Documentación generada en marzo de 2026*
