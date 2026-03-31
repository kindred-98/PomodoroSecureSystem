"""
Función: registrar_anomalia()
Responsabilidad: Registrar una nueva anomalía en la base de datos.

Parámetros:
    usuario_id (str): ID del usuario (ObjectId en string format)
    tipo (str): Tipo de anomalía (ej: "LOGIN_FALLIDO", "SESION_ABRUPTA", etc.)
    descripcion (str): Descripción de la anomalía

Retorna:
    dict: Documento de anomalía creado con _id, usuario_id, tipo, descripcion, 
          fecha_registro, revisada

Excepciones:
    TypeError: Si parámetros no son strings
    ValueError: Si usuario_id no es ObjectId válido o parámetros vacíos
    Exception: Si usuario no existe o falla operación MongoDB
"""

from datetime import datetime, timezone
from bson import ObjectId
from ..conexion import conexion_global


def registrar_anomalia(usuario_id: str, tipo: str, descripcion: str) -> dict:
    """Registra una nueva anomalía asociada a un usuario."""
    
    # Validaciones de tipo
    if not isinstance(usuario_id, str):
        raise TypeError(f"usuario_id debe ser string, recibido: {type(usuario_id).__name__}")
    if not isinstance(tipo, str):
        raise TypeError(f"tipo debe ser string, recibido: {type(tipo).__name__}")
    if not isinstance(descripcion, str):
        raise TypeError(f"descripcion debe ser string, recibido: {type(descripcion).__name__}")
    
    # Validaciones de valor
    if not usuario_id.strip():
        raise ValueError("usuario_id no puede estar vacío")
    if not tipo.strip():
        raise ValueError("tipo no puede estar vacío")
    if not descripcion.strip():
        raise ValueError("descripcion no puede estar vacía")
    
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
    
    # Crear el documento de anomalía
    nueva_anomalia = {
        'usuario_id': usuario_oid,
        'tipo': tipo.strip(),
        'descripcion': descripcion.strip(),
        'fecha_registro': datetime.now(timezone.utc),
        'revisada': False,
    }
    
    # Insertar en la colección
    coleccion_anomalias = db.obtener_coleccion('anomalias')
    resultado = coleccion_anomalias.insert_one(nueva_anomalia)
    
    # Agregar el _id generado
    nueva_anomalia['_id'] = resultado.inserted_id
    
    return nueva_anomalia
