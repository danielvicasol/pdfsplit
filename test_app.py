"""
Tests unitarios para la aplicación y utilidades.

Para ejecutar los tests:
    pip install pytest
    pytest test_app.py -v
"""

import json
import tempfile
import os
from pathlib import Path

# Tests para utils.py
from utils import (
    codificar_a_base64,
    decodificar_contenido_base64,
    validar_json_pdf,
    guardar_texto_plano,
    obtener_estadisticas,
)


class TestCodecBase64:
    """Tests para las funciones de codificación/decodificación base64"""
    
    def test_codificar_simple(self):
        """Test: Codificar un string simple"""
        texto = "Hola Mundo"
        resultado = codificar_a_base64(texto)
        assert isinstance(resultado, str)
        assert len(resultado) > 0
    
    def test_decodificar_simple(self):
        """Test: Decodificar un string simple"""
        texto_original = "Hola Mundo"
        codificado = codificar_a_base64(texto_original)
        decodificado = decodificar_contenido_base64(codificado)
        assert decodificado == texto_original
    
    def test_round_trip(self):
        """Test: Codificar y decodificar son operaciones inversas"""
        textos = [
            "Contenido simple",
            "Contenido con tildes: ñáéíóú",
            "Contenido con números: 123456",
            "Contenido multilinea:\nlinea 1\nlinea 2",
        ]
        
        for texto in textos:
            codificado = codificar_a_base64(texto)
            decodificado = decodificar_contenido_base64(codificado)
            assert decodificado == texto


class TestValidacionJSON:
    """Tests para la validación de archivos JSON"""
    
    def test_validar_json_valido(self):
        """Test: Validar un JSON con estructura correcta"""
        # Crear JSON válido
        datos = {
            "metadata": {
                "nombre_archivo": "test.pdf",
                "total_paginas": 2,
                "fecha_procesamiento": "2024-01-01T00:00:00",
                "formato": "application/pdf"
            },
            "paginas": [
                {
                    "numero_pagina": 1,
                    "contenido": "Página 1",
                    "contenido_base64": codificar_a_base64("Página 1"),
                    "caracteres": 8
                },
                {
                    "numero_pagina": 2,
                    "contenido": "Página 2",
                    "contenido_base64": codificar_a_base64("Página 2"),
                    "caracteres": 8
                }
            ]
        }
        
        # Guardar en archivo temporal
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(datos, f)
            temp_path = f.name
        
        try:
            resultado = validar_json_pdf(temp_path)
            assert resultado == True
        finally:
            os.unlink(temp_path)
    
    def test_validar_json_invalido(self):
        """Test: Validar un JSON con estructura incorrecta"""
        # Crear JSON inválido (falta metadata)
        datos = {"paginas": []}
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(datos, f)
            temp_path = f.name
        
        try:
            resultado = validar_json_pdf(temp_path)
            assert resultado == False
        finally:
            os.unlink(temp_path)


class TestExportacion:
    """Tests para exportación de datos"""
    
    def test_guardar_texto_plano(self):
        """Test: Guardar contenido en archivo de texto"""
        datos = {
            "metadata": {
                "nombre_archivo": "test.pdf",
                "total_paginas": 2,
                "fecha_procesamiento": "2024-01-01T00:00:00",
                "formato": "application/pdf"
            },
            "paginas": [
                {
                    "numero_pagina": 1,
                    "contenido": "Contenido página 1",
                    "contenido_base64": codificar_a_base64("Contenido página 1"),
                    "caracteres": 18
                },
                {
                    "numero_pagina": 2,
                    "contenido": "Contenido página 2",
                    "contenido_base64": codificar_a_base64("Contenido página 2"),
                    "caracteres": 18
                }
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            temp_path = f.name
        
        try:
            resultado = guardar_texto_plano(datos, temp_path)
            assert resultado == True
            
            # Verificar que el archivo fue creado
            assert os.path.exists(temp_path)
            
            # Verificar contenido
            with open(temp_path, 'r', encoding='utf-8') as f:
                contenido = f.read()
                assert "Página 1" in contenido
                assert "Página 2" in contenido
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)


class TestEstadisticas:
    """Tests para cálculo de estadísticas"""
    
    def test_obtener_estadisticas(self):
        """Test: Calcular estadísticas del PDF"""
        datos = {
            "metadata": {
                "nombre_archivo": "test.pdf",
                "total_paginas": 2,
                "fecha_procesamiento": "2024-01-01T00:00:00",
                "formato": "application/pdf"
            },
            "paginas": [
                {
                    "numero_pagina": 1,
                    "contenido": "A" * 100,
                    "contenido_base64": codificar_a_base64("A" * 100),
                    "caracteres": 100
                },
                {
                    "numero_pagina": 2,
                    "contenido": "B" * 200,
                    "contenido_base64": codificar_a_base64("B" * 200),
                    "caracteres": 200
                }
            ]
        }
        
        stats = obtener_estadisticas(datos)
        
        assert stats["archivo"] == "test.pdf"
        assert stats["total_paginas"] == 2
        assert stats["total_caracteres"] == 300
        assert stats["caracteres_promedio"] == 150.0


# Tests de integración
class TestIntegracion:
    """Tests de integración para flujos completos"""
    
    def test_flujo_completo(self):
        """Test: Flujo completo de procesamiento"""
        # Crear JSON de prueba
        datos_originales = {
            "metadata": {
                "nombre_archivo": "documento.pdf",
                "total_paginas": 1,
                "fecha_procesamiento": "2024-01-01T00:00:00",
                "formato": "application/pdf"
            },
            "paginas": [
                {
                    "numero_pagina": 1,
                    "contenido": "Este es un documento de prueba",
                    "contenido_base64": codificar_a_base64("Este es un documento de prueba"),
                    "caracteres": 30
                }
            ]
        }
        
        # Guardar JSON
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(datos_originales, f)
            json_path = f.name
        
        try:
            # Validar
            assert validar_json_pdf(json_path) == True
            
            # Cargar y procesar
            with open(json_path, 'r') as f:
                datos_cargados = json.load(f)
            
            # Verificar integridad
            assert datos_cargados["metadata"]["nombre_archivo"] == "documento.pdf"
            assert len(datos_cargados["paginas"]) == 1
            
            # Exportar
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                txt_path = f.name
            
            try:
                guardar_texto_plano(datos_cargados, txt_path)
                assert os.path.exists(txt_path)
            finally:
                if os.path.exists(txt_path):
                    os.unlink(txt_path)
        
        finally:
            os.unlink(json_path)


if __name__ == "__main__":
    print("Para ejecutar los tests, instala pytest y ejecuta:")
    print("  pip install pytest")
    print("  pytest test_app.py -v")
