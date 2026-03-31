"""Tests para timer/ciclo_pomodoro.py"""

import pytest
from bson import ObjectId
from src.timer.ciclo_pomodoro import (
    iniciar_ciclo,
    obtener_estado_ciclo,
    manejar_evento_timer,
    registrar_callback,
)
from src.timer.estados import (
    ESTADO_TRABAJANDO,
    ESTADO_DESCANSO_CORTO,
    ESTADO_DESCANSO_LARGO,
    ESTADO_INACTIVO,
)


class TestIniciarCiclo:
    """Tests para iniciar_ciclo"""
    
    def test_creacion_exitosa(self, mock_conexion_global, usuario_en_db):
        """Debe crear un ciclo activo"""
        resultado = iniciar_ciclo(str(usuario_en_db['_id']))
        
        assert 'ciclo_id' in resultado
        assert resultado['estado'] == ESTADO_TRABAJANDO
        assert resultado['pomodoro_actual'] == 1
        assert resultado['pomodoros_totales'] == 4
    
    def test_configuracion_custom(self, mock_conexion_global, usuario_en_db):
        """Debe respetar configuración personalizada"""
        config = {
            'pomodoro_min': 30,
            'descansos_cortos': [8, 8, 8, 8],
            'descanso_largo': 18,
        }
        resultado = iniciar_ciclo(str(usuario_en_db['_id']), config)
        
        assert resultado['configuracion']['pomodoro_min'] == 30
        assert resultado['configuracion']['descansos_cortos'] == [8, 8, 8, 8]
        assert resultado['configuracion']['descanso_largo'] == 18
    
    def test_dos_ciclos_consecutivos_falla(self, mock_conexion_global, usuario_en_db):
        """No debe permitir dos ciclos activos"""
        iniciar_ciclo(str(usuario_en_db['_id']))
        
        with pytest.raises(Exception, match="ciclo.*activo"):
            iniciar_ciclo(str(usuario_en_db['_id']))
    
    def test_numero_ciclo_incremental(self, mock_conexion_global, usuario_en_db):
        """Cada ciclo nuevo debe tener número mayor"""
        uid = str(usuario_en_db['_id'])
        
        r1 = iniciar_ciclo(uid)
        # Completar ciclo 1
        coleccion = mock_conexion_global.obtener_coleccion('ciclos_pomodoro')
        coleccion.update_one(
            {'_id': ObjectId(r1['ciclo_id'])},
            {'$set': {'completado': True}}
        )
        
        r2 = iniciar_ciclo(uid)
        assert r2['numero_ciclo'] == r1['numero_ciclo'] + 1
    
    def test_usuario_id_no_string(self, mock_conexion_global):
        with pytest.raises(TypeError, match="usuario_id debe ser string"):
            iniciar_ciclo(123)
    
    def test_usuario_id_vacio(self, mock_conexion_global):
        with pytest.raises(ValueError, match="no puede estar vacío"):
            iniciar_ciclo("")
    
    def test_usuario_id_invalido(self, mock_conexion_global):
        with pytest.raises(ValueError, match="inválido"):
            iniciar_ciclo("no_es_objectid")
    
    def test_pomodoro_min_invalido(self, mock_conexion_global, usuario_en_db):
        with pytest.raises(ValueError, match="pomodoro_min"):
            iniciar_ciclo(str(usuario_en_db['_id']), {'pomodoro_min': -5})


class TestObtenerEstadoCiclo:
    """Tests para obtener_estado_ciclo"""
    
    def test_sin_ciclo_activo(self, mock_conexion_global, usuario_en_db):
        """Sin ciclo debe retornar en_ciclo=False"""
        estado = obtener_estado_ciclo(str(usuario_en_db['_id']))
        assert estado['en_ciclo'] is False
    
    def test_con_ciclo_activo(self, mock_conexion_global, usuario_en_db):
        """Con ciclo activo debe retornar estado"""
        uid = str(usuario_en_db['_id'])
        iniciar_ciclo(uid)
        
        estado = obtener_estado_ciclo(uid)
        assert estado['en_ciclo'] is True
        assert estado['estado'] == ESTADO_TRABAJANDO
        assert estado['pomodoro_actual'] == 1
    
    def test_usuario_id_no_string(self, mock_conexion_global):
        with pytest.raises(TypeError, match="usuario_id debe ser string"):
            obtener_estado_ciclo(123)
    
    def test_usuario_id_vacio(self, mock_conexion_global):
        with pytest.raises(ValueError, match="no puede estar vacío"):
            obtener_estado_ciclo("")


class TestManejarEventoTimer:
    """Tests para manejar_evento_timer"""
    
    def test_pomodoro_completado_descanso_corto(self, mock_conexion_global, usuario_en_db):
        """Pomodoro 1/4 completado → DESCANSO_CORTO"""
        uid = str(usuario_en_db['_id'])
        iniciar_ciclo(uid)
        
        resultado = manejar_evento_timer(uid, "pomodoro_completado")
        
        assert resultado['nuevo_estado'] == ESTADO_DESCANSO_CORTO
        assert resultado['accion'] == 'descanso_corto'
        assert resultado['datos_extra']['duracion_min'] == 5
    
    def test_pomodoro_4_completado_descanso_largo(self, mock_conexion_global, usuario_en_db):
        """Pomodoro 4/4 completado → DESCANSO_LARGO"""
        uid = str(usuario_en_db['_id'])
        iniciar_ciclo(uid)
        
        # Completar pomodoros 1, 2, 3
        for _ in range(3):
            r = manejar_evento_timer(uid, "pomodoro_completado")
            manejar_evento_timer(uid, "descanso_completado")
        
        # Completar pomodoro 4
        resultado = manejar_evento_timer(uid, "pomodoro_completado")
        assert resultado['nuevo_estado'] == ESTADO_DESCANSO_LARGO
        assert resultado['accion'] == 'descanso_largo'
    
    def test_descanso_corto_completado_vuelve_trabajar(self, mock_conexion_global, usuario_en_db):
        """Descanso corto completado → TRABAJANDO"""
        uid = str(usuario_en_db['_id'])
        iniciar_ciclo(uid)
        
        manejar_evento_timer(uid, "pomodoro_completado")
        resultado = manejar_evento_timer(uid, "descanso_completado")
        
        assert resultado['nuevo_estado'] == ESTADO_TRABAJANDO
        assert resultado['accion'] == 'trabajar'
        assert resultado['pomodoro_actual'] == 2
    
    def test_sin_ciclo_activo_falla(self, mock_conexion_global, usuario_en_db):
        """Sin ciclo activo debe fallar"""
        with pytest.raises(Exception, match="No hay ciclo"):
            manejar_evento_timer(str(usuario_en_db['_id']), "pomodoro_completado")
    
    def test_evento_invalido(self, mock_conexion_global, usuario_en_db):
        """Evento no válido debe fallar"""
        uid = str(usuario_en_db['_id'])
        iniciar_ciclo(uid)
        
        with pytest.raises(ValueError, match="evento debe ser uno de"):
            manejar_evento_timer(uid, "evento_raro")
    
    def test_usuario_id_no_string(self, mock_conexion_global):
        with pytest.raises(TypeError, match="usuario_id debe ser string"):
            manejar_evento_timer(123, "pomodoro_completado")
    
    def test_evento_no_string(self, mock_conexion_global, usuario_en_db):
        with pytest.raises(TypeError, match="evento debe ser string"):
            manejar_evento_timer(str(usuario_en_db['_id']), 123)
    
    def test_registra_sesion_en_bd(self, mock_conexion_global, usuario_en_db):
        """Al completar pomodoro debe registrar sesión en BD"""
        uid = str(usuario_en_db['_id'])
        iniciar_ciclo(uid)
        
        manejar_evento_timer(uid, "pomodoro_completado")
        
        coleccion = mock_conexion_global.obtener_coleccion('sesiones')
        sesiones = list(coleccion.find({'usuario_id': usuario_en_db['_id']}))
        assert len(sesiones) >= 1
        assert sesiones[0]['tipo_sesion'] == 'pomodoro'


class TestRegistrarCallback:
    """Tests para registrar_callback"""
    
    def test_registro_exitoso(self, mock_conexion_global):
        """Debe registrar callback sin error"""
        registrar_callback('descanso_iniciado', lambda x: None)
    
    def test_evento_invalido(self, mock_conexion_global):
        """Evento no registrado debe fallar"""
        with pytest.raises(ValueError, match="no válido"):
            registrar_callback('evento_falso', lambda x: None)
    
    def test_no_callable(self, mock_conexion_global):
        """Función no callable debe fallar"""
        with pytest.raises(TypeError, match="callable"):
            registrar_callback('descanso_iniciado', "no_funcion")
