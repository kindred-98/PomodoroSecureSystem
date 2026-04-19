"""Tests para auth/verificacion_email.py"""

import pytest
from datetime import datetime, timezone, timedelta
from src.auth.verificacion_email import (
    generar_token_verificacion,
    crear_token_verificacion,
    verificar_token,
    verificar_email_esta_verificado,
    obtener_token_pendiente,
)


class TestGenerarToken:
    """Tests para generación de tokens."""
    
    def test_token_longitud_6(self):
        """Token debe tener 6 dígitos."""
        token = generar_token_verificacion(6)
        assert len(token) == 6
        assert token.isdigit()
    
    def test_token_longitud_8(self):
        """Token debe tener 8 dígitos."""
        token = generar_token_verificacion(8)
        assert len(token) == 8
        assert token.isdigit()
    
    def test_tokens_unicos(self):
        """Tokens deben ser únicos."""
        tokens = [generar_token_verificacion(6) for _ in range(100)]
        assert len(set(tokens)) == 100


class TestCrearToken:
    """Tests para crear token de verificación."""
    
    def test_crear_token(self, mock_conexion_global):
        """Debe crear un token para el email."""
        resultado = crear_token_verificacion("test@example.com")
        
        assert 'token' in resultado
        assert 'expira' in resultado
        assert resultado['email'] == "test@example.com"
        assert len(resultado['token']) == 6
    
    def test_token_en_bd(self, mock_conexion_global):
        """Token debe guardarse en BD."""
        from src.db.conexion import conexion_global
        
        crear_token_verificacion("test2@example.com")
        
        coleccion = conexion_global.obtener_coleccion('verificaciones_email')
        doc = coleccion.find_one({'email': 'test2@example.com'})
        
        assert doc is not None
        assert doc['verificado'] is False
    
    def test_reemplaza_token_anterior(self, mock_conexion_global):
        """Debe eliminar tokens anteriores."""
        # Crear primer token
        crear_token_verificacion("test3@example.com")
        
        # Crear segundo token
        crear_token_verificacion("test3@example.com")
        
        from src.db.conexion import conexion_global
        coleccion = conexion_global.obtener_coleccion('verificaciones_email')
        tokens = list(coleccion.find({'email': 'test3@example.com'}))
        
        # Solo debe haber 1 token
        assert len(tokens) == 1


class TestVerificarToken:
    """Tests para verificar token."""
    
    def test_token_correcto(self, mock_conexion_global):
        """Token correcto debe verificar."""
        resultado = crear_token_verificacion("ok@example.com")
        token = resultado['token']
        
        verificacion = verificar_token("ok@example.com", token)
        
        assert verificacion['valido'] is True
        assert verificacion['mensaje'] == 'Email verificado correctamente'
    
    def test_token_incorrecto(self, mock_conexion_global):
        """Token incorrecto debe fallar."""
        crear_token_verificacion("fail@example.com")
        
        verificacion = verificar_token("fail@example.com", "000000")
        
        assert verificacion['valido'] is False
        assert verificacion['mensaje'] == 'Token inválido o no encontrado'
    
    def test_token_expirado(self, mock_conexion_global):
        """Token expirado debe fallar."""
        from src.db.conexion import conexion_global
        
        # Crear token con expiración en el pasado
        coleccion = conexion_global.obtener_coleccion('verificaciones_email')
        coleccion.insert_one({
            'email': 'expired@example.com',
            'token': '123456',
            'expira': datetime.now(timezone.utc) - timedelta(minutes=1),
            'creado': datetime.now(timezone.utc),
            'verificado': False
        })
        
        verificacion = verificar_token("expired@example.com", "123456")
        
        assert verificacion['valido'] is False
        assert verificacion['mensaje'] == 'Token expirado'
    
    def test_verificar_email_ya_verificado(self, mock_conexion_global):
        """No debe verificar dos veces."""
        from src.db.conexion import conexion_global
        
        coleccion = conexion_global.obtener_coleccion('verificaciones_email')
        coleccion.insert_one({
            'email': 'duplicate@example.com',
            'token': '654321',
            'expira': datetime.now(timezone.utc) + timedelta(minutes=30),
            'creado': datetime.now(timezone.utc),
            'verificado': True
        })
        
        verificacion = verificar_token("duplicate@example.com", "654321")
        
        assert verificacion['valido'] is False


class TestVerificarEmailVerificado:
    """Tests para verificar si email está verificado."""
    
    def test_email_verificado(self, mock_conexion_global):
        """Debe retornar True si está verificado."""
        from src.db.conexion import conexion_global
        
        coleccion = conexion_global.obtener_coleccion('verificaciones_email')
        coleccion.insert_one({
            'email': 'yes@example.com',
            'token': '111111',
            'expira': datetime.now(timezone.utc) + timedelta(minutes=30),
            'creado': datetime.now(timezone.utc),
            'verificado': True
        })
        
        assert verificar_email_esta_verificado("yes@example.com") is True
    
    def test_email_no_verificado(self, mock_conexion_global):
        """Debe retornar False si no está verificado."""
        from src.db.conexion import conexion_global
        
        coleccion = conexion_global.obtener_coleccion('verificaciones_email')
        coleccion.insert_one({
            'email': 'no@example.com',
            'token': '222222',
            'expira': datetime.now(timezone.utc) + timedelta(minutes=30),
            'creado': datetime.now(timezone.utc),
            'verificado': False
        })
        
        assert verificar_email_esta_verificado("no@example.com") is False
    
    def test_email_sin_token(self, mock_conexion_global):
        """Debe retornar False si no hay token."""
        assert verificar_email_esta_verificado("notfound@example.com") is False