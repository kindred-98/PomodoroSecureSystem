"""Tests para otp/gestor_otp.py"""

import pytest
from unittest.mock import patch
from datetime import datetime, timedelta, timezone
from bson import ObjectId
from src.otp.gestor_otp import (
    generar_otp,
    verificar_otp,
    obtener_estado_otp,
    cancelar_otp,
)


class TestGenerarOtp:
    """Tests para generar_otp"""

    def test_generacion_exitosa(self, mock_conexion_global, usuario_en_db):
        """Debe generar código de 6 dígitos"""
        resultado = generar_otp(str(usuario_en_db['_id']))
        
        assert 'codigo' in resultado
        assert len(resultado['codigo']) == 6
        assert resultado['codigo'].isdigit()
        assert resultado['expira_en_seg'] == 420
        assert 'evento_id' in resultado

    def test_codigo_en_rango_valido(self, mock_conexion_global, usuario_en_db):
        """Código debe estar entre 100000 y 999999"""
        resultado = generar_otp(str(usuario_en_db['_id']))
        codigo = int(resultado['codigo'])
        assert 100000 <= codigo <= 999999

    def test_hash_en_bd(self, mock_conexion_global, usuario_en_db):
        """OTP hash debe guardarse en BD"""
        resultado = generar_otp(str(usuario_en_db['_id']))
        
        coleccion = mock_conexion_global.obtener_coleccion('eventos_otp')
        evento = coleccion.find_one({'_id': ObjectId(resultado['evento_id'])})
        
        assert evento is not None
        assert evento['otp_hash'].startswith('$2b$')
        assert evento['resuelto'] is False
        assert evento['intentos_fallidos'] == 0

    def test_con_ciclo_id(self, mock_conexion_global, usuario_en_db):
        """Debe aceptar ciclo_id opcional"""
        ciclo_id = str(ObjectId())
        resultado = generar_otp(str(usuario_en_db['_id']), ciclo_id)
        
        coleccion = mock_conexion_global.obtener_coleccion('eventos_otp')
        evento = coleccion.find_one({'_id': ObjectId(resultado['evento_id'])})
        assert evento['ciclo_id'] is not None

    def test_sin_ciclo_id(self, mock_conexion_global, usuario_en_db):
        """Debe funcionar sin ciclo_id"""
        resultado = generar_otp(str(usuario_en_db['_id']))
        assert 'evento_id' in resultado

    def test_usuario_id_no_string(self, mock_conexion_global):
        with pytest.raises(TypeError, match="usuario_id debe ser string"):
            generar_otp(123)

    def test_usuario_id_vacio(self, mock_conexion_global):
        with pytest.raises(ValueError, match="no puede estar vacío"):
            generar_otp("")

    def test_usuario_id_invalido(self, mock_conexion_global):
        with pytest.raises(ValueError, match="inválido"):
            generar_otp("no_es_objectid")

    def test_codigos_son_diferentes(self, mock_conexion_global, usuario_en_db):
        """Cada OTP debe ser diferente"""
        r1 = generar_otp(str(usuario_en_db['_id']))
        r2 = generar_otp(str(usuario_en_db['_id']))
        # Pueden coincidir por azar, pero hashes serán diferentes
        coleccion = mock_conexion_global.obtener_coleccion('eventos_otp')
        e1 = coleccion.find_one({'_id': ObjectId(r1['evento_id'])})
        e2 = coleccion.find_one({'_id': ObjectId(r2['evento_id'])})
        assert e1['otp_hash'] != e2['otp_hash']


class TestVerificarOtp:
    """Tests para verificar_otp"""

    def test_verificacion_correcta(self, mock_conexion_global, usuario_en_db):
        """OTP correcto debe retornar éxito"""
        uid = str(usuario_en_db['_id'])
        otp = generar_otp(uid)
        
        resultado = verificar_otp(uid, otp['codigo'])
        
        assert resultado['correcto'] is True
        assert resultado['expirado'] is False
        assert resultado['requiere_credenciales'] is False

    def test_verificacion_incorrecta(self, mock_conexion_global, usuario_en_db):
        """OTP incorrecto debe retornar fallo"""
        uid = str(usuario_en_db['_id'])
        generar_otp(uid)
        
        resultado = verificar_otp(uid, "000000")
        
        assert resultado['correcto'] is False
        assert resultado['intentos_restantes'] == 2
        assert resultado['requiere_credenciales'] is False

    def test_segundo_intento_fallido(self, mock_conexion_global, usuario_en_db):
        """Segundo fallo debe quedar 1 intento"""
        uid = str(usuario_en_db['_id'])
        generar_otp(uid)
        
        verificar_otp(uid, "000000")
        resultado = verificar_otp(uid, "111111")
        
        assert resultado['correcto'] is False
        assert resultado['intentos_restantes'] == 1

    def test_tercer_intento_fallido_anomalia(self, mock_conexion_global, usuario_en_db):
        """3er fallo debe generar anomalía"""
        uid = str(usuario_en_db['_id'])
        generar_otp(uid)
        
        verificar_otp(uid, "000000")
        verificar_otp(uid, "111111")
        resultado = verificar_otp(uid, "222222")
        
        assert resultado['correcto'] is False
        assert resultado['requiere_credenciales'] is True
        assert resultado['anomalia'] is not None
        assert resultado['anomalia']['tipo'] == 'tercer_intento_otp'

    def test_otp_expirado(self, mock_conexion_global, usuario_en_db):
        """OTP expirado debe generar anomalía"""
        uid = str(usuario_en_db['_id'])
        oid = usuario_en_db['_id']
        otp = generar_otp(uid)
        
        # Simular expiración
        coleccion = mock_conexion_global.obtener_coleccion('eventos_otp')
        coleccion.update_one(
            {'_id': ObjectId(otp['evento_id'])},
            {'$set': {'timestamp_expira': datetime.now(timezone.utc) - timedelta(minutes=1)}}
        )
        
        resultado = verificar_otp(uid, otp['codigo'])
        
        assert resultado['correcto'] is False
        assert resultado['expirado'] is True
        assert resultado['requiere_credenciales'] is True
        assert resultado['anomalia'] is not None
        assert resultado['anomalia']['tipo'] == 'otp_expirado'

    def test_sin_otp_activo(self, mock_conexion_global, usuario_en_db):
        """Sin OTP activo debe retornar requiere_credenciales"""
        resultado = verificar_otp(str(usuario_en_db['_id']), "123456")
        
        assert resultado['correcto'] is False
        assert resultado['requiere_credenciales'] is True

    def test_otp_correcto_marca_resuelto(self, mock_conexion_global, usuario_en_db):
        """OTP correcto debe marcar resuelto=True en BD"""
        uid = str(usuario_en_db['_id'])
        otp = generar_otp(uid)
        verificar_otp(uid, otp['codigo'])
        
        coleccion = mock_conexion_global.obtener_coleccion('eventos_otp')
        evento = coleccion.find_one({'_id': ObjectId(otp['evento_id'])})
        assert evento['resuelto'] is True

    def test_usuario_id_no_string(self, mock_conexion_global):
        with pytest.raises(TypeError, match="usuario_id debe ser string"):
            verificar_otp(123, "123456")

    def test_codigo_no_string(self, mock_conexion_global, usuario_en_db):
        with pytest.raises(TypeError, match="codigo_introducido debe ser string"):
            verificar_otp(str(usuario_en_db['_id']), 123456)

    def test_usuario_id_vacio(self, mock_conexion_global):
        with pytest.raises(ValueError, match="no puede estar vacío"):
            verificar_otp("", "123456")

    def test_usuario_id_invalido(self, mock_conexion_global):
        with pytest.raises(ValueError, match="inválido"):
            verificar_otp("no_es_id", "123456")


class TestObtenerEstadoOtp:
    """Tests para obtener_estado_otp"""

    def test_con_otp_activo(self, mock_conexion_global, usuario_en_db):
        """Con OTP activo debe retornar estado"""
        uid = str(usuario_en_db['_id'])
        generar_otp(uid)
        
        estado = obtener_estado_otp(uid)
        
        assert estado['tiene_otp_activo'] is True
        assert estado['expira_en_seg'] > 0
        assert estado['intentos_usados'] == 0
        assert estado['intentos_restantes'] == 3

    def test_sin_otp_activo(self, mock_conexion_global, usuario_en_db):
        """Sin OTP debe retornar inactivo"""
        estado = obtener_estado_otp(str(usuario_en_db['_id']))
        
        assert estado['tiene_otp_activo'] is False
        assert estado['expira_en_seg'] == 0
        assert estado['intentos_restantes'] == 3

    def test_con_intentos_usados(self, mock_conexion_global, usuario_en_db):
        """Debe reflejar intentos usados"""
        uid = str(usuario_en_db['_id'])
        generar_otp(uid)
        verificar_otp(uid, "000000")
        
        estado = obtener_estado_otp(uid)
        assert estado['intentos_usados'] == 1
        assert estado['intentos_restantes'] == 2

    def test_usuario_id_no_string(self, mock_conexion_global):
        with pytest.raises(TypeError, match="usuario_id debe ser string"):
            obtener_estado_otp(123)

    def test_usuario_id_vacio(self, mock_conexion_global):
        with pytest.raises(ValueError, match="no puede estar vacío"):
            obtener_estado_otp("")

    def test_usuario_id_invalido(self, mock_conexion_global):
        with pytest.raises(ValueError, match="inválido"):
            obtener_estado_otp("no_es_id")


class TestCancelarOtp:
    """Tests para cancelar_otp"""

    def test_cancelacion_exitosa(self, mock_conexion_global, usuario_en_db):
        """Debe cancelar OTP activo"""
        uid = str(usuario_en_db['_id'])
        generar_otp(uid)
        
        assert cancelar_otp(uid) is True

    def test_sin_otp_retorna_false(self, mock_conexion_global, usuario_en_db):
        """Sin OTP debe retornar False"""
        assert cancelar_otp(str(usuario_en_db['_id'])) is False

    def test_cancelado_no_es_verificable(self, mock_conexion_global, usuario_en_db):
        """OTP cancelado no debe ser verificable"""
        uid = str(usuario_en_db['_id'])
        otp = generar_otp(uid)
        cancelar_otp(uid)
        
        resultado = verificar_otp(uid, otp['codigo'])
        assert resultado['correcto'] is False

    def test_usuario_id_no_string(self, mock_conexion_global):
        with pytest.raises(TypeError, match="usuario_id debe ser string"):
            cancelar_otp(123)

    def test_usuario_id_vacio(self, mock_conexion_global):
        with pytest.raises(ValueError, match="no puede estar vacío"):
            cancelar_otp("")
