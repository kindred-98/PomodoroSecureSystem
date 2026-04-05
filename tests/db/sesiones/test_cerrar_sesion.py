"""
Tests para src.db.sesiones.cerrar_sesion
"""

import pytest
from unittest.mock import patch
from bson import ObjectId

from src.db.sesiones.cerrar_sesion import cerrar_sesion


class TestCerrarSesion:
    """Tests para la función cerrar_sesion"""

    def test_sesion_id_no_string_lanza_typeerror(self, mock_conexion_global):
        """Verifica que se rechace sesion_id no string"""
        with pytest.raises(TypeError):
            cerrar_sesion(123)

    def test_completada_no_bool_lanza_typeerror(self, mock_conexion_global):
        """Verifica que se rechace completada no bool"""
        with pytest.raises(TypeError):
            cerrar_sesion(str(ObjectId()), completada="si")

    def test_sesion_id_invalido_lanza_valueerror(self, mock_conexion_global):
        """Verifica que se rechace sesion_id inválido"""
        with pytest.raises(ValueError):
            cerrar_sesion("id-invalido")

    def test_sesion_no_existe_lanza_exception(self, mock_conexion_global):
        """Verifica que lance excepción si sesión no existe"""
        with pytest.raises(Exception) as exc_info:
            with patch('src.db.sesiones.cerrar_sesion.conexion_global', mock_conexion_global):
                cerrar_sesion(str(ObjectId()))
        
        assert "no existe" in str(exc_info.value)
