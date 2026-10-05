"""
Módulo: auth/__init__.py
Responsabilidad: Exportar funciones de autenticación y gestión de contraseñas.
"""

from src.auth.registro import registrar_usuario
from src.auth.login import iniciar_sesion
from src.auth.logout import cerrar_sesion
from src.auth.sesion import crear_sesion, verificar_sesion, cerrar_sesion_por_token
from src.auth.ver_contrasena import ver_contrasena
from src.auth.regenerar_contrasena import regenerar_contrasena
from src.auth.cambiar_contrasena import cambiar_contrasena
from src.auth.exportar_contrasena import exportar_contrasena
from src.auth.verificacion_email import (
    crear_token_verificacion,
    verificar_token_legacy as verificar_token,
    verificar_email_esta_verificado,
    obtener_token_pendiente,
    crear_o_actualizar_verificacion,
    verificar_token_db,
    enviar_token_por_email,
    esta_verificado,
)
from src.excepciones import ErrorRecursoNoEncontrado


def obtener_contrasena(usuario_id: str) -> str:
    """
    Obtiene la contraseña desencriptada del usuario.
    Sin verificación (el usuario ya está autenticado).
    """
    from bson import ObjectId
    from src.db.conexion import conexion_global
    from src.seguridad.encriptacion import descifrar
    
    try:
        oid = ObjectId(usuario_id)
    except Exception:
        raise ValueError("ID inválido")
    
    coleccion = conexion_global.obtener_coleccion('usuarios')
    usuario = coleccion.find_one({'_id': oid})
    
    if not usuario:
        raise ErrorRecursoNoEncontrado("Usuario no encontrado")
    
    return descifrar(usuario.get('contraseña_encriptada', ''))

__all__ = [
    "registrar_usuario",
    "iniciar_sesion",
    "cerrar_sesion",
    "crear_sesion",
    "verificar_sesion",
    "cerrar_sesion_por_token",
    "ver_contrasena",
    "regenerar_contrasena",
    "cambiar_contrasena",
    "exportar_contrasena",
    "obtener_contrasena",
    "crear_token_verificacion",
    "crear_o_actualizar_verificacion",
    "verificar_token",
    "verificar_token_db",
    "verificar_email_esta_verificado",
    "obtener_token_pendiente",
    "enviar_token_por_email",
    "esta_verificado",
]
