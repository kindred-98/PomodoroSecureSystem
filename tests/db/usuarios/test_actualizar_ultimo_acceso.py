"""Tests para actualizar_ultimo_acceso()"""

import pytest
from datetime import datetime
from bson import ObjectId
from unittest.mock import patch
from src.db.usuarios.actualizar_ultimo_acceso import actualizar_ultimo_acceso


class TestActualizarUltimoAccesoValidacion:
    """Tests para validación en actualizar_ultimo_acceso"""
    
    def test_usuario_id_no_string(self, conexion_mongodb_mock):
        """Debe fallar si usuario_id no es string"""
        with patch('src.db.usuarios.actualizar_ultimo_acceso.ConexionMongoDB', return_value=conexion_mongodb_mock):
            with pytest.raises(TypeError, match="usuario_id debe ser string"):
                actualizar_ultimo_acceso(123)
    
    def test_usuario_id_vacio(self, conexion_mongodb_mock):
        """Debe fallar si usuario_id es vacío"""
        with patch('src.db.usuarios.actualizar_ultimo_acceso.ConexionMongoDB', return_value=conexion_mongodb_mock):
            with pytest.raises(ValueError, match="usuario_id no puede estar vacío"):
                actualizar_ultimo_acceso('')
    
    def test_usuario_id_invalido(self, conexion_mongodb_mock):
        """Debe fallar si usuario_id no es ObjectId válido"""
        with patch('src.db.usuarios.actualizar_ultimo_acceso.ConexionMongoDB', return_value=conexion_mongodb_mock):
            with pytest.raises(ValueError, match="usuario_id .* no es un ObjectId válido"):
                actualizar_ultimo_acceso('invalid')


class TestActualizarUltimoAccesoExito:
    """Tests para casos exitosos de actualizar_ultimo_acceso"""
    
    def test_actualiza_timestamp(self, usuario_en_db, coleccion_usuarios):
        """Debe actualizar el timestamp de último acceso"""
        with patch('src.db.usuarios.actualizar_ultimo_acceso.ConexionMongoDB') as mock_db:
            mock_db.return_value.obtener_coleccion.return_value = coleccion_usuarios
            
            resultado = actualizar_ultimo_acceso(str(usuario_en_db['_id']))
            
            assert 'ultimo_acceso' in resultado
            assert isinstance(resultado['ultimo_acceso'], datetime)
    
    def test_timestamp_es_reciente(self, usuario_en_db, coleccion_usuarios):
        """Timestamp debe ser muy reciente (menos de 1 segundo pasado)"""
        with patch('src.db.usuarios.actualizar_ultimo_acceso.ConexionMongoDB') as mock_db:
            mock_db.return_value.obtener_coleccion.return_value = coleccion_usuarios
            
            ahora_antes = datetime.utcnow()
            resultado = actualizar_ultimo_acceso(str(usuario_en_db['_id']))
            ahora_despues = datetime.utcnow()
            
            ts = resultado['ultimo_acceso']
            # El timestamp debe estar entre ahora_antes y ahora_despues
            assert ahora_antes <= ts <= ahora_despues
    
    def test_usuario_no_existe(self, coleccion_usuarios):
        """Debe fallar si usuario no existe"""
        with patch('src.db.usuarios.actualizar_ultimo_acceso.ConexionMongoDB') as mock_db:
            mock_db.return_value.obtener_coleccion.return_value = coleccion_usuarios
            
            id_falso = str(ObjectId())
            with pytest.raises(Exception, match="Usuario con ID .* no existe"):
                actualizar_ultimo_acceso(id_falso)
