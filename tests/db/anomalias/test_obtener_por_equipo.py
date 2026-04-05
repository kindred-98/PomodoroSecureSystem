"""
Tests para src.db.anomalias.obtener_por_equipo
"""

import pytest
from datetime import datetime, timezone
from unittest.mock import patch
from bson import ObjectId

from src.db.anomalias.obtener_por_equipo import obtener_por_equipo


class TestObtenerPorEquipo:
    """Tests para la función obtener_por_equipo"""

    def test_obtiene_anomalias_del_equipo(self, mock_conexion_global):
        """Verifica que obtenga las anomalías de los miembros del equipo"""
        coleccion_equipos = mock_conexion_global.obtener_coleccion('equipos')
        coleccion_anomalias = mock_conexion_global.obtener_coleccion('anomalias')
        
        equipo_id = ObjectId()
        miembro1 = ObjectId()
        miembro2 = ObjectId()
        
        coleccion_equipos.insert_one({
            '_id': equipo_id,
            'nombre': 'Equipo Test',
            'miembros': [miembro1, miembro2],
        })
        
        coleccion_anomalias.insert_many([
            {'usuario_id': miembro1, 'tipo': 'tercera_pausa'},
            {'usuario_id': miembro2, 'tipo': 'exceso_descanso'},
        ])
        
        with patch('src.db.anomalias.obtener_por_equipo.conexion_global', mock_conexion_global):
            resultado = obtener_por_equipo(str(equipo_id))
        
        assert len(resultado) == 2

    def test_retorna_lista_vacia_si_sin_miembros(self, mock_conexion_global):
        """Verifica que retorne lista vacía si el equipo no tiene miembros"""
        coleccion_equipos = mock_conexion_global.obtener_coleccion('equipos')
        
        equipo_id = ObjectId()
        coleccion_equipos.insert_one({
            '_id': equipo_id,
            'nombre': 'Equipo Vacío',
            'miembros': [],
        })
        
        with patch('src.db.anomalias.obtener_por_equipo.conexion_global', mock_conexion_global):
            resultado = obtener_por_equipo(str(equipo_id))
        
        assert resultado == []

    def test_retorna_lista_vacia_si_sin_anomalias(self, mock_conexion_global):
        """Verifica que retorne lista vacía si no hay anomalías"""
        coleccion_equipos = mock_conexion_global.obtener_coleccion('equipos')
        
        equipo_id = ObjectId()
        miembro_id = ObjectId()
        coleccion_equipos.insert_one({
            '_id': equipo_id,
            'nombre': 'Equipo Limpio',
            'miembros': [miembro_id],
        })
        
        with patch('src.db.anomalias.obtener_por_equipo.conexion_global', mock_conexion_global):
            resultado = obtener_por_equipo(str(equipo_id))
        
        assert resultado == []

    def test_equipo_no_existe_lanza_exception(self, mock_conexion_global):
        """Verifica que lance excepción si el equipo no existe"""
        with pytest.raises(Exception) as exc_info:
            with patch('src.db.anomalias.obtener_por_equipo.conexion_global', mock_conexion_global):
                obtener_por_equipo(str(ObjectId()))
        
        assert "no existe" in str(exc_info.value)

    def test_equipo_id_no_string_lanza_typeerror(self, mock_conexion_global):
        """Verifica que se rechace equipo_id no string"""
        with pytest.raises(TypeError):
            obtener_por_equipo(123)

    def test_equipo_id_vacio_lanza_valueerror(self, mock_conexion_global):
        """Verifica que se rechace equipo_id vacío"""
        with pytest.raises(ValueError):
            obtener_por_equipo("")

    def test_equipo_id_invalido_lanza_valueerror(self, mock_conexion_global):
        """Verifica que se rechace equipo_id inválido"""
        with pytest.raises(ValueError):
            obtener_por_equipo("id-invalido")

    def test_limite_default(self, mock_conexion_global):
        """Verifica el límite por defecto (100)"""
        coleccion_equipos = mock_conexion_global.obtener_coleccion('equipos')
        coleccion_anomalias = mock_conexion_global.obtener_coleccion('anomalias')
        
        equipo_id = ObjectId()
        miembro_id = ObjectId()
        coleccion_equipos.insert_one({
            '_id': equipo_id,
            'nombre': 'Equipo Test',
            'miembros': [miembro_id],
        })
        
        for i in range(120):
            coleccion_anomalias.insert_one({'usuario_id': miembro_id, 'tipo': f'test_{i}'})
        
        with patch('src.db.anomalias.obtener_por_equipo.conexion_global', mock_conexion_global):
            resultado = obtener_por_equipo(str(equipo_id))
        
        assert len(resultado) == 100

    def test_limite_personalizado(self, mock_conexion_global):
        """Verifica que respete el límite personalizado"""
        coleccion_equipos = mock_conexion_global.obtener_coleccion('equipos')
        coleccion_anomalias = mock_conexion_global.obtener_coleccion('anomalias')
        
        equipo_id = ObjectId()
        miembro_id = ObjectId()
        coleccion_equipos.insert_one({
            '_id': equipo_id,
            'nombre': 'Equipo Test',
            'miembros': [miembro_id],
        })
        
        for i in range(20):
            coleccion_anomalias.insert_one({'usuario_id': miembro_id, 'tipo': f'test_{i}'})
        
        with patch('src.db.anomalias.obtener_por_equipo.conexion_global', mock_conexion_global):
            resultado = obtener_por_equipo(str(equipo_id), limite=5)
        
        assert len(resultado) == 5

    def test_solo_anomalias_del_equipo(self, mock_conexion_global):
        """Verifica que solo retorne anomalías de miembros del equipo"""
        coleccion_equipos = mock_conexion_global.obtener_coleccion('equipos')
        coleccion_anomalias = mock_conexion_global.obtener_coleccion('anomalias')
        
        equipo_id = ObjectId()
        miembro_equipo = ObjectId()
        miembro_externo = ObjectId()
        
        coleccion_equipos.insert_one({
            '_id': equipo_id,
            'nombre': 'Equipo Test',
            'miembros': [miembro_equipo],
        })
        
        coleccion_anomalias.insert_many([
            {'usuario_id': miembro_equipo, 'tipo': 'del_equipo'},
            {'usuario_id': miembro_externo, 'tipo': 'externo'},
        ])
        
        with patch('src.db.anomalias.obtener_por_equipo.conexion_global', mock_conexion_global):
            resultado = obtener_por_equipo(str(equipo_id))
        
        assert len(resultado) == 1
        assert resultado[0]['tipo'] == 'del_equipo'
