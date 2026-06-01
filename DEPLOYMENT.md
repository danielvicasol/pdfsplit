# Guía de despliegue en Streamlit Cloud

## 📱 Pasos para desplegar en Streamlit.io

### 1. Preparación previa

Asegúrate de tener:
- Una cuenta en GitHub
- Una cuenta en Streamlit Community Cloud (https://streamlit.io/cloud)

### 2. Subir el código a GitHub

```bash
# Inicializar git en el directorio del proyecto
git init

# Agregar todos los archivos
git add .

# Hacer el primer commit
git commit -m "Initial commit: PDF to JSON converter"

# Agregar el repositorio remoto (reemplaza con tu URL)
git remote add origin https://github.com/tuusuario/pdfsplit.git

# Subir a GitHub
git branch -M main
git push -u origin main
```

### 3. Desplegar en Streamlit Cloud

1. Abre https://share.streamlit.io
2. Haz clic en "New app"
3. Selecciona:
   - **Repository**: tuusuario/pdfsplit
   - **Branch**: main
   - **Main file path**: app.py
4. Haz clic en "Deploy"

### 4. Esperar a que se despliegue

El despliegue tomará algunos minutos. Verás una barra de progreso. Una vez completado, tu aplicación estará disponible en:

```
https://pdfsplit.streamlit.app/
```

## ⚙️ Configuración en Streamlit Cloud

### Secrets (si es necesario)

1. Ve a los ajustes de tu aplicación
2. Ve a "Secrets"
3. Aquí puedes agregar variables de entorno

Para esta aplicación no se requieren secrets, pero si los necesitas en el futuro:

```toml
# .streamlit/secrets.toml (local)
# NO subir este archivo a GitHub

api_key = "tu_clave_api"
```

## 🔄 Actualizaciones automáticas

Cada vez que hagas push a la rama `main`, Streamlit Cloud:
1. Detecta los cambios automáticamente
2. Redeploy la aplicación
3. Muestra un indicador de "Updating..."

## 📊 Monitoreo

En el panel de Streamlit Cloud puedes:
- Ver logs de despliegue
- Monitorear uso de recursos
- Ver estadísticas de uso
- Configurar notificaciones

## 🚨 Límites de Streamlit Cloud

- **Recursos**: 1 GB RAM, 100 MB almacenamiento
- **Tamaño de archivo**: 200 MB por carga
- **Tiempo de ejecución**: Sin límite de tiempo
- **Gratuito**: Sí, con opción de plan premium

## 💡 Optimizaciones

### Para mejor rendimiento:

1. **Caché de resultados**:
```python
@st.cache_data
def procesar_pdf(archivo_pdf):
    # Tu código aquí
    pass
```

2. **Limpieza de sesión**:
```python
@st.cache_resource
def limpiar_temporales():
    # Ejecuta al inicio
    pass
```

3. **Reducción de carga**:
- Usa sesiones para almacenar resultados
- Evita reprocesar PDFs innecesariamente
- Limpia archivos temporales regularmente

## 🐛 Solución de problemas de despliegue

### El despliegue falla

1. Verifica que `requirements.txt` esté correcto
2. Asegúrate de que `app.py` sea el archivo principal
3. Revisa los logs de error en el panel

### La aplicación es lenta

1. Optimiza el código
2. Usa caché para cálculos pesados
3. Considera reducir el tamaño máximo de carga

### Error de librerías

1. Asegúrate de que todas las dependencias estén en `requirements.txt`
2. Usa versiones específicas en `requirements.txt`

## 📈 Próximos pasos

Considera agregar:
- Autenticación de usuarios
- Base de datos para historial
- Proceamiento asincrónico
- API REST backend
- Docker para despliegue personalizado

## 📚 Recursos útiles

- [Documentación de Streamlit Cloud](https://docs.streamlit.io/streamlit-cloud)
- [GitHub Pages para hosting estático](https://pages.github.com/)
- [Documentación de PyPDF2](https://pypdf2.readthedocs.io/)

---

¡Tu aplicación está lista para desplegarse! 🚀
