"""
Módulo: logout.py
Responsabilidad: Cierre de sesión de usuarios.
"""

from .sesion import cerrar_sesion_por_token


def cerrar_sesion(token_sesion: str) -> bool:
    """
    Cierra la sesión activa de un usuario.
    
    Args:
        token_sesion (str): Token de la sesión a cerrar
    
    Returns:
        bool: True si se cerró correctamente
    
    Raises:
        TypeError: Si token_sesion no es string
        ValueError: Si token_sesion está vacío
        Exception: Si sesión no encontrada o ya cerrada
    """
    if not isinstance(token_sesion, str):
        raise TypeError(f"token_sesion debe ser string, recibido: {type(token_sesion).__name__}")
    if not token_sesion.strip():
        raise ValueError("token_sesion no puede estar vacío")
    
    return cerrar_sesion_por_token(token_sesion)
