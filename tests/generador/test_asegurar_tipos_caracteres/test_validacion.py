"""
tests/generador/test_asegurar_tipos_caracteres/test_validacion.py
Tests de validación de entrada para asegurar_tipos_caracteres()
"""

import pytest
from src.generador import asegurar_tipos_caracteres


class TestValidacion:
    """Tests para validar que la función rechaza entrada inválida"""
    
    def test_rechaza_lista_vacia(self):
        """Test: Rechaza lista vacía"""
        parametros = {
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True
        }
        with pytest.raises(ValueError):
            asegurar_tipos_caracteres([], parametros)
    
    def test_rechaza_no_lista(self):
        """Test: Rechaza entrada que no es lista"""
        parametros = {
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True
        }
        with pytest.raises(TypeError):
            asegurar_tipos_caracteres("no es lista", parametros)
    
    def test_rechaza_diccionario(self):
        """Test: Rechaza diccionario como primer argumento"""
        parametros = {
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True
        }
        with pytest.raises(TypeError):
            asegurar_tipos_caracteres({"a": "b"}, parametros)
    
    def test_rechaza_tipos_mas_que_espacios(self):
        """Test: Rechaza si hay más tipos requeridos que espacio en lista"""
        contraseña = ['a']  # Solo 1 espacio
        parametros = {
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True  # 3 tipos pero solo 1 espacio
        }
        with pytest.raises(ValueError):
            asegurar_tipos_caracteres(contraseña, parametros)
    
    def test_rechaza_2_tipos_en_lista_1_elemento(self):
        """Test: Rechaza 2 tipos en lista de 1 elemento"""
        contraseña = ['a']  # Solo 1 espacio
        parametros = {
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": False
        }
        with pytest.raises(ValueError):
            asegurar_tipos_caracteres(contraseña, parametros)
    
    def test_acepta_1_tipo_en_lista_1_elemento(self):
        """Test: Acepta 1 tipo en lista de 1 elemento"""
        contraseña = ['a']
        parametros = {
            "usar_mayusculas": True,
            "usar_numeros": False,
            "usar_simbolos": False
        }
        resultado = asegurar_tipos_caracteres(contraseña, parametros)
        assert len(resultado) == 1
        assert resultado[0].isupper()
    
    def test_genera_correcto_con_todos_parametros_validos(self):
        """Test: Funciona correctamente con entrada válida"""
        contraseña = ['a', 'b', 'c', 'd']
        parametros = {
            "usar_mayusculas": True,
            "usar_numeros": False,
            "usar_simbolos": False
        }
        resultado = asegurar_tipos_caracteres(contraseña, parametros)
        assert isinstance(resultado, list)
        assert len(resultado) == 4
