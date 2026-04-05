"""
Tests para src.timer.servicio_timer - Funciones de expiración de sesión
"""

import pytest
from datetime import datetime, timezone, timedelta
from unittest.mock import MagicMock, patch
from bson import ObjectId

from src.timer.servicio_timer import ServicioTimer, HORAS_MAXIMAS_SESION
from src.timer.estados import (
    ESTADO_INACTIVO,
    ESTADO_TRABAJANDO,
    ESTADO_DESCANSO_CORTO,
    ESTADO_DESCANSO_LARGO,
)


class TestVerificarSesionExpirada:
    """Tests para verificar_sesion_expirada"""

    def test_sin_sesion_en_bd_no_expirada(self, mock_conexion_global):
        """Verifica que sin sesión en BD retorne no expirada"""
        timer = ServicioTimer()
        
        with patch('src.timer.servicio_timer.conexion_global', mock_conexion_global):
            resultado = timer.verificar_sesion_expirada(str(ObjectId()))
        
        assert resultado['expirada'] is False
        assert resultado['motivo'] == 'sin_sesion'

    def test_sin_timestamp_no_expirada(self, mock_conexion_global):
        """Verifica que sesión sin timestamp no se expire"""
        timer = ServicioTimer()
        usuario_id = str(ObjectId())
        
        coleccion = mock_conexion_global.obtener_coleccion('timer_estado')
        coleccion.insert_one({
            'usuario_id': ObjectId(usuario_id),
            'estado': ESTADO_TRABAJANDO,
        })
        
        with patch('src.timer.servicio_timer.conexion_global', mock_conexion_global):
            resultado = timer.verificar_sesion_expirada(usuario_id)
        
        assert resultado['expirada'] is False
        assert resultado['motivo'] == 'sin_timestamp'


class TestForzarResetPorExpiracion:
    """Tests para forzar_reset_por_expiracion"""

    def test_sin_sesion_retorna_false(self, mock_conexion_global):
        """Verifica que retorne False si no hay sesión"""
        timer = ServicioTimer()
        usuario_id = str(ObjectId())
        
        with patch('src.timer.servicio_timer.conexion_global', mock_conexion_global):
            resultado = timer.forzar_reset_por_expiracion(
                usuario_id,
                "Sin sesión"
            )
        
        assert resultado is False


class TestFinJornadaLaboral:
    """Tests para fin_jornada_laboral"""

    def test_fin_jornada_exitoso(self, mock_conexion_global):
        """Verifica que fin de jornada funcione correctamente"""
        timer = ServicioTimer()
        usuario_id = str(ObjectId())
        
        with patch('src.timer.servicio_timer.conexion_global', mock_conexion_global):
            resultado = timer.fin_jornada_laboral(usuario_id)
        
        assert resultado['exito'] is True
        assert 'resumen' in resultado

    def test_resetea_servicio(self, mock_conexion_global):
        """Verifica que el servicio quede reseteado"""
        timer = ServicioTimer()
        usuario_id = str(ObjectId())
        
        timer.ciclo_activo = True
        timer.estado = ESTADO_TRABAJANDO
        
        with patch('src.timer.servicio_timer.conexion_global', mock_conexion_global):
            timer.fin_jornada_laboral(usuario_id)
        
        assert timer.ciclo_activo is False
        assert timer.estado == ESTADO_INACTIVO


class TestHorasyMaximasSesion:
    """Tests para la constante HORAS_MAXIMAS_SESION"""

    def test_horas_maximas_definidas(self):
        """Verifica que HORAS_MAXIMAS_SESION esté definida"""
        assert HORAS_MAXIMAS_SESION == 12

    def test_horas_maximas_es_entero(self):
        """Verifica que sea un entero"""
        assert isinstance(HORAS_MAXIMAS_SESION, int)


class TestParsearOid:
    """Tests para _parsear_oid"""

    def test_parsea_objectid_string(self):
        """Verifica que convierta string a ObjectId"""
        timer = ServicioTimer()
        oid_str = str(ObjectId())
        
        resultado = timer._parsear_oid(oid_str)
        
        assert isinstance(resultado, ObjectId)

    def test_maneja_objectid(self):
        """Verifica que maneje ObjectId directamente"""
        timer = ServicioTimer()
        oid = ObjectId()
        
        resultado = timer._parsear_oid(oid)
        
        assert resultado == oid

    def test_maneja_id_invalido(self):
        """Verifica que maneje ID inválido"""
        timer = ServicioTimer()
        
        resultado = timer._parsear_oid("id-invalido")
        
        assert resultado == "id-invalido"
