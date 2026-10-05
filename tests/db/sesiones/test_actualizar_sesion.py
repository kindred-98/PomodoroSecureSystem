"""
Tests para src.db.sesiones.actualizar_sesion
"""

import pytest
from unittest.mock import patch
from bson import ObjectId

from src.db.sesiones.actualizar_sesion import actualizar_sesion
from src.excepciones import ErrorRecursoNoEncontrado


class TestActualizarSesion:
    """Tests para la función actualizar_sesion"""

    def test_actualiza_sesion_exitosamente(self, mock_conexion_global):
        """Verifica que se actualice una sesión"""
        coleccion = mock_conexion_global.obtener_coleccion('sesiones')
        sesion_id = ObjectId()
        coleccion.insert_one({
            '_id': sesion_id,
            'usuario_id': ObjectId(),
            'pausas_utilizadas': 0,
            'tiempo_trabajado': 0,
        })
        
        with patch('src.db.sesiones.actualizar_sesion.conexion_global', mock_conexion_global):
            resultado = actualizar_sesion(str(sesion_id), {'pausas_utilizadas': 2})
        
        assert resultado is not None
        assert resultado['pausas_utilizadas'] == 2

    def test_sesion_id_no_string_lanza_typeerror(self, mock_conexion_global):
        """Verifica que se rechace sesion_id no string"""
        with pytest.raises(TypeError):
            actualizar_sesion(123, {'pausas_utilizadas': 1})

    def test_actualizaciones_no_dict_lanza_typeerror(self, mock_conexion_global):
        """Verifica que se rechace actualizaciones no dict"""
        oid_texto = str(ObjectId())
        with pytest.raises(TypeError):
            actualizar_sesion(oid_texto, "no es dict")

    def test_sesion_id_invalido_lanza_valueerror(self, mock_conexion_global):
        """Verifica que se rechace sesion_id inválido"""
        with pytest.raises(ValueError):
            actualizar_sesion("id-invalido", {'pausas_utilizadas': 1})

    def test_sesion_no_existe_lanza_error(self, mock_conexion_global):
        """Verifica que lance error si la sesión no existe"""
        with patch('src.db.sesiones.actualizar_sesion.conexion_global', mock_conexion_global):
            oid_texto = str(ObjectId())
            with pytest.raises(ErrorRecursoNoEncontrado, match="no existe"):
                actualizar_sesion(oid_texto, {'pausas_utilizadas': 1})

    def test_multiple_campos_actualizados(self, mock_conexion_global):
        """Verifica que se actualicen múltiples campos"""
        coleccion = mock_conexion_global.obtener_coleccion('sesiones')
        sesion_id = ObjectId()
        coleccion.insert_one({
            '_id': sesion_id,
            'usuario_id': ObjectId(),
            'campo1': 'original',
            'campo2': 0,
        })
        
        with patch('src.db.sesiones.actualizar_sesion.conexion_global', mock_conexion_global):
            resultado = actualizar_sesion(str(sesion_id), {
                'campo1': 'modificado',
                'campo2': 100,
            })
        
        assert resultado['campo1'] == 'modificado'
        assert resultado['campo2'] == 100
