"""
Función: obtener_por_equipo()
Responsabilidad: Obtener todas las anomalías de los miembros de un equipo.

Parámetros:
    equipo_id (str): ID del equipo (ObjectId en string format)
    limite (int): Número máximo de anomalías a retornar (default: 100)

Retorna:
    list: Lista de documentos de anomalías ordenados por fecha (más recientes primero)
          Incluye información del usuario mediante lookup

Excepciones:
    TypeError: Si equipo_id no es string o limite no es int
    ValueError: Si equipo_id no es ObjectId válido o limite < 1
    Exception: Si equipo no existe
"""

from bson import ObjectId
from ..conexion import conexion_global


def obtener_por_equipo(equipo_id: str, limite: int = 100) -> list:
    """Obtiene todas las anomalías de los miembros de un equipo."""
    
    # Validaciones de tipo
    if not isinstance(equipo_id, str):
        raise TypeError(f"equipo_id debe ser string, recibido: {type(equipo_id).__name__}")
    if not isinstance(limite, int):
        raise TypeError(f"limite debe ser int, recibido: {type(limite).__name__}")
    
    # Validaciones de valor
    if not equipo_id.strip():
        raise ValueError("equipo_id no puede estar vacío")
    if limite < 1:
        raise ValueError(f"limite debe ser >= 1, recibido: {limite}")
    
    # Validar ObjectId format
    try:
        equipo_oid = ObjectId(equipo_id)
    except Exception:
        raise ValueError(f"equipo_id '{equipo_id}' no es un ObjectId válido")
    
    # Verificar que el equipo existe
    db = conexion_global
    coleccion_equipos = db.obtener_coleccion('equipos')
    equipo = coleccion_equipos.find_one({'_id': equipo_oid})
    
    if not equipo:
        raise Exception(f"Equipo con ID '{equipo_id}' no existe")
    
    # Obtener lista de IDs de miembros del equipo
    miembros_ids = equipo.get('miembros', [])
    
    if not miembros_ids:
        return []
    
    # Obtener anomalías de todos los miembros
    coleccion_anomalias = conexion_global.obtener_coleccion('anomalias')
    anomalias = list(
        coleccion_anomalias.find({'usuario_id': {'$in': miembros_ids}})
                          .sort('fecha_registro', -1)
                          .limit(limite)
    )
    
    return anomalias
