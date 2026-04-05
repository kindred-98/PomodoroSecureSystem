"""
Tests para src.db.sesiones.obtener_historial
"""

import pytest
from datetime import datetime, timezone, timedelta
from unittest.mock import patch
from bson import ObjectId

from src.db.sesiones.obtener_historial import obtener_historial


class TestObtenerHistorial:
    """Tests para la función obtener_historial"""

    def test_obtiene_historial_exitosamente(self, mock_conexion_global):
        """Verifica que obtenga el historial"""
        coleccion = mock_conexion_global.obtener_coleccion('sesiones')
        usuario_id = ObjectId()
        
        coleccion.insert_many([
            {'usuario_id': usuario_id, 'tipo_sesion': 'pomodoro', 'inicio': datetime.now(timezone.utc)},
            {'usuario_id': usuario_id, 'tipo_sesion': 'pomodoro', 'inicio': datetime.now(timezone.utc)},
        ])
        
        with patch('src.db.sesiones.obtener_historial.conexion_global', mock_conexion_global):
            resultado = obtener_historial(str(usuario_id))
        
        assert len(resultado) == 2

    def test_retorna_lista_vacia_si_sin_sesiones(self, mock_conexion_global):
        """Verifica que retorne lista vacía si no hay sesiones"""
        with patch('src.db.sesiones.obtener_historial.conexion_global', mock_conexion_global):
            resultado = obtener_historial(str(ObjectId()))
        
        assert resultado == []

    def test_ordena_por_mas_recientes(self, mock_conexion_global):
        """Verifica que ordene por más recientes"""
        coleccion = mock_conexion_global.obtener_coleccion('sesiones')
        usuario_id = ObjectId()
        ahora = datetime.now(timezone.utc)
        
        coleccion.insert_many([
            {'usuario_id': usuario_id, 'inicio': ahora - timedelta(days=2)},
            {'usuario_id': usuario_id, 'inicio': ahora - timedelta(days=1)},
            {'usuario_id': usuario_id, 'inicio': ahora},
        ])
        
        with patch('src.db.sesiones.obtener_historial.conexion_global', mock_conexion_global):
            resultado = obtener_historial(str(usuario_id))
        
        assert len(resultado) == 3
        assert resultado[0]['inicio'] >= resultado[1]['inicio']

    def test_solo_retorna_del_usuario(self, mock_conexion_global):
        """Verifica que solo retorne sesiones del usuario"""
        coleccion = mock_conexion_global.obtener_coleccion('sesiones')
        usuario_id = ObjectId()
        otro_usuario = ObjectId()
        
        coleccion.insert_many([
            {'usuario_id': usuario_id, 'tipo': 'mia'},
            {'usuario_id': otro_usuario, 'tipo': 'ajena'},
        ])
        
        with patch('src.db.sesiones.obtener_historial.conexion_global', mock_conexion_global):
            resultado = obtener_historial(str(usuario_id))
        
        assert len(resultado) == 1
        assert resultado[0]['tipo'] == 'mia'

    def test_usuario_id_no_string_lanza_typeerror(self, mock_conexion_global):
        """Verifica que se rechace usuario_id no string"""
        with pytest.raises(TypeError):
            obtener_historial(123)

    def test_usuario_id_invalido_lanza_valueerror(self, mock_conexion_global):
        """Verifica que se rechace usuario_id inválido"""
        with pytest.raises(ValueError):
            obtener_historial("id-invalido")

    def test_limite_no_int_lanza_typeerror(self, mock_conexion_global):
        """Verifica que se rechace límite no int"""
        with pytest.raises(TypeError):
            obtener_historial(str(ObjectId()), limite="10")

    def test_limite_cero_lanza_valueerror(self, mock_conexion_global):
        """Verifica que se rechace límite 0"""
        with pytest.raises(ValueError):
            obtener_historial(str(ObjectId()), limite=0)

    def test_limite_negativo_lanza_valueerror(self, mock_conexion_global):
        """Verifica que se rechace límite negativo"""
        with pytest.raises(ValueError):
            obtener_historial(str(ObjectId()), limite=-5)

    def test_limite_default(self, mock_conexion_global):
        """Verifica el límite por defecto (50)"""
        coleccion = mock_conexion_global.obtener_coleccion('sesiones')
        usuario_id = ObjectId()
        
        for i in range(60):
            coleccion.insert_one({'usuario_id': usuario_id, 'tipo': f'sesion_{i}'})
        
        with patch('src.db.sesiones.obtener_historial.conexion_global', mock_conexion_global):
            resultado = obtener_historial(str(usuario_id))
        
        assert len(resultado) == 50

    def test_limite_personalizado(self, mock_conexion_global):
        """Verifica que respete el límite personalizado"""
        coleccion = mock_conexion_global.obtener_coleccion('sesiones')
        usuario_id = ObjectId()
        
        for i in range(20):
            coleccion.insert_one({'usuario_id': usuario_id, 'tipo': f'sesion_{i}'})
        
        with patch('src.db.sesiones.obtener_historial.conexion_global', mock_conexion_global):
            resultado = obtener_historial(str(usuario_id), limite=10)
        
        assert len(resultado) == 10
