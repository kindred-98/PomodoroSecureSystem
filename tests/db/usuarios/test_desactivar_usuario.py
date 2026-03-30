"""Tests para desactivar_usuario()"""

import pytest
from bson import ObjectId
from unittest.mock import patch
from src.db.usuarios.desactivar_usuario import desactivar_usuario


class TestDesactivarUsuarioValidacion:
    """Tests para validación en desactivar_usuario"""
    
    def test_usuario_id_no_string(self, conexion_mongodb_mock):
        """Debe fallar si usuario_id no es string"""
        with patch('src.db.usuarios.desactivar_usuario.ConexionMongoDB', return_value=conexion_mongodb_mock):
            with pytest.raises(TypeError, match="usuario_id debe ser string"):
                desactivar_usuario(123)
    
    def test_usuario_id_vacio(self, conexion_mongodb_mock):
        """Debe fallar si usuario_id es vacío"""
        with patch('src.db.usuarios.desactivar_usuario.ConexionMongoDB', return_value=conexion_mongodb_mock):
            with pytest.raises(ValueError, match="usuario_id no puede estar vacío"):
                desactivar_usuario('')
    
    def test_usuario_id_invalido(self, conexion_mongodb_mock):
        """Debe fallar si usuario_id no es ObjectId válido"""
        with patch('src.db.usuarios.desactivar_usuario.ConexionMongoDB', return_value=conexion_mongodb_mock):
            with pytest.raises(ValueError, match="usuario_id .* no es un ObjectId válido"):
                desactivar_usuario('invalid')


class TestDesactivarUsuarioExito:
    """Tests para casos exitosos de desactivar_usuario"""
    
    def test_marca_como_inactivo(self, usuario_en_db, coleccion_usuarios):
        """Debe marcar usuario como inactivo (soft delete)"""
        with patch('src.db.usuarios.desactivar_usuario.ConexionMongoDB') as mock_db:
            mock_db.return_value.obtener_coleccion.return_value = coleccion_usuarios
            
            usuario_antes = coleccion_usuarios.find_one({'_id': usuario_en_db['_id']})
            assert usuario_antes['activo'] is True
            
            resultado = desactivar_usuario(str(usuario_en_db['_id']))
            
            assert resultado['activo'] is False
    
    def test_usuario_no_existe(self, coleccion_usuarios):
        """Debe fallar si usuario no existe"""
        with patch('src.db.usuarios.desactivar_usuario.ConexionMongoDB') as mock_db:
            mock_db.return_value.obtener_coleccion.return_value = coleccion_usuarios
            
            id_falso = str(ObjectId())
            with pytest.raises(Exception, match="Usuario con ID .* no existe"):
                desactivar_usuario(id_falso)
    
    def test_desactivar_dos_veces(self, usuario_en_db, coleccion_usuarios):
        """Desactivar usuario ya inactivo debe funcionar (idempotente)"""
        with patch('src.db.usuarios.desactivar_usuario.ConexionMongoDB') as mock_db:
            mock_db.return_value.obtener_coleccion.return_value = coleccion_usuarios
            
            # Primera desactivación
            desactivar_usuario(str(usuario_en_db['_id']))
            
            # Segunda desactivación debe funcionar sin error
            resultado = desactivar_usuario(str(usuario_en_db['_id']))
            
            assert resultado['activo'] is False
