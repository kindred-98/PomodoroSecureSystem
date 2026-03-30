"""
Módulo: crear_equipo.py
Responsabilidad: Crear un nuevo equipo.
"""

from datetime import datetime
from bson import ObjectId
from ..conexion import conexion_global


def crear_equipo(nombre: str, encargado_id: str, descripcion: str = "") -> dict:
    """
    Crea un nuevo equipo en la base de datos.
    
    Args:
        nombre (str): Nombre del equipo
        encargado_id (str): ID del usuario encargado (debe ser rol 'encargado' o 'supervisor')
        descripcion (str): Descripción del equipo (opcional)
    
    Returns:
        dict: Documento del equipo creado
            {
                '_id': ObjectId,
                'nombre': str,
                'encargado_id': ObjectId,
                'descripcion': str,
                'miembros': [],
                'fecha_creacion': datetime,
                'activo': True
            }
    
    Raises:
        ValueError: Si validación falla
        TypeError: Si tipos incorrectos
        Exception: Si encargado no existe
    """
    if not isinstance(nombre, str):
        raise TypeError(f"nombre debe ser string, recibido: {type(nombre).__name__}")
    if not isinstance(encargado_id, str):
        raise TypeError(f"encargado_id debe ser string, recibido: {type(encargado_id).__name__}")
    if not isinstance(descripcion, str):
        raise TypeError(f"descripcion debe ser string, recibido: {type(descripcion).__name__}")
    
    nombre = nombre.strip()
    descripcion = descripcion.strip()
    
    if not nombre:
        raise ValueError("Nombre no puede estar vacío")
    
    # Verificar que encargado existe
    try:
        encargado_objeto_id = ObjectId(encargado_id)
    except Exception:
        raise ValueError(f"encargado_id inválido: '{encargado_id}'")
    
    coleccion_usuarios = conexion_global.obtener_coleccion('usuarios')
    encargado = coleccion_usuarios.find_one({'_id': encargado_objeto_id})
    if encargado is None:
        raise Exception(f"Encargado con ID '{encargado_id}' no existe")
    
    # Crear equipo
    equipo = {
        'nombre': nombre,
        'encargado_id': encargado_objeto_id,
        'descripcion': descripcion,
        'miembros': [encargado_objeto_id],  # El encargado es el primer miembro
        'fecha_creacion': datetime.utcnow(),
        'activo': True
    }
    
    coleccion_equipos = conexion_global.obtener_coleccion('equipos')
    resultado = coleccion_equipos.insert_one(equipo)
    equipo['_id'] = resultado.inserted_id
    
    return equipo
