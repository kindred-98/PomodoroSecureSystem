"""
Tests para src.db.anomalias.obtener_por_usuario
"""

import pytest
from datetime import datetime, timezone
from unittest.mock import patch
from bson import ObjectId

from src.db.anomalias.obtener_por_usuario import obtener_por_usuario


class TestObtenerPorUsuario:
    """Tests para la función obtener_por_usuario"""

    def test_obtiene_anomalias_del_usuario(self, mock_conexion_global):
        """Verifica que obtenga las anomalías del usuario"""
        coleccion_usuarios = mock_conexion_global.obtener_coleccion('usuarios')
        coleccion_anomalias = mock_conexion_global.obtener_coleccion('anomalias')
        
        usuario_id = ObjectId()
        coleccion_usuarios.insert_one({'_id': usuario_id, 'nombre': 'Test User'})
        
        coleccion_anomalias.insert_many([
            {'usuario_id': usuario_id, 'tipo': 'tercera_pausa', 'detalle': 'Pausa 3'},
            {'usuario_id': usuario_id, 'tipo': 'exceso_descanso', 'detalle': 'Descanso largo'},
        ])
        
        with patch('src.db.anomalias.obtener_por_usuario.conexion_global', mock_conexion_global):
            resultado = obtener_por_usuario(str(usuario_id))
        
        assert len(resultado) == 2

    def test_retorna_lista_vacia_si_sin_anomalias(self, mock_conexion_global):
        """Verifica que retorne lista vacía si no hay anomalías"""
        coleccion_usuarios = mock_conexion_global.obtener_coleccion('usuarios')
        
        usuario_id = ObjectId()
        coleccion_usuarios.insert_one({'_id': usuario_id, 'nombre': 'Usuario Limpio'})
        
        with patch('src.db.anomalias.obtener_por_usuario.conexion_global', mock_conexion_global):
            resultado = obtener_por_usuario(str(usuario_id))
        
        assert resultado == []

    def test_usuario_no_existe_lanza_exception(self, mock_conexion_global):
        """Verifica que lance excepción si el usuario no existe"""
        with pytest.raises(Exception) as exc_info:
            with patch('src.db.anomalias.obtener_por_usuario.conexion_global', mock_conexion_global):
                obtener_por_usuario(str(ObjectId()))
        
        assert "no existe" in str(exc_info.value)

    def test_usuario_id_no_string_lanza_typeerror(self, mock_conexion_global):
        """Verifica que se rechace usuario_id no string"""
        with pytest.raises(TypeError):
            obtener_por_usuario(123)

    def test_usuario_id_vacio_lanza_valueerror(self, mock_conexion_global):
        """Verifica que se rechace usuario_id vacío"""
        with pytest.raises(ValueError):
            obtener_por_usuario("")

    def test_usuario_id_invalido_lanza_valueerror(self, mock_conexion_global):
        """Verifica que se rechace usuario_id inválido"""
        with pytest.raises(ValueError):
            obtener_por_usuario("id-invalido")

    def test_limite_default(self, mock_conexion_global):
        """Verifica el límite por defecto (50)"""
        coleccion_usuarios = mock_conexion_global.obtener_coleccion('usuarios')
        coleccion_anomalias = mock_conexion_global.obtener_coleccion('anomalias')
        
        usuario_id = ObjectId()
        coleccion_usuarios.insert_one({'_id': usuario_id})
        
        for i in range(60):
            coleccion_anomalias.insert_one({'usuario_id': usuario_id, 'tipo': f'test_{i}'})
        
        with patch('src.db.anomalias.obtener_por_usuario.conexion_global', mock_conexion_global):
            resultado = obtener_por_usuario(str(usuario_id))
        
        assert len(resultado) == 50

    def test_limite_personalizado(self, mock_conexion_global):
        """Verifica que respete el límite personalizado"""
        coleccion_usuarios = mock_conexion_global.obtener_coleccion('usuarios')
        coleccion_anomalias = mock_conexion_global.obtener_coleccion('anomalias')
        
        usuario_id = ObjectId()
        coleccion_usuarios.insert_one({'_id': usuario_id})
        
        for i in range(20):
            coleccion_anomalias.insert_one({'usuario_id': usuario_id, 'tipo': f'test_{i}'})
        
        with patch('src.db.anomalias.obtener_por_usuario.conexion_global', mock_conexion_global):
            resultado = obtener_por_usuario(str(usuario_id), limite=5)
        
        assert len(resultado) == 5

    def test_limite_no_int_lanza_typeerror(self, mock_conexion_global):
        """Verifica que se rechace límite no int"""
        coleccion_usuarios = mock_conexion_global.obtener_coleccion('usuarios')
        usuario_id = ObjectId()
        coleccion_usuarios.insert_one({'_id': usuario_id})
        
        with pytest.raises(TypeError):
            obtener_por_usuario(str(usuario_id), limite="10")

    def test_limite_menor_que_uno_lanza_valueerror(self, mock_conexion_global):
        """Verifica que se rechace límite < 1"""
        coleccion_usuarios = mock_conexion_global.obtener_coleccion('usuarios')
        usuario_id = ObjectId()
        coleccion_usuarios.insert_one({'_id': usuario_id})
        
        with pytest.raises(ValueError):
            obtener_por_usuario(str(usuario_id), limite=0)
