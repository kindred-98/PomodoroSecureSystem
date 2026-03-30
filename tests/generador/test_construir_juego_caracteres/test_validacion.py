"""
tests/generador/test_construir_juego_caracteres/test_validacion.py
Tests de validación de entrada de construir_juego_caracteres
"""

import pytest
from src.generador import construir_juego_caracteres


class TestConstruirJuegoCaracteresValidacion:
    """Tests de validación de parámetros"""
    
    def test_no_es_diccionario(self):
        """Test: Levanta TypeError si no es dict"""
        with pytest.raises(TypeError, match="diccionario"):
            construir_juego_caracteres("no soy dict")
    
    def test_parametros_lista(self):
        """Test: Levanta TypeError si es lista"""
        with pytest.raises(TypeError):
            construir_juego_caracteres([])
    
    def test_parametros_none(self):
        """Test: Levanta TypeError si es None"""
        with pytest.raises(TypeError):
            construir_juego_caracteres(None)
    
    def test_falta_clave_usar_mayusculas(self):
        """Test: ValueError si falta clave usar_mayusculas"""
        parametros = {
            'usar_numeros': True,
            'usar_simbolos': False,
            'excluir_ambiguos': False
        }
        with pytest.raises(ValueError, match="Faltan claves"):
            construir_juego_caracteres(parametros)
    
    def test_falta_clave_usar_numeros(self):
        """Test: ValueError si falta clave usar_numeros"""
        parametros = {
            'usar_mayusculas': True,
            'usar_simbolos': False,
            'excluir_ambiguos': False
        }
        with pytest.raises(ValueError, match="Faltan claves"):
            construir_juego_caracteres(parametros)
    
    def test_falta_clave_usar_simbolos(self):
        """Test: ValueError si falta clave usar_simbolos"""
        parametros = {
            'usar_mayusculas': True,
            'usar_numeros': False,
            'excluir_ambiguos': False
        }
        with pytest.raises(ValueError, match="Faltan claves"):
            construir_juego_caracteres(parametros)
    
    def test_falta_clave_excluir_ambiguos(self):
        """Test: ValueError si falta clave excluir_ambiguos"""
        parametros = {
            'usar_mayusculas': True,
            'usar_numeros': True,
            'usar_simbolos': False
        }
        with pytest.raises(ValueError, match="Faltan claves"):
            construir_juego_caracteres(parametros)
    
    def test_valor_no_booleano_usar_mayusculas(self):
        """Test: TypeError si usar_mayusculas no es bool"""
        parametros = {
            'usar_mayusculas': "true",  # String no válido
            'usar_numeros': False,
            'usar_simbolos': False,
            'excluir_ambiguos': False
        }
        with pytest.raises(TypeError, match="debe ser bool"):
            construir_juego_caracteres(parametros)
    
    def test_valor_no_booleano_usar_numeros(self):
        """Test: TypeError si usar_numeros no es bool"""
        parametros = {
            'usar_mayusculas': False,
            'usar_numeros': 1,  # Int no válido
            'usar_simbolos': False,
            'excluir_ambiguos': False
        }
        with pytest.raises(TypeError, match="debe ser bool"):
            construir_juego_caracteres(parametros)
    
    def test_valor_no_booleano_usar_simbolos(self):
        """Test: TypeError si usar_simbolos no es bool"""
        parametros = {
            'usar_mayusculas': False,
            'usar_numeros': False,
            'usar_simbolos': None,  # None no válido
            'excluir_ambiguos': False
        }
        with pytest.raises(TypeError, match="debe ser bool"):
            construir_juego_caracteres(parametros)
    
    def test_valor_no_booleano_excluir_ambiguos(self):
        """Test: TypeError si excluir_ambiguos no es bool"""
        parametros = {
            'usar_mayusculas': False,
            'usar_numeros': False,
            'usar_simbolos': False,
            'excluir_ambiguos': []  # List no válido
        }
        with pytest.raises(TypeError, match="debe ser bool"):
            construir_juego_caracteres(parametros)
