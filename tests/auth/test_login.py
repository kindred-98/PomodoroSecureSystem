"""Tests para auth/login.py — Inicio de sesión"""

import pytest
from src.auth.login import iniciar_sesion


class TestLoginValidacion:
    """Tests para validación de entrada en iniciar_sesion"""
    
    def test_email_no_string(self, mock_conexion_global, fernet_key_env):
        with pytest.raises(TypeError, match="email debe ser string"):
            iniciar_sesion(123, "pass")
    
    def test_contraseña_no_string(self, mock_conexion_global, fernet_key_env):
        with pytest.raises(TypeError, match="contraseña debe ser string"):
            iniciar_sesion("a@b.com", 123)
    
    def test_email_vacio(self, mock_conexion_global, fernet_key_env):
        with pytest.raises(ValueError, match="email no puede estar vacío"):
            iniciar_sesion("", "pass")
    
    def test_contraseña_vacia(self, mock_conexion_global, fernet_key_env):
        with pytest.raises(ValueError, match="contraseña no puede estar vacía"):
            iniciar_sesion("a@b.com", "")


class TestLoginCredenciales:
    """Tests para verificación de credenciales"""
    
    def test_login_exitoso(self, mock_conexion_global, fernet_key_env, usuario_registrado):
        """Login con credenciales correctas debe retornar usuario + token"""
        usr = usuario_registrado
        resultado = iniciar_sesion(usr['usuario']['email'], usr['contraseña'])
        
        assert 'usuario' in resultado
        assert 'token_sesion' in resultado
        assert len(resultado['token_sesion']) == 64
    
    def test_email_inexistente(self, mock_conexion_global, fernet_key_env):
        """Email que no existe debe fallar"""
        with pytest.raises(Exception, match="Credenciales incorrectas"):
            iniciar_sesion("noexiste@test.com", "pass123")
    
    def test_contraseña_incorrecta(self, mock_conexion_global, fernet_key_env, usuario_registrado):
        """Contraseña incorrecta debe fallar"""
        usr = usuario_registrado
        with pytest.raises(Exception, match="Credenciales incorrectas"):
            iniciar_sesion(usr['usuario']['email'], "Contraseña_Mal_123!")
    
    def test_usuario_desactivado(self, mock_conexion_global, fernet_key_env, usuario_registrado):
        """Usuario desactivado no debe poder hacer login"""
        usr = usuario_registrado
        coleccion = mock_conexion_global.obtener_coleccion('usuarios')
        coleccion.update_one(
            {'_id': usr['usuario']['_id']},
            {'$set': {'activo': False}}
        )
        
        with pytest.raises(Exception, match="Usuario desactivado"):
            iniciar_sesion(usr['usuario']['email'], usr['contraseña'])


class TestLoginSesion:
    """Tests para creación de sesión durante login"""
    
    def test_token_se_guarda_en_bd(self, mock_conexion_global, fernet_key_env, usuario_registrado):
        """Token de sesión debe guardarse en colección sesiones_auth"""
        usr = usuario_registrado
        resultado = iniciar_sesion(usr['usuario']['email'], usr['contraseña'])
        
        coleccion = mock_conexion_global.obtener_coleccion('sesiones_auth')
        sesion = coleccion.find_one({'token_sesion': resultado['token_sesion']})
        
        assert sesion is not None
        assert sesion['activa'] is True
    
    def test_ultimo_acceso_se_actualiza(self, mock_conexion_global, fernet_key_env, usuario_registrado):
        """Login debe actualizar último acceso del usuario"""
        usr = usuario_registrado
        iniciar_sesion(usr['usuario']['email'], usr['contraseña'])
        
        coleccion = mock_conexion_global.obtener_coleccion('usuarios')
        usuario_bd = coleccion.find_one({'_id': usr['usuario']['_id']})
        
        assert usuario_bd['ultimo_acceso'] is not None


class TestLoginValidacionesSeguridad:
    """Tests para validaciones de seguridad adicionales"""
    
    def test_login_email_con_espacios(self, mock_conexion_global, fernet_key_env, usuario_registrado):
        """Email con espacios debe ser limpiado y aceptado"""
        usr = usuario_registrado
        # Con strip y lowercase debe funcionar
        resultado = iniciar_sesion("  " + usr['usuario']['email'] + "  ", usr['contraseña'])
        assert resultado is not None
    
    def test_login_email_mayusculas(self, mock_conexion_global, fernet_key_env, usuario_registrado):
        """Email en mayúsculas debe funcionar"""
        usr = usuario_registrado
        email_mayus = usr['usuario']['email'].upper()
        resultado = iniciar_sesion(email_mayus, usr['contraseña'])
        assert resultado is not None
