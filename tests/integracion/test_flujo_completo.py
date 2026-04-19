"""
Tests de integración: Flujo completo de autenticación.
Registro → Verificación de email → Login
"""

import pytest
import time


class TestFlujoCompletoRegistroLogin:
    """Tests del flujo completo desde registro hasta login."""

    def test_registro_genera_contraseña(self, mock_conexion_global, fernet_key_env):
        """El registro debe generar una contraseña válida."""
        from src.auth.registro import registrar_usuario

        resultado = registrar_usuario(
            "test@integration.com",
            "Test User",
            "empleado",
            {"longitud": 24, "usar_mayusculas": True, "usar_numeros": True, "usar_simbolos": True, "excluir_ambiguos": False}
        )

        assert resultado is not None
        assert "usuario" in resultado
        assert "contraseña_generada" in resultado
        assert len(resultado["contraseña_generada"]) == 24

    def test_registro_guarda_usuario_no_verificado(self, mock_conexion_global, fernet_key_env):
        """El usuario debe registrarse con email_verificado=False."""
        from src.auth.registro import registrar_usuario

        resultado = registrar_usuario(
            "notverified@test.com",
            "Not Verified",
            "empleado",
            {"longitud": 16, "usar_mayusculas": True, "usar_numeros": True, "usar_simbolos": True, "excluir_ambiguos": False}
        )

        usuario = resultado["usuario"]
        assert usuario["email_verificado"] is False
        assert usuario.get("email") == "notverified@test.com"

    def test_verificacion_marca_email_como_verificado(self, mock_conexion_global, fernet_key_env):
        """La verificación debe marcar email_verified=True."""
        from src.auth.registro import registrar_usuario
        from src.auth.verificacion_email import crear_o_actualizar_verificacion, verificar_token_db

        resultado = registrar_usuario(
            "toverify@test.com",
            "To Verify",
            "empleado",
            {"longitud": 16, "usar_mayusculas": True, "usar_numeros": True, "usar_simbolos": True, "excluir_ambiguos": False}
        )

        email = resultado["usuario"]["email"]

        token = crear_o_actualizar_verificacion(email)
        resultado_verif = verificar_token_db(email, token)

        assert resultado_verif["valido"] is True

        from src.db.conexion import conexion_global
        usuarios = conexion_global.obtener_coleccion('usuarios')
        usuario = usuarios.find_one({"email": email})
        assert usuario["email_verified"] is True

    def test_login_falla_sin_verificar(self, mock_conexion_global, fernet_key_env):
        """Login debe fallar si email no está verificado."""
        from src.auth.registro import registrar_usuario
        from src.auth.login import iniciar_sesion

        resultado = registrar_usuario(
            "unverified@test.com",
            "Unverified User",
            "empleado",
            {"longitud": 16, "usar_mayusculas": True, "usar_numeros": True, "usar_simbolos": True, "excluir_ambiguos": False}
        )

        contraseña = resultado["contraseña_generada"]

        with pytest.raises(Exception) as exc_info:
            iniciar_sesion("unverified@test.com", contraseña)

        assert "verificar tu email" in str(exc_info.value)

    def test_login_exitoso_tras_verificacion(self, mock_conexion_global, fernet_key_env):
        """Login debe funcionar después de verificar email."""
        from src.auth.registro import registrar_usuario
        from src.auth.verificacion_email import crear_o_actualizar_verificacion, verificar_token_db
        from src.auth.login import iniciar_sesion

        resultado = registrar_usuario(
            "verifiedlogin@test.com",
            "Verified Login",
            "empleado",
            {"longitud": 16, "usar_mayusculas": True, "usar_numeros": True, "usar_simbolos": True, "excluir_ambiguos": False}
        )

        email = resultado["usuario"]["email"]
        contraseña = resultado["contraseña_generada"]

        token = crear_o_actualizar_verificacion(email)
        verificar_token_db(email, token)

        login_result = iniciar_sesion(email, contraseña)

        assert "usuario" in login_result
        assert "token_sesion" in login_result
        assert login_result["usuario"]["email"] == email

    def test_login_crea_sesion(self, mock_conexion_global, fernet_key_env):
        """Login debe crear una sesión activa."""
        from src.auth.registro import registrar_usuario
        from src.auth.verificacion_email import crear_o_actualizar_verificacion, verificar_token_db
        from src.auth.login import iniciar_sesion
        from src.auth.sesion import verificar_sesion

        resultado = registrar_usuario(
            "session@test.com",
            "Session User",
            "empleado",
            {"longitud": 16, "usar_mayusculas": True, "usar_numeros": True, "usar_simbolos": True, "excluir_ambiguos": False}
        )

        email = resultado["usuario"]["email"]
        contraseña = resultado["contraseña_generada"]

        token_creado = crear_o_actualizar_verificacion(email)
        verificar_token_db(email, token_creado)

        login_result = iniciar_sesion(email, contraseña)
        token_sesion = login_result["token_sesion"]

        resultado_verificar = verificar_sesion(token_sesion)
        assert resultado_verificar is not False


class TestFlujoVerificacionEmail:
    """Tests específicos del flujo de verificación."""

    def test_token_expira_en_5_minutos(self, mock_conexion_global):
        """Token de verificación debe expirar en 5 minutos."""
        from src.auth.verificacion_email import crear_o_actualizar_verificacion, obtener_verificacion_pendiente

        email = "expire@test.com"
        token = crear_o_actualizar_verificacion(email)

        verificacion = obtener_verificacion_pendiente(email)

        assert verificacion is not None
        expira = verificacion["expira"]
        ahora = int(time.time())
        assert expira > ahora
        assert expira <= ahora + (5 * 60)

    def test_max_5_intentos(self, mock_conexion_global):
        """Máximo 5 intentos para verificar."""
        from src.auth.verificacion_email import crear_o_actualizar_verificacion, verificar_token_db

        email = "attempts@test.com"
        token = crear_o_actualizar_verificacion(email)

        for i in range(5):
            resultado = verificar_token_db(email, "000000")
            assert resultado["valido"] is False

        resultado = verificar_token_db(email, "000000")
        assert "intentos" in resultado["mensaje"].lower() or "bloqueado" in resultado["mensaje"].lower()


class TestFlujoRecuperacion:
    """Tests del flujo de recuperación de contraseña."""

    def test_contraseña_se_guarda_encriptada(self, mock_conexion_global, fernet_key_env):
        """La contraseña debe guardarse encriptada."""
        from src.auth.registro import registrar_usuario
        from src.seguridad.encriptacion import descifrar

        resultado = registrar_usuario(
            "encrypt@test.com",
            "Encrypt User",
            "empleado",
            {"longitud": 16, "usar_mayusculas": True, "usar_numeros": True, "usar_simbolos": True, "excluir_ambiguos": False}
        )

        contraseña_original = resultado["contraseña_generada"]
        contraseña_encriptada = resultado["usuario"]["contraseña_encriptada"]

        contraseña_descifrada = descifrar(contraseña_encriptada)

        assert contraseña_descifrada == contraseña_original