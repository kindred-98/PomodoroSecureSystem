"""Tests para auth __init__.py."""

import pytest


class TestAuthInit:
    """Tests para funciones del módulo auth."""

    def test_tiene_registrar_usuario(self):
        """registrar_usuario existe."""
        from src.auth import registrar_usuario
        assert callable(registrar_usuario)

    def test_tiene_iniciar_sesion(self):
        """iniciar_sesion existe."""
        from src.auth import iniciar_sesion
        assert callable(iniciar_sesion)

    def test_tiene_cerrar_sesion(self):
        """cerrar_sesion existe."""
        from src.auth import cerrar_sesion
        assert callable(cerrar_sesion)

    def test_tiene_crear_sesion(self):
        """crear_sesion existe."""
        from src.auth import crear_sesion
        assert callable(crear_sesion)

    def test_tiene_verificar_sesion(self):
        """verificar_sesion existe."""
        from src.auth import verificar_sesion
        assert callable(verificar_sesion)

    def test_tiene_cerrar_sesion_por_token(self):
        """cerrar_sesion_por_token existe."""
        from src.auth import cerrar_sesion_por_token
        assert callable(cerrar_sesion_por_token)

    def test_tiene_ver_contraseña(self):
        """ver_contraseña existe."""
        from src.auth import ver_contraseña
        assert callable(ver_contraseña)

    def test_tiene_regenerar_contraseña(self):
        """regenerar_contraseña existe."""
        from src.auth import regenerar_contraseña
        assert callable(regenerar_contraseña)

    def test_tiene_cambiar_contraseña(self):
        """cambiar_contraseña existe."""
        from src.auth import cambiar_contraseña
        assert callable(cambiar_contraseña)

    def test_tiene_exportar_contraseña(self):
        """exportar_contraseña existe."""
        from src.auth import exportar_contraseña
        assert callable(exportar_contraseña)

    def test_tiene_obtener_contraseña(self):
        """obtener_contraseña existe."""
        from src.auth import obtener_contraseña
        assert callable(obtener_contraseña)

    def test_tiene_obtener_contraseña_tipo(self):
        """obtener_contraseña requiere string."""
        from src.auth import obtener_contraseña
        
        with pytest.raises(ValueError):
            obtener_contraseña("invalid")