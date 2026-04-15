"""Tests para estado_conexion.py"""

import pytest
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch
from bson import ObjectId


@pytest.fixture
def mock_conexion_global():
    """Mock de conexión a MongoDB."""
    mock_db = MagicMock()
    return mock_db


@pytest.fixture
def usuario_en_db():
    """Usuario de prueba."""
    return {'_id': ObjectId(), 'nombre': 'Test User', 'email': 'test@test.com', 'rol': 'empleado', 'activo': True}


class TestObtenerEstadoTodosLosUsuarios:
    """Tests para obtener_estado_todos_los_usuarios()."""

    def test_retorna_lista_vacia_si_no_hay_usuarios(self, mock_conexion_global):
        """Retorna lista vacía si no hay usuarios."""
        mock_ciclos = MagicMock()
        mock_ciclos.find.return_value = []
        
        mock_usuarios = MagicMock()
        mock_usuarios.find.return_value = []
        
        mock_conexion_global.obtener_coleccion.side_effect = [mock_ciclos, mock_usuarios]
        
        with patch('src.db.usuarios.estado_conexion.conexion_global', mock_conexion_global):
            from src.db.usuarios.estado_conexion import obtener_estado_todos_los_usuarios
            resultado = obtener_estado_todos_los_usuarios()
            assert resultado == []

    def test_retorna_usuarios_inactivos(self, mock_conexion_global, usuario_en_db):
        """Retorna usuarios inactivos correctamente."""
        mock_ciclos = MagicMock()
        mock_ciclos.find.return_value = []
        
        mock_usuarios = MagicMock()
        mock_usuarios.find.return_value = [usuario_en_db]
        
        mock_conexion_global.obtener_coleccion.side_effect = [mock_ciclos, mock_usuarios]
        
        with patch('src.db.usuarios.estado_conexion.conexion_global', mock_conexion_global):
            from src.db.usuarios.estado_conexion import obtener_estado_todos_los_usuarios
            resultado = obtener_estado_todos_los_usuarios()
            assert len(resultado) == 1
            assert resultado[0]['conectado'] is False

    def test_retorna_usuarios_conectados(self, mock_conexion_global, usuario_en_db):
        """Retorna usuarios conectados cuando tienen ciclo activo."""
        ciclo = {'usuario_id': usuario_en_db['_id'], 'completado': False}
        
        mock_ciclos = MagicMock()
        mock_ciclos.find.return_value = [ciclo]
        
        mock_usuarios = MagicMock()
        mock_usuarios.find.return_value = [usuario_en_db]
        
        mock_conexion_global.obtener_coleccion.side_effect = [mock_ciclos, mock_usuarios]
        
        with patch('src.db.usuarios.estado_conexion.conexion_global', mock_conexion_global):
            from src.db.usuarios.estado_conexion import obtener_estado_todos_los_usuarios
            resultado = obtener_estado_todos_los_usuarios()
            assert len(resultado) == 1
            assert resultado[0]['conectado'] is True

    def test_retorna_campos_completos(self, mock_conexion_global, usuario_en_db):
        """Retorna todos los campos necesarios."""
        mock_ciclos = MagicMock()
        mock_ciclos.find.return_value = []
        
        mock_usuarios = MagicMock()
        mock_usuarios.find.return_value = [usuario_en_db]
        
        mock_conexion_global.obtener_coleccion.side_effect = [mock_ciclos, mock_usuarios]
        
        with patch('src.db.usuarios.estado_conexion.conexion_global', mock_conexion_global):
            from src.db.usuarios.estado_conexion import obtener_estado_todos_los_usuarios
            resultado = obtener_estado_todos_los_usuarios()
            assert 'usuario_id' in resultado[0]
            assert 'nombre' in resultado[0]
            assert 'email' in resultado[0]
            assert 'rol' in resultado[0]
            assert 'conectado' in resultado[0]
            assert 'ultima_conexion' in resultado[0]


class TestEstaConectado:
    """Tests para esta_conectado()."""

    def test_retorna_true_si_tiene_ciclo_activo(self, mock_conexion_global):
        """Retorna True si tiene ciclo activo."""
        mock_coleccion = MagicMock()
        mock_coleccion.find_one.return_value = {'_id': ObjectId()}
        
        mock_conexion_global.obtener_coleccion.return_value = mock_coleccion
        
        with patch('src.db.usuarios.estado_conexion.conexion_global', mock_conexion_global):
            from src.db.usuarios.estado_conexion import esta_conectado
            resultado = esta_conectado(str(ObjectId()))
            assert resultado is True

    def test_retorna_false_si_no_tiene_ciclo(self, mock_conexion_global):
        """Retorna False si no tiene ciclo."""
        mock_coleccion = MagicMock()
        mock_coleccion.find_one.return_value = None
        
        mock_conexion_global.obtener_coleccion.return_value = mock_coleccion
        
        with patch('src.db.usuarios.estado_conexion.conexion_global', mock_conexion_global):
            from src.db.usuarios.estado_conexion import esta_conectado
            resultado = esta_conectado(str(ObjectId()))
            assert resultado is False

    def test_retorna_false_con_id_invalido(self, mock_conexion_global):
        """Retorna False con ID inválido."""
        with patch('src.db.usuarios.estado_conexion.conexion_global', mock_conexion_global):
            from src.db.usuarios.estado_conexion import esta_conectado
            resultado = esta_conectado("invalid_id")
            assert resultado is False

    def test_retorna_false_con_excepcion(self, mock_conexion_global):
        """Retorna False si hay excepción."""
        mock_conexion_global.obtener_coleccion.side_effect = Exception("Error")
        
        with patch('src.db.usuarios.estado_conexion.conexion_global', mock_conexion_global):
            from src.db.usuarios.estado_conexion import esta_conectado
            resultado = esta_conectado(str(ObjectId()))
            assert resultado is False


class TestObtenerTiempoDesconectado:
    """Tests para obtener_tiempo_desconectado()."""

    def test_retorna_trabajando_si_ciclo_activo(self, mock_conexion_global):
        """Retorna Trabajando si está en ciclo."""
        mock_coleccion = MagicMock()
        mock_coleccion.find_one.return_value = {
            'estado_actual': 'TRABAJANDO',
            'completado': False
        }
        
        mock_conexion_global.obtener_coleccion.return_value = mock_coleccion
        
        with patch('src.db.usuarios.estado_conexion.conexion_global', mock_conexion_global):
            from src.db.usuarios.estado_conexion import obtener_tiempo_desconectado
            resultado = obtener_tiempo_desconectado(str(ObjectId()))
            assert resultado == "Trabajando"

    def test_retorna_descanso_si_en_descanso(self, mock_conexion_global):
        """Retorna En descanso si está en descanso."""
        mock_coleccion = MagicMock()
        mock_coleccion.find_one.return_value = {
            'estado_actual': 'DESCANSO_CORTO',
            'completado': False
        }
        
        mock_conexion_global.obtener_coleccion.return_value = mock_coleccion
        
        with patch('src.db.usuarios.estado_conexion.conexion_global', mock_conexion_global):
            from src.db.usuarios.estado_conexion import obtener_tiempo_desconectado
            resultado = obtener_tiempo_desconectado(str(ObjectId()))
            assert resultado == "En descanso"

    def test_retorna_descanso_largo(self, mock_conexion_global):
        """Retorna En descanso si está en descanso largo."""
        mock_coleccion = MagicMock()
        mock_coleccion.find_one.return_value = {
            'estado_actual': 'DESCANSO_LARGO',
            'completado': False
        }
        
        mock_conexion_global.obtener_coleccion.return_value = mock_coleccion
        
        with patch('src.db.usuarios.estado_conexion.conexion_global', mock_conexion_global):
            from src.db.usuarios.estado_conexion import obtener_tiempo_desconectado
            resultado = obtener_tiempo_desconectado(str(ObjectId()))
            assert resultado == "En descanso"

    def test_retorna_tiempo_hace_minutos(self, mock_conexion_global):
        """Retorna tiempo hace X min."""
        mock_coleccion = MagicMock()
        mock_coleccion.find_one.side_effect = [None, {
            'fin_ciclo': datetime.now(timezone.utc) - timedelta(minutes=30)
        }]
        
        mock_conexion_global.obtener_coleccion.return_value = mock_coleccion
        
        with patch('src.db.usuarios.estado_conexion.conexion_global', mock_conexion_global):
            from src.db.usuarios.estado_conexion import obtener_tiempo_desconectado
            resultado = obtener_tiempo_desconectado(str(ObjectId()))
            assert "min" in resultado

    def test_retorna_tiempo_hace_horas(self, mock_conexion_global):
        """Retorna tiempo hace X horas."""
        mock_coleccion = MagicMock()
        mock_coleccion.find_one.side_effect = [None, {
            'fin_ciclo': datetime.now(timezone.utc) - timedelta(hours=2, minutes=30)
        }]
        
        mock_conexion_global.obtener_coleccion.return_value = mock_coleccion
        
        with patch('src.db.usuarios.estado_conexion.conexion_global', mock_conexion_global):
            from src.db.usuarios.estado_conexion import obtener_tiempo_desconectado
            resultado = obtener_tiempo_desconectado(str(ObjectId()))
            assert "h" in resultado

    def test_retorna_sin_actividad_reciente(self, mock_conexion_global):
        """Retorna sin actividad reciente."""
        mock_coleccion = MagicMock()
        mock_coleccion.find_one.return_value = None
        
        mock_conexion_global.obtener_coleccion.return_value = mock_coleccion
        
        with patch('src.db.usuarios.estado_conexion.conexion_global', mock_conexion_global):
            from src.db.usuarios.estado_conexion import obtener_tiempo_desconectado
            resultado = obtener_tiempo_desconectado(str(ObjectId()))
            assert resultado == "Sin actividad reciente"

    def test_retorna_desconocido_si_excepcion(self, mock_conexion_global):
        """Retorna Desconocido si hay excepción."""
        mock_conexion_global.obtener_coleccion.side_effect = Exception("Error")
        
        with patch('src.db.usuarios.estado_conexion.conexion_global', mock_conexion_global):
            from src.db.usuarios.estado_conexion import obtener_tiempo_desconectado
            resultado = obtener_tiempo_desconectado(str(ObjectId()))
            assert resultado == "Desconocido"

    def test_retorna_hace_menos_de_1_minuto(self, mock_conexion_global):
        """RetornaHace menos de 1 minuto."""
        mock_coleccion = MagicMock()
        mock_coleccion.find_one.side_effect = [None, {
            'fin_ciclo': datetime.now(timezone.utc) - timedelta(seconds=30)
        }]
        
        mock_conexion_global.obtener_coleccion.return_value = mock_coleccion
        
        with patch('src.db.usuarios.estado_conexion.conexion_global', mock_conexion_global):
            from src.db.usuarios.estado_conexion import obtener_tiempo_desconectado
            resultado = obtener_tiempo_desconectado(str(ObjectId()))
            assert resultado == "Hace menos de 1 minuto"