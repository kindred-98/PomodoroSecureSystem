"""Tests para crear_sesion()"""

import pytest
from datetime import datetime
from bson import ObjectId
from src.db.sesiones.crear_sesion import crear_sesion


class TestCrearSesionValidacion:
    """Tests para validación en crear_sesion"""
    
    def test_usuario_id_no_string(self, mock_conexion_global):
        """Debe fallar si usuario_id no es string"""
        with pytest.raises(TypeError, match="usuario_id debe ser string"):
            crear_sesion(123, 'pomodoro')
    
    def test_tipo_sesion_no_string(self, mock_conexion_global):
        """Debe fallar si tipo_sesion no es string"""
        with pytest.raises(TypeError, match="tipo_sesion debe ser string"):
            crear_sesion(str(ObjectId()), 123)
    
    def test_usuario_id_vacio(self, mock_conexion_global):
        """Debe fallar si usuario_id es vacío"""
        with pytest.raises(ValueError, match="usuario_id inválido"):
            crear_sesion('', 'pomodoro')
    
    def test_tipo_sesion_vacio(self, mock_conexion_global):
        """Debe fallar si tipo_sesion es vacío"""
        with pytest.raises(ValueError, match="tipo_sesion debe ser uno de"):
            crear_sesion(str(ObjectId()), '')
    
    def test_usuario_id_invalido(self, mock_conexion_global):
        """Debe fallar si usuario_id no es ObjectId válido"""
        with pytest.raises(ValueError, match="usuario_id inválido"):
            crear_sesion('invalid', 'pomodoro')


class TestCrearSesionExito:
    """Tests para casos exitosos de crear_sesion"""
    
    def test_crea_sesion_correctamente(self, mock_conexion_global, usuario_en_db, coleccion_usuarios, coleccion_sesiones):
        """Debe crear sesión correctamente"""
        resultado = crear_sesion(str(usuario_en_db['_id']), 'pomodoro')
        
        assert resultado['usuario_id'] == usuario_en_db['_id']
        assert resultado['tipo_sesion'] == 'pomodoro'
        assert resultado['fin'] is None
        assert resultado['completada'] is False
        assert 'inicio' in resultado
        assert isinstance(resultado['inicio'], datetime)
    
    def test_usuario_no_existe(self, mock_conexion_global, coleccion_usuarios, coleccion_sesiones):
        """Debe fallar si usuario no existe"""
        id_falso = str(ObjectId())
        with pytest.raises(Exception, match="Usuario con ID .* no existe"):
            crear_sesion(id_falso, 'pomodoro')
    
    def test_tipos_sesion_validos(self, mock_conexion_global, usuario_en_db, coleccion_usuarios, coleccion_sesiones):
        """Debe permitir diferentes tipos de sesión"""
        for tipo in ['pomodoro', 'pausa', 'trabajo']:
            resultado = crear_sesion(str(usuario_en_db['_id']), tipo)
            assert resultado['tipo_sesion'] == tipo
