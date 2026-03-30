"""Tests para desactivar_usuario()"""

import pytest
from bson import ObjectId
from src.db.usuarios.desactivar_usuario import desactivar_usuario


class TestDesactivarUsuarioValidacion:
    """Tests para validación en desactivar_usuario"""
    
    def test_usuario_id_no_string(self, mock_conexion_global):
        """Debe fallar si usuario_id no es string"""
        with pytest.raises(TypeError, match="usuario_id debe ser string"):
            desactivar_usuario(123)
    
    def test_usuario_id_vacio(self, mock_conexion_global):
        """Debe fallar si usuario_id es vacío"""
        with pytest.raises(ValueError, match="ID inválido"):
            desactivar_usuario('')
    
    def test_usuario_id_invalido(self, mock_conexion_global):
        """Debe fallar si usuario_id no es ObjectId válido"""
        with pytest.raises(ValueError, match="ID inválido"):
            desactivar_usuario('invalid')


class TestDesactivarUsuarioExito:
    """Tests para casos exitosos de desactivar_usuario"""
    
    def test_marca_como_inactivo(self, mock_conexion_global, usuario_en_db, coleccion_usuarios):
        """Debe marcar usuario como inactivo (soft delete)"""
        usuario_antes = coleccion_usuarios.find_one({'_id': usuario_en_db['_id']})
        assert usuario_antes['activo'] is True
        
        resultado = desactivar_usuario(str(usuario_en_db['_id']))
        
        assert resultado['activo'] is False
    
    def test_usuario_no_existe(self, mock_conexion_global, coleccion_usuarios):
        """Debe fallar si usuario no existe"""
        id_falso = str(ObjectId())
        with pytest.raises(Exception, match="Usuario con ID .* no existe"):
            desactivar_usuario(id_falso)
    
    def test_desactivar_dos_veces(self, mock_conexion_global, usuario_en_db, coleccion_usuarios):
        """Desactivar usuario ya inactivo debe funcionar (idempotente)"""
        # Primera desactivación
        desactivar_usuario(str(usuario_en_db['_id']))
        
        # Segunda desactivación debe funcionar sin error
        resultado = desactivar_usuario(str(usuario_en_db['_id']))
        
        assert resultado['activo'] is False
