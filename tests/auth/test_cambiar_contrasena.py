"""Tests para auth/cambiar_contraseña.py"""

import pytest
from bson import ObjectId
from src.auth.cambiar_contrasena import cambiar_contrasena


class TestCambiarContrasenaValidacion:
    """Tests para validación en cambiar_contraseña"""
    
    def test_usuario_id_no_string(self, mock_conexion_global, fernet_key_env):
        with pytest.raises(TypeError, match="usuario_id debe ser string"):
            cambiar_contrasena(123, "Pass123!")
    
    def test_contrasena_no_string(self, mock_conexion_global, fernet_key_env):
        with pytest.raises(TypeError, match="nueva_contraseña debe ser string"):
            cambiar_contrasena("id", 123)
    
    def test_usuario_id_vacio(self, mock_conexion_global, fernet_key_env):
        with pytest.raises(ValueError, match="usuario_id no puede estar vacío"):
            cambiar_contrasena("", "Pass123!")
    
    def test_contrasena_vacia(self, mock_conexion_global, fernet_key_env):
        with pytest.raises(ValueError, match="nueva_contraseña no puede estar vacía"):
            cambiar_contrasena("id", "")
    
    def test_usuario_id_invalido(self, mock_conexion_global, fernet_key_env):
        with pytest.raises(ValueError, match="usuario_id inválido"):
            cambiar_contrasena("no_es_objectid", "Pass123!")


class TestCambiarContrasenaFortaleza:
    """Tests para verificación de fortaleza"""
    
    def test_contrasena_debil_rechazada(self, mock_conexion_global, fernet_key_env, usuario_registrado):
        """Contraseña débil debe ser rechazada"""
        usr = usuario_registrado
        with pytest.raises(ValueError, match="Muy Fuerte"):
            cambiar_contrasena(str(usr['usuario']['_id']), "abc")
    
    def test_contrasena_normal_rechazada(self, mock_conexion_global, fernet_key_env, usuario_registrado):
        """Contraseña normal debe ser rechazada"""
        usr = usuario_registrado
        with pytest.raises(ValueError, match="Muy Fuerte"):
            cambiar_contrasena(str(usr['usuario']['_id']), "Abc12345!")


class TestCambiarContrasenaExito:
    """Tests para cambio exitoso"""
    
    def test_contrasena_fuerte_aceptada(self, mock_conexion_global, fernet_key_env, usuario_registrado):
        """Contraseña muy fuerte debe ser aceptada"""
        usr = usuario_registrado
        pw_fuerte = "K#mW7$hPq9xN2zB!Lw4T"
        resultado = cambiar_contrasena(str(usr['usuario']['_id']), pw_fuerte)
        
        assert resultado['mensaje'] == "Contraseña cambiada exitosamente"
        assert resultado['fortaleza']['nivel'] == "Muy Fuerte"
    
    def test_hash_se_actualiza(self, mock_conexion_global, fernet_key_env, usuario_registrado):
        """Hash debe cambiar en BD"""
        usr = usuario_registrado
        hash_original = usr['usuario']['contraseña_hash']
        pw_fuerte = "XyZ9!@Bw$qR3nK7mP1tV"
        
        cambiar_contrasena(str(usr['usuario']['_id']), pw_fuerte)
        
        coleccion = mock_conexion_global.obtener_coleccion('usuarios')
        usuario_bd = coleccion.find_one({'_id': usr['usuario']['_id']})
        assert usuario_bd['contraseña_hash'] != hash_original
    
    def test_usuario_no_existe(self, mock_conexion_global, fernet_key_env):
        pw_fuerte = "K#mW7$hPq9xN2zB!Lw4T"
        id_falso = str(ObjectId())
        with pytest.raises(Exception, match="Usuario no encontrado"):
            cambiar_contrasena(id_falso, pw_fuerte)
