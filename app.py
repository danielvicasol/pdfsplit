import streamlit as st
import PyPDF2
import base64
import json
import os
from pathlib import Path
from datetime import datetime
import tempfile
import time

# Configuración de la página
st.set_page_config(
    page_title="PDF a JSON Base64",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos personalizados
st.markdown("""
    <style>
    .stProgress > div > div > div > div {
        background-color: #1f77b4;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    </style>
""", unsafe_allow_html=True)

def procesar_pdf(archivo_pdf):
    """
    Procesa un archivo PDF y extrae todas las páginas como imágenes en base64.
    
    Args:
        archivo_pdf: Archivo PDF subido
        
    Returns:
        dict: Diccionario con información del PDF y páginas en base64
    """
    temp_path = None
    try:
        # Leer contenido del archivo en memoria
        contenido_pdf = archivo_pdf.read()
        
        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(contenido_pdf)
            temp_path = tmp_file.name
        
        # Leer el PDF y mantener el archivo abierto durante el procesamiento
        pdf_file = open(temp_path, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_paginas = len(pdf_reader.pages)
        
        # Crear contenedor para el progreso
        progress_container = st.container()
        contador_container = st.container()
        
        with progress_container:
            progress_bar = st.progress(0)
        
        # Estructura de datos para el resultado
        resultado = {
            "metadata": {
                "nombre_archivo": archivo_pdf.name,
                "fecha_procesamiento": datetime.now().isoformat(),
                "total_paginas": num_paginas,
                "formato": "application/pdf"
            },
            "paginas": []
        }
        
        # Procesar cada página
        with st.spinner("🔄 Procesando PDF..."):
            for idx in range(num_paginas):
                # Actualizar barra de progreso
                progreso = (idx + 1) / num_paginas
                progress_bar.progress(progreso)
                
                with contador_container:
                    st.metric(
                        "Progreso", 
                        f"{idx + 1} / {num_paginas}",
                        f"{int(progreso * 100)}%"
                    )
                
                # Extraer texto de la página
                pagina = pdf_reader.pages[idx]
                texto_pagina = pagina.extract_text()
                
                # Crear información de la página
                info_pagina = {
                    "numero_pagina": idx + 1,
                    "contenido": texto_pagina,
                    "contenido_base64": base64.b64encode(
                        texto_pagina.encode('utf-8')
                    ).decode('utf-8') if texto_pagina else "",
                    "caracteres": len(texto_pagina) if texto_pagina else 0
                }
                
                resultado["paginas"].append(info_pagina)
                
                # Pequeña pausa para visualizar el progreso
                time.sleep(0.1)
        
        # Cerrar el archivo
        pdf_file.close()
        
        # Limpiar archivo temporal
        os.unlink(temp_path)
        
        return resultado
    
    except Exception as e:
        st.error(f"❌ Error al procesar el PDF: {str(e)}")
        # Intentar limpiar archivo temporal
        if temp_path:
            try:
                os.unlink(temp_path)
            except:
                pass
        return None

def descargar_json(datos_json):
    """
    Genera y retorna el JSON para descarga.
    
    Args:
        datos_json: Diccionario con datos del PDF procesado
        
    Returns:
        str: JSON formateado
    """
    return json.dumps(datos_json, ensure_ascii=False, indent=2)

# Interfaz principal
st.title("📄 Convertidor PDF a JSON Base64")
st.markdown("---")
st.markdown("Sube un PDF y recibe un archivo JSON con el contenido de cada página en base64")

# Sección de carga
st.subheader("📤 Subir PDF")
archivo_pdf = st.file_uploader(
    "Selecciona un archivo PDF",
    type="pdf",
    key="pdf_uploader"
)

# Variables de sesión
if 'resultado_pdf' not in st.session_state:
    st.session_state.resultado_pdf = None

if 'archivo_procesado' not in st.session_state:
    st.session_state.archivo_procesado = None

# Procesar PDF si se cargó
if archivo_pdf is not None:
    st.info(f"📄 Archivo: {archivo_pdf.name} ({archivo_pdf.size / 1024:.2f} KB)")
    
    if st.button("🚀 Procesar PDF", type="primary", use_container_width=True):
        st.session_state.resultado_pdf = procesar_pdf(archivo_pdf)
        st.session_state.archivo_procesado = archivo_pdf.name

# Mostrar resultados si están disponibles
if st.session_state.resultado_pdf is not None:
    st.markdown("---")
    st.success("✅ ¡PDF procesado exitosamente!")
    
    # Información del archivo
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Total de páginas",
            st.session_state.resultado_pdf["metadata"]["total_paginas"]
        )
    with col2:
        st.metric(
            "Archivo",
            st.session_state.resultado_pdf["metadata"]["nombre_archivo"]
        )
    with col3:
        st.metric(
            "Fecha",
            datetime.fromisoformat(
                st.session_state.resultado_pdf["metadata"]["fecha_procesamiento"]
            ).strftime("%H:%M:%S")
        )
    
    st.markdown("---")
    st.subheader("📋 Vista previa del contenido")
    
    # Selector de página
    num_paginas = st.session_state.resultado_pdf["metadata"]["total_paginas"]
    pagina_seleccionada = st.slider(
        "Selecciona una página para previsualizar:",
        min_value=1,
        max_value=num_paginas,
        value=1
    )
    
    # Mostrar contenido de la página seleccionada
    pagina = st.session_state.resultado_pdf["paginas"][pagina_seleccionada - 1]
    
    st.markdown(f"**Página {pagina['numero_pagina']}**")
    st.info(f"Caracteres: {pagina['caracteres']}")
    
    with st.expander("📝 Ver contenido de texto"):
        st.text_area(
            "Contenido extraído:",
            value=pagina['contenido'] if pagina['contenido'] else "No se extrajo contenido",
            height=200,
            disabled=True
        )
    
    with st.expander("🔐 Ver contenido en Base64"):
        st.text_area(
            "Contenido en Base64:",
            value=pagina['contenido_base64'] if pagina['contenido_base64'] else "No hay contenido",
            height=150,
            disabled=True
        )
    
    st.markdown("---")
    st.subheader("💾 Descargar resultados")
    
    # Generar JSON
    json_resultado = descargar_json(st.session_state.resultado_pdf)
    
    # Botón de descarga
    st.download_button(
        label="⬇️ Descargar JSON",
        data=json_resultado,
        file_name=f"resultado_{Path(st.session_state.archivo_procesado).stem}.json",
        mime="application/json",
        use_container_width=True
    )
    
    # Información de la descarga
    st.markdown("""
    <div class="success-box">
    <strong>✨ Instrucciones:</strong><br>
    1. Haz clic en el botón para descargar el archivo JSON<br>
    2. El JSON contiene todas las páginas con su contenido en base64<br>
    3. El archivo PDF se eliminará automáticamente después de descargar
    </div>
    """, unsafe_allow_html=True)
    
    # Botón para limpiar y procesar otro PDF
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Limpiar y comenzar de nuevo", use_container_width=True):
            st.session_state.resultado_pdf = None
            st.session_state.archivo_procesado = None
            st.rerun()
    
    with col2:
        # Información sobre limpieza automática
        st.caption("🔄 Los archivos se limpian automáticamente")

else:
    if archivo_pdf is None:
        st.markdown("""
        ### 🎯 ¿Cómo funciona?
        
        1. **📤 Sube** un archivo PDF
        2. **⚙️ Procesa** automáticamente cada página
        3. **📊 Visualiza** el contenido extraído
        4. **💾 Descarga** como JSON con base64
        5. **🧹 Limpia** los archivos temporales
        
        ### 📋 Formato del JSON resultante:
        ```json
        {
            "metadata": {
                "nombre_archivo": "documento.pdf",
                "fecha_procesamiento": "2024-01-01T12:00:00",
                "total_paginas": 5,
                "formato": "application/pdf"
            },
            "paginas": [
                {
                    "numero_pagina": 1,
                    "contenido": "Texto extraído de la página...",
                    "contenido_base64": "VGV4dG8gZXh0cmHDsWRvIGRl...",
                    "caracteres": 1234
                }
            ]
        }
        ```
        """)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray; font-size: 0.8rem;'>"
    "Aplicación de procesamiento de PDF | Versión 1.0 | 2024"
    "</p>",
    unsafe_allow_html=True
)
