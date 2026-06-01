# PDF to JSON Base64 Converter

Aplicación Streamlit para convertir archivos PDF a JSON con contenido en base64.

## 🚀 Características

- ✅ Carga de archivos PDF
- ✅ Procesamiento de todas las páginas
- ✅ Extracción de contenido de texto
- ✅ Codificación en base64 de cada página
- ✅ Barra de progreso con contador
- ✅ Spinner animado durante el procesamiento
- ✅ Descarga de JSON con resultados
- ✅ Limpieza automática de archivos temporales
- ✅ Vista previa del contenido
- ✅ Información detallada de metadatos

## 📋 Requisitos previos

- Python 3.8+
- pip (gestor de paquetes de Python)

## 🔧 Instalación

### 1. Clonar el repositorio o descargar los archivos

```bash
cd pdfsplit
```

### 2. Crear un entorno virtual (recomendado)

**En Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**En macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 🎯 Uso

### Ejecución local

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en `http://localhost:8501`

### Desplegar en Streamlit Cloud

1. Sube tu repositorio a GitHub
2. Ve a https://share.streamlit.io
3. Inicia sesión con tu cuenta de GitHub
4. Selecciona tu repositorio
5. La aplicación se desplegará automáticamente

## 📊 Formato de salida JSON

El JSON generado tiene la siguiente estructura:

```json
{
    "metadata": {
        "nombre_archivo": "documento.pdf",
        "fecha_procesamiento": "2024-01-01T12:00:00.123456",
        "total_paginas": 5,
        "formato": "application/pdf"
    },
    "paginas": [
        {
            "numero_pagina": 1,
            "contenido": "Texto extraído de la página...",
            "contenido_base64": "VGV4dG8gZXh0cmHDsWRvIGRlIGxhIHDDomdpbmEu...",
            "caracteres": 1234
        },
        {
            "numero_pagina": 2,
            "contenido": "Contenido de la segunda página...",
            "contenido_base64": "Q29udGVuaWRvIGRlIGxhIHNlZ3VuZGEgcMOhZ2luYS4u...",
            "caracteres": 2567
        }
    ]
}
```

## 🎨 Interfaz de usuario

### Sección de carga
- Selector de archivo PDF
- Información del archivo seleccionado

### Sección de procesamiento
- Barra de progreso en tiempo real
- Contador de páginas procesadas
- Spinner animado

### Sección de resultados
- Información de metadatos (página, tamaño, fecha)
- Selector de página para previsualizar
- Vista previa de contenido de texto
- Vista previa de contenido en Base64
- Botón de descarga de JSON

### Limpieza
- Eliminación automática de archivos temporales
- Botón para procesar otro PDF

## 🔒 Seguridad

- Los archivos se procesan localmente
- Los archivos temporales se eliminan automáticamente
- Tamaño máximo de carga: 200 MB
- No se almacenan datos en servidores externos

## 📦 Dependencias

- **streamlit**: Framework para crear aplicaciones web interactivas
- **PyPDF2**: Librería para leer y procesar archivos PDF
- **python-multipart**: Soporte para cargas de archivos

## 🐛 Solución de problemas

### El PDF no se procesa correctamente
- Verifica que el PDF sea válido
- Intenta con un PDF diferente
- Revisa que el PDF no esté corrupto

### Error de memoria
- Los PDFs muy grandes pueden causar problemas
- Intenta procesar PDFs más pequeños
- Aumenta la memoria disponible del sistema

### La aplicación no inicia
- Verifica que todas las dependencias estén instaladas: `pip install -r requirements.txt`
- Reinicia el entorno virtual
- Revisa los logs de error en la consola

## 📝 Estructura del proyecto

```
pdfsplit/
├── app.py                 # Aplicación principal de Streamlit
├── requirements.txt       # Dependencias de Python
├── .streamlit/
│   └── config.toml       # Configuración de Streamlit
├── .gitignore            # Archivos a ignorar en Git
├── README.md             # Este archivo
└── __pycache__/          # Cache de Python (auto-generado)
```

## 📄 Licencia

Este proyecto está disponible bajo la Licencia MIT.

## 👨‍💻 Contribuciones

Las contribuciones son bienvenidas. Por favor, crea un fork del repositorio y envía un pull request.

## 📧 Contacto

Para preguntas o sugerencias, abre un issue en el repositorio.

---

**Versión**: 1.0  
**Última actualización**: 2024
