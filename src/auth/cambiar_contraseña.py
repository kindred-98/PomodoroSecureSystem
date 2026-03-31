"""
Módulo: cambiar_contraseña.py
Responsabilidad: Cambio manual de contraseña por el usuario.
Requiere que la nueva contraseña alcance nivel "Muy Fuerte" (99%+).
"""

from src.db.conexion import conexion_global
from src.seguridad.encriptacion import hashear_contraseña, cifrar
from src.generador import evaluar_fortaleza


def cambiar_contraseña(usuario_id: str, nueva_contraseña: str) -> dict:
    """
    Permite al usuario cambiar su contraseña manualmente.
    
    La nueva contraseña DEBE alcanzar nivel "Muy Fuerte" (≥80 puntos)
    equivalente a lo que generan las contraseñas automáticas del sistema.
    
    Args:
        usuario_id (str): ID del usuario
        nueva_contraseña (str): Nueva contraseña deseada
    
    Returns:
        dict: {
            'mensaje': str,
            'fortaleza': dict (resultado de evaluar_fortaleza)
        }
    
    Raises:
        TypeError: Si tipos son incorrectos
        ValueError: Si contraseña no cumple nivel "Muy Fuerte"
        Exception: Si usuario no encontrado
    """
    if not isinstance(usuario_id, str):
        raise TypeError(f"usuario_id debe ser string, recibido: {type(usuario_id).__name__}")
    if not isinstance(nueva_contraseña, str):
        raise TypeError(
            f"nueva_contraseña debe ser string, "
            f"recibido: {type(nueva_contraseña).__name__}"
        )
    
    if not usuario_id.strip():
        raise ValueError("usuario_id no puede estar vacío")
    if not nueva_contraseña:
        raise ValueError("nueva_contraseña no puede estar vacía")
    
    from bson import ObjectId
    try:
        objeto_id = ObjectId(usuario_id)
    except Exception:
        raise ValueError(f"usuario_id inválido: '{usuario_id}'")
    
    # Evaluar fortaleza de la nueva contraseña
    resultado = evaluar_fortaleza(nueva_contraseña)
    
    if resultado['nivel'] != "Muy Fuerte":
        raise ValueError(
            f"La contraseña debe ser nivel 'Muy Fuerte'. "
            f"Nivel actual: {resultado['nivel']} "
            f"({resultado['puntuacion']}/100 puntos)"
        )
    
    coleccion = conexion_global.obtener_coleccion('usuarios')
    usuario = coleccion.find_one({'_id': objeto_id})
    
    if usuario is None:
        raise Exception("Usuario no encontrado")
    
    # Guardar
    nuevo_hash = hashear_contraseña(nueva_contraseña)
    nueva_encriptada = cifrar(nueva_contraseña)
    
    coleccion.update_one(
        {'_id': objeto_id},
        {'$set': {
            'contraseña_hash': nuevo_hash,
            'contraseña_encriptada': nueva_encriptada
        }}
    )
    
    return {
        'mensaje': "Contraseña cambiada exitosamente",
        'fortaleza': resultado
    }
