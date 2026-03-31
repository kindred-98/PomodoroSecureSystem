"""Tests para auth/ver_contraseña.py"""

import pytest
from bson import ObjectId
from src.auth.ver_contraseña import ver_contraseña


class TestVerContraseñaValidacion:
    """Tests para validación en ver_contraseña"""
    
    def test_usuario_id_no_string(self, mock_conexion_global, fernet_key_env):
        with pytest.raises(TypeError, match="usuario_id debe ser string"):
            ver_contraseña(123, "pass")
    
    def test_contraseña_login_no_string(self, mock_conexion_global, fernet_key_env):
        with pytest.raises(TypeError, match="contraseña_login debe ser string"):
            ver_contraseña("id", 123)
    
    def test_usuario_id_vacio(self, mock_conexion_global, fernet_key_env):
        with pytest.raises(ValueError, match="usuario_id no puede estar vacío"):
            ver_contraseña("", "pass")
    
    def test_contraseña_login_vacia(self, mock_conexion_global, fernet_key_env):
        with pytest.raises(ValueError, match="contraseña_login no puede estar vacía"):
            ver_contraseña("id", "")
    
    def test_usuario_id_invalido(self, mock_conexion_global, fernet_key_env):
        with pytest.raises(ValueError, match="usuario_id inválido"):
            ver_contraseña("no_es_objectid", "pass")


class TestVerContraseñaExito:
    """Tests para verificación exitosa de contraseña"""
    
    def test_ver_contraseña_correcta(self, mock_conexion_global, fernet_key_env, usuario_registrado):
        """Ver contraseña con login correcto debe retornar contraseña"""
        usr = usuario_registrado
        contraseña = ver_contraseña(str(usr['usuario']['_id']), usr['contraseña'])
        assert contraseña == usr['contraseña']
    
    def test_ver_contraseña_login_incorrecto(self, mock_conexion_global, fernet_key_env, usuario_registrado):
        """Login incorrecto debe fallar"""
        usr = usuario_registrado
        with pytest.raises(Exception, match="verificación incorrecta"):
            ver_contraseña(str(usr['usuario']['_id']), "Contraseña_Mal_123!")
    
    def test_usuario_no_existe(self, mock_conexion_global, fernet_key_env):
        """Usuario inexistente debe fallar"""
        id_falso = str(ObjectId())
        with pytest.raises(Exception, match="Usuario no encontrado"):
            ver_contraseña(id_falso, "pass")
