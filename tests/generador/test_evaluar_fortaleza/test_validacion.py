"""
tests/generador/test_evaluar_fortaleza/test_validacion.py
Tests de validación de entrada para evaluar_fortaleza
"""

import pytest
from src.generador import evaluar_fortaleza


class TestValidacionEvaluarFortaleza:
    """Tests de validación de entrada"""
    
    def test_no_es_string(self):
        """Test: TypeError si no es string"""
        with pytest.raises(TypeError, match="string"):
            evaluar_fortaleza(12345)
    
    def test_parametro_none(self):
        """Test: TypeError si es None"""
        with pytest.raises(TypeError):
            evaluar_fortaleza(None)
    
    def test_parametro_lista(self):
        """Test: TypeError si es lista"""
        with pytest.raises(TypeError):
            evaluar_fortaleza(['a', 'b', 'c'])
    
    def test_contraseña_vacia(self):
        """Test: ValueError si está vacía"""
        with pytest.raises(ValueError, match="vacía"):
            evaluar_fortaleza("")


class TestEstructuraRetorno:
    """Tests de estructura del retorno"""
    
    def test_tiene_clave_puntuacion(self):
        """Test: Retorna clave 'puntuacion'"""
        resultado = evaluar_fortaleza("abc123XYZ!@#")
        assert 'puntuacion' in resultado
    
    def test_tiene_clave_nivel(self):
        """Test: Retorna clave 'nivel'"""
        resultado = evaluar_fortaleza("abc123XYZ!@#")
        assert 'nivel' in resultado
    
    def test_tiene_clave_detalles(self):
        """Test: Retorna clave 'detalles'"""
        resultado = evaluar_fortaleza("abc123XYZ!@#")
        assert 'detalles' in resultado
    
    def test_detalles_tiene_subclavesrequeridas(self):
        """Test: Detalles contiene subclavesrequeridas"""
        resultado = evaluar_fortaleza("abc123XYZ!@#")
        detalles_requeridos = {
            'longitud', 'tiene_mayusculas', 'tiene_minusculas',
            'tiene_numeros', 'tiene_simbolos', 'entropia_bits',
            'puntos_longitud', 'puntos_diversidad', 'puntos_entropia',
            'puntos_patrones', 'penalizacion_patrones'
        }
        assert detalles_requeridos.issubset(set(resultado['detalles'].keys()))
    
    def test_puntuacion_es_entero(self):
        """Test: puntuacion es int"""
        resultado = evaluar_fortaleza("abc123XYZ")
        assert isinstance(resultado['puntuacion'], int)
    
    def test_nivel_es_string(self):
        """Test: nivel es string"""
        resultado = evaluar_fortaleza("abc123XYZ")
        assert isinstance(resultado['nivel'], str)
    
    def test_puntuacion_en_rango(self):
        """Test: puntuacion está entre 0 y 100"""
        resultado = evaluar_fortaleza("abc123XYZ")
        assert 0 <= resultado['puntuacion'] <= 100
