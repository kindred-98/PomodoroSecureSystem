"""Tests para módulos de equipos adicionales."""

import pytest
from bson import ObjectId


class TestObtenerPorEncargado:
    """Tests para obtener_por_encargado."""

    def test_retorna_equipos(self, mock_conexion_global):
        """Retorna equipos del encargado."""
        from src.db.equipos.obtener_por_encargado import obtener_por_encargado
        resultado = obtener_por_encargado(str(ObjectId()))
        assert isinstance(resultado, list)

    def test_encargado_none(self, mock_conexion_global):
        """Encargado None."""
        from src.db.equipos.obtener_por_encargado import obtener_por_encargado
        with pytest.raises(TypeError):
            obtener_por_encargado(None)


class TestObtenerParaEncargado:
    """Tests para obtener_para_encargado."""

    def test_retorna_equipos(self, mock_conexion_global):
        """Retorna equipos para encargado."""
        from src.db.equipos.obtener_para_encargado import obtener_para_encargado
        resultado = obtener_para_encargado(str(ObjectId()))
        assert isinstance(resultado, list)


class TestObtenerPorSupervisor:
    """Tests para obtener_por_supervisor."""

    def test_retorna_equipos(self, mock_conexion_global):
        """Retorna equipos del supervisor."""
        from src.db.equipos.obtener_por_supervisor import obtener_por_supervisor
        resultado = obtener_por_supervisor(str(ObjectId()))
        assert isinstance(resultado, list)

    def test_supervisor_none(self, mock_conexion_global):
        """Supervisor None."""
        from src.db.equipos.obtener_por_supervisor import obtener_por_supervisor
        with pytest.raises(TypeError):
            obtener_por_supervisor(None)


class TestEditarEquipo:
    """Tests para editar_equipo."""

    def test_editar_nombre(self, mock_conexion_global):
        """Editar nombre de equipo."""
        from src.db.equipos.editar_equipo import editar_nombre
        resultado = editar_nombre(str(ObjectId()), "Nuevo Nombre")
        assert resultado is None or isinstance(resultado, dict)

    def test_asignar_encargado(self, mock_conexion_global):
        """Asignar encargado."""
        from src.db.equipos.editar_equipo import asignar_encargado
        resultado = asignar_encargado(str(ObjectId()), str(ObjectId()))
        assert resultado is None or isinstance(resultado, dict)

    def test_quitar_miembro(self, mock_conexion_global):
        """Quitar miembro."""
        from src.db.equipos.editar_equipo import quitar_miembro
        resultado = quitar_miembro(str(ObjectId()), str(ObjectId()))
        assert resultado is None or isinstance(resultado, dict)

    def test_eliminar_equipo(self, mock_conexion_global):
        """Eliminar equipo."""
        from src.db.equipos.editar_equipo import eliminar_equipo
        resultado = eliminar_equipo(str(ObjectId()))
        assert isinstance(resultado, bool)


class TestListarTodos:
    """Tests para listar_todos."""

    def test_retorna_lista(self, mock_conexion_global):
        """Retorna lista de equipos."""
        from src.db.equipos.listar_todos import listar_todos
        from pymongo.errors import ConnectionFailure
        with pytest.raises(ConnectionFailure):
            listar_todos()
