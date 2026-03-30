"""
Función: obtener_por_usuario()
Responsabilidad: Obtener todas las anomalías de un usuario específico.

Parámetros:
    usuario_id (str): ID del usuario (ObjectId en string format)
    limite (int): Número máximo de anomalías a retornar (default: 50)

Retorna:
    list: Lista de documentos de anomalías ordenados por fecha (más recientes primero)

Excepciones:
    TypeError: Si usuario_id no es string o limite no es int
    ValueError: Si usuario_id no es ObjectId válido o limite < 1
    Exception: Si usuario no existe
"""

from bson import ObjectId
from ..conexion import conexion_global


def obtener_por_usuario(usuario_id: str, limite: int = 50) -> list:
    """Obtiene todas las anomalías de un usuario."""
    
    # Validaciones de tipo
    if not isinstance(usuario_id, str):
        raise TypeError(f"usuario_id debe ser string, recibido: {type(usuario_id).__name__}")
    if not isinstance(limite, int):
        raise TypeError(f"limite debe ser int, recibido: {type(limite).__name__}")
    
    # Validaciones de valor
    if not usuario_id.strip():
        raise ValueError("usuario_id no puede estar vacío")
    if limite < 1:
        raise ValueError(f"limite debe ser >= 1, recibido: {limite}")
    
    # Validar ObjectId format
    try:
        usuario_oid = ObjectId(usuario_id)
    except Exception:
        raise ValueError(f"usuario_id '{usuario_id}' no es un ObjectId válido")
    
    # Verificar que el usuario existe
    db = conexion_global
    coleccion_usuarios = db.obtener_coleccion('usuarios')
    usuario = coleccion_usuarios.find_one({'_id': usuario_oid})
    
    if not usuario:
        raise Exception(f"Usuario con ID '{usuario_id}' no existe")
    
    # Obtener anomalías ordenadas por fecha (más recientes primero)
    coleccion_anomalias = conexion_global.obtener_coleccion('anomalias')
    anomalias = list(
        coleccion_anomalias.find({'usuario_id': usuario_oid})
                          .sort('fecha_registro', -1)
                          .limit(limite)
    )
    
    return anomalias
