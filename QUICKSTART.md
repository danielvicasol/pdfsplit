## Inicio Rápido

### 1. Instalación

```bash
# Crear entorno virtual (opcional pero recomendado)
python -m venv venv
venv\Scripts\activate  # En Windows
# source venv/bin/activate  # En macOS/Linux

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Ejecutar la aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá en `http://localhost:8501`

### 3. Verificar la instalación

```bash
python setup_check.py
```

### 4. Usar ejemplos

```bash
python examples.py
```

### 5. Desplegar en Streamlit Cloud

Ver archivo [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 📁 Estructura del proyecto

```
pdfsplit/
├── app.py                    # Aplicación Streamlit
├── utils.py                  # Funciones auxiliares
├── examples.py              # Ejemplos prácticos
├── setup_check.py           # Verificador de setup
├── requirements.txt         # Dependencias
├── README.md               # Documentación completa
├── QUICKSTART.md           # Este archivo
├── DEPLOYMENT.md           # Guía de despliegue
├── .streamlit/
│   └── config.toml         # Config de Streamlit
├── .gitignore             # Archivos a ignorar
└── temp/                  # Archivos temporales (creados automáticamente)
```

## 🎯 Características principales

- ✅ Carga de PDFs
- ✅ Procesamiento de páginas
- ✅ Extracción de texto
- ✅ Codificación en base64
- ✅ Generación de JSON
- ✅ Barra de progreso
- ✅ Vista previa
- ✅ Descarga de resultados
- ✅ Limpieza automática

## 🚨 Solución de problemas

**Error: ModuleNotFoundError**
```bash
pip install -r requirements.txt
```

**La aplicación es lenta**
- Usa PDFs más pequeños
- Aumenta la RAM disponible

**Error al subir PDF**
- Verifica que el PDF sea válido
- Intenta con otro PDF

---

Para más información, ver [README.md](README.md)
