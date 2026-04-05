"""
Tests para src.timer.ciclo_pomodoro - Casos adicionales de cobertura
"""

import pytest
from datetime import datetime, timezone
from unittest.mock import patch, MagicMock
from bson import ObjectId

from src.timer.ciclo_pomodoro import (
    iniciar_ciclo,
    obtener_estado_ciclo,
    manejar_evento_timer,
    registrar_callback,
    _emitir_evento,
    _callbacks,
)
from src.timer.estados import (
    ESTADO_INACTIVO,
    ESTADO_TRABAJANDO,
    ESTADO_DESCANSO_CORTO,
    ESTADO_DESCANSO_LARGO,
)


class TestEmitirEvento:
    """Tests para _emitir_evento (manejo de excepciones en callbacks)"""

    def test_callback_sin_excepcion(self, mock_conexion_global):
        """Verifica que callback sin excepción se ejecute"""
        resultados = []
        
        def callback_exitoso(datos):
            resultados.append(datos)
        
        with patch('src.timer.ciclo_pomodoro._callbacks', {'test': [callback_exitoso]}):
            _emitir_evento('test', {'valor': 123})
        
        assert len(resultados) == 1
        assert resultados[0]['valor'] == 123

    def test_callback_con_excepcion_no_rompe_timer(self, mock_conexion_global):
        """Verifica que callback con excepción no rompa el timer"""
        resultados = []
        
        def callback_exitoso(datos):
            resultados.append(datos)
        
        def callback_fallido(datos):
            raise RuntimeError("Error simulado")
        
        callbacks_modulo = {
            'test': [callback_exitoso, callback_fallido],
        }
        
        with patch('src.timer.ciclo_pomodoro._callbacks', callbacks_modulo):
            _emitir_evento('test', {'valor': 456})
        
        assert len(resultados) == 1
        assert resultados[0]['valor'] == 456

    def test_evento_sin_callbacks(self, mock_conexion_global):
        """Verifica que evento sin callbacks no falle"""
        with patch('src.timer.ciclo_pomodoro._callbacks', {}):
            _emitir_evento('inexistente', {})
        
        assert True

    def test_multiple_callbacks_se_ejecutan(self, mock_conexion_global):
        """Verifica que todos los callbacks se ejecuten"""
        resultados = []
        
        def callback1(datos):
            resultados.append(1)
        
        def callback2(datos):
            resultados.append(2)
        
        callbacks_modulo = {
            'multi': [callback1, callback2],
        }
        
        with patch('src.timer.ciclo_pomodoro._callbacks', callbacks_modulo):
            _emitir_evento('multi', {})
        
        assert resultados == [1, 2]


class TestIniciarCicloValidacion:
    """Tests adicionales para iniciar_ciclo con validación"""

    def test_descansos_cortos_no_es_lista(self, mock_conexion_global):
        """Verifica que descansos_cortos debe ser lista"""
        with patch('src.timer.ciclo_pomodoro.conexion_global', mock_conexion_global):
            with pytest.raises(ValueError) as exc_info:
                iniciar_ciclo(
                    str(ObjectId()),
                    {'descansos_cortos': "no es lista"}
                )
        
        assert "descansos_cortos debe ser list" in str(exc_info.value)


class TestObtenerEstadoCicloValidacion:
    """Tests adicionales para obtener_estado_ciclo"""

    def test_usuario_id_invalido(self, mock_conexion_global):
        """Verifica que rechace usuario_id inválido"""
        with patch('src.timer.ciclo_pomodoro.conexion_global', mock_conexion_global):
            with pytest.raises(ValueError):
                obtener_estado_ciclo("id-no-valido")


class TestManejarEventoTimerCasosEspeciales:
    """Tests para casos especiales de manejar_evento_timer"""

    def test_usuario_id_invalido(self, mock_conexion_global):
        """Verifica que rechace usuario_id inválido"""
        with patch('src.timer.ciclo_pomodoro.conexion_global', mock_conexion_global):
            with pytest.raises(ValueError):
                manejar_evento_timer("id-invalido", "pomodoro_completado")

    def test_evento_invalido_tipo(self, mock_conexion_global):
        """Verifica que rechace evento no string"""
        with patch('src.timer.ciclo_pomodoro.conexion_global', mock_conexion_global):
            with pytest.raises(TypeError):
                manejar_evento_timer(str(ObjectId()), 123)

    def test_no_hay_ciclo_activo(self, mock_conexion_global):
        """Verifica que falle si no hay ciclo activo"""
        with patch('src.timer.ciclo_pomodoro.conexion_global', mock_conexion_global):
            with pytest.raises(Exception) as exc_info:
                manejar_evento_timer(str(ObjectId()), "pomodoro_completado")
        
        assert "No hay ciclo Pomodoro activo" in str(exc_info.value)


class TestDescansoLargoCompletado:
    """Tests para el flujo de descanso largo completado"""

    def test_descanso_largo_inicia_nuevo_ciclo(self, mock_conexion_global):
        """Verifica que descanso largo iniciado correctamente"""
        usuario_id = str(ObjectId())
        
        coleccion = mock_conexion_global.obtener_coleccion('ciclos_pomodoro')
        ciclo_id = ObjectId()
        coleccion.insert_one({
            '_id': ciclo_id,
            'usuario_id': ObjectId(usuario_id),
            'estado_actual': ESTADO_DESCANSO_LARGO,
            'pomodoro_actual': 4,
            'pomodoros_totales': 4,
            'pomodoros_completados': 3,
            'configuracion': {
                'pomodoro_min': 25,
                'descansos_cortos': [5, 5, 5, 5],
                'descanso_largo': 30,
            },
            'descansos_cortos_restantes': [],
            'descanso_largo_restante': 30,
            'completado': False,
            'numero_ciclo': 1,
        })
        
        with patch('src.timer.ciclo_pomodoro.conexion_global', mock_conexion_global):
            with patch('src.timer.ciclo_pomodoro.iniciar_ciclo') as mock_iniciar:
                mock_iniciar.return_value = {
                    'ciclo_id': str(ObjectId()),
                    'numero_ciclo': 2,
                    'estado': ESTADO_TRABAJANDO,
                    'pomodoro_actual': 1,
                    'pomodoros_totales': 4,
                    'configuracion': {},
                }
                
                resultado = manejar_evento_timer(usuario_id, "descanso_completado")
        
        assert resultado['accion'] == 'nuevo_ciclo'
        assert resultado['nuevo_estado'] == ESTADO_TRABAJANDO

    def test_descanso_largo_fin_jornada_si_error(self, mock_conexion_global):
        """Verifica que fin de jornada si no se puede iniciar nuevo ciclo"""
        usuario_id = str(ObjectId())
        
        coleccion = mock_conexion_global.obtener_coleccion('ciclos_pomodoro')
        ciclo_id = ObjectId()
        coleccion.insert_one({
            '_id': ciclo_id,
            'usuario_id': ObjectId(usuario_id),
            'estado_actual': ESTADO_DESCANSO_LARGO,
            'pomodoro_actual': 4,
            'pomodoros_totales': 4,
            'pomodoros_completados': 3,
            'configuracion': {
                'pomodoro_min': 25,
                'descansos_cortos': [5, 5, 5, 5],
                'descanso_largo': 30,
            },
            'descansos_cortos_restantes': [],
            'descanso_largo_restante': 30,
            'completado': False,
            'numero_ciclo': 1,
        })
        
        with patch('src.timer.ciclo_pomodoro.conexion_global', mock_conexion_global):
            with patch('src.timer.ciclo_pomodoro.iniciar_ciclo') as mock_iniciar:
                mock_iniciar.side_effect = Exception("No se puede iniciar")
                
                resultado = manejar_evento_timer(usuario_id, "descanso_completado")
        
        assert resultado['accion'] == 'fin_jornada'
        assert resultado['nuevo_estado'] == ESTADO_INACTIVO


class TestDescansoCortoCompletado:
    """Tests para el flujo de descanso corto completado"""

    def test_descanso_corto_pasa_a_siguiente_pomodoro(self, mock_conexion_global):
        """Verifica que descanso corto passe al siguiente pomodoro"""
        usuario_id = str(ObjectId())
        
        coleccion = mock_conexion_global.obtener_coleccion('ciclos_pomodoro')
        ciclo_id = ObjectId()
        coleccion.insert_one({
            '_id': ciclo_id,
            'usuario_id': ObjectId(usuario_id),
            'estado_actual': ESTADO_DESCANSO_CORTO,
            'pomodoro_actual': 2,
            'pomodoros_totales': 4,
            'pomodoros_completados': 1,
            'configuracion': {
                'pomodoro_min': 25,
                'descansos_cortos': [5, 5, 5, 5],
                'descanso_largo': 30,
            },
            'descansos_cortos_restantes': [5, 5, 5],
            'descanso_largo_restante': 30,
            'completado': False,
            'numero_ciclo': 1,
        })
        
        with patch('src.timer.ciclo_pomodoro.conexion_global', mock_conexion_global):
            resultado = manejar_evento_timer(usuario_id, "descanso_completado")
        
        assert resultado['accion'] == 'trabajar'
        assert resultado['nuevo_estado'] == ESTADO_TRABAJANDO
        assert resultado['pomodoro_actual'] == 3


class TestPomodoroCompletado:
    """Tests para el flujo de pomodoro completado"""

    def test_pomodoro_final_descanso_largo(self, mock_conexion_global):
        """Verifica que el último pomodoro inicie descanso largo"""
        usuario_id = str(ObjectId())
        
        coleccion = mock_conexion_global.obtener_coleccion('ciclos_pomodoro')
        ciclo_id = ObjectId()
        coleccion.insert_one({
            '_id': ciclo_id,
            'usuario_id': ObjectId(usuario_id),
            'estado_actual': ESTADO_TRABAJANDO,
            'pomodoro_actual': 4,
            'pomodoros_totales': 4,
            'pomodoros_completados': 3,
            'configuracion': {
                'pomodoro_min': 25,
                'descansos_cortos': [5, 5, 5, 5],
                'descanso_largo': 30,
            },
            'descansos_cortos_restantes': [5, 5, 5],
            'descanso_largo_restante': 30,
            'completado': False,
            'numero_ciclo': 1,
        })
        
        with patch('src.timer.ciclo_pomodoro.conexion_global', mock_conexion_global):
            with patch('src.timer.ciclo_pomodoro._emitir_evento'):
                with patch('src.timer.servicio_sesiones.registrar_sesion_pomodoro'):
                    resultado = manejar_evento_timer(usuario_id, "pomodoro_completado")
        
        assert resultado['accion'] == 'descanso_largo'
        assert resultado['nuevo_estado'] == ESTADO_DESCANSO_LARGO

    def test_pomodoro_intermedio_descanso_corto(self, mock_conexion_global):
        """Verifica que pomodoro intermedio inicie descanso corto"""
        usuario_id = str(ObjectId())
        
        coleccion = mock_conexion_global.obtener_coleccion('ciclos_pomodoro')
        ciclo_id = ObjectId()
        coleccion.insert_one({
            '_id': ciclo_id,
            'usuario_id': ObjectId(usuario_id),
            'estado_actual': ESTADO_TRABAJANDO,
            'pomodoro_actual': 2,
            'pomodoros_totales': 4,
            'pomodoros_completados': 1,
            'configuracion': {
                'pomodoro_min': 25,
                'descansos_cortos': [5, 5, 5, 5],
                'descanso_largo': 30,
            },
            'descansos_cortos_restantes': [5, 5, 5],
            'descanso_largo_restante': 30,
            'completado': False,
            'numero_ciclo': 1,
        })
        
        with patch('src.timer.ciclo_pomodoro.conexion_global', mock_conexion_global):
            with patch('src.timer.ciclo_pomodoro._emitir_evento'):
                with patch('src.timer.servicio_sesiones.registrar_sesion_pomodoro'):
                    resultado = manejar_evento_timer(usuario_id, "pomodoro_completado")
        
        assert resultado['accion'] == 'descanso_corto'
        assert resultado['nuevo_estado'] == ESTADO_DESCANSO_CORTO


class TestRegistrarCallback:
    """Tests adicionales para registrar_callback"""

    def test_registra_en_evento_existente(self, mock_conexion_global):
        """Verifica que registra callback en evento existente"""
        callbacks_inicial = len(_callbacks.get('descanso_iniciado', []))
        
        def mi_callback(datos):
            pass
        
        registrar_callback('descanso_iniciado', mi_callback)
        
        assert len(_callbacks.get('descanso_iniciado', [])) == callbacks_inicial + 1

    def test_evento_no_existente_lanza_error(self, mock_conexion_global):
        """Verifica que lance error si evento no existe"""
        with pytest.raises(ValueError) as exc_info:
            registrar_callback('evento_inexistente', lambda x: x)
        
        assert "no válido" in str(exc_info.value)

    def test_funcion_no_callable_lanza_error(self, mock_conexion_global):
        """Verifica que rechace función no callable"""
        with pytest.raises(TypeError) as exc_info:
            registrar_callback('descanso_iniciado', "no es callable")
        
        assert "callable" in str(exc_info.value)
