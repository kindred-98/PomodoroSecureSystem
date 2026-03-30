"""
tests/generador/test_detectar_patrones/test_validacion.py
Tests de validación de entrada para detectar_patrones
"""

import pytest
from src.generador import detectar_patrones


class TestDetectarPatronesValidacion:
    """Tests de validaciónde entrada"""
    
    def test_no_es_string(self):
        """Test: TypeError si no es string"""
        with pytest.raises(TypeError, match="string"):
            detectar_patrones(12345)
    
    def test_parametro_none(self):
        """Test: TypeError si es None"""
        with pytest.raises(TypeError):
            detectar_patrones(None)
    
    def test_parametro_lista(self):
        """Test: TypeError si es lista"""
        with pytest.raises(TypeError):
            detectar_patrones(['a', 'b', 'c'])
    
    def test_contraseña_vacia(self):
        """Test: ValueError si está vacía"""
        with pytest.raises(ValueError, match="vacía"):
            detectar_patrones("")
    
    def test_una_letra(self):
        """Test: Acepta contraseña de 1 carácter"""
        resultado = detectar_patrones("a")
        assert resultado is not None
        assert 'fortaleza_patron' in resultado


class TestEstructuraRetorno:
    """Tests de estructura del diccionario retornado"""
    
    def test_tiene_todas_claves(self):
        """Test: Retorna todas las claves esperadas"""
        resultado = detectar_patrones("abc123XYZ!@#")
        claves_esperadas = {
            'tiene_secuencias_consecutivas',
            'secuencias_encontradas',
            'tiene_repeticiones',
            'repeticiones_encontradas',
            'tiene_teclado_adyacente',
            'adyacencias_encontradas',
            'tiene_patrones_crecientes',
            'patrones_crecientes',
            'tiene_patrones_invertidos',
            'patrones_invertidos',
            'fortaleza_patron'
        }
        assert set(resultado.keys()) == claves_esperadas
    
    def test_fortaleza_en_rango(self):
        """Test: Fortaleza siempre está entre 0.0 y 1.0"""
        resultado = detectar_patrones("Xy9!ZaBc")
        assert 0.0 <= resultado['fortaleza_patron'] <= 1.0
    
    def test_tipos_retorno(self):
        """Test: Tipos de retorno son correctos"""
        resultado = detectar_patrones("abc123")
        assert isinstance(resultado['tiene_secuencias_consecutivas'], bool)
        assert isinstance(resultado['secuencias_encontradas'], list)
        assert isinstance(resultado['fortaleza_patron'], float)
