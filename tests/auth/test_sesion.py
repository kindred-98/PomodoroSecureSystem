"""Tests para auth/sesion.py — Gestión de sesiones"""

import pytest
from src.auth.sesion import crear_sesion, verificar_sesion, cerrar_sesion_por_token
from src.seguridad.encriptacion import generar_token_sesion


class TestCrearSesion:
    """Tests para crear_sesion"""
    
    def test_creacion_exitosa(self, mock_conexion_global, usuario_en_db):
        """Crear sesión debe retornar documento con token"""
        token = generar_token_sesion()
        sesion = crear_sesion(str(usuario_en_db['_id']), token)
        
        assert sesion['token_sesion'] == token
        assert sesion['activa'] is True
        assert '_id' in sesion
    
    def test_usuario_id_no_string(self, mock_conexion_global):
        with pytest.raises(TypeError, match="usuario_id debe ser string"):
            crear_sesion(123, "token")
    
    def test_token_no_string(self, mock_conexion_global):
        with pytest.raises(TypeError, match="token_sesion debe ser string"):
            crear_sesion("id", 123)
    
    def test_usuario_id_vacio(self, mock_conexion_global):
        with pytest.raises(ValueError, match="usuario_id no puede estar vacío"):
            crear_sesion("", "token")
    
    def test_token_vacio(self, mock_conexion_global):
        with pytest.raises(ValueError, match="token_sesion no puede estar vacío"):
            crear_sesion("id", "")
    
    def test_usuario_id_invalido(self, mock_conexion_global):
        with pytest.raises(ValueError, match="usuario_id inválido"):
            crear_sesion("no_es_objectid", "token")


class TestVerificarSesion:
    """Tests para verificar_sesion"""
    
    def test_sesion_valida(self, mock_conexion_global, usuario_en_db):
        """Sesión activa debe retornar usuario"""
        token = generar_token_sesion()
        crear_sesion(str(usuario_en_db['_id']), token)
        
        usuario = verificar_sesion(token)
        assert usuario is not None
    
    def test_token_inexistente(self, mock_conexion_global):
        """Token que no existe debe fallar"""
        with pytest.raises(Exception, match="Sesión inválida"):
            verificar_sesion("token_inexistente_1234567890abcdef")
    
    def test_sesion_cerrada(self, mock_conexion_global, usuario_en_db):
        """Sesión cerrada no debe ser válida"""
        token = generar_token_sesion()
        crear_sesion(str(usuario_en_db['_id']), token)
        cerrar_sesion_por_token(token)
        
        with pytest.raises(Exception, match="Sesión inválida"):
            verificar_sesion(token)
    
    def test_token_no_string(self, mock_conexion_global):
        with pytest.raises(TypeError, match="token_sesion debe ser string"):
            verificar_sesion(123)
    
    def test_token_vacio(self, mock_conexion_global):
        with pytest.raises(ValueError, match="token_sesion no puede estar vacío"):
            verificar_sesion("")


class TestCerrarSesionPorToken:
    """Tests para cerrar_sesion_por_token"""
    
    def test_cierre_exitoso(self, mock_conexion_global, usuario_en_db):
        """Debe cerrar sesión activa"""
        token = generar_token_sesion()
        crear_sesion(str(usuario_en_db['_id']), token)
        
        assert cerrar_sesion_por_token(token) is True
    
    def test_sesion_no_existe(self, mock_conexion_global):
        with pytest.raises(Exception, match="Sesión no encontrada"):
            cerrar_sesion_por_token("no_existe_token_1234567890abcdef")
    
    def test_token_no_string(self, mock_conexion_global):
        with pytest.raises(TypeError, match="token_sesion debe ser string"):
            cerrar_sesion_por_token(123)
