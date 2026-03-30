"""
tests/generador/test_construir_juego_caracteres/test_exclusion_ambiguos.py
Tests de exclusión de caracteres ambiguos
"""

import pytest
from src.generador import construir_juego_caracteres


class TestExclusionAmbiguos:
    """Tests de exclusión de caracteres ambiguos (0, O, l, I, 1)"""
    
    def test_excluir_ambiguos_en_numeros(self):
        """Test: Excluye 0 y 1 de números"""
        parametros = {
            'usar_mayusculas': False,
            'usar_numeros': True,
            'usar_simbolos': False,
            'excluir_ambiguos': True
        }
        resultado = construir_juego_caracteres(parametros)
        assert '0' not in resultado
        assert '1' not in resultado
        assert '2' in resultado
        assert '9' in resultado
    
    def test_excluir_ambiguos_en_mayusculas(self):
        """Test: Excluye O e I de mayúsculas"""
        parametros = {
            'usar_mayusculas': True,
            'usar_numeros': False,
            'usar_simbolos': False,
            'excluir_ambiguos': True
        }
        resultado = construir_juego_caracteres(parametros)
        assert 'O' not in resultado
        assert 'I' not in resultado
        assert 'A' in resultado
        assert 'Z' in resultado
    
    def test_excluir_ambiguos_en_minusculas(self):
        """Test: Excluye l de minúsculas"""
        parametros = {
            'usar_mayusculas': False,
            'usar_numeros': False,
            'usar_simbolos': False,
            'excluir_ambiguos': True
        }
        resultado = construir_juego_caracteres(parametros)
        assert 'l' not in resultado
        assert 'a' in resultado
        assert 'z' in resultado
    
    def test_excluir_ambiguos_completo(self):
        """Test: Excluye todos los ambiguos en juego completo"""
        parametros = {
            'usar_mayusculas': True,
            'usar_numeros': True,
            'usar_simbolos': False,
            'excluir_ambiguos': True
        }
        resultado = construir_juego_caracteres(parametros)
        ambiguos = ['0', 'O', 'l', 'I', '1']
        for char in ambiguos:
            assert char not in resultado, f"Carácter ambiguo '{char}' debe ser excluido"
    
    def test_no_excluir_ambiguos_mantiene_numeros(self):
        """Test: Sin exclusión, mantiene 0 y 1"""
        parametros = {
            'usar_mayusculas': False,
            'usar_numeros': True,
            'usar_simbolos': False,
            'excluir_ambiguos': False
        }
        resultado = construir_juego_caracteres(parametros)
        assert '0' in resultado
        assert '1' in resultado
    
    def test_no_excluir_ambiguos_mantiene_letras(self):
        """Test: Sin exclusión, mantiene O, I, l"""
        parametros = {
            'usar_mayusculas': True,
            'usar_numeros': False,
            'usar_simbolos': False,
            'excluir_ambiguos': False
        }
        resultado = construir_juego_caracteres(parametros)
        assert 'O' in resultado
        assert 'I' in resultado
        assert 'l' in resultado
    
    def test_longitud_estimada_con_exclusion(self):
        """Test: Longitud se reduce con exclusión (26+26-5 ~ 47)"""
        parametros = {
            'usar_mayusculas': True,
            'usar_numeros': False,
            'usar_simbolos': False,
            'excluir_ambiguos': True
        }
        resultado = construir_juego_caracteres(parametros)
        # 26 minúsc + 26 mayús - 1(l) - 2(O,I) = 51
        assert len(resultado) == 49  # 26 + 26 - 3 (l, O, I)
    
    def test_longitud_estimada_exclusion_con_numeros(self):
        """Test: Longitud se reduce correctamente con números excluidos"""
        parametros = {
            'usar_mayusculas': False,
            'usar_numeros': True,
            'usar_simbolos': False,
            'excluir_ambiguos': True
        }
        resultado = construir_juego_caracteres(parametros)
        # 26 minúsc + 10 dígitos - 1(l) - 2(0,1) = 33
        assert len(resultado) == 33  # 26 + 10 - 2 - 1
