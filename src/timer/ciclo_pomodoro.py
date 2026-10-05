"""
Módulo: ciclo_pomodoro.py
Responsabilidad: Orquestar ciclos Pomodoro completos.
Gestiona estados, callbacks de eventos y registro en BD.
"""

from datetime import datetime, timezone
from src.timer.estados import (
    ESTADO_INACTIVO,
    ESTADO_TRABAJANDO,
    ESTADO_DESCANSO_CORTO,
    ESTADO_DESCANSO_LARGO,
    ESTADO_PAUSADO,
    TRANSICIONES_VALIDAS,
)
from src.db.conexion import conexion_global
from src.excepciones import ErrorEstadoInvalido

# Callbacks registrados por otros módulos (FASE 6 los usará)
_callbacks = {
    'descanso_iniciado': [],
    'descanso_finalizado': [],
    'ciclo_completado': [],
    'pomodoro_completado': [],
    'anomalia_generada': [],
}


def registrar_callback(evento: str, funcion):
    """
    Registra una función callback para un tipo de evento.
    
    Args:
        evento (str): Nombre del evento ('descanso_iniciado', etc.)
        funcion: Función a llamar cuando ocurra el evento
    """
    if evento not in _callbacks:
        raise ValueError(
            f"Evento '{evento}' no válido. "
            f"Eventos disponibles: {list(_callbacks.keys())}"
        )
    if not callable(funcion):
        raise TypeError("funcion debe ser callable")
    _callbacks[evento].append(funcion)


def _emitir_evento(evento: str, datos: dict):
    """Emite un evento a todos los callbacks registrados."""
    for callback in _callbacks.get(evento, []):
        try:
            callback(datos)
        except Exception:  # nosec - un callback fallido no rompe el timer
            pass


def _validar_usuario_id(usuario_id: str):
    """Valida el usuario_id y devuelve su ObjectId."""
    if not isinstance(usuario_id, str):
        raise TypeError(f"usuario_id debe ser string, recibido: {type(usuario_id).__name__}")
    if not usuario_id.strip():
        raise ValueError("usuario_id no puede estar vacío")

    from bson import ObjectId
    try:
        return ObjectId(usuario_id)
    except Exception:
        raise ValueError(f"usuario_id inválido: '{usuario_id}'")


def _validar_configuracion(configuracion: dict) -> tuple:
    """Valida la configuración y devuelve (pomodoro_min, descansos_cortos, descanso_largo)."""
    configuracion = configuracion or {}

    pomodoro_min = configuracion.get('pomodoro_min', 25)
    descansos_cortos = configuracion.get('descansos_cortos', [5, 5, 5, 5])
    descanso_largo = configuracion.get('descanso_largo', 30)

    if not isinstance(pomodoro_min, int) or pomodoro_min < 1:
        raise ValueError(f"pomodoro_min debe ser int positivo, recibido: {pomodoro_min}")
    if not isinstance(descansos_cortos, list):
        raise ValueError("descansos_cortos debe ser list")

    return pomodoro_min, descansos_cortos, descanso_largo


def iniciar_ciclo(usuario_id: str, configuracion: dict = None) -> dict:
    """
    Inicia un nuevo ciclo Pomodoro para un usuario.
    
    Crea el registro del ciclo en BD y configura el primer pomodoro.
    
    Args:
        usuario_id (str): ID del usuario
        configuracion (dict, optional): Configuración personalizada:
            - pomodoro_min (int): Minutos por pomodoro (default 25)
            - descansos_cortos (list): Minutos por descanso corto (default [5,5,5,5])
            - descanso_largo (int): Minutos descanso largo (default 30)
    
    Returns:
        dict: {
            'ciclo_id': str,
            'numero_ciclo': int,
            'estado': str,
            'pomodoro_actual': int,
            'pomodoros_totales': int,
            'configuracion': dict,
        }
    
    Raises:
        TypeError: Si tipos son incorrectos
        ValueError: Si usuario_id vacío o configuración inválida
        Exception: Si usuario ya tiene un ciclo activo
    """
    usuario_oid = _validar_usuario_id(usuario_id)
    pomodoro_min, descansos_cortos, descanso_largo = _validar_configuracion(configuracion)

    # Verificar que no hay ciclo activo
    coleccion_ciclos = conexion_global.obtener_coleccion('ciclos_pomodoro')

    # Cerrar ciclos residuales de sesiones anteriores (crash, force close, etc.)
    coleccion_ciclos.update_many(
        {'usuario_id': usuario_oid, 'completado': False},
        {'$set': {'completado': True, 'estado_actual': 'INACTIVO'}}
    )
    
    # Contar ciclos previos para número de ciclo
    ciclos_previos = coleccion_ciclos.count_documents({'usuario_id': usuario_oid})
    numero_ciclo = ciclos_previos + 1
    
    # Crear registro del ciclo
    ciclo = {
        'usuario_id': usuario_oid,
        'numero_ciclo': numero_ciclo,
        'pomodoros_completados': 0,
        'pomodoro_actual': 1,
        'pomodoros_totales': len(descansos_cortos),
        'estado_actual': ESTADO_TRABAJANDO,
        'inicio_ciclo': datetime.now(timezone.utc),
        'configuracion': {
            'pomodoro_min': pomodoro_min,
            'descansos_cortos': descansos_cortos,
            'descanso_largo': descanso_largo,
        },
        'descansos_cortos_restantes': list(descansos_cortos),
        'descanso_largo_restante': descanso_largo,
        'completado': False,
    }
    
    resultado = coleccion_ciclos.insert_one(ciclo)
    ciclo['_id'] = resultado.inserted_id
    
    return {
        'ciclo_id': str(ciclo['_id']),
        'numero_ciclo': numero_ciclo,
        'estado': ESTADO_TRABAJANDO,
        'pomodoro_actual': 1,
        'pomodoros_totales': len(descansos_cortos),
        'configuracion': ciclo['configuracion'],
    }


def obtener_estado_ciclo(usuario_id: str) -> dict:
    """
    Retorna el estado actual del ciclo Pomodoro del usuario.
    
    Args:
        usuario_id (str): ID del usuario
    
    Returns:
        dict: Estado del ciclo o None si no hay ciclo activo
    
    Raises:
        TypeError: Si usuario_id no es string
        ValueError: Si usuario_id vacío
    """
    usuario_oid = _validar_usuario_id(usuario_id)

    coleccion = conexion_global.obtener_coleccion('ciclos_pomodoro')
    ciclo = coleccion.find_one({
        'usuario_id': usuario_oid,
        'completado': False,
    })
    
    if ciclo is None:
        return {'en_ciclo': False}
    
    return {
        'en_ciclo': True,
        'ciclo_id': str(ciclo['_id']),
        'numero_ciclo': ciclo['numero_ciclo'],
        'pomodoro_actual': ciclo['pomodoro_actual'],
        'pomodoros_totales': ciclo['pomodoros_totales'],
        'estado': ciclo['estado_actual'],
        'pomodoros_completados': ciclo['pomodoros_completados'],
        'descansos_cortos_restantes': ciclo.get('descansos_cortos_restantes', []),
        'descanso_largo_restante': ciclo.get('descanso_largo_restante', 0),
        'configuracion': ciclo['configuracion'],
    }


def manejar_evento_timer(usuario_id: str, evento: str) -> dict:
    """
    Procesa un evento del timer y realiza la transición de estado correspondiente.
    
    Este es el motor principal del ciclo Pomodoro.
    
    Args:
        usuario_id (str): ID del usuario
        evento (str): Tipo de evento:
            - "pomodoro_completado": Pomodoro terminó
            - "descanso_completado": Descanso terminó
    
    Returns:
        dict: {
            'nuevo_estado': str,
            'pomodoro_actual': int,
            'accion': str,
            'datos_extra': dict,
        }
    
    Raises:
        TypeError: Si tipos son incorrectos
        ValueError: Si evento no es válido
        Exception: Si no hay ciclo activo o transición inválida
    """
    usuario_oid = _validar_usuario_id(usuario_id)

    eventos_validos = {"pomodoro_completado", "descanso_completado"}
    if not isinstance(evento, str):
        raise TypeError(f"evento debe ser string, recibido: {type(evento).__name__}")
    if evento not in eventos_validos:
        raise ValueError(f"evento debe ser uno de {eventos_validos}, recibido: {evento}")

    coleccion = conexion_global.obtener_coleccion('ciclos_pomodoro')
    ciclo = coleccion.find_one({
        'usuario_id': usuario_oid,
        'completado': False,
    })

    if ciclo is None:
        raise ErrorEstadoInvalido("No hay ciclo Pomodoro activo para este usuario")

    manejadores = {
        "pomodoro_completado": _manejar_pomodoro_completado,
        "descanso_completado": _manejar_descanso_completado,
    }
    return manejadores[evento](usuario_id, ciclo, coleccion)


def _cerrar_pausa_manual(usuario_id: str) -> None:
    """Cierra la pausa manual si existe (el descanso automático la reemplaza)."""
    try:
        from src.pausas.gestor_pausas import limpiar_pausa_huerfana
        limpiar_pausa_huerfana(usuario_id)
    except Exception:  # nosec B110
        pass


def _iniciar_descanso_largo(usuario_id, ciclo, coleccion, pomodoro_actual):
    """Transiciona al descanso largo tras el último pomodoro del ciclo."""
    nuevo_estado = ESTADO_DESCANSO_LARGO
    descanso_duracion = ciclo['configuracion']['descanso_largo']

    coleccion.update_one(
        {'_id': ciclo['_id']},
        {'$set': {'estado_actual': nuevo_estado}}
    )

    _emitir_evento('descanso_iniciado', {
        'usuario_id': usuario_id,
        'tipo_descanso': 'largo',
        'duracion_min': descanso_duracion,
        'ciclo_id': str(ciclo['_id']),
    })

    return {
        'nuevo_estado': nuevo_estado,
        'pomodoro_actual': pomodoro_actual,
        'accion': 'descanso_largo',
        'datos_extra': {'duracion_min': descanso_duracion},
    }


def _iniciar_descanso_corto(usuario_id, ciclo, coleccion, pomodoro_actual):
    """Transiciona al siguiente descanso corto consumiendo uno de la cola."""
    nuevos_cortos = list(ciclo.get('descansos_cortos_restantes', []))
    descanso_duracion = nuevos_cortos[0] if nuevos_cortos else 5
    nuevos_cortos.pop(0)

    coleccion.update_one(
        {'_id': ciclo['_id']},
        {'$set': {
            'estado_actual': ESTADO_DESCANSO_CORTO,
            'descansos_cortos_restantes': nuevos_cortos,
        }}
    )

    _emitir_evento('descanso_iniciado', {
        'usuario_id': usuario_id,
        'tipo_descanso': 'corto',
        'duracion_min': descanso_duracion,
        'ciclo_id': str(ciclo['_id']),
    })

    return {
        'nuevo_estado': ESTADO_DESCANSO_CORTO,
        'pomodoro_actual': pomodoro_actual,
        'accion': 'descanso_corto',
        'datos_extra': {'duracion_min': descanso_duracion},
    }


def _manejar_pomodoro_completado(usuario_id, ciclo, coleccion):
    """Registra el pomodoro terminado y arranca el descanso que corresponda."""
    from src.timer.servicio_sesiones import registrar_sesion_pomodoro

    config = ciclo['configuracion']
    pomodoro_actual = ciclo['pomodoro_actual']
    registrar_sesion_pomodoro(usuario_id, ciclo, config['pomodoro_min'])

    pomodoros_completados = ciclo['pomodoros_completados'] + 1
    coleccion.update_one(
        {'_id': ciclo['_id']},
        {'$set': {'pomodoros_completados': pomodoros_completados}}
    )

    _emitir_evento('pomodoro_completado', {
        'usuario_id': usuario_id,
        'ciclo_id': str(ciclo['_id']),
        'pomodoro_numero': pomodoros_completados,
    })

    _cerrar_pausa_manual(usuario_id)

    if pomodoro_actual >= ciclo['pomodoros_totales']:
        return _iniciar_descanso_largo(usuario_id, ciclo, coleccion, pomodoro_actual)
    return _iniciar_descanso_corto(usuario_id, ciclo, coleccion, pomodoro_actual)


def _completar_ciclo(usuario_id, ciclo, coleccion):
    """Marca el ciclo como finalizado y arranca el siguiente si queda jornada."""
    coleccion.update_one(
        {'_id': ciclo['_id']},
        {'$set': {
            'completado': True,
            'fin_ciclo': datetime.now(timezone.utc),
            'estado_actual': ESTADO_INACTIVO,
        }}
    )

    _emitir_evento('ciclo_completado', {
        'usuario_id': usuario_id,
        'ciclo_id': str(ciclo['_id']),
        'numero_ciclo': ciclo['numero_ciclo'],
        'pomodoros_completados': ciclo['pomodoros_completados'] + 1,
    })

    try:
        resultado_siguiente = iniciar_ciclo(usuario_id, ciclo['configuracion'])
        return {
            'nuevo_estado': ESTADO_TRABAJANDO,
            'pomodoro_actual': 1,
            'accion': 'nuevo_ciclo',
            'datos_extra': resultado_siguiente,
        }
    except Exception:
        # No se pudo iniciar (no hay tiempo o hay ciclo activo)
        return {
            'nuevo_estado': ESTADO_INACTIVO,
            'pomodoro_actual': 0,
            'accion': 'fin_jornada',
            'datos_extra': {},
        }


def _reanudar_trabajo(usuario_id, ciclo, coleccion):
    """Tras un descanso corto vuelve al siguiente pomodoro del ciclo."""
    siguiente_pomodoro = ciclo['pomodoro_actual'] + 1

    coleccion.update_one(
        {'_id': ciclo['_id']},
        {'$set': {
            'estado_actual': ESTADO_TRABAJANDO,
            'pomodoro_actual': siguiente_pomodoro,
        }}
    )

    _emitir_evento('descanso_finalizado', {
        'usuario_id': usuario_id,
        'tipo_descanso': 'corto',
        'siguiente_pomodoro': siguiente_pomodoro,
    })

    return {
        'nuevo_estado': ESTADO_TRABAJANDO,
        'pomodoro_actual': siguiente_pomodoro,
        'accion': 'trabajar',
        'datos_extra': {'duracion_min': ciclo['configuracion']['pomodoro_min']},
    }


def _manejar_descanso_completado(usuario_id, ciclo, coleccion):
    """Tras un descanso largo cierra el ciclo; tras uno corto, sigue trabajando."""
    if ciclo['estado_actual'] == ESTADO_DESCANSO_LARGO:
        return _completar_ciclo(usuario_id, ciclo, coleccion)
    return _reanudar_trabajo(usuario_id, ciclo, coleccion)
