"""
Tests para src.db.equipos.obtener_miembros
"""

import pytest
from unittest.mock import patch
from bson import ObjectId

from src.db.equipos.obtener_miembros import obtener_miembros


class TestObtenerMiembros:
    """Tests para la función obtener_miembros"""

    def test_obtiene_miembros_exitosamente(self, mock_conexion_global):
        """Verifica que obtenga los miembros de un equipo"""
        coleccion_equipos = mock_conexion_global.obtener_coleccion('equipos')
        coleccion_usuarios = mock_conexion_global.obtener_coleccion('usuarios')
        
        equipo_id = ObjectId()
        miembro1 = ObjectId()
        miembro2 = ObjectId()
        
        coleccion_equipos.insert_one({
            '_id': equipo_id,
            'nombre': 'Equipo Test',
            'miembros': [miembro1, miembro2],
        })
        
        coleccion_usuarios.insert_many([
            {'_id': miembro1, 'nombre': 'Miembro 1', 'email': 'm1@test.com'},
            {'_id': miembro2, 'nombre': 'Miembro 2', 'email': 'm2@test.com'},
        ])
        
        with patch('src.db.equipos.obtener_miembros.conexion_global', mock_conexion_global):
            resultado = obtener_miembros(str(equipo_id))
        
        assert len(resultado) == 2

    def test_equipo_sin_miembros(self, mock_conexion_global):
        """Verifica que retorne lista vacía si no hay miembros"""
        coleccion_equipos = mock_conexion_global.obtener_coleccion('equipos')
        coleccion_usuarios = mock_conexion_global.obtener_coleccion('usuarios')
        
        equipo_id = ObjectId()
        coleccion_equipos.insert_one({
            '_id': equipo_id,
            'nombre': 'Equipo Vacío',
            'miembros': [],
        })
        
        with patch('src.db.equipos.obtener_miembros.conexion_global', mock_conexion_global):
            resultado = obtener_miembros(str(equipo_id))
        
        assert resultado == []

    def test_equipo_no_existe_lanza_exception(self, mock_conexion_global):
        """Verifica que lance excepción si el equipo no existe"""
        with pytest.raises(Exception) as exc_info:
            with patch('src.db.equipos.obtener_miembros.conexion_global', mock_conexion_global):
                obtener_miembros(str(ObjectId()))
        
        assert "no existe" in str(exc_info.value)

    def test_equipo_id_no_string_lanza_typeerror(self, mock_conexion_global):
        """Verifica que se rechace equipo_id no string"""
        with pytest.raises(TypeError):
            obtener_miembros(123)

    def test_equipo_id_invalido_lanza_valueerror(self, mock_conexion_global):
        """Verifica que se rechace equipo_id inválido"""
        with pytest.raises(ValueError):
            obtener_miembros("id-invalido")

    def test_un_solo_miembro(self, mock_conexion_global):
        """Verifica que funcione con un solo miembro"""
        coleccion_equipos = mock_conexion_global.obtener_coleccion('equipos')
        coleccion_usuarios = mock_conexion_global.obtener_coleccion('usuarios')
        
        equipo_id = ObjectId()
        miembro_id = ObjectId()
        
        coleccion_equipos.insert_one({
            '_id': equipo_id,
            'nombre': 'Equipo Unipersonal',
            'miembros': [miembro_id],
        })
        
        coleccion_usuarios.insert_one({
            '_id': miembro_id,
            'nombre': 'Solo Uno',
            'email': 'solo@test.com',
        })
        
        with patch('src.db.equipos.obtener_miembros.conexion_global', mock_conexion_global):
            resultado = obtener_miembros(str(equipo_id))
        
        assert len(resultado) == 1
