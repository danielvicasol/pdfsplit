"""
Ejemplos de uso de la aplicación y el JSON generado.

Este archivo contiene ejemplos prácticos para:
- Procesar PDFs desde Python directamente
- Trabajar con los JSONs generados
- Buscar y filtrar contenido
- Exportar a diferentes formatos
"""

import json
import base64
from utils import (
    decodificar_contenido_base64,
    cargar_json_pdf,
    obtener_contenido_pagina,
    extraer_texto_completo,
    guardar_texto_plano,
    obtener_estadisticas,
    validar_json_pdf
)


# ============================================================================
# EJEMPLO 1: Cargar y explorar un JSON de PDF
# ============================================================================

def ejemplo_1_cargar_json():
    """Cargar y explorar un JSON de PDF procesado"""
    print("=" * 60)
    print("EJEMPLO 1: Cargar y explorar un JSON")
    print("=" * 60)
    
    # Cargar el JSON
    ruta_json = "resultado_documento.json"
    datos = cargar_json_pdf(ruta_json)
    
    if datos:
        print(f"\nArchivo: {datos['metadata']['nombre_archivo']}")
        print(f"Total de páginas: {datos['metadata']['total_paginas']}")
        print(f"Fecha: {datos['metadata']['fecha_procesamiento']}")
        
        # Información de la primera página
        primera_pagina = datos['paginas'][0]
        print(f"\nPrimera página contiene {primera_pagina['caracteres']} caracteres")
        print(f"Primeros 100 caracteres: {primera_pagina['contenido'][:100]}...")


# ============================================================================
# EJEMPLO 2: Decodificar contenido base64
# ============================================================================

def ejemplo_2_decodificar_base64():
    """Decodificar contenido que está en base64"""
    print("\n" + "=" * 60)
    print("EJEMPLO 2: Decodificar contenido base64")
    print("=" * 60)
    
    ruta_json = "resultado_documento.json"
    datos = cargar_json_pdf(ruta_json)
    
    if datos:
        # Obtener la primera página
        pagina = datos['paginas'][0]
        
        # Decodificar el base64
        if pagina['contenido_base64']:
            contenido_decodificado = decodificar_contenido_base64(
                pagina['contenido_base64']
            )
            print(f"Contenido decodificado: {contenido_decodificado[:150]}...")


# ============================================================================
# EJEMPLO 3: Buscar contenido en todas las páginas
# ============================================================================

def ejemplo_3_buscar_contenido():
    """Buscar una palabra clave en todo el PDF"""
    print("\n" + "=" * 60)
    print("EJEMPLO 3: Buscar contenido en el PDF")
    print("=" * 60)
    
    ruta_json = "resultado_documento.json"
    datos = cargar_json_pdf(ruta_json)
    palabra_buscada = "importante"
    
    resultados = []
    for pagina in datos['paginas']:
        if palabra_buscada.lower() in pagina['contenido'].lower():
            resultados.append({
                'pagina': pagina['numero_pagina'],
                'apariciones': pagina['contenido'].lower().count(palabra_buscada.lower())
            })
    
    if resultados:
        print(f"\nSe encontró '{palabra_buscada}' en {len(resultados)} páginas:")
        for resultado in resultados:
            print(f"  - Página {resultado['pagina']}: {resultado['apariciones']} vez(veces)")
    else:
        print(f"\nNo se encontró '{palabra_buscada}' en el PDF")


# ============================================================================
# EJEMPLO 4: Guardar contenido en un archivo de texto
# ============================================================================

def ejemplo_4_exportar_texto():
    """Exportar todo el contenido del PDF a un archivo de texto"""
    print("\n" + "=" * 60)
    print("EJEMPLO 4: Exportar a archivo de texto")
    print("=" * 60)
    
    ruta_json = "resultado_documento.json"
    datos = cargar_json_pdf(ruta_json)
    
    if datos:
        # Guardar como texto
        if guardar_texto_plano(datos, "contenido_extracto.txt"):
            print("✓ Archivo 'contenido_extracto.txt' creado exitosamente")
        else:
            print("✗ Error al guardar el archivo")


# ============================================================================
# EJEMPLO 5: Obtener estadísticas del PDF
# ============================================================================

def ejemplo_5_estadisticas():
    """Obtener estadísticas del PDF procesado"""
    print("\n" + "=" * 60)
    print("EJEMPLO 5: Estadísticas del PDF")
    print("=" * 60)
    
    ruta_json = "resultado_documento.json"
    datos = cargar_json_pdf(ruta_json)
    
    if datos:
        stats = obtener_estadisticas(datos)
        print(f"\nEstadísticas del archivo:")
        print(f"  Nombre: {stats['archivo']}")
        print(f"  Total de páginas: {stats['total_paginas']}")
        print(f"  Total de caracteres: {stats['total_caracteres']:,}")
        print(f"  Caracteres promedio por página: {stats['caracteres_promedio']:.0f}")
        print(f"  Fecha de procesamiento: {stats['fecha_procesamiento']}")


# ============================================================================
# EJEMPLO 6: Filtrar páginas por longitud de contenido
# ============================================================================

def ejemplo_6_filtrar_paginas():
    """Filtrar páginas que tengan más de X caracteres"""
    print("\n" + "=" * 60)
    print("EJEMPLO 6: Filtrar páginas por contenido")
    print("=" * 60)
    
    ruta_json = "resultado_documento.json"
    datos = cargar_json_pdf(ruta_json)
    minimo_caracteres = 500
    
    paginas_filtradas = [
        p for p in datos['paginas'] 
        if p['caracteres'] >= minimo_caracteres
    ]
    
    print(f"\nPáginas con al menos {minimo_caracteres} caracteres:")
    for pagina in paginas_filtradas:
        print(f"  - Página {pagina['numero_pagina']}: {pagina['caracteres']} caracteres")


# ============================================================================
# EJEMPLO 7: Crear un nuevo JSON combinado
# ============================================================================

def ejemplo_7_procesar_multiplos():
    """Procesar y combinar información de múltiples JSONs"""
    print("\n" + "=" * 60)
    print("EJEMPLO 7: Procesar múltiples JSONs")
    print("=" * 60)
    
    archivos = ["resultado_1.json", "resultado_2.json", "resultado_3.json"]
    
    datos_combinados = {
        "archivos_procesados": len(archivos),
        "resumen": []
    }
    
    for archivo in archivos:
        datos = cargar_json_pdf(archivo)
        if datos:
            resumen = obtener_estadisticas(datos)
            datos_combinados["resumen"].append(resumen)
    
    # Guardar el combinado
    with open("resumen_combinado.json", 'w', encoding='utf-8') as f:
        json.dump(datos_combinados, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Resumen de {len(archivos)} archivos guardado en 'resumen_combinado.json'")


# ============================================================================
# EJEMPLO 8: Validar estructura del JSON
# ============================================================================

def ejemplo_8_validar():
    """Validar que el JSON tenga la estructura correcta"""
    print("\n" + "=" * 60)
    print("EJEMPLO 8: Validar estructura del JSON")
    print("=" * 60)
    
    ruta_json = "resultado_documento.json"
    
    if validar_json_pdf(ruta_json):
        print(f"✓ El archivo '{ruta_json}' tiene una estructura válida")
    else:
        print(f"✗ El archivo '{ruta_json}' tiene errores de estructura")


# ============================================================================
# EJEMPLO 9: Extraer metadata
# ============================================================================

def ejemplo_9_metadata():
    """Extraer y mostrar metadata del PDF"""
    print("\n" + "=" * 60)
    print("EJEMPLO 9: Metadata del PDF")
    print("=" * 60)
    
    ruta_json = "resultado_documento.json"
    datos = cargar_json_pdf(ruta_json)
    
    if datos:
        metadata = datos['metadata']
        print(f"\nMetadata:")
        for clave, valor in metadata.items():
            print(f"  {clave}: {valor}")


# ============================================================================
# EJEMPLO 10: Crear archivo CSV con índice de páginas
# ============================================================================

def ejemplo_10_generar_csv():
    """Generar un archivo CSV con índice de todas las páginas"""
    print("\n" + "=" * 60)
    print("EJEMPLO 10: Generar CSV con índice")
    print("=" * 60)
    
    ruta_json = "resultado_documento.json"
    datos = cargar_json_pdf(ruta_json)
    
    if datos:
        import csv
        
        with open("indice_paginas.csv", 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Página', 'Caracteres', 'Primeros 100 caracteres'])
            
            for pagina in datos['paginas']:
                primer_texto = pagina['contenido'][:100].replace('\n', ' ')
                writer.writerow([
                    pagina['numero_pagina'],
                    pagina['caracteres'],
                    primer_texto
                ])
        
        print("✓ Archivo 'indice_paginas.csv' creado exitosamente")


# ============================================================================
# EJEMPLO 11: Verificar integridad del contenido base64
# ============================================================================

def ejemplo_11_verificar_integridad():
    """Verificar que el contenido base64 sea válido"""
    print("\n" + "=" * 60)
    print("EJEMPLO 11: Verificar integridad base64")
    print("=" * 60)
    
    ruta_json = "resultado_documento.json"
    datos = cargar_json_pdf(ruta_json)
    
    si_valido = 0
    for pagina in datos['paginas']:
        try:
            # Intentar decodificar
            decodificado = decodificar_contenido_base64(pagina['contenido_base64'])
            # Verificar que coincida con el original
            if decodificado == pagina['contenido']:
                si_valido += 1
        except:
            pass
    
    total = len(datos['paginas'])
    print(f"\nIntegridad verificada: {si_valido}/{total} páginas válidas")
    
    if si_valido == total:
        print("✓ Todos los contenidos en base64 son válidos")
    else:
        print(f"✗ {total - si_valido} páginas tienen problemas")


# ============================================================================
# MENÚ PRINCIPAL
# ============================================================================

def menu_principal():
    """Muestra un menú con todos los ejemplos disponibles"""
    ejemplos = {
        '1': ('Cargar y explorar JSON', ejemplo_1_cargar_json),
        '2': ('Decodificar base64', ejemplo_2_decodificar_base64),
        '3': ('Buscar contenido', ejemplo_3_buscar_contenido),
        '4': ('Exportar a texto', ejemplo_4_exportar_texto),
        '5': ('Estadísticas del PDF', ejemplo_5_estadisticas),
        '6': ('Filtrar páginas', ejemplo_6_filtrar_paginas),
        '7': ('Procesar múltiples', ejemplo_7_procesar_multiplos),
        '8': ('Validar estructura', ejemplo_8_validar),
        '9': ('Extraer metadata', ejemplo_9_metadata),
        '10': ('Generar CSV', ejemplo_10_generar_csv),
        '11': ('Verificar integridad', ejemplo_11_verificar_integridad),
    }
    
    print("\n" + "=" * 60)
    print("EJEMPLOS DE USO - PDF a JSON Converter")
    print("=" * 60)
    print("\nElige un ejemplo para ejecutar:")
    
    for clave, (descripcion, _) in ejemplos.items():
        print(f"  {clave}. {descripcion}")
    
    print(f"  0. Ejecutar todos")
    print(f"  q. Salir\n")
    
    opcion = input("Opción: ").strip().lower()
    
    if opcion == 'q':
        print("¡Hasta luego!")
        return
    
    if opcion == '0':
        for _, (_, func) in ejemplos.items():
            try:
                func()
            except FileNotFoundError:
                print(f"⚠ Archivo no encontrado. Asegúrate de tener archivos JSON generados.")
                break
            except Exception as e:
                print(f"⚠ Error: {e}")
    
    elif opcion in ejemplos:
        _, func = ejemplos[opcion]
        try:
            func()
        except FileNotFoundError:
            print("⚠ Archivo no encontrado. Asegúrate de tener archivos JSON generados.")
        except Exception as e:
            print(f"⚠ Error: {e}")
    else:
        print("Opción inválida")


if __name__ == "__main__":
    menu_principal()
