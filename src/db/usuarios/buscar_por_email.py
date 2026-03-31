"""
Módulo: buscar_por_email.py
Responsabilidad: Buscar un usuario por su email.
"""

from bson import ObjectId
from src.db.conexion import conexion_global


def buscar_por_email(email: str) -> dict:
    """
    Busca un usuario por email.
    
    Args:
        email (str): Email del usuario a buscar
    
    Returns:
        dict: Documento del usuario si existe, None si no existe
        
    Raises:
        ValueError: Si email está vacío
        TypeError: Si email no es string
    """
    if not isinstance(email, str):
        raise TypeError(f"Email debe ser string, recibido: {type(email).__name__}")
    
    email = email.strip()
    if not email:
        raise ValueError("Email no puede estar vacío")
    
    coleccion = conexion_global.obtener_coleccion('usuarios')
    usuario = coleccion.find_one({'email': email})
    
    return usuario
