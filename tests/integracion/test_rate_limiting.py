"""
Tests de Rate Limiting y Auditoría.
"""

import pytest
import time


class TestRateLimitingLogin:
    """Tests para rate limiting en login."""

    def test_permite_hasta_5_intentos(self, mock_conexion_global, fernet_key_env):
        """Debe permitir hasta 5 intentos."""
        from src.auth.rate_limiting import verificar_rate_limit_login, reiniciar_intentos_login

        reiniciar_intentos_login("ratetest@test.com")

        puede, _ = verificar_rate_limit_login("ratetest@test.com")
        assert puede is True

    def test_bloquea_despues_de_5_intentos(self, mock_conexion_global, fernet_key_env):
        """Debe bloquear después de 5 intentos fallidos."""
        from src.auth.rate_limiting import (
            verificar_rate_limit_login,
            reiniciar_intentos_login,
            registrar_intento_login
        )

        email = "block@test.com"
        reiniciar_intentos_login(email)

        for i in range(5):
            registrar_intento_login(email, False)

        puede, mensaje = verificar_rate_limit_login(email)
        assert puede is False
        assert "bloqueado" in mensaje.lower()

    def test_reinicia_intentos_despues_exito(self, mock_conexion_global, fernet_key_env):
        """Debe reiniciar intentos después de login exitoso."""
        from src.auth.rate_limiting import (
            verificar_rate_limit_login,
            reiniciar_intentos_login,
            registrar_intento_login
        )

        email = "success@test.com"
        reiniciar_intentos_login(email)

        registrar_intento_login(email, False)
        registrar_intento_login(email, False)

        puede, _ = verificar_rate_limit_login(email)
        assert puede is True

        registrar_intento_login(email, True)

        puede, _ = verificar_rate_limit_login(email)
        assert puede is True


class TestAuditoria:
    """Tests para auditoría."""

    def test_audit_sin_errores(self, mock_conexion_global, fernet_key_env):
        """Audit debe ejecutarse sin errores."""
        from src.auth.audit import audit_registro, audit_login, audit_verificacion

        audit_registro("test@audit.com", True)
        audit_login("test@audit.com", False)
        audit_verificacion("test@audit.com", True)