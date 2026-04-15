"""Tests para pausas/gestor_pausas.py"""

import pytest
from bson import ObjectId
from unittest.mock import patch
from src.pausas.gestor_pausas import iniciar_pausa, finalizar_pausa
from src.timer.ciclo_pomodoro import iniciar_ciclo


class TestIniciarPausa:
    """Tests para iniciar_pausa"""
    
    def test_inicio_exitoso(self, mock_conexion_global, usuario_en_db):
        """Debe iniciar pausa correctamente"""
        uid = str(usuario_en_db['_id'])
        iniciar_ciclo(uid)
        
        resultado = iniciar_pausa(uid)
        
        assert 'pausa_id' in resultado
        assert resultado['pausas_usadas'] == 1
        assert resultado['pausas_restantes'] == 1
    
    def test_segunda_pausa(self, mock_conexion_global, usuario_en_db):
        """Segunda pausa debe incrementar contador"""
        uid = str(usuario_en_db['_id'])
        iniciar_ciclo(uid)
        
        r1 = iniciar_pausa(uid)
        finalizar_pausa(uid)
        
        r2 = iniciar_pausa(uid)
        assert r2['pausas_usadas'] == 2
        assert r2['pausas_restantes'] == 0
    
    def test_tercera_pausa_falla(self, mock_conexion_global, usuario_en_db):
        """Tercera pausa debe fallar"""
        uid = str(usuario_en_db['_id'])
        iniciar_ciclo(uid)
        
        iniciar_pausa(uid)
        finalizar_pausa(uid)
        iniciar_pausa(uid)
        finalizar_pausa(uid)
        
        with pytest.raises(Exception, match="Máximo de pausas"):
            iniciar_pausa(uid)
    
    def test_sin_ciclo_activo_falla(self, mock_conexion_global, usuario_en_db):
        """Sin ciclo activo debe fallar"""
        with pytest.raises(Exception, match="ciclo.*activo"):
            iniciar_pausa(str(usuario_en_db['_id']))
    
    def test_pausa_activa_existente_falla(self, mock_conexion_global, usuario_en_db):
        """Si hay pausa activa, se limpia automáticamente (pausa huérfana)"""
        uid = str(usuario_en_db['_id'])
        iniciar_ciclo(uid)
        
        iniciar_pausa(uid)
        
        # Ahora limpia automáticamente la pausa huérfana
        resultado = iniciar_pausa(uid)
        assert resultado is not None
    
    def test_usuario_id_no_string(self, mock_conexion_global):
        with pytest.raises(TypeError, match="usuario_id debe ser string"):
            iniciar_pausa(123)
    
    def test_usuario_id_vacio(self, mock_conexion_global):
        with pytest.raises(ValueError, match="no puede estar vacío"):
            iniciar_pausa("")
    
    def test_usuario_id_invalido(self, mock_conexion_global):
        with pytest.raises(ValueError, match="inválido"):
            iniciar_pausa("no_es_objectid")


class TestFinalizarPausa:
    """Tests para finalizar_pausa"""
    
    def test_finalizacion_exitosa(self, mock_conexion_global, usuario_en_db):
        """Debe finalizar pausa correctamente"""
        uid = str(usuario_en_db['_id'])
        iniciar_ciclo(uid)
        iniciar_pausa(uid)
        
        resultado = finalizar_pausa(uid)
        
        assert 'pausa_id' in resultado
        assert resultado['duracion_minutos'] >= 0
        assert resultado['excedida'] is False
        assert resultado['anomalia'] is None
    
    def test_sin_pausa_activa_falla(self, mock_conexion_global, usuario_en_db):
        """Sin pausa activa debe fallar"""
        with pytest.raises(Exception, match="No hay pausa activa"):
            finalizar_pausa(str(usuario_en_db['_id']))
    
    def test_usuario_id_no_string(self, mock_conexion_global):
        with pytest.raises(TypeError, match="usuario_id debe ser string"):
            finalizar_pausa(123)
    
    def test_usuario_id_vacio(self, mock_conexion_global):
        with pytest.raises(ValueError, match="no puede estar vacío"):
            finalizar_pausa("")
    
    def test_pausa_excedida_registra_anomalia(self, mock_conexion_global, usuario_en_db):
        """Pausa > 10 min debe registrar anomalía"""
        uid = str(usuario_en_db['_id'])
        oid = usuario_en_db['_id']
        iniciar_ciclo(uid)
        iniciar_pausa(uid)
        
        # Simular que pasaron 11 minutos
        from datetime import datetime, timezone, timedelta
        coleccion_pausas = mock_conexion_global.obtener_coleccion('pausas_manuales')
        coleccion_pausas.update_one(
            {'usuario_id': oid, 'activa': True},
            {'$set': {'inicio': datetime.now(timezone.utc) - timedelta(minutes=11)}}
        )
        
        resultado = finalizar_pausa(uid)
        
        assert resultado['excedida'] is True
        assert resultado['anomalia'] is not None
        assert resultado['duracion_minutos'] >= 10
    
    def test_no_excedida_no_anomalia(self, mock_conexion_global, usuario_en_db):
        """Pausa <= 10 min NO debe registrar anomalía"""
        uid = str(usuario_en_db['_id'])
        iniciar_ciclo(uid)
        iniciar_pausa(uid)
        
        # Simular que pasaron 3 minutos
        from datetime import datetime, timezone, timedelta
        oid = usuario_en_db['_id']
        coleccion_pausas = mock_conexion_global.obtener_coleccion('pausas_manuales')
        coleccion_pausas.update_one(
            {'usuario_id': oid, 'activa': True},
            {'$set': {'inicio': datetime.now(timezone.utc) - timedelta(minutes=3)}}
        )
        
        resultado = finalizar_pausa(uid)
        
        assert resultado['excedida'] is False
        assert resultado['anomalia'] is None
