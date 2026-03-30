"""Tests para registrar_anomalia()"""

import pytest
from datetime import datetime
from bson import ObjectId
from src.db.anomalias.registrar_anomalia import registrar_anomalia


class TestRegistrarAnomaliaValidacion:
    """Tests para validación en registrar_anomalia"""
    
    def test_usuario_id_no_string(self, mock_conexion_global):
        """Debe fallar si usuario_id no es string"""
        with pytest.raises(TypeError, match="usuario_id debe ser string"):
            registrar_anomalia(123, 'tipo', 'desc')
    
    def test_tipo_no_string(self, mock_conexion_global):
        """Debe fallar si tipo no es string"""
        with pytest.raises(TypeError, match="tipo debe ser string"):
            registrar_anomalia(str(ObjectId()), 123, 'desc')
    
    def test_descripcion_no_string(self, mock_conexion_global):
        """Debe fallar si descripcion no es string"""
        with pytest.raises(TypeError, match="descripcion debe ser string"):
            registrar_anomalia(str(ObjectId()), 'tipo', 123)
    
    def test_usuario_id_vacio(self, mock_conexion_global):
        """Debe fallar si usuario_id es vacío"""
        with pytest.raises(ValueError, match="usuario_id no puede estar vacío"):
            registrar_anomalia('', 'tipo', 'desc')


class TestRegistrarAnomaliaExito:
    """Tests para casos exitosos de registrar_anomalia"""
    
    def test_registra_anomalia_correctamente(self, mock_conexion_global, usuario_en_db, coleccion_usuarios, coleccion_anomalias):
        """Debe registrar anomalía correctamente"""
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
    
    def test_usuario_no_existe(self, mock_conexion_global, coleccion_usuarios, coleccion_anomalias):
        """Debe fallar si usuario no existe"""
        id_falso = str(ObjectId())
        with pytest.raises(Exception, match="Usuario con ID .* no existe"):
            registrar_anomalia(id_falso, 'tipo', 'desc')
