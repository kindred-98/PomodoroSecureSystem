"""
Tests para src.db.equipos.buscar_por_id
"""

import pytest
from unittest.mock import patch
from bson import ObjectId

from src.db.equipos.buscar_por_id import buscar_por_id


class TestBuscarEquipoPorId:
    """Tests para la función buscar_por_id"""

    def test_encuentra_equipo_existente(self, mock_conexion_global):
        """Verifica que encuentre un equipo existente"""
        coleccion = mock_conexion_global.obtener_coleccion('equipos')
        equipo_id = ObjectId()
        coleccion.insert_one({
            '_id': equipo_id,
            'nombre': 'Equipo Test',
            'descripcion': 'Un equipo de prueba',
        })
        
        with patch('src.db.equipos.buscar_por_id.conexion_global', mock_conexion_global):
            resultado = buscar_por_id(str(equipo_id))
        
        assert resultado is not None
        assert resultado['nombre'] == 'Equipo Test'

    def test_retorna_none_si_no_existe(self, mock_conexion_global):
        """Verifica que retorne None si el equipo no existe"""
        with patch('src.db.equipos.buscar_por_id.conexion_global', mock_conexion_global):
            resultado = buscar_por_id(str(ObjectId()))
        
        assert resultado is None

    def test_equipo_id_no_string_lanza_typeerror(self, mock_conexion_global):
        """Verifica que se rechace equipo_id no string"""
        with pytest.raises(TypeError):
            buscar_por_id(123)

    def test_equipo_id_invalido_lanza_valueerror(self, mock_conexion_global):
        """Verifica que se rechace equipo_id inválido"""
        with pytest.raises(ValueError):
            buscar_por_id("id-invalido")

    def test_retorna_todos_los_campos(self, mock_conexion_global):
        """Verifica que retorne todos los campos del equipo"""
        coleccion = mock_conexion_global.obtener_coleccion('equipos')
        equipo_id = ObjectId()
        coleccion.insert_one({
            '_id': equipo_id,
            'nombre': 'Equipo Completo',
            'descripcion': 'Descripción completa',
            'encargado_id': ObjectId(),
            'miembros': [ObjectId()],
            'activo': True,
        })
        
        with patch('src.db.equipos.buscar_por_id.conexion_global', mock_conexion_global):
            resultado = buscar_por_id(str(equipo_id))
        
        assert 'nombre' in resultado
        assert 'descripcion' in resultado
        assert 'encargado_id' in resultado
        assert 'miembros' in resultado
