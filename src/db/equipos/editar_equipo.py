"""
Módulo: editar_equipo.py
Responsabilidad: Editar nombre de equipo.
"""

from bson import ObjectId
from src.db.conexion import conexion_global


def editar_nombre(equipo_id: str, nuevo_nombre: str) -> dict:
    """
    Edita el nombre de un equipo.
    
    Args:
        equipo_id (str): ID del equipo
        nuevo_nombre (str): Nuevo nombre
    
    Returns:
        dict: Equipo actualizado o None si no existe
    
    Raises:
        ValueError: Si ID o nombre inválido
    """
    if not nuevo_nombre.strip():
        raise ValueError("El nombre no puede estar vacío")
    
    try:
        oid = ObjectId(equipo_id)
    except Exception:
        raise ValueError(f"ID inválido: '{equipo_id}'")
    
    coleccion = conexion_global.obtener_coleccion('equipos')
    resultado = coleccion.find_one_and_update(
        {'_id': oid},
        {'$set': {'nombre': nuevo_nombre.strip()}},
        return_document=True
    )
    
    return resultado


def asignar_encargado(equipo_id: str, encargado_id: str) -> dict:
    """
    Asigna un encargado a un equipo.
    
    Args:
        equipo_id (str): ID del equipo
        encargado_id (str): ID del usuario encargado
    
    Returns:
        dict: Equipo actualizado o None si no existe
    
    Raises:
        ValueError: Si IDs inválidos
    """
    try:
        oid_equipo = ObjectId(equipo_id)
        oid_encargado = ObjectId(encargado_id)
    except Exception:
        raise ValueError("ID inválido")
    
    coleccion = conexion_global.obtener_coleccion('equipos')
    resultado = coleccion.find_one_and_update(
        {'_id': oid_equipo},
        {'$set': {'encargado_id': oid_encargado}},
        return_document=True
    )
    
    return resultado


def quitar_miembro(equipo_id: str, miembro_id: str) -> dict:
    """
    Quita un miembro de un equipo.
    
    Args:
        equipo_id (str): ID del equipo
        miembro_id (str): ID del usuario a quitar
    
    Returns:
        dict: Equipo actualizado o None si no existe
    
    Raises:
        ValueError: Si IDs inválidos
    """
    try:
        oid_equipo = ObjectId(equipo_id)
        oid_miembro = ObjectId(miembro_id)
    except Exception:
        raise ValueError("ID inválido")
    
    coleccion = conexion_global.obtener_coleccion('equipos')
    resultado = coleccion.find_one_and_update(
        {'_id': oid_equipo},
        {'$pull': {'miembros': oid_miembro}},
        return_document=True
    )
    
    return resultado


def eliminar_equipo(equipo_id: str) -> bool:
    """
    Elimina un equipo.
    
    Args:
        equipo_id (str): ID del equipo
    
    Returns:
        bool: True si se eliminó, False si no existía
    
    Raises:
        ValueError: Si ID inválido
    """
    try:
        oid = ObjectId(equipo_id)
    except Exception:
        raise ValueError(f"ID inválido: '{equipo_id}'")
    
    coleccion = conexion_global.obtener_coleccion('equipos')
    resultado = coleccion.delete_one({'_id': oid})
    
    return resultado.deleted_count > 0
