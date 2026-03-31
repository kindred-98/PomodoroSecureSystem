"""
Módulo: regenerar_contraseña.py
Responsabilidad: Regenerar la contraseña de un usuario con nuevos parámetros.
"""

from ..db.conexion import conexion_global
from ..seguridad.encriptacion import hashear_contraseña, cifrar
from ..generador import generar_contraseña


def regenerar_contraseña(usuario_id: str, nuevos_parametros: dict) -> dict:
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
        raise Exception("Usuario no encontrado")
    
    # Generar nueva contraseña
    nueva_contraseña = generar_contraseña(nuevos_parametros)
    
    # Crear nuevo hash y encriptación
    nuevo_hash = hashear_contraseña(nueva_contraseña)
    nueva_encriptada = cifrar(nueva_contraseña)
    
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
        'nueva_contraseña': nueva_contraseña,
        'mensaje': "Contraseña regenerada exitosamente"
    }
