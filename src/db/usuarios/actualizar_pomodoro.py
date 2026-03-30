"""
Módulo: actualizar_pomodoro.py
Responsabilidad: Actualizar puntuación de Pomodoro del usuario.
"""

from bson import ObjectId
from ..conexion import conexion_global


def actualizar_pomodoro(usuario_id: str, incremento: int) -> dict:
    """
    Incrementa la puntuación de Pomodoro del usuario.
    
    Args:
        usuario_id (str): ID del usuario
        incremento (int): Puntos a agregar (puede ser negativo para restar)
    
    Returns:
        dict: Documento actualizado del usuario
        
    Raises:
        ValueError: Si validación falla
        TypeError: Si tipos incorrectos
        Exception: Si usuario no existe
    """
    if not isinstance(usuario_id, str):
        raise TypeError(f"usuario_id debe ser string, recibido: {type(usuario_id).__name__}")
    if not isinstance(incremento, int):
        raise TypeError(f"incremento debe ser int, recibido: {type(incremento).__name__}")
    
    try:
        objeto_id = ObjectId(usuario_id)
    except Exception:
        raise ValueError(f"ID inválido: '{usuario_id}'")
    
    coleccion = conexion_global.obtener_coleccion('usuarios')
    resultado = coleccion.find_one_and_update(
        {'_id': objeto_id},
        {'$inc': {'puntuacion_pomodoro': incremento}},
        return_document=True
    )
    
    if resultado is None:
        raise Exception(f"Usuario con ID '{usuario_id}' no existe")
    
    return resultado
