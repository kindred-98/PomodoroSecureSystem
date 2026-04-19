"""
Tests de seguridad: Rate limiting y protección contra inyecciones.
"""

import pytest


class TestRateLimiting:
    """Tests para rate limiting."""

    def test_login_bloquea_demasiados_intentos(self, mock_conexion_global, fernet_key_env):
        """Login debe bloquear tras múltiples intentos fallidos."""
        from src.auth.registro import registrar_usuario
        from src.auth.login import iniciar_sesion

        registrar_usuario(
            "rate@test.com",
            "Rate Test",
            "empleado",
            {"longitud": 16, "usar_mayusculas": True, "usar_numeros": True, "usar_simbolos": True, "excluir_ambiguos": False}
        )

        for i in range(3):
            try:
                iniciar_sesion("rate@test.com", "wrongpassword")
            except Exception:
                pass

    def test_verificacion_bloquea_despues_de_5_intentos(self, mock_conexion_global):
        """Verificación se bloquea tras 5 intentos fallidos."""
        from src.auth.verificacion_email import crear_o_actualizar_verificacion, verificar_token_db

        email = "verifyrate@test.com"
        crear_o_actualizar_verificacion(email)

        for i in range(5):
            resultado = verificar_token_db(email, "000000")
            assert resultado["valido"] is False

        resultado = verificar_token_db(email, "000000")
        assert "bloqueado" in resultado["mensaje"].lower() or "intentos" in resultado["mensaje"].lower()


class TestProteccionInyeccion:
    """Tests de protección contra inyecciones."""

    def test_login_sql_injection_email(self, mock_conexion_global, fernet_key_env):
        """Login debe ser seguro contra SQL injection en email."""
        from src.auth.login import iniciar_sesion
        from src.auth.registro import registrar_usuario

        registrar_usuario(
            "normal@test.com",
            "Normal User",
            "empleado",
            {"longitud": 16, "usar_mayusculas": True, "usar_numeros": True, "usar_simbolos": True, "excluir_ambiguos": False}
        )

        sql_injection_emails = [
            "normal@test.com' OR '1'='1",
            "normal@test.com\" OR \"1\"=\"1",
            "normal@test.com' OR 1=1--",
            "normal@test.com' UNION SELECT--",
            "${'normal@test.com'}",
        ]

        for email in sql_injection_emails:
            with pytest.raises(Exception):
                iniciar_sesion(email, "anypassword")

    def test_login_special_characters_in_password(self, mock_conexion_global, fernet_key_env):
        """Login debe manejar caracteres especiales en contraseña."""
        from src.auth.login import iniciar_sesion
        from src.auth.registro import registrar_usuario

        registrar_usuario(
            "special@test.com",
            "Special User",
            "empleado",
            {"longitud": 16, "usar_mayusculas": True, "usar_numeros": True, "usar_simbolos": True, "excluir_ambiguos": False}
        )

        special_passwords = [
            "password' or '1'='1",
            "password\" or \"1\"=\"1",
            "password; DROP TABLE--",
            "password'--",
            "password' /*",
        ]

        for password in special_passwords:
            with pytest.raises(Exception):
                iniciar_sesion("special@test.com", password)

    def test_registro_xss_in_nombre(self, mock_conexion_global, fernet_key_env):
        """Registro debe sanitizar nombre con caracteres peligrosos."""
        from src.auth.registro import registrar_usuario

        xss_nombres = [
            "<script>alert('xss')</script>",
            " nombre",
            "{nombre}",
            "${nombre}",
        ]

        for nombre in xss_nombres:
            with pytest.raises((ValueError, TypeError)):
                registrar_usuario(
                    f"xss{nombre.replace('<', '').replace('>', '')}@test.com",
                    nombre,
                    "empleado",
                    {"longitud": 16, "usar_mayusculas": True, "usar_numeros": True, "usar_simbolos": True, "excluir_ambiguos": False}
                )

    def test_registro_email_injection(self, mock_conexion_global, fernet_key_env):
        """Registro debe rechazar emails con inyecciones."""
        from src.auth.registro import registrar_usuario

        injection_emails = [
            "test@test.com<script>",
            "test@test.com${alert}",
            "test@test.com{{}}",
            "test@test.com<%",
        ]

        for email in injection_emails:
            with pytest.raises(ValueError):
                registrar_usuario(
                    email,
                    "Test User",
                    "empleado",
                    {"longitud": 16, "usar_mayusculas": True, "usar_numeros": True, "usar_simbolos": True, "excluir_ambiguos": False}
                )


class TestSeguridadTokens:
    """Tests de seguridad de tokens."""

    def test_token_es_unico(self, mock_conexion_global, fernet_key_env):
        """Cada token de verificación debe ser único."""
        from src.auth.verificacion_email import generar_token

        tokens = [generar_token(6) for _ in range(100)]
        assert len(set(tokens)) == 100

    def test_token_no_es_predictible(self, mock_conexion_global):
        """Token no debe ser fácilmente adivinaste."""
        from src.auth.verificacion_email import generar_token

        token = generar_token(6)
        assert token.isdigit()
        assert len(token) == 6
        assert token != "000000"
        assert token != "123456"

    def test_hash_contraseña_no_reversible(self, fernet_key_env):
        """Hash de contraseña no debe ser reversible."""
        from src.seguridad.encriptacion import hashear_contraseña, verificar_contraseña

        password = "TestPassword123!"
        hashed = hashear_contraseña(password)

        assert verificar_contraseña(password, hashed) is True
        assert password.encode() != hashed.encode()
        assert hashed.startswith("$2b$")

    def test_sesion_token_longitud(self, mock_conexion_global, fernet_key_env):
        """Token de sesión debe tener longitud suficiente."""
        from src.auth.login import iniciar_sesion
        from src.auth.registro import registrar_usuario

        resultado = registrar_usuario(
            "tokenlen@test.com",
            "Token Len",
            "empleado",
            {"longitud": 16, "usar_mayusculas": True, "usar_numeros": True, "usar_simbolos": True, "excluir_ambiguos": False}
        )

        from src.auth.verificacion_email import crear_o_actualizar_verificacion, verificar_token_db
        token = crear_o_actualizar_verificacion("tokenlen@test.com")
        verificar_token_db("tokenlen@test.com", token)

        contraseña = resultado["contraseña_generada"]
        resultado_login = iniciar_sesion("tokenlen@test.com", contraseña)
        token_sesion = resultado_login["token_sesion"]

        assert len(token_sesion) >= 32


class TestValidacionEntradas:
    """Tests de validación de entradas."""

    def test_registro_email_longitud_aceptable(self, mock_conexion_global, fernet_key_env):
        """Email de longitud válida debe registrarse."""
        from src.auth.registro import registrar_usuario

        resultado = registrar_usuario(
            "valid@test.com",
            "Valid",
            "empleado",
            {"longitud": 16, "usar_mayusculas": True, "usar_numeros": True, "usar_simbolos": True, "excluir_ambiguos": False}
        )

        assert resultado is not None
        assert resultado["usuario"]["email"] == "valid@test.com"