"""
tests/generador/test_asegurar_tipos_caracteres/test_edge_cases.py
Tests de casos extremos (edge cases) para asegurar_tipos_caracteres()
"""

import pytest
from src.generador import asegurar_tipos_caracteres


class TestEdgeCases:
    """Tests para casos extremos y situaciones límite"""
    
    def test_maneja_lista_con_1_elemento(self):
        """Test: Maneja lista con 1 solo elemento"""
        contraseña = ['a']
        parametros = {
            "usar_mayusculas": True,
            "usar_numeros": False,
            "usar_simbolos": False
        }
        resultado = asegurar_tipos_caracteres(contraseña, parametros)
        # Debe sobrescribir el único elemento con una mayúscula
        assert resultado[0].isupper()
    
    def test_maneja_lista_con_2_elementos(self):
        """Test: Maneja lista con 2 elementos"""
        contraseña = ['a', 'b']
        parametros = {
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": False
        }
        resultado = asegurar_tipos_caracteres(contraseña, parametros)
        assert resultado[0].isupper()
        assert resultado[1].isdigit()
    
    def test_maneja_lista_con_3_elementos(self):
        """Test: Maneja lista con 3 elementos (mínima para 3 tipos)"""
        contraseña = ['a', 'b', 'c']
        parametros = {
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True
        }
        resultado = asegurar_tipos_caracteres(contraseña, parametros)
        assert resultado[0].isupper()
        assert resultado[1].isdigit()
        import string
        assert resultado[2] in string.punctuation
    
    def test_maneja_lista_muy_grande(self):
        """Test: Maneja lista con muchos elementos"""
        contraseña = ['a'] * 100
        parametros = {
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True
        }
        resultado = asegurar_tipos_caracteres(contraseña, parametros)
        assert len(resultado) == 100
        assert resultado[0].isupper()
        assert resultado[1].isdigit()
    
    def test_retorna_lista_misma_longitud(self):
        """Test: La lista resultante tiene la misma longitud"""
        contraseña = ['a', 'b', 'c', 'd', 'e']
        parametros = {
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True
        }
        resultado = asegurar_tipos_caracteres(contraseña, parametros)
        assert len(resultado) == len(contraseña)
    
    def test_numero_con_2_elementos_usa_posicion_1(self):
        """Test: Con 2 elementos, número va a posición 1"""
        contraseña = ['a', 'b']
        parametros = {
            "usar_mayusculas": False,
            "usar_numeros": True,
            "usar_simbolos": False
        }
        resultado = asegurar_tipos_caracteres(contraseña, parametros)
        assert resultado[1].isdigit()
    
    def test_simbolo_con_2_elementos_usa_posicion_1(self):
        """Test: Con 2 elementos, símbolo va a posición 1"""
        contraseña = ['a', 'b']
        parametros = {
            "usar_mayusculas": False,
            "usar_numeros": False,
            "usar_simbolos": True
        }
        resultado = asegurar_tipos_caracteres(contraseña, parametros)
        import string
        assert resultado[1] in string.punctuation
    
    def test_simbolo_con_1_elementos_usa_posicion_0(self):
        """Test: Con 1 elemento, símbolo sobrescribe posición 0"""
        contraseña = ['a']
        parametros = {
            "usar_mayusculas": False,
            "usar_numeros": False,
            "usar_simbolos": True
        }
        resultado = asegurar_tipos_caracteres(contraseña, parametros)
        import string
        assert resultado[0] in string.punctuation
    
    def test_todos_false_no_modifica(self):
        """Test: Si todos los flags son False, no modifica"""
        contraseña = ['a', 'b', 'c', 'd']
        parametros = {
            "usar_mayusculas": False,
            "usar_numeros": False,
            "usar_simbolos": False
        }
        resultado = asegurar_tipos_caracteres(contraseña, parametros)
        # No debería modificar nada
        assert resultado == contraseña
