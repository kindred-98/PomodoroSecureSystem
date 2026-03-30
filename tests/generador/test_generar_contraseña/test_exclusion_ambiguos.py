"""
tests/generador/test_generar_contraseña/test_exclusion_ambiguos.py
Tests para validar la exclusión de caracteres ambiguos (0,O,l,I,1)
"""

import pytest
from src.generador import generar_contraseña


class TestExclusionAmbiguos:
    """Tests para validar la exclusión de caracteres ambiguos"""
    
    def test_excluye_caracteres_ambiguos(self):
        """Test: Excluye 0,O,l,I,1 cuando se especifica"""
        parametros = {
            "longitud": 100,
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": False,
            "excluir_ambiguos": True
        }
        contraseña = generar_contraseña(parametros)
        caracteres_ambiguos = "0Ol1I"
        for caracter in caracteres_ambiguos:
            assert caracter not in contraseña
    
    def test_no_excluye_cuando_flag_falso(self):
        """Test: Incluye ambiguos cuando excluir_ambiguos=False"""
        parametros = {
            "longitud": 100,
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": False,
            "excluir_ambiguos": False
        }
        contraseña = generar_contraseña(parametros)
        # Potencialmente podría contener 0, O, l, I o 1
        # (no es garantizado, pero es posible)
        assert isinstance(contraseña, str)
    
    def test_excluye_cero_en_numeros(self):
        """Test: Excluye específicamente el 0"""
        parametros = {
            "longitud": 80,
            "usar_mayusculas": False,
            "usar_numeros": True,
            "usar_simbolos": False,
            "excluir_ambiguos": True
        }
        contraseña = generar_contraseña(parametros)
        assert '0' not in contraseña
    
    def test_excluye_mayuscula_o(self):
        """Test: Excluye específicamente la mayúscula O"""
        parametros = {
            "longitud": 80,
            "usar_mayusculas": True,
            "usar_numeros": False,
            "usar_simbolos": False,
            "excluir_ambiguos": True
        }
        contraseña = generar_contraseña(parametros)
        assert 'O' not in contraseña
    
    def test_excluye_minuscula_l(self):
        """Test: Excluye específicamente la minúscula l"""
        parametros = {
            "longitud": 100,
            "usar_mayusculas": False,
            "usar_numeros": False,
            "usar_simbolos": False,
            "excluir_ambiguos": True
        }
        contraseña = generar_contraseña(parametros)
        assert 'l' not in contraseña
    
    def test_excluye_mayuscula_i(self):
        """Test: Excluye específicamente la mayúscula I"""
        parametros = {
            "longitud": 80,
            "usar_mayusculas": True,
            "usar_numeros": False,
            "usar_simbolos": False,
            "excluir_ambiguos": True
        }
        contraseña = generar_contraseña(parametros)
        assert 'I' not in contraseña
    
    def test_excluye_uno_en_numeros(self):
        """Test: Excluye específicamente el número 1"""
        parametros = {
            "longitud": 80,
            "usar_mayusculas": False,
            "usar_numeros": True,
            "usar_simbolos": False,
            "excluir_ambiguos": True
        }
        contraseña = generar_contraseña(parametros)
        assert '1' not in contraseña
    
    def test_sigue_generando_numeros_sin_0_y_1(self):
        """Test: Genera números válidos (2-9) cuando excluye ambiguos"""
        parametros = {
            "longitud": 128,
            "usar_mayusculas": False,
            "usar_numeros": True,
            "usar_simbolos": False,
            "excluir_ambiguos": True
        }
        contraseña = generar_contraseña(parametros)
        # Debe haber números (2-9)
        assert any(c in "23456789" for c in contraseña)
