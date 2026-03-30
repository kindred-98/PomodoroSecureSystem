"""Tests para actualizar_ultimo_acceso()"""

import pytest
from datetime import datetime
from bson import ObjectId
from src.db.usuarios.actualizar_ultimo_acceso import actualizar_ultimo_acceso


class TestActualizarUltimoAccesoValidacion:
    """Tests para validación en actualizar_ultimo_acceso"""
    
    def test_usuario_id_no_string(self, mock_conexion_global):
        """Debe fallar si usuario_id no es string"""
        with pytest.raises(TypeError, match="usuario_id debe ser string"):
            actualizar_ultimo_acceso(123)
    
    def test_usuario_id_vacio(self, mock_conexion_global):
        """Debe fallar si usuario_id es vacío"""
        with pytest.raises(ValueError, match="ID inválido"):
            actualizar_ultimo_acceso('')
    
    def test_usuario_id_invalido(self, mock_conexion_global):
        """Debe fallar si usuario_id no es ObjectId válido"""
        with pytest.raises(ValueError, match="ID inválido"):
            actualizar_ultimo_acceso('invalid')


class TestActualizarUltimoAccesoExito:
    """Tests para casos exitosos de actualizar_ultimo_acceso"""
    
    def test_actualiza_timestamp(self, mock_conexion_global, usuario_en_db, coleccion_usuarios):
        """Debe actualizar el timestamp de último acceso"""
        resultado = actualizar_ultimo_acceso(str(usuario_en_db['_id']))
        
        assert 'ultimo_acceso' in resultado
        assert isinstance(resultado['ultimo_acceso'], datetime)
    
    def test_timestamp_es_reciente(self, mock_conexion_global, usuario_en_db, coleccion_usuarios):
        """Timestamp debe ser muy reciente (menos de 5 segundos)"""
        from datetime import timedelta
        
        ahora_antes = datetime.utcnow()
        resultado = actualizar_ultimo_acceso(str(usuario_en_db['_id']))
        ahora_despues = datetime.utcnow()
        
        ts = resultado['ultimo_acceso']
        # El timestamp debería ser cercano a ahora (dentro de 5 segundos)
        assert abs((ts - ahora_antes).total_seconds()) < 5
    
    def test_usuario_no_existe(self, mock_conexion_global, coleccion_usuarios):
        """Debe fallar si usuario no existe"""
        id_falso = str(ObjectId())
        with pytest.raises(Exception, match="Usuario con ID .* no existe"):
            actualizar_ultimo_acceso(id_falso)
