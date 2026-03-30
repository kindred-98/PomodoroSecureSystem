"""
tests/generador/test_construir_juego_caracteres/test_basico.py
Tests básicos de funcionalidad de construir_juego_caracteres
"""

import pytest
import string
from src.generador import construir_juego_caracteres


class TestConstruirJuegoCaracteresBasico:
    """Tests de casos de uso normal"""
    
    def test_solo_minusculas(self):
        """Test: Si no se solicita nada, aún incluye minúsculas"""
        parametros = {
            'usar_mayusculas': False,
            'usar_numeros': False,
            'usar_simbolos': False,
            'excluir_ambiguos': False
        }
        resultado = construir_juego_caracteres(parametros)
        assert string.ascii_lowercase in resultado or resultado == string.ascii_lowercase
    
    def test_minusculas_y_mayusculas(self):
        """Test: Construye juego con minúsculas y mayúsculas"""
        parametros = {
            'usar_mayusculas': True,
            'usar_numeros': False,
            'usar_simbolos': False,
            'excluir_ambiguos': False
        }
        resultado = construir_juego_caracteres(parametros)
        assert all(c in resultado for c in 'abcABC')
        assert len(resultado) >= 52  # 26+26
    
    def test_con_numeros(self):
        """Test: Construye juego con números"""
        parametros = {
            'usar_mayusculas': False,
            'usar_numeros': True,
            'usar_simbolos': False,
            'excluir_ambiguos': False
        }
        resultado = construir_juego_caracteres(parametros)
        assert all(c in resultado for c in '0123456789')
        assert len(resultado) >= 36  # 26+10
    
    def test_con_simbolos(self):
        """Test: Construye juego con símbolos"""
        parametros = {
            'usar_mayusculas': False,
            'usar_numeros': False,
            'usar_simbolos': True,
            'excluir_ambiguos': False
        }
        resultado = construir_juego_caracteres(parametros)
        # Verificar que contiene al menos algunos símbolos
        assert any(c in resultado for c in '!@#$%^&*()')
    
    def test_todas_opciones_activadas(self):
        """Test: Construye juego con todas las opciones"""
        parametros = {
            'usar_mayusculas': True,
            'usar_numeros': True,
            'usar_simbolos': True,
            'excluir_ambiguos': False
        }
        resultado = construir_juego_caracteres(parametros)
        assert all(c in resultado for c in 'aAbB12!@')
        assert len(resultado) >= 90  # 26+26+10+32
        assert len(resultado) <= 95  # Máximo ascii imprimible
    
    def test_longitud_juego_minusculas_solo(self):
        """Test: Longitud del juego es exacto para solo minúsculas"""
        parametros = {
            'usar_mayusculas': False,
            'usar_numeros': False,
            'usar_simbolos': False,
            'excluir_ambiguos': False
        }
        resultado = construir_juego_caracteres(parametros)
        assert len(resultado) == 26  # Exacto para solo minúsculas
    
    def test_longitud_juego_completo(self):
        """Test: Juego completo tiene dimensiones esperadas"""
        parametros = {
            'usar_mayusculas': True,
            'usar_numeros': True,
            'usar_simbolos': True,
            'excluir_ambiguos': False
        }
        resultado = construir_juego_caracteres(parametros)
        # 26 minúsc + 26 mayús + 10 dígitos + 32 símbolos = 94
        assert len(resultado) == 94
