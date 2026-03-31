"""
Módulo: gestor_pausas.py
Responsabilidad: Gestionar pausas manuales del trabajador.
Reglas: máximo 2 pausas por jornada, máximo 10 min cada una.
"""

from datetime import datetime, timezone
from src.db.conexion import conexion_global

MAXIMO_PAUSAS = 2
MAXIMO_DURACION_MIN = 10


def iniciar_pausa(usuario_id: str) -> dict:
    """
    Inicia una pausa manual para el usuario.
    
    Reglas:
    - Debe haber un ciclo activo
    - No puede haber otra pausa activa
    - Máximo 2 pausas por jornada
    
    Args:
        usuario_id (str): ID del usuario
    
    Returns:
        dict: {
            'pausa_id': str,
            'inicio': datetime,
            'pausas_usadas': int,
            'pausas_restantes': int,
        }
    
    Raises:
        TypeError: Si usuario_id no es string
        ValueError: Si usuario_id vacío
        Exception: Si no cumple las reglas de pausas
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
    
    # Verificar ciclo activo
    coleccion_ciclos = conexion_global.obtener_coleccion('ciclos_pomodoro')
    ciclo_activo = coleccion_ciclos.find_one({
        'usuario_id': usuario_oid,
        'completado': False,
    })
    
    if ciclo_activo is None:
        raise Exception("No hay ciclo Pomodoro activo. Inicia un ciclo primero.")
    
    # Verificar que no hay pausa activa
    coleccion_pausas = conexion_global.obtener_coleccion('pausas_manuales')
    pausa_activa = coleccion_pausas.find_one({
        'usuario_id': usuario_oid,
        'activa': True,
    })
    
    if pausa_activa is not None:
        raise Exception("Ya tienes una pausa activa. Finalízala antes de iniciar otra.")
    
    # Contar pausas de hoy
    hoy_inicio = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    pausas_hoy = coleccion_pausas.count_documents({
        'usuario_id': usuario_oid,
        'inicio': {'$gte': hoy_inicio},
    })
    
    if pausas_hoy >= MAXIMO_PAUSAS:
        raise Exception(
            f"Máximo de pausas alcanzado ({MAXIMO_PAUSAS}/{MAXIMO_PAUSAS}). "
            f"Ya no puedes tomar más pausas hoy."
        )
    
    # Registrar pausa
    ahora = datetime.now(timezone.utc)
    pausa = {
        'usuario_id': usuario_oid,
        'ciclo_id': ciclo_activo['_id'],
        'inicio': ahora,
        'fin': None,
        'duracion_minutos': None,
        'activa': True,
        'excedida': False,
    }
    
    resultado = coleccion_pausas.insert_one(pausa)
    pausa['_id'] = resultado.inserted_id
    
    pausas_usadas = pausas_hoy + 1
    
    return {
        'pausa_id': str(pausa['_id']),
        'inicio': ahora,
        'pausas_usadas': pausas_usadas,
        'pausas_restantes': MAXIMO_PAUSAS - pausas_usadas,
    }


def finalizar_pausa(usuario_id: str) -> dict:
    """
    Finaliza la pausa activa del usuario.
    
    Si la pausa supera los 10 minutos, registra una anomalía.
    
    Args:
        usuario_id (str): ID del usuario
    
    Returns:
        dict: {
            'pausa_id': str,
            'duracion_minutos': int,
            'excedida': bool,
            'anomalia': dict or None,
            'pausas_usadas': int,
        }
    
    Raises:
        TypeError: Si usuario_id no es string
        ValueError: Si usuario_id vacío
        Exception: Si no hay pausa activa
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
    
    coleccion_pausas = conexion_global.obtener_coleccion('pausas_manuales')
    pausa_activa = coleccion_pausas.find_one({
        'usuario_id': usuario_oid,
        'activa': True,
    })
    
    if pausa_activa is None:
        raise Exception("No hay pausa activa para finalizar")
    
    ahora = datetime.now(timezone.utc)
    inicio = pausa_activa['inicio']
    
    # Manejar datetime naive de mongomock
    if hasattr(inicio, 'tzinfo') and inicio.tzinfo is None and hasattr(ahora, 'tzinfo') and ahora.tzinfo is not None:
        ahora_naive = ahora.replace(tzinfo=None)
        duracion_segundos = (ahora_naive - inicio).total_seconds()
    else:
        duracion_segundos = (ahora - inicio).total_seconds()
    
    duracion_minutos = int(duracion_segundos / 60)
    excedida = duracion_minutos > MAXIMO_DURACION_MIN
    
    # Actualizar pausa
    coleccion_pausas.update_one(
        {'_id': pausa_activa['_id']},
        {'$set': {
            'fin': ahora,
            'duracion_minutos': duracion_minutos,
            'activa': False,
            'excedida': excedida,
        }}
    )
    
    anomalia_registrada = None
    
    if excedida:
        # Registrar anomalía
        from src.db.anomalias import registrar_anomalia
        anomalia_registrada = registrar_anomalia(
            str(usuario_oid),
            'pausa_excedida',
            f"Pausa manual excedió {MAXIMO_DURACION_MIN} min. "
            f"Duración real: {duracion_minutos} min."
        )
    
    # Contar pausas totales hoy
    hoy_inicio = ahora.replace(hour=0, minute=0, second=0, microsecond=0)
    pausas_hoy = coleccion_pausas.count_documents({
        'usuario_id': usuario_oid,
        'inicio': {'$gte': hoy_inicio},
    })
    
    return {
        'pausa_id': str(pausa_activa['_id']),
        'duracion_minutos': duracion_minutos,
        'excedida': excedida,
        'anomalia': anomalia_registrada,
        'pausas_usadas': pausas_hoy,
    }
