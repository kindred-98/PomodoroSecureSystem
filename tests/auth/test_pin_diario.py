"""
Tests para src.auth.pin_diario
Módulo: Generar y verificar PIN diario de 6 dígitos
"""

import pytest
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch
from bson import ObjectId

from src.auth.pin_diario import generar_pin_diario, verificar_pin_diario
from src.seguridad.encriptacion import hashear_contraseña


class TestGenerarPinDiario:
    """Tests para la función generar_pin_diario"""

    def test_genera_pin_se_guarda_en_bd(self, mock_conexion_global):
        """Verifica que el PIN se genere y guarde correctamente"""
        usuario_id = str(ObjectId())
        
        with patch('src.auth.pin_diario.conexion_global', mock_conexion_global):
            generar_pin_diario(usuario_id)
        
        coleccion = mock_conexion_global.obtener_coleccion('pines_diarios')
        registro = coleccion.find_one({'usuario_id': ObjectId(usuario_id)})
        
        assert registro is not None
        assert 'pin_hash' in registro
        assert 'fecha' in registro
        assert 'intentos_fallidos' in registro

    def test_usuario_id_no_string_lanza_error(self, mock_conexion_global):
        """Verifica que se rechace usuario_id no string"""
        with pytest.raises(Exception):
            generar_pin_diario(123)

    def test_usuario_id_vacio_lanza_error(self, mock_conexion_global):
        """Verifica que se rechace usuario_id vacío"""
        with pytest.raises(Exception):
            generar_pin_diario("")


class TestVerificarPinDiario:
    """Tests para la función verificar_pin_diario"""

    def test_sin_pin_para_hoy_retorna_false(self, mock_conexion_global):
        """Verifica que retorne False si no hay PIN para hoy"""
        usuario_id = str(ObjectId())
        
        with patch('src.auth.pin_diario.conexion_global', mock_conexion_global):
            resultado = verificar_pin_diario(usuario_id, "123456")
        
        assert resultado is False

    def test_usuario_id_no_string_lanza_error(self, mock_conexion_global):
        """Verifica que se rechace usuario_id no string"""
        with pytest.raises(Exception):
            verificar_pin_diario(123, "123456")

    def test_usuario_id_vacio_retorna_false(self, mock_conexion_global):
        """Verifica que se rechace usuario_id vacío"""
        with patch('src.auth.pin_diario.conexion_global', mock_conexion_global):
            resultado = verificar_pin_diario("", "123456")
        assert resultado is False

    def test_pin_no_string_lanza_error(self, mock_conexion_global):
        """Verifica que se rechace PIN no string"""
        usuario_id = str(ObjectId())
        with pytest.raises(Exception):
            verificar_pin_diario(usuario_id, 123456)

    def test_pin_vacio_retorna_false(self, mock_conexion_global):
        """Verifica que se rechace PIN vacío"""
        usuario_id = str(ObjectId())
        with patch('src.auth.pin_diario.conexion_global', mock_conexion_global):
            resultado = verificar_pin_diario(usuario_id, "")
        assert resultado is False
