"""
Módulo: servicio_sesiones.py
Responsabilidad: Capa intermedia entre el timer y la base de datos.
Registra sesiones Pomodoro individuales en la colección "sesiones".
NO sabe nada de threading ni lógica de ciclos.
"""

from datetime import datetime, timezone
from ..db.conexion import conexion_global


def registrar_sesion_pomodoro(usuario_id: str, datos_ciclo: dict, duracion_min: int) -> dict:
    """
    Registra una sesión Pomodoro completada en la base de datos.
    
    Esta función es llamada por ciclo_pomodoro cuando un pomodoro termina.
    Solo recibe datos limpios y los guarda en MongoDB.
    
    Args:
        usuario_id (str): ID del usuario
        datos_ciclo (dict): Datos del ciclo al que pertenece:
            - _id: ID del ciclo
            - numero_ciclo: número del ciclo
            - pomodoro_actual: pomodoro que se completó
        duracion_min (int): Duración del pomodoro en minutos
    
    Returns:
        dict: Documento de la sesión creada
    """
    if not isinstance(usuario_id, str):
        raise TypeError(f"usuario_id debe ser string, recibido: {type(usuario_id).__name__}")
    if not isinstance(datos_ciclo, dict):
        raise TypeError(f"datos_ciclo debe ser dict, recibido: {type(datos_ciclo).__name__}")
    if not isinstance(duracion_min, int):
        raise TypeError(f"duracion_min debe ser int, recibido: {type(duracion_min).__name__}")
    
    from bson import ObjectId
    try:
        usuario_oid = ObjectId(usuario_id)
    except Exception:
        raise ValueError(f"usuario_id inválido: '{usuario_id}'")
    
    ahora = datetime.now(timezone.utc)
    
    sesion = {
        'usuario_id': usuario_oid,
        'ciclo_id': datos_ciclo.get('_id'),
        'numero_ciclo': datos_ciclo.get('numero_ciclo', 1),
        'tipo_sesion': 'pomodoro',
        'pomodoro_numero': datos_ciclo.get('pomodoro_actual', 1),
        'inicio': ahora,
        'duracion_programada_min': duracion_min,
        'duracion_segundos': duracion_min * 60,
    }
    
    coleccion = conexion_global.obtener_coleccion('sesiones')
    resultado = coleccion.insert_one(sesion)
    sesion['_id'] = resultado.inserted_id
    
    return sesion
