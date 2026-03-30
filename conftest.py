"""
conftest.py - Configuración de pytest y fixtures compartidos
Aquí se definen todas las fixtures reutilizables para los tests
"""

import pytest
from unittest.mock import Mock, MagicMock
from datetime import datetime
from bson import ObjectId


# ====================
# FIXTURES - GENERADOR
# ====================

@pytest.fixture
def parametros_generador_defecto():
    """Fixture: Parámetros por defecto para generador de contraseñas"""
    return {
        "longitud": 12,
        "usar_mayusculas": True,
        "usar_numeros": True,
        "usar_simbolos": True,
        "excluir_ambiguos": False
    }


@pytest.fixture
def parametros_generador_solo_minusculas():
    """Fixture: Parámetros solo minúsculas"""
    return {
        "longitud": 12,
        "usar_mayusculas": False,
        "usar_numeros": False,
        "usar_simbolos": False,
        "excluir_ambiguos": False
    }


@pytest.fixture
def parametros_generador_basico():
    """Fixture: Parámetros básicos (mayús + números)"""
    return {
        "longitud": 12,
        "usar_mayusculas": True,
        "usar_numeros": True,
        "usar_simbolos": False,
        "excluir_ambiguos": False
    }


# ================
# FIXTURES - DATOS
# ================

@pytest.fixture
def usuario_empleado_mock():
    """Fixture: Usuario de tipo empleado para tests"""
    return {
        "_id": ObjectId(),
        "nombre": "Ana García",
        "email": "ana@empresa.com",
        "rol": "empleado",
        "equipo_id": ObjectId(),
        "password_encriptada": "gAAAAAB...",
        "password_hash": "$2b$12$...",
        "parametros_password": {
            "longitud": 16,
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True,
            "excluir_ambiguos": False
        },
        "horario": {
            "inicio": "09:00",
            "fin": "16:00",
            "zona_horaria": "Europe/Madrid"
        },
        "configuracion_pomodoro": {
            "descansos_cortos": [5, 5, 5, 5],
            "descanso_largo": 30,
            "banco_total": 50
        },
        "activo": True,
        "fecha_registro": datetime.now(),
        "ultimo_acceso": datetime.now()
    }


@pytest.fixture
def usuario_encargado_mock():
    """Fixture: Usuario de tipo encargado para tests"""
    return {
        "_id": ObjectId(),
        "nombre": "Carlos López",
        "email": "carlos@empresa.com",
        "rol": "encargado",
        "equipo_id": ObjectId(),
        "password_encriptada": "gAAAAAB...",
        "password_hash": "$2b$12$...",
        "parametros_password": {
            "longitud": 20,
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True,
            "excluir_ambiguos": True
        },
        "horario": {
            "inicio": "08:00",
            "fin": "16:00",
            "zona_horaria": "Europe/Madrid"
        },
        "configuracion_pomodoro": {
            "descansos_cortos": [5, 5, 5, 5],
            "descanso_largo": 30,
            "banco_total": 50
        },
        "activo": True,
        "fecha_registro": datetime.now(),
        "ultimo_acceso": datetime.now()
    }


@pytest.fixture
def sesion_activa_mock():
    """Fixture: Sesión activa para tests"""
    return {
        "_id": ObjectId(),
        "usuario_id": ObjectId(),
        "fecha": datetime.now().date(),
        "inicio_jornada": datetime.now(),
        "fin_jornada": None,
        "ciclos_completados": 0,
        "tiempo_trabajado_min": 0,
        "tiempo_descansos_reglados_min": 0,
        "tiempo_descansos_fijos_min": 0,
        "tiempo_pausas_manuales_min": 0,
        "tiempo_bloqueos_min": 0,
        "pausas_manuales": [],
        "pausas_manuales_usadas": 0,
        "estado": "activa"
    }


@pytest.fixture
def anomalia_mock():
    """Fixture: Anomalía para tests"""
    return {
        "_id": ObjectId(),
        "usuario_id": ObjectId(),
        "sesion_id": ObjectId(),
        "timestamp": datetime.now(),
        "tipo": "tercera_pausa",
        "detalle": "Usuario solicitó una tercera pausa manual",
        "minutos_exceso": 0,
        "resuelto": False,
        "visto_por_encargado": False,
        "visto_por_supervisor": False
    }


# ========================
# FIXTURES - MONGODB MOCK
# ========================

@pytest.fixture
def cliente_mongodb_mock():
    """Fixture: Cliente MongoDB mockeado"""
    cliente = MagicMock()
    cliente.servidor.conectado = True
    return cliente


@pytest.fixture
def base_datos_mock(cliente_mongodb_mock):
    """Fixture: Base de datos MongoDB mockeada"""
    base_datos = MagicMock()
    base_datos.cliente = cliente_mongodb_mock
    return base_datos


@pytest.fixture
def coleccion_usuarios_mock(base_datos_mock):
    """Fixture: Colección de usuarios mockeada"""
    coleccion = MagicMock()
    coleccion.insertar_uno = MagicMock(return_value=ObjectId())
    coleccion.buscar_uno = MagicMock(return_value=None)
    coleccion.actualizar_uno = MagicMock(return_value={"modificados": 1})
    return coleccion


# ============================
# FIXTURES - PARAMETRIZACIÓN
# ============================

@pytest.fixture(params=[8, 12, 20, 128])
def longitudes_validas(request):
    """Fixture parametrizada: Distintas longitudes válidas"""
    return request.param


@pytest.fixture(params=[4, 7, 129, -1])
def longitudes_invalidas(request):
    """Fixture parametrizada: Longitudes fuera de rango"""
    return request.param


# ====================
# CONFIGURACIÓN PYTEST
# ====================

def pytest_configure(config):
    """Se ejecuta al iniciar pytest"""
    config.addinivalue_line(
        "markers", "unitario: tests unitarios rápidos"
    )
    config.addinivalue_line(
        "markers", "integracion: tests con dependencias externas"
    )
    config.addinivalue_line(
        "markers", "lento: tests que tardan más de 1 segundo"
    )


# ====================
# HELPER FUNCTIONS
# ====================

def crear_parametros_password(longitud=12, mayusculas=True, numeros=True, 
                              simbolos=True, excluir_ambiguos=False):
    """Helper: Crear parámetros personalizados para generador"""
    return {
        "longitud": longitud,
        "usar_mayusculas": mayusculas,
        "usar_numeros": numeros,
        "usar_simbolos": simbolos,
        "excluir_ambiguos": excluir_ambiguos
    }
