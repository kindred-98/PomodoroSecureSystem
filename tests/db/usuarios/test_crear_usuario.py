"""Tests para crear_usuario()"""

import pytest
from datetime import datetime
from bson import ObjectId
from unittest.mock import patch, MagicMock
from src.db.usuarios.crear_usuario import crear_usuario


class TestCrearUsuarioValidacionTipos:
    """Tests para validación de tipos en crear_usuario"""
    
    def test_email_no_string(self, mock_conexion_global):
        """Debe fallar si email no es string"""
        with pytest.raises(TypeError, match="Email debe ser string"):
            crear_usuario(123, 'Test', 'hash', 'empleado')
    
    def test_nombre_no_string(self, mock_conexion_global):
        """Debe fallar si nombre no es string"""
        with pytest.raises(TypeError, match="Nombre debe ser string"):
            crear_usuario('test@example.com', 123, 'hash', 'empleado')
    
    def test_contraseña_hash_no_string(self, mock_conexion_global):
        """Debe fallar si contraseña_hash no es string"""
        with pytest.raises(TypeError, match="Contraseña_hash debe ser string"):
            crear_usuario('test@example.com', 'Test', 123, 'empleado')
    
    def test_rol_no_string(self, mock_conexion_global):
        """Debe fallar si rol no es string"""
        with pytest.raises(TypeError, match="Rol debe ser string"):
            crear_usuario('test@example.com', 'Test', 'hash', 123)


class TestCrearUsuarioValidacionValores:
    """Tests para validación de valores en crear_usuario"""
    
    def test_email_vacio(self, mock_conexion_global):
        """Debe fallar si email es vacío"""
        with pytest.raises(ValueError, match="Email no puede estar vacío"):
            crear_usuario('', 'Test', 'hash', 'empleado')
    
    def test_nombre_vacio(self, mock_conexion_global):
        """Debe fallar si nombre es vacío"""
        with pytest.raises(ValueError, match="Nombre no puede estar vacío"):
            crear_usuario('test@example.com', '', 'hash', 'empleado')
    
    def test_hash_vacio(self, mock_conexion_global):
        """Debe fallar si hash es vacío"""
        with pytest.raises(ValueError, match="Contraseña_hash no puede estar vacía"):
            crear_usuario('test@example.com', 'Test', '', 'empleado')
    
    def test_rol_vacio(self, mock_conexion_global):
        """Debe fallar si rol es vacío"""
        with pytest.raises(ValueError, match="Rol debe ser uno de"):
            crear_usuario('test@example.com', 'Test', 'hash', '')


class TestCrearUsuarioExito:
    """Tests para casos exitosos de crear_usuario"""
    
    def test_crea_usuario_correctamente(self, mock_conexion_global, coleccion_usuarios):
        """Debe crear usuario correctamente en BD"""
        resultado = crear_usuario('nuevo@example.com', 'Nuevo User', 'hash_123', 'empleado')
        
        assert resultado['email'] == 'nuevo@example.com'
        assert resultado['nombre'] == 'Nuevo User'
        assert resultado['rol'] == 'empleado'
        assert resultado['activo'] is True
        assert '_id' in resultado
    
    def test_usuario_en_bd(self, mock_conexion_global, coleccion_usuarios):
        """Debe guardar usuario en la BD"""
        crear_usuario('test@example.com', 'Test', 'hash', 'empleado')
        
        usuario_en_bd = coleccion_usuarios.find_one({'email': 'test@example.com'})
        assert usuario_en_bd is not None
        assert usuario_en_bd['nombre'] == 'Test'
    
    def test_email_duplicado_falla(self, mock_conexion_global, coleccion_usuarios):
        """Debe fallar si email ya existe en BD"""
        # Crear primer usuario
        crear_usuario('test@example.com', 'Test 1', 'hash1', 'empleado')
        
        # Intentar crear segundo con mismo email debe fallar
        with pytest.raises(Exception, match="email .* ya está registrado"):
            crear_usuario('test@example.com', 'Test 2', 'hash2', 'empleado')


class TestCrearUsuarioMetadatos:
    """Tests para que usuario tenga metadatos correctos"""
    
    def test_tiene_timestamp_registro(self, mock_conexion_global):
        """Usuario debe tener fecha_registro"""
        resultado = crear_usuario('test@example.com', 'Test', 'hash', 'empleado')
        
        assert 'fecha_registro' in resultado
        assert isinstance(resultado['fecha_registro'], datetime)
    
    def test_puntuacion_inicial_cero(self, mock_conexion_global):
        """Usuario debe empezar con puntuación 0"""
        resultado = crear_usuario('test@example.com', 'Test', 'hash', 'empleado')
        
        assert resultado['puntuacion_pomodoro'] == 0
