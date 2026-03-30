"""
tests/generador/test_generar_contraseña/test_tipos_caracteres.py
Tests de validación de tipos de caracteres para generar_contraseña()
"""

import pytest
import string
from src.generador import generar_contraseña


class TestTiposCaracteres:
    """Tests para validar que la contraseña incluye los tipos solicitados"""
    
    def test_genera_con_mayusculas(self):
        """Test: Incluye mayúsculas cuando se especifica"""
        parametros = {
            "longitud": 20,
            "usar_mayusculas": True,
            "usar_numeros": False,
            "usar_simbolos": False,
            "excluir_ambiguos": False
        }
        contraseña = generar_contraseña(parametros)
        assert any(c.isupper() for c in contraseña)
    
    def test_genera_con_numeros(self):
        """Test: Incluye números cuando se especifica"""
        parametros = {
            "longitud": 20,
            "usar_mayusculas": False,
            "usar_numeros": True,
            "usar_simbolos": False,
            "excluir_ambiguos": False
        }
        contraseña = generar_contraseña(parametros)
        assert any(c.isdigit() for c in contraseña)
    
    def test_genera_con_simbolos(self):
        """Test: Incluye símbolos cuando se especifica"""
        parametros = {
            "longitud": 30,
            "usar_mayusculas": False,
            "usar_numeros": False,
            "usar_simbolos": True,
            "excluir_ambiguos": False
        }
        contraseña = generar_contraseña(parametros)
        simbolos = set(string.punctuation)
        assert any(c in simbolos for c in contraseña)
    
    def test_genera_con_mayusculas_y_numeros(self):
        """Test: Combina mayúsculas y números"""
        parametros = {
            "longitud": 25,
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": False,
            "excluir_ambiguos": False
        }
        contraseña = generar_contraseña(parametros)
        assert any(c.isupper() for c in contraseña)
        assert any(c.isdigit() for c in contraseña)
    
    def test_genera_con_todos_tipos(self):
        """Test: Combina todos los tipos (mayúsculas, números, símbolos)"""
        parametros = {
            "longitud": 30,
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True,
            "excluir_ambiguos": False
        }
        contraseña = generar_contraseña(parametros)
        assert any(c.isupper() for c in contraseña)
        assert any(c.isdigit() for c in contraseña)
        simbolos = set(string.punctuation)
        assert any(c in simbolos for c in contraseña)
    
    def test_genera_solo_minusculas(self):
        """Test: Sin flags, genera solo minúsculas"""
        parametros = {
            "longitud": 12,
            "usar_mayusculas": False,
            "usar_numeros": False,
            "usar_simbolos": False,
            "excluir_ambiguos": False
        }
        contraseña = generar_contraseña(parametros)
        assert contraseña.islower()
    
    def test_no_contiene_mayusculas_si_no_especificado(self):
        """Test: No contiene mayúsculas si no se especifica"""
        parametros = {
            "longitud": 50,
            "usar_mayusculas": False,
            "usar_numeros": True,
            "usar_simbolos": True,
            "excluir_ambiguos": False
        }
        contraseña = generar_contraseña(parametros)
        assert not any(c.isupper() for c in contraseña)
