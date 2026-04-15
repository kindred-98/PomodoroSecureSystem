"""
conftest.py - Configuración de pytest y fixtures compartidos
Aquí se definen todas las fixtures reutilizables para los tests
"""

import os
import pytest
from contextlib import ExitStack
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime, timezone
from bson import ObjectId
import mongomock


# ====================
# FIXTURE GLOBAL - BLOQUEO WINDOWS
# ====================

@pytest.fixture(autouse=True)
def _mock_lock_workstation():
    """Evita que LockWorkStation() se ejecute de verdad durante los tests."""
    with patch('ctypes.windll.user32.LockWorkStation', return_value=1):
        yield


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
        "RAWI_encriptada": "<TEST_FERNET_ENCRYPTED>",
        "RAWI_hash": "<TEST_BCRYPT_HASH>",
        "RAWI_parametros": {
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
        "RAWI_encriptada": "<TEST_FERNET_ENCRYPTED>",
        "RAWI_hash": "<TEST_BCRYPT_HASH>",
        "RAWI_parametros": {
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
def mongodb_client():
    """Fixture: Cliente MongoDB mockeado con mongomock"""
    return mongomock.MongoClient()


@pytest.fixture
def mongodb_db(mongodb_client):
    """Fixture: Base de datos MongoDB mockeada"""
    return mongodb_client['test_pomodoro_db']


@pytest.fixture
def conexion_mongodb_mock(mongodb_db):
    """Fixture: Conexión MongoDB mockeada (singleton)"""
    mock = MagicMock()
    mock.obtener_coleccion = lambda nombre: mongodb_db[nombre]
    mock.conectar = MagicMock()
    mock.desconectar = MagicMock()
    return mock


@pytest.fixture
def mock_conexion_global(conexion_mongodb_mock):
    """Fixture: Parchea conexion_global en todos los módulos (db + auth)"""
    modulos_db = [
        'src.db.usuarios.crear_usuario',
        'src.db.usuarios.buscar_por_email',
        'src.db.usuarios.buscar_por_id',
        'src.db.usuarios.actualizar_pomodoro',
        'src.db.usuarios.actualizar_ultimo_acceso',
        'src.db.usuarios.desactivar_usuario',
        'src.db.equipos.crear_equipo',
        'src.db.equipos.buscar_por_id',
        'src.db.equipos.obtener_miembros',
        'src.db.equipos.obtener_por_encargado',
        'src.db.equipos.añadir_miembro',
        'src.db.sesiones.crear_sesion',
        'src.db.sesiones.actualizar_sesion',
        'src.db.sesiones.cerrar_sesion',
        'src.db.sesiones.obtener_historial',
        'src.db.anomalias.registrar_anomalia',
        'src.db.anomalias.obtener_por_usuario',
        'src.db.anomalias.obtener_por_equipo',
        'src.db.anomalias.marcar_revisada',
    ]
    modulos_auth = [
        'src.auth.sesion',
        'src.auth.login',
        'src.auth.ver_contraseña',
        'src.auth.regenerar_contraseña',
        'src.auth.cambiar_contraseña',
        'src.auth.exportar_contraseña',
        'src.auth.registro',
    ]
    modulos_timer = [
        'src.timer.ciclo_pomodoro',
        'src.timer.servicio_sesiones',
        'src.pausas.gestor_pausas',
    ]
    modulos_equipos_extra = [
        'src.db.equipos.editar_equipo',
        'src.db.equipos.obtener_para_encargado',
        'src.db.equipos.obtener_por_supervisor',
    ]
    modulos_otp = [
        'src.otp.gestor_otp',
    ]
    
    with ExitStack() as stack:
        for modulo in modulos_db + modulos_auth + modulos_timer + modulos_otp + modulos_equipos_extra:
            stack.enter_context(
                patch(f'{modulo}.conexion_global', conexion_mongodb_mock)
            )
        yield conexion_mongodb_mock


@pytest.fixture
def fernet_key_env():
    """Fixture: Genera una clave Fernet de test y la establece en os.environ"""
    from cryptography.fernet import Fernet
    clave_test = Fernet.generate_key().decode()
    with patch.dict(os.environ, {'FERNET_KEY': clave_test}):
        yield clave_test


@pytest.fixture
def parametros_contraseña_defecto():
    """Fixture: Parámetros por defecto para generación de contraseña en auth"""
    return {
        "longitud": 16,
        "usar_mayusculas": True,
        "usar_numeros": True,
        "usar_simbolos": True,
        "excluir_ambiguos": False
    }


@pytest.fixture
def usuario_registrado(mock_conexion_global, fernet_key_env, parametros_contraseña_defecto):
    """Fixture: Usuario completamente registrado con hash + encriptado en BD"""
    from src.seguridad.encriptacion import hashear_contraseña, cifrar
    from src.generador import generar_contraseña
    
    contraseña = generar_contraseña(parametros_contraseña_defecto)
    hash_pw = hashear_contraseña(contraseña)
    enc_pw = cifrar(contraseña)
    
    coleccion = mock_conexion_global.obtener_coleccion('usuarios')
    usuario = {
        'email': 'auth@test.com',
        'nombre': 'Usuario Auth',
        'contraseña_hash': hash_pw,
        'contraseña_encriptada': enc_pw,
        'parametros_contraseña': parametros_contraseña_defecto,
        'rol': 'empleado',
        'activo': True,
        'fecha_registro': datetime.now(timezone.utc),
        'ultimo_acceso': datetime.now(timezone.utc),
        'puntuacion_pomodoro': 0,
        'team_id': None,
        'metadata': {
            'ciclos_completados': 0,
            'pausas_utilizadas': 0,
            'anomalias_registradas': 0
        }
    }
    resultado = coleccion.insert_one(usuario)
    usuario['_id'] = resultado.inserted_id
    
    return {
        'usuario': usuario,
        'contraseña': contraseña
    }


@pytest.fixture
def coleccion_usuarios(mongodb_db):
    """Fixture: Colección de usuarios en MongoDB mockeada"""
    return mongodb_db['usuarios']


@pytest.fixture
def coleccion_equipos(mongodb_db):
    """Fixture: Colección de equipos en MongoDB mockeada"""
    return mongodb_db['equipos']


@pytest.fixture
def coleccion_sesiones(mongodb_db):
    """Fixture: Colección de sesiones en MongoDB mockeada"""
    return mongodb_db['sesiones']


@pytest.fixture
def coleccion_anomalias(mongodb_db):
    """Fixture: Colección de anomalías en MongoDB mockeada"""
    return mongodb_db['anomalias']


@pytest.fixture
def usuario_en_db(coleccion_usuarios):
    """Fixture: Usuario creado en la BD para tests"""
    usuario = {
        'email': 'test@example.com',
        'nombre': 'Test User',
        'contraseña_hash': 'hash_seguro',
        'rol': 'empleado',
        'activo': True,
        'fecha_registro': datetime.now(timezone.utc),
        'ultimo_acceso': datetime.now(timezone.utc),
        'puntuacion_pomodoro': 0,
        'metadata': {}
    }
    resultado = coleccion_usuarios.insert_one(usuario)
    usuario['_id'] = resultado.inserted_id
    return usuario


@pytest.fixture
def equipo_en_db(coleccion_equipos, usuario_en_db):
    """Fixture: Equipo creado en la BD para tests"""
    equipo = {
        'nombre': 'Team Test',
        'encargado_id': usuario_en_db['_id'],
        'descripcion': 'Test team',
        'miembros': [usuario_en_db['_id']],
        'fecha_creacion': datetime.now(timezone.utc),
        'activo': True
    }
    resultado = coleccion_equipos.insert_one(equipo)
    equipo['_id'] = resultado.inserted_id
    return equipo


@pytest.fixture
def sesion_en_db(coleccion_sesiones, usuario_en_db):
    """Fixture: Sesión creada en la BD para tests"""
    sesion = {
        'usuario_id': usuario_en_db['_id'],
        'tipo_sesion': 'pomodoro',
        'inicio': datetime.now(timezone.utc),
        'fin': None,
        'duracion_segundos': None,
        'pausas_utilizadas': 0,
        'completada': False
    }
    resultado = coleccion_sesiones.insert_one(sesion)
    sesion['_id'] = resultado.inserted_id
    return sesion


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
