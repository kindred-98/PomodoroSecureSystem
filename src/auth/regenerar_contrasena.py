"""
Módulo: regenerar_contraseña.py
Responsabilidad: Regenerar la contraseña de un usuario con nuevos parámetros.
"""

from src.db.conexion import conexion_global
from src.seguridad.encriptacion import hashear_contrasena, cifrar
from src.generador import generar_contrasena
from src.excepciones import ErrorRecursoNoEncontrado


def regenerar_contrasena(usuario_id: str, nuevos_parametros: dict) -> dict:
    """
    Regenera la contraseña de un usuario con nuevos parámetros.
    
    Args:
        usuario_id (str): ID del usuario
        nuevos_parametros (dict): Nuevos parámetros para la contraseña:
            - longitud (int): 8-128
            - usar_mayusculas (bool)
            - usar_numeros (bool)
            - usar_simbolos (bool)
            - excluir_ambiguos (bool)
    
    Returns:
        dict: {
            'nueva_contraseña': str,
            'mensaje': str
        }
    
    Raises:
        TypeError: Si tipos son incorrectos
        ValueError: Si parámetros inválidos o ID inválido
        Exception: Si usuario no encontrado
    """
    if not isinstance(usuario_id, str):
        raise TypeError(f"usuario_id debe ser string, recibido: {type(usuario_id).__name__}")
    if not isinstance(nuevos_parametros, dict):
        raise TypeError(
            f"nuevos_parametros debe ser dict, "
            f"recibido: {type(nuevos_parametros).__name__}"
        )
    
    if not usuario_id.strip():
        raise ValueError("usuario_id no puede estar vacío")
    
    from bson import ObjectId
    try:
        objeto_id = ObjectId(usuario_id)
    except Exception:
        raise ValueError(f"usuario_id inválido: '{usuario_id}'")
    
    coleccion = conexion_global.obtener_coleccion('usuarios')
    usuario = coleccion.find_one({'_id': objeto_id})
    
    if usuario is None:
        raise ErrorRecursoNoEncontrado("Usuario no encontrado")
    
    # Generar nueva contraseña
    nueva_contrasena = generar_contrasena(nuevos_parametros)
    
    # Crear nuevo hash y encriptación
    nuevo_hash = hashear_contrasena(nueva_contrasena)
    nueva_encriptada = cifrar(nueva_contrasena)
    
    # Actualizar en base de datos
    coleccion.update_one(
        {'_id': objeto_id},
        {'$set': {
            'contraseña_hash': nuevo_hash,
            'contraseña_encriptada': nueva_encriptada,
            'parametros_contraseña': nuevos_parametros
        }}
    )
    
    return {
        'nueva_contraseña': nueva_contrasena,
        'mensaje': "Contraseña regenerada exitosamente"
    }
