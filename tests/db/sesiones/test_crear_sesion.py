"""Tests para crear_sesion()"""

import pytest
from datetime import datetime
from bson import ObjectId
from unittest.mock import patch
from src.db.sesiones.crear_sesion import crear_sesion


class TestCrearSesionValidacion:
    """Tests para validación en crear_sesion"""
    
    def test_usuario_id_no_string(self, conexion_mongodb_mock):
        """Debe fallar si usuario_id no es string"""
        with patch('src.db.sesiones.crear_sesion.ConexionMongoDB', return_value=conexion_mongodb_mock):
            with pytest.raises(TypeError, match="usuario_id debe ser string"):
                crear_sesion(123, 'pomodoro')
    
    def test_tipo_sesion_no_string(self, conexion_mongodb_mock):
        """Debe fallar si tipo_sesion no es string"""
        with patch('src.db.sesiones.crear_sesion.ConexionMongoDB', return_value=conexion_mongodb_mock):
            with pytest.raises(TypeError, match="tipo_sesion debe ser string"):
                crear_sesion(str(ObjectId()), 123)
    
    def test_usuario_id_vacio(self, conexion_mongodb_mock):
        """Debe fallar si usuario_id es vacío"""
        with patch('src.db.sesiones.crear_sesion.ConexionMongoDB', return_value=conexion_mongodb_mock):
            with pytest.raises(ValueError, match="usuario_id no puede estar vacío"):
                crear_sesion('', 'pomodoro')
    
    def test_tipo_sesion_vacio(self, conexion_mongodb_mock):
        """Debe fallar si tipo_sesion es vacío"""
        with patch('src.db.sesiones.crear_sesion.ConexionMongoDB', return_value=conexion_mongodb_mock):
            with pytest.raises(ValueError, match="tipo_sesion no puede estar vacío"):
                crear_sesion(str(ObjectId()), '')
    
    def test_usuario_id_invalido(self, conexion_mongodb_mock):
        """Debe fallar si usuario_id no es ObjectId válido"""
        with patch('src.db.sesiones.crear_sesion.ConexionMongoDB', return_value=conexion_mongodb_mock):
            with pytest.raises(ValueError, match="usuario_id .* no es un ObjectId válido"):
                crear_sesion('invalid', 'pomodoro')


class TestCrearSesionExito:
    """Tests para casos exitosos de crear_sesion"""
    
    def test_crea_sesion_correctamente(self, usuario_en_db, coleccion_usuarios, coleccion_sesiones):
        """Debe crear sesión correctamente"""
        with patch('src.db.sesiones.crear_sesion.ConexionMongoDB') as mock_db:
            mock_db.return_value.obtener_coleccion = lambda nombre: (
                coleccion_usuarios if nombre == 'usuarios' else coleccion_sesiones
            )
            
            resultado = crear_sesion(str(usuario_en_db['_id']), 'pomodoro')
            
            assert resultado['usuario_id'] == usuario_en_db['_id']
            assert resultado['tipo_sesion'] == 'pomodoro'
            assert resultado['fin'] is None
            assert resultado['completada'] is False
            assert 'inicio' in resultado
            assert isinstance(resultado['inicio'], datetime)
    
    def test_usuario_no_existe(self, coleccion_usuarios, coleccion_sesiones):
        """Debe fallar si usuario no existe"""
        with patch('src.db.sesiones.crear_sesion.ConexionMongoDB') as mock_db:
            mock_db.return_value.obtener_coleccion = lambda nombre: (
                coleccion_usuarios if nombre == 'usuarios' else coleccion_sesiones
            )
            
            id_falso = str(ObjectId())
            with pytest.raises(Exception, match="Usuario con ID .* no existe"):
                crear_sesion(id_falso, 'pomodoro')
    
    def test_tipos_sesion_validos(self, usuario_en_db, coleccion_usuarios, coleccion_sesiones):
        """Debe permitir diferentes tipos de sesión"""
        with patch('src.db.sesiones.crear_sesion.ConexionMongoDB') as mock_db:
            mock_db.return_value.obtener_coleccion = lambda nombre: (
                coleccion_usuarios if nombre == 'usuarios' else coleccion_sesiones
            )
            
            for tipo in ['pomodoro', 'pausa', 'trabajo']:
                resultado = crear_sesion(str(usuario_en_db['_id']), tipo)
                assert resultado['tipo_sesion'] == tipo
