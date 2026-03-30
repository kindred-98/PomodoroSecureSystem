"""Tests para buscar_por_id()"""

import pytest
from datetime import datetime
from bson import ObjectId
from src.db.usuarios.buscar_por_id import buscar_por_id


class TestBuscarPorIdValidacion:
    """Tests para validación en buscar_por_id"""
    
    def test_usuario_id_no_string(self, mock_conexion_global):
        """Debe fallar si usuario_id no es string"""
        with pytest.raises(TypeError, match="usuario_id debe ser string"):
            buscar_por_id(123)
    
    def test_usuario_id_vacio(self, mock_conexion_global):
        """Debe fallar si usuario_id es vacío"""
        with pytest.raises(ValueError, match="no es un ObjectId válido"):
            buscar_por_id('')
    
    def test_usuario_id_invalido(self, mock_conexion_global):
        """Debe fallar si usuario_id no es ObjectId válido"""
        with pytest.raises(ValueError, match="ID inválido"):
            buscar_por_id('invalid_id')


class TestBuscarPorIdExitoso:
    """Tests para casos exitosos de buscar_por_id"""
    
    def test_encuentra_usuario_por_id(self, mock_conexion_global, usuario_en_db):
        """Debe encontrar usuario por su ID"""
        resultado = buscar_por_id(str(usuario_en_db['_id']))
        
        assert resultado is not None
        assert resultado['_id'] == usuario_en_db['_id']
        assert resultado['email'] == usuario_en_db['email']
    
    def test_no_encuentra_id_inexistente(self, mock_conexion_global, coleccion_usuarios):
        """Debe retornar None si ID no existe"""
        id_falso = str(ObjectId())
        resultado = buscar_por_id(id_falso)
        
        assert resultado is None
    
    def test_formato_hexadecimal_24_caracteres(self, mock_conexion_global, usuario_en_db):
        """ObjectId debe ser hexadecimal de 24 caracteres"""
        id_hex = str(usuario_en_db['_id'])
        assert len(id_hex) == 24
        
        resultado = buscar_por_id(id_hex)
        assert resultado is not None
