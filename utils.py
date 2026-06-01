"""
Utilidades para procesar PDFs y trabajar con los archivos JSON generados.

Este módulo proporciona funciones auxiliares para:
- Decodificar contenido base64
- Validar archivos JSON
- Procesar lotes de PDFs
- Exportar a diferentes formatos
"""

import json
import base64
from pathlib import Path
from typing import Dict, List, Optional
import tempfile
import os


def decodificar_contenido_base64(contenido_base64: str) -> str:
    """
    Decodifica contenido base64 a texto.
    
    Args:
        contenido_base64: String en base64
        
    Returns:
        String decodificado
    """
    try:
        return base64.b64decode(contenido_base64).decode('utf-8')
    except Exception as e:
        print(f"Error decodificando base64: {e}")
        return ""


def codificar_a_base64(texto: str) -> str:
    """
    Codifica texto a base64.
    
    Args:
        texto: String a codificar
        
    Returns:
        String en base64
    """
    try:
        return base64.b64encode(texto.encode('utf-8')).decode('utf-8')
    except Exception as e:
        print(f"Error codificando a base64: {e}")
        return ""


def validar_json_pdf(ruta_json: str) -> bool:
    """
    Valida que un archivo JSON tenga la estructura esperada.
    
    Args:
        ruta_json: Ruta al archivo JSON
        
    Returns:
        True si es válido, False si no
    """
    try:
        with open(ruta_json, 'r', encoding='utf-8') as f:
            datos = json.load(f)
        
        # Validar estructura
        assert "metadata" in datos, "Falta 'metadata'"
        assert "paginas" in datos, "Falta 'paginas'"
        assert "nombre_archivo" in datos["metadata"], "Falta 'nombre_archivo' en metadata"
        assert "total_paginas" in datos["metadata"], "Falta 'total_paginas' en metadata"
        
        # Validar que el número de páginas coincida
        assert len(datos["paginas"]) == datos["metadata"]["total_paginas"], \
            "El número de páginas no coincide"
        
        # Validar estructura de cada página
        for pagina in datos["paginas"]:
            assert "numero_pagina" in pagina, "Falta 'numero_pagina'"
            assert "contenido" in pagina, "Falta 'contenido'"
            assert "contenido_base64" in pagina, "Falta 'contenido_base64'"
        
        return True
    except (json.JSONDecodeError, AssertionError, FileNotFoundError) as e:
        print(f"Error validando JSON: {e}")
        return False


def cargar_json_pdf(ruta_json: str) -> Optional[Dict]:
    """
    Carga un archivo JSON de PDF procesado.
    
    Args:
        ruta_json: Ruta al archivo JSON
        
    Returns:
        Diccionario con los datos o None si hay error
    """
    try:
        with open(ruta_json, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error cargando JSON: {e}")
        return None


def obtener_pagina(datos_pdf: Dict, numero_pagina: int) -> Optional[Dict]:
    """
    Obtiene información de una página específica.
    
    Args:
        datos_pdf: Diccionario con datos del PDF
        numero_pagina: Número de página (1-indexado)
        
    Returns:
        Diccionario con datos de la página o None
    """
    try:
        if numero_pagina < 1 or numero_pagina > len(datos_pdf["paginas"]):
            return None
        return datos_pdf["paginas"][numero_pagina - 1]
    except (KeyError, IndexError, TypeError):
        return None


def obtener_contenido_pagina(datos_pdf: Dict, numero_pagina: int, 
                            usar_base64: bool = False) -> Optional[str]:
    """
    Obtiene el contenido de una página específica.
    
    Args:
        datos_pdf: Diccionario con datos del PDF
        numero_pagina: Número de página (1-indexado)
        usar_base64: Si es True, retorna el contenido en base64
        
    Returns:
        String con el contenido o None
    """
    pagina = obtener_pagina(datos_pdf, numero_pagina)
    if pagina is None:
        return None
    
    clave = "contenido_base64" if usar_base64 else "contenido"
    return pagina.get(clave)


def extraer_texto_completo(datos_pdf: Dict, usar_base64: bool = False) -> str:
    """
    Extrae todo el texto del PDF.
    
    Args:
        datos_pdf: Diccionario con datos del PDF
        usar_base64: Si es True, usa el contenido en base64
        
    Returns:
        String con todo el texto
    """
    texto_completo = []
    
    for pagina in datos_pdf.get("paginas", []):
        numero = pagina.get("numero_pagina")
        
        if usar_base64:
            contenido = decodificar_contenido_base64(pagina.get("contenido_base64", ""))
        else:
            contenido = pagina.get("contenido", "")
        
        if contenido:
            texto_completo.append(f"--- Página {numero} ---\n{contenido}")
    
    return "\n\n".join(texto_completo)


def guardar_texto_plano(datos_pdf: Dict, ruta_salida: str) -> bool:
    """
    Guarda todo el contenido del PDF como archivo de texto.
    
    Args:
        datos_pdf: Diccionario con datos del PDF
        ruta_salida: Ruta donde guardar el archivo
        
    Returns:
        True si se guardó exitosamente, False si no
    """
    try:
        texto = extraer_texto_completo(datos_pdf)
        with open(ruta_salida, 'w', encoding='utf-8') as f:
            f.write(texto)
        return True
    except Exception as e:
        print(f"Error guardando texto: {e}")
        return False


def obtener_estadisticas(datos_pdf: Dict) -> Dict:
    """
    Obtiene estadísticas del PDF procesado.
    
    Args:
        datos_pdf: Diccionario con datos del PDF
        
    Returns:
        Diccionario con estadísticas
    """
    total_caracteres = sum(
        pagina.get("caracteres", 0) 
        for pagina in datos_pdf.get("paginas", [])
    )
    
    return {
        "archivo": datos_pdf["metadata"]["nombre_archivo"],
        "total_paginas": datos_pdf["metadata"]["total_paginas"],
        "total_caracteres": total_caracteres,
        "caracteres_promedio": (
            total_caracteres / datos_pdf["metadata"]["total_paginas"]
            if datos_pdf["metadata"]["total_paginas"] > 0 else 0
        ),
        "fecha_procesamiento": datos_pdf["metadata"]["fecha_procesamiento"]
    }


def combinar_jsons(lista_rutas_json: List[str], ruta_salida: str) -> bool:
    """
    Combina múltiples archivos JSON de PDFs en uno solo.
    
    Args:
        lista_rutas_json: Lista de rutas a archivos JSON
        ruta_salida: Ruta donde guardar el JSON combinado
        
    Returns:
        True si se combinó exitosamente, False si no
    """
    try:
        todos_datos = {
            "metadata": {
                "cantidad_archivos": len(lista_rutas_json),
                "descripcion": "Múltiples PDFs combinados"
            },
            "archivos": []
        }
        
        for ruta in lista_rutas_json:
            datos = cargar_json_pdf(ruta)
            if datos:
                todos_datos["archivos"].append(datos)
        
        with open(ruta_salida, 'w', encoding='utf-8') as f:
            json.dump(todos_datos, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        print(f"Error combinando JSONs: {e}")
        return False


def limpiar_temporales(directorio: str = None) -> bool:
    """
    Limpia archivos temporales.
    
    Args:
        directorio: Directorio a limpiar (None para usar temp del sistema)
        
    Returns:
        True si se limpió exitosamente
    """
    try:
        if directorio is None:
            directorio = tempfile.gettempdir()
        
        for archivo in Path(directorio).glob("*.pdf"):
            try:
                archivo.unlink()
            except:
                pass
        
        return True
    except Exception as e:
        print(f"Error limpiando temporales: {e}")
        return False


# Ejemplo de uso
if __name__ == "__main__":
    # Ejemplo: validar un JSON
    # if validar_json_pdf("resultado_documento.json"):
    #     print("JSON válido")
    #     datos = cargar_json_pdf("resultado_documento.json")
    #     stats = obtener_estadisticas(datos)
    #     print(f"Estadísticas: {stats}")
    pass
