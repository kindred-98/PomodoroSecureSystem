"""Tests para auth/verificacion_email.py"""

import pytest
import time
from datetime import datetime, timezone, timedelta
from src.auth.verificacion_email import (
    generar_token,
    generar_token_verificacion,
    crear_token_verificacion,
    crear_o_actualizar_verificacion,
    verificar_token_db,
    verificar_token_legacy as verificar_token,
    verificar_email_esta_verificado,
    obtener_token_pendiente,
    obtener_verificacion_pendiente,
    esta_verificado,
    hash_token,
    verificar_token_hash,
)


class TestGenerarToken:
    """Tests para generación de tokens."""
    
    def test_token_longitud_6(self):
        """Token debe tener 6 dígitos."""
        token = generar_token(6)
        assert len(token) == 6
        assert token.isdigit()
    
    def test_token_longitud_8(self):
        """Token debe tener 8 dígitos."""
        token = generar_token(8)
        assert len(token) == 8
        assert token.isdigit()
    
    def test_tokens_unicos(self):
        """Tokens deben ser únicos."""
        tokens = [generar_token(6) for _ in range(100)]
        assert len(set(tokens)) == 100
    
    def test_hash_token(self):
        """Hash debe ser consistente."""
        token = "123456"
        h1 = hash_token(token)
        h2 = hash_token(token)
        assert h1 == h2
        assert len(h1) == 64  # SHA256 hex


class TestCrearToken:
    """Tests para crear token de verificación."""
    
    def test_crear_token(self, mock_conexion_global):
        """Debe crear un token para el email."""
        resultado = crear_o_actualizar_verificacion("test@example.com")
        
        assert resultado is not None
        assert len(resultado) == 6
        assert resultado.isdigit()
    
    def test_token_en_bd(self, mock_conexion_global):
        """Token debe guardarse en BD."""
        from src.db.conexion import conexion_global
        
        crear_o_actualizar_verificacion("test2@example.com")
        
        coleccion = conexion_global.obtener_coleccion('verificaciones_email')
        doc = coleccion.find_one({'email': 'test2@example.com'})
        
        assert doc is not None
        assert 'token_hash' in doc
        assert 'expira' in doc
    
    def test_reemplaza_token_anterior(self, mock_conexion_global):
        """Debe eliminar tokens anteriores."""
        crear_o_actualizar_verificacion("test3@example.com")
        crear_o_actualizar_verificacion("test3@example.com")
        
        from src.db.conexion import conexion_global
        coleccion = conexion_global.obtener_coleccion('verificaciones_email')
        tokens = list(coleccion.find({'email': 'test3@example.com'}))
        
        assert len(tokens) == 1


class TestVerificarToken:
    """Tests para verificar token."""
    
    def test_token_correcto(self, mock_conexion_global):
        """Token correcto debe verificar."""
        token = crear_o_actualizar_verificacion("ok@example.com")
        
        resultado = verificar_token_db("ok@example.com", token)
        
        assert resultado['valido'] is True
        assert resultado['mensaje'] == 'Email verificado correctamente'
    
    def test_token_incorrecto(self, mock_conexion_global):
        """Token incorrecto debe fallar."""
        crear_o_actualizar_verificacion("fail@example.com")
        
        resultado = verificar_token_db("fail@example.com", "000000")
        
        assert resultado['valido'] is False
        assert 'incorrecto' in resultado['mensaje'].lower()
    
    def test_token_expirado(self, mock_conexion_global):
        """Token expirado debe fallar."""
        from src.db.conexion import conexion_global
        
        coleccion = conexion_global.obtener_coleccion('verificaciones_email')
        coleccion.insert_one({
            'email': 'expired@example.com',
            'token_hash': hash_token('123456'),
            'expira': int(time.time()) - 60,
            'intentos': 0,
            'max_intentos': 5,
            'creado_en': int(time.time()) - 300,
            'bloqueado_hasta': None
        })
        
        resultado = verificar_token_db("expired@example.com", "123456")
        
        assert resultado['valido'] is False
        assert 'expirado' in resultado['mensaje'].lower()
    
    def test_demasiados_intentos(self, mock_conexion_global):
        """Demasiados intentos debe bloquear."""
        from src.db.conexion import conexion_global
        
        # Crear token con 5 intentos
        coleccion = conexion_global.obtener_coleccion('verificaciones_email')
        coleccion.insert_one({
            'email': 'blocked@example.com',
            'token_hash': hash_token('999999'),
            'expira': int(time.time()) + 300,
            'intentos': 5,
            'max_intentos': 5,
            'creado_en': int(time.time()) - 60,
            'bloqueado_hasta': None
        })
        
        resultado = verificar_token_db("blocked@example.com", "999999")
        
        assert resultado['valido'] is False
        assert 'intentos' in resultado['mensaje'].lower() or 'bloqueado' in resultado['mensaje'].lower()


class TestVerificarEmailVerificado:
    """Tests para verificar si email está verificado."""
    
    def test_email_verificado(self, mock_conexion_global):
        """Debe retornar True si está verificado."""
        from src.db.conexion import conexion_global
        
        coleccion = conexion_global.obtener_coleccion('usuarios')
        coleccion.insert_one({
            'email': 'yes@example.com',
            'email_verified': True,
            'nombre': 'Test'
        })
        
        assert esta_verificado("yes@example.com") is True
    
    def test_email_no_verificado(self, mock_conexion_global):
        """Debe retornar False si no está verificado."""
        from src.db.conexion import conexion_global
        
        coleccion = conexion_global.obtener_coleccion('usuarios')
        coleccion.insert_one({
            'email': 'no@example.com',
            'email_verified': False,
            'nombre': 'Test'
        })
        
        assert esta_verificado("no@example.com") is False
    
    def test_email_sin_usuario(self, mock_conexion_global):
        """Debe retornar False si no existe usuario."""
        assert esta_verificado("notfound@example.com") is False