"""
Tests para src.db.anomalias.marcar_revisada
"""

import pytest
from datetime import datetime, timezone
from unittest.mock import patch
from bson import ObjectId

from src.db.anomalias.marcar_revisada import marcar_revisada


class TestMarcarRevisada:
    """Tests para la función marcar_revisada"""

    def test_marca_como_revisada(self, mock_conexion_global):
        """Verifica que marque la anomalía como revisada"""
        coleccion = mock_conexion_global.obtener_coleccion('anomalias')
        anomalia_id = ObjectId()
        coleccion.insert_one({
            '_id': anomalia_id,
            'usuario_id': ObjectId(),
            'tipo': 'tercera_pausa',
            'revisada': False,
        })
        
        with patch('src.db.anomalias.marcar_revisada.conexion_global', mock_conexion_global):
            resultado = marcar_revisada(str(anomalia_id))
        
        assert resultado['revisada'] is True
        assert 'fecha_revision' in resultado

    def test_retorna_anomalia_actualizada(self, mock_conexion_global):
        """Verifica que retorne la anomalía actualizada"""
        coleccion = mock_conexion_global.obtener_coleccion('anomalias')
        anomalia_id = ObjectId()
        coleccion.insert_one({
            '_id': anomalia_id,
            'usuario_id': ObjectId(),
            'tipo': 'exceso_descanso',
            'revisada': False,
        })
        
        with patch('src.db.anomalias.marcar_revisada.conexion_global', mock_conexion_global):
            resultado = marcar_revisada(str(anomalia_id))
        
        assert resultado['_id'] == anomalia_id
        assert resultado['tipo'] == 'exceso_descanso'

    def test_anomalia_no_existe_lanza_exception(self, mock_conexion_global):
        """Verifica que lance excepción si la anomalía no existe"""
        with pytest.raises(Exception) as exc_info:
            with patch('src.db.anomalias.marcar_revisada.conexion_global', mock_conexion_global):
                marcar_revisada(str(ObjectId()))
        
        assert "no existe" in str(exc_info.value)

    def test_anomalia_id_no_string_lanza_typeerror(self, mock_conexion_global):
        """Verifica que se rechace anomalia_id no string"""
        with pytest.raises(TypeError):
            marcar_revisada(123)

    def test_anomalia_id_vacio_lanza_valueerror(self, mock_conexion_global):
        """Verifica que se rechace anomalia_id vacío"""
        with pytest.raises(ValueError):
            marcar_revisada("")

    def test_anomalia_id_solo_espacios_lanza_valueerror(self, mock_conexion_global):
        """Verifica que se rechace anomalia_id con solo espacios"""
        with pytest.raises(ValueError):
            marcar_revisada("   ")

    def test_anomalia_id_invalido_lanza_valueerror(self, mock_conexion_global):
        """Verifica que se rechace anomalia_id inválido"""
        with pytest.raises(ValueError):
            marcar_revisada("id-invalido")

    def test_ya_revisada_se_puede_volver_a_marcar(self, mock_conexion_global):
        """Verifica que se pueda marcar una ya revisada"""
        coleccion = mock_conexion_global.obtener_coleccion('anomalias')
        anomalia_id = ObjectId()
        coleccion.insert_one({
            '_id': anomalia_id,
            'usuario_id': ObjectId(),
            'tipo': 'tercera_pausa',
            'revisada': True,
            'fecha_revision': datetime.now(timezone.utc),
        })
        
        with patch('src.db.anomalias.marcar_revisada.conexion_global', mock_conexion_global):
            resultado = marcar_revisada(str(anomalia_id))
        
        assert resultado['revisada'] is True
