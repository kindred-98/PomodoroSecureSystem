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
    if not isinstance(usuario_id, str):
        raise TypeError(f"usuario_id debe ser string, recibido: {type(usuario_id).__name__}")
    if not usuario_id.strip():
        raise ValueError("usuario_id no puede estar vacío")
    
    from bson import ObjectId
    try:
        usuario_oid = ObjectId(usuario_id)
    except Exception:
        raise ValueError(f"usuario_id inválido: '{usuario_id}'")
    
    # Configuración por defecto
    if configuracion is None:
        configuracion = {}
    
    pomodoro_min = configuracion.get('pomodoro_min', 25)
    descansos_cortos = configuracion.get('descansos_cortos', [5, 5, 5, 5])
    descanso_largo = configuracion.get('descanso_largo', 30)
    
    if not isinstance(pomodoro_min, int) or pomodoro_min < 1:
        raise ValueError(f"pomodoro_min debe ser int positivo, recibido: {pomodoro_min}")
    if not isinstance(descansos_cortos, list):
        raise ValueError("descansos_cortos debe ser list")
    
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
    if not isinstance(usuario_id, str):
        raise TypeError(f"usuario_id debe ser string, recibido: {type(usuario_id).__name__}")
    if not usuario_id.strip():
        raise ValueError("usuario_id no puede estar vacío")
    
    from bson import ObjectId
    try:
        usuario_oid = ObjectId(usuario_id)
    except Exception:
        raise ValueError(f"usuario_id inválido: '{usuario_id}'")
    
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
    if not isinstance(usuario_id, str):
        raise TypeError(f"usuario_id debe ser string, recibido: {type(usuario_id).__name__}")
    if not isinstance(evento, str):
        raise TypeError(f"evento debe ser string, recibido: {type(evento).__name__}")
    
    eventos_validos = {"pomodoro_completado", "descanso_completado"}
    if evento not in eventos_validos:
        raise ValueError(f"evento debe ser uno de {eventos_validos}, recibido: {evento}")
    
    from bson import ObjectId
    try:
        usuario_oid = ObjectId(usuario_id)
    except Exception:
        raise ValueError(f"usuario_id inválido: '{usuario_id}'")
    
    coleccion = conexion_global.obtener_coleccion('ciclos_pomodoro')
    ciclo = coleccion.find_one({
        'usuario_id': usuario_oid,
        'completado': False,
    })
    
    if ciclo is None:
        raise Exception("No hay ciclo Pomodoro activo para este usuario")
    
    estado_actual = ciclo['estado_actual']
    pomodoro_actual = ciclo['pomodoro_actual']
    pomodoros_totales = ciclo['pomodoros_totales']
    cortos_restantes = list(ciclo.get('descansos_cortos_restantes', []))
    config = ciclo['configuracion']
    
    if evento == "pomodoro_completado":
        # Registrar sesión del pomodoro completado
        from src.timer.servicio_sesiones import registrar_sesion_pomodoro
        registrar_sesion_pomodoro(usuario_id, ciclo, config['pomodoro_min'])
        
        # Incrementar contador
        pomodoros_completados = ciclo['pomodoros_completados'] + 1
        coleccion.update_one(
            {'_id': ciclo['_id']},
            {'$set': {'pomodoros_completados': pomodoros_completados}}
        )
        
        # Emitir evento
        _emitir_evento('pomodoro_completado', {
            'usuario_id': usuario_id,
            'ciclo_id': str(ciclo['_id']),
            'pomodoro_numero': pomodoros_completados,
        })
        
        # Cerrar pausa manual si existe (el descanso automático reemplaza la pausa)
        try:
            from src.pausas.gestor_pausas import limpiar_pausa_huerfana
            limpiar_pausa_huerfana(usuario_id)
        except Exception:
            pass
        
        # ¿Es el último pomodoro del ciclo?
        if pomodoro_actual >= pomodoros_totales:
            # Descanso largo
            nuevo_estado = ESTADO_DESCANSO_LARGO
            descanso_duracion = config['descanso_largo']
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
        else:
            # Descanso corto
            nuevo_estado = ESTADO_DESCANSO_CORTO
            descanso_duracion = cortos_restantes[0] if cortos_restantes else 5
            cortos_restantes.pop(0)
            
            coleccion.update_one(
                {'_id': ciclo['_id']},
                {'$set': {
                    'estado_actual': nuevo_estado,
                    'descansos_cortos_restantes': cortos_restantes,
                }}
            )
            
            _emitir_evento('descanso_iniciado', {
                'usuario_id': usuario_id,
                'tipo_descanso': 'corto',
                'duracion_min': descanso_duracion,
                'ciclo_id': str(ciclo['_id']),
            })
            
            return {
                'nuevo_estado': nuevo_estado,
                'pomodoro_actual': pomodoro_actual,
                'accion': 'descanso_corto',
                'datos_extra': {'duracion_min': descanso_duracion},
            }
    
    elif evento == "descanso_completado":
        if estado_actual == ESTADO_DESCANSO_LARGO:
            # Ciclo completado
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
            
            # Intentar iniciar siguiente ciclo automáticamente
            try:
                resultado_siguiente = iniciar_ciclo(usuario_id, config)
                return {
                    'nuevo_estado': ESTADO_TRABAJANDO,
                    'pomodoro_actual': 1,
                    'accion': 'nuevo_ciclo',
                    'datos_extra': resultado_siguiente,
                }
            except Exception:
                # No se pudo iniciar (no hay tiempo o hay activo)
                return {
                    'nuevo_estado': ESTADO_INACTIVO,
                    'pomodoro_actual': 0,
                    'accion': 'fin_jornada',
                    'datos_extra': {},
                }
        else:
            # Descanso corto terminó, siguiente pomodoro
            siguiente_pomodoro = pomodoro_actual + 1
            
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
                'datos_extra': {'duracion_min': config['pomodoro_min']},
            }
    
    # No debería llegar aquí
    raise ValueError(f"Evento '{evento}' no manejado en estado '{estado_actual}'")
