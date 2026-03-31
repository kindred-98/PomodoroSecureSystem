"""Tests para timer/servicio_sesiones.py"""

import pytest
from bson import ObjectId
from src.timer.servicio_sesiones import registrar_sesion_pomodoro


class TestRegistrarSesionPomodoro:
    """Tests para registrar_sesion_pomodoro"""
    
    def test_registro_exitoso(self, mock_conexion_global, usuario_en_db):
        """Debe registrar sesión en BD"""
        datos_ciclo = {
            '_id': ObjectId(),
            'numero_ciclo': 1,
            'pomodoro_actual': 1,
        }
        
        sesion = registrar_sesion_pomodoro(
            str(usuario_en_db['_id']), datos_ciclo, 25
        )
        
        assert '_id' in sesion
        assert sesion['tipo_sesion'] == 'pomodoro'
        assert sesion['duracion_programada_min'] == 25
        assert sesion['duracion_segundos'] == 1500
    
    def test_datos_ciclo_en_sesion(self, mock_conexion_global, usuario_en_db):
        """Datos del ciclo deben estar en la sesión"""
        datos_ciclo = {
            '_id': ObjectId(),
            'numero_ciclo': 3,
            'pomodoro_actual': 2,
        }
        
        sesion = registrar_sesion_pomodoro(
            str(usuario_en_db['_id']), datos_ciclo, 30
        )
        
        assert sesion['numero_ciclo'] == 3
        assert sesion['pomodoro_numero'] == 2
    
    def test_usuario_id_no_string(self, mock_conexion_global):
        with pytest.raises(TypeError, match="usuario_id debe ser string"):
            registrar_sesion_pomodoro(123, {}, 25)
    
    def test_datos_no_dict(self, mock_conexion_global, usuario_en_db):
        with pytest.raises(TypeError, match="datos_ciclo debe ser dict"):
            registrar_sesion_pomodoro(str(usuario_en_db['_id']), "no", 25)
    
    def test_duracion_no_int(self, mock_conexion_global, usuario_en_db):
        with pytest.raises(TypeError, match="duracion_min debe ser int"):
            registrar_sesion_pomodoro(str(usuario_en_db['_id']), {}, "25")
    
    def test_usuario_id_invalido(self, mock_conexion_global):
        with pytest.raises(ValueError, match="inválido"):
            registrar_sesion_pomodoro("no_es_id", {}, 25)
