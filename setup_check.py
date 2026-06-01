"""
Script de prueba rápida para validar la instalación y configuración.
Ejecuta este archivo para verificar que todo funciona correctamente.
"""

import sys
import importlib


def verificar_dependencias():
    """Verifica que todas las dependencias necesarias estén instaladas"""
    print("=" * 60)
    print("VERIFICACIÓN DE DEPENDENCIAS")
    print("=" * 60)
    
    dependencias = {
        'streamlit': 'Streamlit',
        'PyPDF2': 'PyPDF2',
        'json': 'JSON (Built-in)',
        'base64': 'Base64 (Built-in)',
    }
    
    todos_ok = True
    for modulo, nombre in dependencias.items():
        try:
            if modulo not in ['json', 'base64']:
                importlib.import_module(modulo)
            print(f"✓ {nombre}: OK")
        except ImportError:
            print(f"✗ {nombre}: NO INSTALADO")
            todos_ok = False
    
    print("\n" + "=" * 60)
    if todos_ok:
        print("✓ ¡TODAS LAS DEPENDENCIAS ESTÁN CORRECTAMENTE INSTALADAS!")
    else:
        print("✗ Faltan algunas dependencias.")
        print("Ejecuta: pip install -r requirements.txt")
    print("=" * 60)
    
    return todos_ok


def mostrar_info_sistema():
    """Muestra información del sistema"""
    print("\n" + "=" * 60)
    print("INFORMACIÓN DEL SISTEMA")
    print("=" * 60)
    
    print(f"Python: {sys.version}")
    print(f"Plataforma: {sys.platform}")
    print(f"Versión de pip: {importlib.import_module('pip').__version__ if hasattr(importlib.import_module('pip'), '__version__') else 'Desconocida'}")
    
    print("=" * 60)


def mostrar_instrucciones():
    """Muestra instrucciones de inicio rápido"""
    print("\n" + "=" * 60)
    print("INSTRUCCIONES DE INICIO RÁPIDO")
    print("=" * 60)
    
    print("""
1. INSTALAR DEPENDENCIAS:
   pip install -r requirements.txt

2. EJECUTAR LA APLICACIÓN:
   streamlit run app.py
   
   La aplicación se abrirá en: http://localhost:8501

3. USAR LA APLICACIÓN:
   - Sube un PDF
   - Haz clic en "Procesar PDF"
   - Espera a que se complete el procesamiento
   - Visualiza y descarga el JSON

4. EJEMPLOS DE USO EN PYTHON:
   python examples.py

5. DESPLEGAR EN STREAMLIT CLOUD:
   - Sube el código a GitHub
   - Ve a https://share.streamlit.io
   - Selecciona tu repositorio
   - Espera a que se despliegue

ARCHIVOS DEL PROYECTO:
├── app.py                    # Aplicación principal Streamlit
├── utils.py                  # Utilidades para procesamiento
├── examples.py              # Ejemplos de uso
├── requirements.txt         # Dependencias de Python
├── README.md               # Documentación completa
├── DEPLOYMENT.md           # Guía de despliegue
└── .streamlit/config.toml  # Configuración de Streamlit
    """)
    
    print("=" * 60)


def main():
    """Función principal"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "PDF a JSON Base64 - VERIFICACIÓN DE SETUP" + " " * 6 + "║")
    print("╚" + "=" * 58 + "╝")
    
    # Verificar dependencias
    deps_ok = verificar_dependencias()
    
    # Mostrar información del sistema
    mostrar_info_sistema()
    
    # Mostrar instrucciones
    mostrar_instrucciones()
    
    # Resumen final
    print("\n" + "=" * 60)
    if deps_ok:
        print("✓ ¡SETUP COMPLETADO! Ejecuta: streamlit run app.py")
    else:
        print("✗ Por favor instala las dependencias primero:")
        print("  pip install -r requirements.txt")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
