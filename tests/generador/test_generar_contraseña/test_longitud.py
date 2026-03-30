"""
tests/generador/test_generar_contraseña/test_longitud.py
Tests de validación de longitud para generar_contraseña()
"""

import pytest
from src.generador import generar_contraseña


class TestLongitud:
    """Tests para validar la longitud de las contraseñas generadas"""
    
    def test_genera_con_longitud_correcta(self, parametros_generador_defecto):
        """Test: La contraseña generada tiene la longitud especificada"""
        contraseña = generar_contraseña(parametros_generador_defecto)
        assert len(contraseña) == parametros_generador_defecto["longitud"]
    
    def test_genera_con_longitud_8(self):
        """Test: Genera contraseña con longitud mínima (8)"""
        parametros = {
            "longitud": 8,
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": False,
            "excluir_ambiguos": False
        }
        contraseña = generar_contraseña(parametros)
        assert len(contraseña) == 8
    
    def test_genera_con_longitud_12(self):
        """Test: Genera contraseña con longitud estándar (12)"""
        parametros = {
            "longitud": 12,
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True,
            "excluir_ambiguos": False
        }
        contraseña = generar_contraseña(parametros)
        assert len(contraseña) == 12
    
    def test_genera_con_longitud_20(self):
        """Test: Genera contraseña con longitud intermedia (20)"""
        parametros = {
            "longitud": 20,
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True,
            "excluir_ambiguos": False
        }
        contraseña = generar_contraseña(parametros)
        assert len(contraseña) == 20
    
    def test_genera_con_longitud_128(self):
        """Test: Genera contraseña con longitud máxima (128)"""
        parametros = {
            "longitud": 128,
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True,
            "excluir_ambiguos": False
        }
        contraseña = generar_contraseña(parametros)
        assert len(contraseña) == 128
    
    def test_rechaza_longitud_menor_8(self):
        """Test: Rechaza longitud menor a 8"""
        parametros = {
            "longitud": 7,
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True,
            "excluir_ambiguos": False
        }
        with pytest.raises(ValueError):
            generar_contraseña(parametros)
    
    def test_rechaza_longitud_0(self):
        """Test: Rechaza longitud 0"""
        parametros = {
            "longitud": 0,
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True,
            "excluir_ambiguos": False
        }
        with pytest.raises(ValueError):
            generar_contraseña(parametros)
    
    def test_rechaza_longitud_negativa(self):
        """Test: Rechaza longitud negativa"""
        parametros = {
            "longitud": -5,
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True,
            "excluir_ambiguos": False
        }
        with pytest.raises(ValueError):
            generar_contraseña(parametros)
    
    def test_rechaza_longitud_mayor_128(self):
        """Test: Rechaza longitud mayor a 128"""
        parametros = {
            "longitud": 129,
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True,
            "excluir_ambiguos": False
        }
        with pytest.raises(ValueError):
            generar_contraseña(parametros)
    
    def test_rechaza_longitud_muy_grande(self):
        """Test: Rechaza longitud excessivamente grande"""
        parametros = {
            "longitud": 1000,
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True,
            "excluir_ambiguos": False
        }
        with pytest.raises(ValueError):
            generar_contraseña(parametros)
