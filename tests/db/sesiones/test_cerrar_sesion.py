"""
Tests para src.db.sesiones.cerrar_sesion
"""

import pytest
from unittest.mock import patch
from bson import ObjectId

from src.db.sesiones.cerrar_sesion import cerrar_sesion
from src.excepciones import ErrorRecursoNoEncontrado


class TestCerrarSesion:
    """Tests para la función cerrar_sesion"""

    def test_sesion_id_no_string_lanza_typeerror(self, mock_conexion_global):
        """Verifica que se rechace sesion_id no string"""
        with pytest.raises(TypeError):
            cerrar_sesion(123)

    def test_completada_no_bool_lanza_typeerror(self, mock_conexion_global):
        """Verifica que se rechace completada no bool"""
        oid_texto = str(ObjectId())
        with pytest.raises(TypeError):
            cerrar_sesion(oid_texto, completada="si")

    def test_sesion_id_invalido_lanza_valueerror(self, mock_conexion_global):
        """Verifica que se rechace sesion_id inválido"""
        with pytest.raises(ValueError):
            cerrar_sesion("id-invalido")

    def test_sesion_no_existe_lanza_error(self, mock_conexion_global):
        """Verifica que lance error si la sesión no existe"""
        with patch('src.db.sesiones.cerrar_sesion.conexion_global', mock_conexion_global):
            oid_texto = str(ObjectId())
            with pytest.raises(ErrorRecursoNoEncontrado, match="no existe"):
                cerrar_sesion(oid_texto)
