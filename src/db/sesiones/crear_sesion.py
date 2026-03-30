"""
Módulo: crear_sesion.py
Responsabilidad: Crear una nueva sesión de trabajo.
"""

from datetime import datetime
from bson import ObjectId
from ..conexion import conexion_global


def crear_sesion(usuario_id: str, tipo_sesion: str = "pomodoro") -> dict:
    """
    Crea una nueva sesión de trabajo.
    
    Args:
        usuario_id (str): ID del usuario
        tipo_sesion (str): Tipo ("pomodoro"|"pausa"|"trabajo"). Default: "pomodoro"
    
    Returns:
        dict: Documento de sesión creada
            {
                '_id': ObjectId,
                'usuario_id': ObjectId,
                'tipo_sesion': str,
                'inicio': datetime,
                'fin': None,
                'duracion_segundos': None,
                'pausas_utilizadas': 0,
                'completada': False
            }
    
    Raises:
        ValueError: Si validación falla
        TypeError: Si tipos incorrectos
        Exception: Si usuario no existe
    """
    if not isinstance(usuario_id, str):
        raise TypeError(f"usuario_id debe ser string, recibido: {type(usuario_id).__name__}")
    if not isinstance(tipo_sesion, str):
        raise TypeError(f"tipo_sesion debe ser string, recibido: {type(tipo_sesion).__name__}")
    
    tipo_sesion = tipo_sesion.strip().lower()
    tipos_validos = {"pomodoro", "pausa", "trabajo"}
    if tipo_sesion not in tipos_validos:
        raise ValueError(f"tipo_sesion debe ser uno de {tipos_validos}, recibido: {tipo_sesion}")
    
    try:
        usuario_objeto_id = ObjectId(usuario_id)
    except Exception:
        raise ValueError(f"usuario_id inválido: '{usuario_id}'")
    
    # Verificar que usuario existe
    coleccion_usuarios = conexion_global.obtener_coleccion('usuarios')
    usuario = coleccion_usuarios.find_one({'_id': usuario_objeto_id})
    if usuario is None:
        raise Exception(f"Usuario con ID '{usuario_id}' no existe")
    
    # Crear sesión
    sesion = {
        'usuario_id': usuario_objeto_id,
        'tipo_sesion': tipo_sesion,
        'inicio': datetime.utcnow(),
        'fin': None,
        'duracion_segundos': None,
        'pausas_utilizadas': 0,
        'completada': False
    }
    
    coleccion_sesiones = conexion_global.obtener_coleccion('sesiones')
    resultado = coleccion_sesiones.insert_one(sesion)
    sesion['_id'] = resultado.inserted_id
    
    return sesion
