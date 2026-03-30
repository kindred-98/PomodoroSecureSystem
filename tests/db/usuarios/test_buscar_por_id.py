"""Tests para buscar_por_id()"""

import pytest
from datetime import datetime
from bson import ObjectId
from unittest.mock import patch
from src.db.usuarios.buscar_por_id import buscar_por_id


class TestBuscarPorIdValidacion:
    """Tests para validación en buscar_por_id"""
    
    def test_usuario_id_no_string(self, conexion_mongodb_mock):
        """Debe fallar si usuario_id no es string"""
        with patch('src.db.usuarios.buscar_por_id.ConexionMongoDB', return_value=conexion_mongodb_mock):
            with pytest.raises(TypeError, match="usuario_id debe ser string"):
                buscar_por_id(123)
    
    def test_usuario_id_vacio(self, conexion_mongodb_mock):
        """Debe fallar si usuario_id es vacío"""
        with patch('src.db.usuarios.buscar_por_id.ConexionMongoDB', return_value=conexion_mongodb_mock):
            with pytest.raises(ValueError, match="usuario_id no puede estar vacío"):
                buscar_por_id('')
    
    def test_usuario_id_invalido(self, conexion_mongodb_mock):
        """Debe fallar si usuario_id no es ObjectId válido"""
        with patch('src.db.usuarios.buscar_por_id.ConexionMongoDB', return_value=conexion_mongodb_mock):
            with pytest.raises(ValueError, match="usuario_id .* no es un ObjectId válido"):
                buscar_por_id('invalid_id')


class TestBuscarPorIdExitoso:
    """Tests para casos exitosos de buscar_por_id"""
    
    def test_encuentra_usuario_por_id(self, usuario_en_db, coleccion_usuarios):
        """Debe encontrar usuario por su ID"""
        with patch('src.db.usuarios.buscar_por_id.ConexionMongoDB') as mock_db:
            mock_db.return_value.obtener_coleccion.return_value = coleccion_usuarios
            
            resultado = buscar_por_id(str(usuario_en_db['_id']))
            
            assert resultado is not None
            assert resultado['_id'] == usuario_en_db['_id']
            assert resultado['email'] == usuario_en_db['email']
    
    def test_no_encuentra_id_inexistente(self, coleccion_usuarios):
        """Debe retornar None si ID no existe"""
        with patch('src.db.usuarios.buscar_por_id.ConexionMongoDB') as mock_db:
            mock_db.return_value.obtener_coleccion.return_value = coleccion_usuarios
            
            id_falso = str(ObjectId())
            resultado = buscar_por_id(id_falso)
            
            assert resultado is None
    
    def test_formato_hexadecimal_24_caracteres(self, usuario_en_db, coleccion_usuarios):
        """ObjectId debe ser hexadecimal de 24 caracteres"""
        with patch('src.db.usuarios.buscar_por_id.ConexionMongoDB') as mock_db:
            mock_db.return_value.obtener_coleccion.return_value = coleccion_usuarios
            
            id_hex = str(usuario_en_db['_id'])
            assert len(id_hex) == 24
            
            resultado = buscar_por_id(id_hex)
            assert resultado is not None
