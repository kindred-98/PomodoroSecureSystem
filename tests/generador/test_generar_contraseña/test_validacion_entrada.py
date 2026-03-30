"""
tests/generador/test_generar_contraseña/test_validacion_entrada.py
Tests de validación de entrada para generar_contraseña()
"""

import pytest
from src.generador import generar_contraseña


class TestValidacionEntrada:
    """Tests para validar que la función rechaza entrada inválida"""
    
    def test_rechaza_parametros_no_dict(self):
        """Test: Rechaza entrada que no es dict"""
        with pytest.raises(TypeError):
            generar_contraseña("no es dict")
    
    def test_rechaza_parametros_lista(self):
        """Test: Rechaza lista como parámetros"""
        with pytest.raises(TypeError):
            generar_contraseña([12, True, True, True, False])
    
    def test_rechaza_parametros_none(self):
        """Test: Rechaza None como parámetros"""
        with pytest.raises(TypeError):
            generar_contraseña(None)
    
    def test_rechaza_parametros_faltantes(self):
        """Test: Rechaza si faltan claves en dict"""
        parametros = {"longitud": 12}  # Faltan muchas claves
        with pytest.raises(ValueError):
            generar_contraseña(parametros)
    
    def test_rechaza_dict_con_claves_equivocadas(self):
        """Test: Rechaza dict con claves incorrectas"""
        parametros = {
            "largo": 12,  # Debería ser "longitud"
            "mayus": True,
            "numeros": True,
            "simbolos": True,
            "ambiguos": False
        }
        with pytest.raises(ValueError):
            generar_contraseña(parametros)
    
    def test_rechaza_longitud_no_entero(self):
        """Test: Rechaza longitud que no es entero"""
        parametros = {
            "longitud": "12",  # String en lugar de int
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True,
            "excluir_ambiguos": False
        }
        with pytest.raises(ValueError):
            generar_contraseña(parametros)
    
    def test_rechaza_longitud_float(self):
        """Test: Rechaza longitud como float"""
        parametros = {
            "longitud": 12.5,
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True,
            "excluir_ambiguos": False
        }
        with pytest.raises(ValueError):
            generar_contraseña(parametros)
    
    def test_dict_vacio(self):
        """Test: Rechaza dict vacío"""
        with pytest.raises(ValueError):
            generar_contraseña({})
    
    def test_genera_correctamente_con_todos_los_parametros(self):
        """Test: Genera correctamente cuando todos los parámetros son válidos"""
        parametros = {
            "longitud": 12,
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True,
            "excluir_ambiguos": False
        }
        contraseña = generar_contraseña(parametros)
        assert isinstance(contraseña, str)
        assert len(contraseña) == 12
