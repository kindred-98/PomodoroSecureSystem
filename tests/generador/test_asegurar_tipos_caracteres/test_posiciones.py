"""
tests/generador/test_asegurar_tipos_caracteres/test_posiciones.py
Tests para validar la asignación de caracteres en posiciones específicas
"""

import pytest
import string
from src.generador import asegurar_tipos_caracteres


class TestPosiciones:
    """Tests para validar que los caracteres se colocan en las posiciones correctas"""
    
    def test_asegura_mayuscula_en_posicion_0(self):
        """Test: Coloca mayúscula en posición 0 si se requiere"""
        contraseña = ['a', 'b', 'c', 'd']
        parametros = {
            "usar_mayusculas": True,
            "usar_numeros": False,
            "usar_simbolos": False
        }
        resultado = asegurar_tipos_caracteres(contraseña, parametros)
        assert resultado[0].isupper()
    
    def test_asegura_numero_en_posicion_1(self):
        """Test: Coloca número en posición 1 si se requiere"""
        contraseña = ['a', 'b', 'c', 'd']
        parametros = {
            "usar_mayusculas": False,
            "usar_numeros": True,
            "usar_simbolos": False
        }
        resultado = asegurar_tipos_caracteres(contraseña, parametros)
        assert resultado[1].isdigit()
    
    def test_asegura_simbolo_en_posicion_2(self):
        """Test: Coloca símbolo en posición 2 si se requiere"""
        contraseña = ['a', 'b', 'c', 'd', 'e']
        parametros = {
            "usar_mayusculas": False,
            "usar_numeros": False,
            "usar_simbolos": True
        }
        resultado = asegurar_tipos_caracteres(contraseña, parametros)
        assert resultado[2] in string.punctuation
    
    def test_asegura_mayuscula_numero_simbolo(self):
        """Test: Asegura los tres tipos en sus posiciones"""
        contraseña = ['a', 'b', 'c', 'd', 'e']
        parametros = {
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True
        }
        resultado = asegurar_tipos_caracteres(contraseña, parametros)
        assert resultado[0].isupper()
        assert resultado[1].isdigit()
        assert resultado[2] in string.punctuation
    
    def test_solo_mayuscula_deja_resto_intacto(self):
        """Test: Con solo mayúscula, solo modifica posición 0"""
        contraseña = ['a', 'b', 'c', 'd']
        parametros = {
            "usar_mayusculas": True,
            "usar_numeros": False,
            "usar_simbolos": False
        }
        resultado = asegurar_tipos_caracteres(contraseña, parametros)
        assert resultado[0].isupper()
        # Resto debería mantener minúscula (aunque aleatoria)
        assert resultado[1] == 'b'
        assert resultado[2] == 'c'
    
    def test_solo_numero_deja_resto_intacto(self):
        """Test: Con solo número, solo modifica posición 1"""
        contraseña = ['a', 'b', 'c', 'd']
        parametros = {
            "usar_mayusculas": False,
            "usar_numeros": True,
            "usar_simbolos": False
        }
        resultado = asegurar_tipos_caracteres(contraseña, parametros)
        assert resultado[1].isdigit()
        assert resultado[0] == 'a'
        assert resultado[2] == 'c'
    
    def test_solo_simbolo_deja_resto_intacto(self):
        """Test: Con solo símbolo, solo modifica posición 2"""
        contraseña = ['a', 'b', 'c', 'd']
        parametros = {
            "usar_mayusculas": False,
            "usar_numeros": False,
            "usar_simbolos": True
        }
        resultado = asegurar_tipos_caracteres(contraseña, parametros)
        assert resultado[2] in string.punctuation
        assert resultado[0] == 'a'
        assert resultado[1] == 'b'
