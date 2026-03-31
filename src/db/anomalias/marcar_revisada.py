"""
Función: marcar_revisada()
Responsabilidad: Marcar una anomalía como revisada.

Parámetros:
    anomalia_id (str): ID de la anomalía (ObjectId en string format)

Retorna:
    dict: Documento de anomalía actualizado

Excepciones:
    TypeError: Si anomalia_id no es string
    ValueError: Si anomalia_id no es ObjectId válido o está vacío
    Exception: Si anomalía no existe
"""

from datetime import datetime, timezone
from bson import ObjectId
from src.db.conexion import conexion_global


def marcar_revisada(anomalia_id: str) -> dict:
    """Marca una anomalía como revisada."""
    
    # Validaciones de tipo
    if not isinstance(anomalia_id, str):
        raise TypeError(f"anomalia_id debe ser string, recibido: {type(anomalia_id).__name__}")
    
    # Validaciones de valor
    if not anomalia_id.strip():
        raise ValueError("anomalia_id no puede estar vacío")
    
    # Validar ObjectId format
    try:
        anomalia_oid = ObjectId(anomalia_id)
    except Exception:
        raise ValueError(f"anomalia_id '{anomalia_id}' no es un ObjectId válido")
    
    # Obtener la colección
    db = conexion_global
    coleccion_anomalias = db.obtener_coleccion('anomalias')
    
    # Verificar que la anomalía existe
    anomalia = coleccion_anomalias.find_one({'_id': anomalia_oid})
    if not anomalia:
        raise Exception(f"Anomalía con ID '{anomalia_id}' no existe")
    
    # Actualizar documento: marcar como revisada y registrar fecha de revisión
    actualizaciones = {
        'revisada': True,
        'fecha_revision': datetime.now(timezone.utc),
    }
    
    coleccion_anomalias.update_one(
        {'_id': anomalia_oid},
        {'$set': actualizaciones}
    )
    
    # Retornar documento actualizado
    anomalia_actualizada = coleccion_anomalias.find_one({'_id': anomalia_oid})
    
    return anomalia_actualizada
