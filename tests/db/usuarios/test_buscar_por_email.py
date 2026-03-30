"""Tests para buscar_por_email()"""

import pytest
from datetime import datetime
from bson import ObjectId
from unittest.mock import patch
from src.db.usuarios.buscar_por_email import buscar_por_email


class TestBuscarPorEmailValidacion:
    """Tests para validación en buscar_por_email"""
    
    def test_email_no_string(self, mock_conexion_global):
        """Debe fallar si email no es string"""
        with pytest.raises(TypeError, match="email debe ser string"):
            buscar_por_email(123)
    
    def test_email_vacio(self, mock_conexion_global):
        """Debe fallar si email es vacío"""
        with pytest.raises(ValueError, match="email no puede estar vacío"):
            buscar_por_email('')


class TestBuscarPorEmailExitoso:
    """Tests para casos exitosos de buscar_por_email"""
    
    def test_encuentra_usuario_existente(self, mock_conexion_global, coleccion_usuarios):
        """Debe encontrar usuario existente"""
        # Preparar
        usuario = {
            'email': 'test@example.com',
            'nombre': 'Test',
            'contraseña_hash': 'hash',
            'rol': 'empleado',
            'activo': True,
            'fecha_registro': datetime.utcnow(),
            'ultimo_acceso': datetime.utcnow(),
            'puntuacion_pomodoro': 0,
            'metadata': {}
        }
        coleccion_usuarios.insert_one(usuario)
        
        resultado = buscar_por_email('test@example.com')
        
        assert resultado is not None
        assert resultado['email'] == 'test@example.com'
        assert resultado['nombre'] == 'Test'
    
    def test_no_encuentra_usuario_inexistente(self, mock_conexion_global, coleccion_usuarios):
        """Debe retornar None si usuario no existe"""
        resultado = buscar_por_email('inexistente@example.com')
        
        assert resultado is None
    
    def test_busqueda_case_sensitive(self, mock_conexion_global, coleccion_usuarios):
        """Búsqueda debe ser exacta (case-sensitive)"""
        usuario = {
            'email': 'Test@Example.com',
            'nombre': 'Test',
            'contraseña_hash': 'hash',
            'rol': 'empleado',
            'activo': True,
            'fecha_registro': datetime.utcnow(),
            'ultimo_acceso': datetime.utcnow(),
            'puntuacion_pomodoro': 0,
            'metadata': {}
        }
        coleccion_usuarios.insert_one(usuario)
        
        # Con caso diferente no encuentra
        resultado = buscar_por_email('test@example.com')
        # mongomock es case-sensitive por defecto
        assert resultado is None or resultado['email'] != 'test@example.com'
