"""Tests para auth/registro.py — Registro de usuarios"""

import pytest
from unittest.mock import patch
from src.auth.registro import registrar_usuario


class TestRegistroValidacion:
    """Tests para validación de entrada en registrar_usuario"""
    
    def test_email_no_string(self, mock_conexion_global, fernet_key_env, parametros_contraseña_defecto):
        with pytest.raises(TypeError, match="email debe ser string"):
            registrar_usuario(123, "Nombre", "empleado", parametros_contraseña_defecto)
    
    def test_nombre_no_string(self, mock_conexion_global, fernet_key_env, parametros_contraseña_defecto):
        with pytest.raises(TypeError, match="nombre debe ser string"):
            registrar_usuario("a@b.com", 123, "empleado", parametros_contraseña_defecto)
    
    def test_rol_no_string(self, mock_conexion_global, fernet_key_env, parametros_contraseña_defecto):
        with pytest.raises(TypeError, match="rol debe ser string"):
            registrar_usuario("a@b.com", "Nombre", 123, parametros_contraseña_defecto)
    
    def test_parametros_no_dict(self, mock_conexion_global, fernet_key_env):
        with pytest.raises(TypeError, match="parametros_contraseña debe ser dict"):
            registrar_usuario("a@b.com", "Nombre", "empleado", "no_dict")
    
    def test_email_vacio(self, mock_conexion_global, fernet_key_env, parametros_contraseña_defecto):
        with pytest.raises(ValueError, match="email no puede estar vacío"):
            registrar_usuario("", "Nombre", "empleado", parametros_contraseña_defecto)
    
    def test_nombre_vacio(self, mock_conexion_global, fernet_key_env, parametros_contraseña_defecto):
        with pytest.raises(ValueError, match="nombre no puede estar vacío"):
            registrar_usuario("a@b.com", "", "empleado", parametros_contraseña_defecto)


class TestRegistroExito:
    """Tests para registro exitoso"""
    
    def test_registro_completo(self, mock_conexion_global, fernet_key_env, parametros_contraseña_defecto):
        """Registro exitoso debe retornar usuario + contraseña generada"""
        resultado = registrar_usuario(
            "nuevo@test.com", "Nuevo Usuario", "empleado", parametros_contraseña_defecto
        )
        
        assert 'usuario' in resultado
        assert 'contraseña_generada' in resultado
        assert resultado['usuario']['email'] == "nuevo@test.com"
        assert resultado['usuario']['nombre'] == "Nuevo Usuario"
        assert resultado['usuario']['rol'] == "supervisor"  # Primer usuario = supervisor
    
    def test_contraseña_en_bd(self, mock_conexion_global, fernet_key_env, parametros_contraseña_defecto):
        """Usuario en BD debe tener hash y encriptada"""
        resultado = registrar_usuario(
            "bd@test.com", "Test BD", "empleado", parametros_contraseña_defecto
        )
        usuario = resultado['usuario']
        
        assert 'contraseña_hash' in usuario
        assert 'contraseña_encriptada' in usuario
        assert usuario['contraseña_hash'].startswith("$2b$")
        assert usuario['rol'] == "supervisor"  # Primer usuario
    
    def test_contraseña_generada_cumple_longitud(self, mock_conexion_global, fernet_key_env, parametros_contraseña_defecto):
        """Contraseña generada debe tener la longitud solicitada"""
        resultado = registrar_usuario(
            "long@test.com", "Test", "empleado", parametros_contraseña_defecto
        )
        assert len(resultado['contraseña_generada']) == parametros_contraseña_defecto['longitud']
        assert resultado['usuario']['rol'] == "supervisor"
    
    def test_email_duplicado_falla(self, mock_conexion_global, fernet_key_env, parametros_contraseña_defecto):
        """No debe permitir registrar el mismo email dos veces"""
        from src.db.conexion import conexion_global as conn
        usuarios = conn.obtener_coleccion('usuarios')
        
        registrar_usuario("dup@test.com", "Primero", "empleado", parametros_contraseña_defecto)
        duplicado = usuarios.find_one({'email': 'dup@test.com'})
        
        assert duplicado is not None
    
    def test_todos_los_roles(self, mock_conexion_global, fernet_key_env, parametros_contraseña_defecto):
        """Primer usuario supervisor, resto empleados"""
        for i, rol in enumerate(["empleado", "encargado", "supervisor"]):
            email = f"{rol}@test.com"
            resultado = registrar_usuario(email, rol.title(), rol, parametros_contraseña_defecto)
            if i == 0:
                assert resultado['usuario']['rol'] == "supervisor"
            else:
                assert resultado['usuario']['rol'] == "empleado"
    
    def test_parametros_se_guardan(self, mock_conexion_global, fernet_key_env, parametros_contraseña_defecto):
        """Parámetros de contraseña deben guardarse en el usuario"""
        resultado = registrar_usuario(
            "params@test.com", "Params", "empleado", parametros_contraseña_defecto
        )
        assert resultado['usuario']['parametros_contraseña'] == parametros_contraseña_defecto
        assert resultado['usuario']['rol'] == "supervisor"


class TestRegistroPrimerUsuario:
    """Tests para lógica de primer usuario (supervisor automático)"""
    
    def test_primer_usuario_es_supervisor(self, mock_conexion_global, fernet_key_env, parametros_contraseña_defecto):
        """Primer usuario debe ser supervisor automáticamente"""
        resultado = registrar_usuario(
            "supervisor@test.com", "Supervisor", "empleado", parametros_contraseña_defecto
        )
        assert resultado['usuario']['rol'] == "supervisor"
    
    def test_segundo_usuario_es_empleado(self, mock_conexion_global, fernet_key_env, parametros_contraseña_defecto):
        """Segundo usuario debe ser empleado aunque pase otro rol"""
        registrar_usuario("admin@test.com", "Admin", "encargado", parametros_contraseña_defecto)
        
        resultado = registrar_usuario(
            "emp@test.com", "Empleado", "supervisor", parametros_contraseña_defecto
        )
        assert resultado['usuario']['rol'] == "empleado"


class TestRegistroContraseñaPersonalizada:
    """Tests para contraseña personalizada"""
    
    def test_contraseña_personalizada(self, mock_conexion_global, fernet_key_env):
        """Debe aceptar contraseña personalizada"""
        params = {
            "tipo": "personalizada",
            "contraseña": "MiPass$123"
        }
        resultado = registrar_usuario(
            "custom@test.com", "Custom User", "empleado", params
        )
        assert resultado['contraseña_generada'] == "MiPass$123"
    
    def test_contraseña_personalizada_sin_tipo_falla(self, mock_conexion_global, fernet_key_env):
        """Sin tipo=personalizada debe usar generador"""
        params = {
            "longitud": 12,
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True,
            "excluir_ambiguos": False,
        }
        resultado = registrar_usuario(
            "sistema@test.com", "Sistema User", "empleado", params
        )
        assert len(resultado['contraseña_generada']) == 12


class TestRegistroValidacionesSeguridad:
    """Tests para validaciones de seguridad adicionales"""
    
    def test_email_con_espacios(self, mock_conexion_global, fernet_key_env):
        """Email con espacios debe ser limpiado"""
        resultado = registrar_usuario(
            "  usuario@test.com  ", "Usuario Prueba", "empleado", {"longitud": 8}
        )
        assert resultado['usuario']['email'] == "usuario@test.com"
    
    def test_nombre_con_espacios(self, mock_conexion_global, fernet_key_env):
        """Nombre con espacios debe ser limpiado"""
        resultado = registrar_usuario(
            "nom@test.com", "  Juan Perez  ", "empleado", {"longitud": 8}
        )
        assert resultado['usuario']['nombre'] == "Juan Perez"
    
    def test_email_mayusculas_minusculas(self, mock_conexion_global, fernet_key_env):
        """Email debe guardarse en minúsculas"""
        resultado = registrar_usuario(
            "USUARIO@TEST.COM", "Usuario Test", "empleado", {"longitud": 8}
        )
        # Primer usuario siempre es supervisor y email debe ser lowercase
        assert resultado['usuario']['email'] == "usuario@test.com"
        assert resultado['usuario']['rol'] == "supervisor"
    
    def test_rol_con_mayusculas(self, mock_conexion_global, fernet_key_env):
        """Rol debe forzarse a minúsculas"""
        # Primer usuario: rol se fuerza a supervisor
        resultado_1 = registrar_usuario(
            "rol1@test.com", "Rol Test 1", "ENCARGADO", {"longitud": 8}
        )
        assert resultado_1['usuario']['rol'] == "supervisor"
        
        # Segundo usuario: rol se fuerza a empleado
        resultado_2 = registrar_usuario(
            "rol2@test.com", "Rol Test 2", "SUPERVISOR", {"longitud": 8}
        )
        assert resultado_2['usuario']['rol'] == "empleado" 
    
    def test_contraseña_vacia_personalizada(self, mock_conexion_global, fernet_key_env):
        """Contraseña personalizada vacía debe fallar"""
        with pytest.raises(ValueError, match="Contraseña personalizada no proporcionada"):
            registrar_usuario(
                "vacio@test.com", "Vacio", "empleado", 
                {"tipo": "personalizada", "contraseña": ""}
            )
    
    def test_parametros_vacios(self, mock_conexion_global, fernet_key_env):
        """Parámetros vacíos deben usar valores por defecto"""
        resultado = registrar_usuario(
            "defecto@test.com", "Defecto", "empleado", {}
        )
        assert resultado is not None
        assert 'contraseña_generada' in resultado


class TestRegistroValidacionEmail:
    """Tests para validación de formato email"""
    
    def test_email_sin_arroba(self, mock_conexion_global, fernet_key_env):
        """Email sin @ debe fallar"""
        with pytest.raises(ValueError, match="@"):
            registrar_usuario("emailinvalido.com", "Test", "empleado", {"longitud": 8})
    
    def test_email_sin_dominio(self, mock_conexion_global, fernet_key_env):
        """Email sin dominio debe fallar"""
        with pytest.raises(ValueError, match="formato|dominio"):
            registrar_usuario("test@", "Test", "empleado", {"longitud": 8})
    
    def test_email_punto_inicio(self, mock_conexion_global, fernet_key_env):
        """Email con punto al inicio debe fallar"""
        with pytest.raises(ValueError, match="punto"):
            registrar_usuario(".test@test.com", "Test", "empleado", {"longitud": 8})
    
    def test_email_puntos_consecutivos(self, mock_conexion_global, fernet_key_env):
        """Email con puntos consecutivos debe fallar"""
        with pytest.raises(ValueError, match="consecutivos"):
            registrar_usuario("te..st@test.com", "Test", "empleado", {"longitud": 8})
    
    def test_email_tld_muy_corto(self, mock_conexion_global, fernet_key_env):
        """Email con TLD muy corto debe fallar"""
        with pytest.raises(ValueError, match="TLD"):
            registrar_usuario("test@test.c", "Test", "empleado", {"longitud": 8})
    
    def test_email_tld_sin_letras(self, mock_conexion_global, fernet_key_env):
        """Email con TLD con números debe fallar"""
        with pytest.raises(ValueError, match="letras"):
            registrar_usuario("test@test.c1", "Test", "empleado", {"longitud": 8})
    
    def test_email_valido(self, mock_conexion_global, fernet_key_env):
        """Email válido debe pasar"""
        resultado = registrar_usuario("test@dominio.co", "Test", "empleado", {"longitud": 8})
        assert resultado is not None
