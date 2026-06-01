FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Crear directorio para archivos temporales
RUN mkdir -p /tmp/streamlit

# Configurar Streamlit
RUN mkdir -p ~/.streamlit && \
    echo "[server]\n\
headless = true\n\
port = 8501\n\
runOnSave = true\n\
\n\
[client]\n\
toolbarMode = \"auto\"" > ~/.streamlit/config.toml

# Exponer puerto
EXPOSE 8501

# Health check
HEALTHCHECK CMD python -c "import requests; requests.get('http://localhost:8501')"

# Ejecutar la aplicación
CMD ["streamlit", "run", "app.py"]
