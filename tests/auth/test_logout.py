"""Tests para auth/logout.py — Cierre de sesión"""

import pytest
from src.auth.logout import cerrar_sesion


class TestLogoutValidacion:
    """Tests para validación en cerrar_sesion"""
    
    def test_token_no_string(self, mock_conexion_global):
        with pytest.raises(TypeError, match="token_sesion debe ser string"):
            cerrar_sesion(123)
    
    def test_token_vacio(self, mock_conexion_global):
        with pytest.raises(ValueError, match="token_sesion no puede estar vacío"):
            cerrar_sesion("")


class TestLogoutExito:
    """Tests para cierre de sesión exitoso"""
    
    def test_cierra_sesion(self, mock_conexion_global, fernet_key_env, usuario_registrado):
        """Cerrar sesión debe marcar sesión como inactiva"""
        from src.auth.login import iniciar_sesion
        
        usr = usuario_registrado
        resultado = iniciar_sesion(usr['usuario']['email'], usr['contraseña'])
        token = resultado['token_sesion']
        
        assert cerrar_sesion(token) is True
        
        coleccion = mock_conexion_global.obtener_coleccion('sesiones_auth')
        sesion = coleccion.find_one({'token_sesion': token})
        assert sesion['activa'] is False
    
    def test_token_inexistente(self, mock_conexion_global):
        """Token que no existe debe fallar"""
        with pytest.raises(Exception, match="Sesión no encontrada"):
            cerrar_sesion("token_que_no_existe_1234567890abcdef")
    
    def test_sesion_ya_cerrada(self, mock_conexion_global, fernet_key_env, usuario_registrado):
        """Cerrar sesión ya cerrada debe fallar"""
        from src.auth.login import iniciar_sesion
        
        usr = usuario_registrado
        resultado = iniciar_sesion(usr['usuario']['email'], usr['contraseña'])
        token = resultado['token_sesion']
        
        cerrar_sesion(token)
        
        with pytest.raises(Exception, match="ya está cerrada"):
            cerrar_sesion(token)
