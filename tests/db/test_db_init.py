"""Tests para db __init__."""

import pytest


class TestDbInit:
    """Tests para funciones del módulo db."""

    def test_tiene_conexion_global(self):
        """conexion_global existe."""
        from src.db import conexion_global
        assert conexion_global is not None

    def test_tiene_crear_usuario(self):
        """crear_usuario existe."""
        from src.db import crear_usuario
        assert callable(crear_usuario)

    def test_tiene_buscar_por_id(self):
        """buscar_por_id existe."""
        from src.db import buscar_por_id
        assert callable(buscar_por_id)

    def test_tiene_buscar_por_email(self):
        """buscar_por_email existe."""
        from src.db import buscar_por_email
        assert callable(buscar_por_email)

    def test_tiene_actualizar_pomodoro(self):
        """actualizar_pomodoro existe."""
        from src.db import actualizar_pomodoro
        assert callable(actualizar_pomodoro)

    def test_tiene_desactivar_usuario(self):
        """desactivar_usuario existe."""
        from src.db import desactivar_usuario
        assert callable(desactivar_usuario)