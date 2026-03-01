# Configuración del Entorno Virtual - KAKEBIA

## Proyecto: Kakebo Analytics - Análisis de Gastos del Hogar

### Fecha de Configuración: 20 de febrero de 2026

---

## 📦 Entorno Virtual Creado

Se ha configurado exitosamente un entorno virtual para el proyecto KAKEBIA con las siguientes características:

- **Tipo de Entorno**: Virtual Environment (.venv)
- **Versión de Python**: 3.13.0
- **Ubicación**: `.venv/` en el directorio raíz del proyecto

---

## 🔧 Pasos Realizados

### 1. Creación del Entorno Virtual

```powershell
python -m venv venv
```

### 2. Activación del Entorno Virtual

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Instalación de Dependencias

Todas las dependencias del archivo `requirements.txt` fueron instaladas exitosamente.

---

## 📚 Librerías Instaladas

| Librería | Versión | Propósito |
|----------|---------|-----------|
| **pandas** | 2.2.3 | Manipulación y análisis de datos |
| **numpy** | 2.2.0 | Operaciones numéricas |
| **plotly** | 5.24.1 | Visualización interactiva de datos |
| **statsmodels** | 0.14.4 | Modelos estadísticos y series temporales (ARIMA) |
| **openai** | 1.90.0 | Integración con la API de OpenAI |
| **openpyxl** | 3.1.5 | Lectura/escritura de archivos Excel |
| **python-dotenv** | 1.1.0 | Gestión de variables de entorno |

---

## 🚀 Uso del Entorno Virtual

### Activar el Entorno Virtual

En **PowerShell**:
```powershell
.\.venv\Scripts\Activate.ps1
```

En **CMD**:
```cmd
.venv\Scripts\activate.bat
```

### Desactivar el Entorno Virtual

```powershell
deactivate
```

### Instalar Nuevas Dependencias

```powershell
pip install nombre-paquete
```

### Actualizar requirements.txt

Después de instalar nuevas dependencias:
```powershell
pip freeze > requirements.txt
```

---

## 📝 Notas Importantes

1. **Siempre activa el entorno virtual** antes de ejecutar scripts o notebooks del proyecto.
2. El entorno virtual está configurado para usar **Python 3.13.0**.
3. Las variables de entorno sensibles (como `OPENAI_API_KEY`) deben configurarse en un archivo `.env`.
4. El directorio `.venv/` debe estar incluido en `.gitignore` para no subir el entorno virtual al repositorio.

---

## 🔍 Verificación de la Instalación

Para verificar que todas las librerías están correctamente instaladas:

```powershell
pip list
```

Para verificar la versión de Python:

```powershell
python --version
```

---

## ⚙️ Comando para Ejecutar Python

Cuando el entorno virtual está activado, puedes ejecutar scripts directamente:

```powershell
python pipelines/main.py
```

O de manera explícita usando la ruta completa:

```powershell
"KAKEBIA/.venv/Scripts/python.exe" pipelines/main.py
```

---

## ✅ Estado del Proyecto

- ✅ Entorno virtual creado
- ✅ Python 3.13.0 configurado
- ✅ Todas las dependencias instaladas
- ✅ Proyecto listo para desarrollo y ejecución

---

**Elaborado por**: Wagner Fernández V.  
**Especialista en Ciencia de Datos y Analítica**
---

*Documentación generada en marzo de 2026*