"""Tests para registrar_anomalia()"""

import pytest
from datetime import datetime
from bson import ObjectId
from unittest.mock import patch
from src.db.anomalias.registrar_anomalia import registrar_anomalia


class TestRegistrarAnomaliaValidacion:
    """Tests para validación en registrar_anomalia"""
    
    def test_usuario_id_no_string(self, conexion_mongodb_mock):
        """Debe fallar si usuario_id no es string"""
        with patch('src.db.anomalias.registrar_anomalia.ConexionMongoDB', return_value=conexion_mongodb_mock):
            with pytest.raises(TypeError, match="usuario_id debe ser string"):
                registrar_anomalia(123, 'tipo', 'desc')
    
    def test_tipo_no_string(self, conexion_mongodb_mock):
        """Debe fallar si tipo no es string"""
        with patch('src.db.anomalias.registrar_anomalia.ConexionMongoDB', return_value=conexion_mongodb_mock):
            with pytest.raises(TypeError, match="tipo debe ser string"):
                registrar_anomalia(str(ObjectId()), 123, 'desc')
    
    def test_descripcion_no_string(self, conexion_mongodb_mock):
        """Debe fallar si descripcion no es string"""
        with patch('src.db.anomalias.registrar_anomalia.ConexionMongoDB', return_value=conexion_mongodb_mock):
            with pytest.raises(TypeError, match="descripcion debe ser string"):
                registrar_anomalia(str(ObjectId()), 'tipo', 123)
    
    def test_usuario_id_vacio(self, conexion_mongodb_mock):
        """Debe fallar si usuario_id es vacío"""
        with patch('src.db.anomalias.registrar_anomalia.ConexionMongoDB', return_value=conexion_mongodb_mock):
            with pytest.raises(ValueError, match="usuario_id no puede estar vacío"):
                registrar_anomalia('', 'tipo', 'desc')


class TestRegistrarAnomaliaExito:
    """Tests para casos exitosos de registrar_anomalia"""
    
    def test_registra_anomalia_correctamente(self, usuario_en_db, coleccion_usuarios, coleccion_anomalias):
        """Debe registrar anomalía correctamente"""
        with patch('src.db.anomalias.registrar_anomalia.ConexionMongoDB') as mock_db:
            mock_db.return_value.obtener_coleccion = lambda nombre: (
                coleccion_usuarios if nombre == 'usuarios' else coleccion_anomalias
            )
            
            resultado = registrar_anomalia(
                str(usuario_en_db['_id']),
                'LOGIN_FALLIDO',
                'Múltiples intentos fallidos'
            )
            
            assert resultado['usuario_id'] == usuario_en_db['_id']
            assert resultado['tipo'] == 'LOGIN_FALLIDO'
            assert resultado['descripcion'] == 'Múltiples intentos fallidos'
            assert resultado['revisada'] is False
            assert '_id' in resultado
    
    def test_usuario_no_existe(self, coleccion_usuarios, coleccion_anomalias):
        """Debe fallar si usuario no existe"""
        with patch('src.db.anomalias.registrar_anomalia.ConexionMongoDB') as mock_db:
            mock_db.return_value.obtener_coleccion = lambda nombre: (
                coleccion_usuarios if nombre == 'usuarios' else coleccion_anomalias
            )
            
            id_falso = str(ObjectId())
            with pytest.raises(Exception, match="Usuario con ID .* no existe"):
                registrar_anomalia(id_falso, 'tipo', 'desc')
