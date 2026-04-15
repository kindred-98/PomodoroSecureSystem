"""
Módulo: pin_diario.py
Responsabilidad: Generar y verificar PIN diario de 6 dígitos.
Se genera al login o desde gestión de contraseña.
Se hashea con bcrypt. Solo se devuelve en texto plano en el momento de creación.
"""

import secrets
from datetime import datetime, timezone
from src.seguridad.encriptacion import hashear_contraseña, verificar_contraseña
from src.db.conexion import conexion_global


def generar_pin_diario(usuario_id: str) -> str | None:
    """
    Genera un PIN de 6 dígitos para el día de hoy.
    Se llama al hacer login o desde la pantalla de gestión de contraseña.
    Solo se guarda su hash en BD.

    Returns:
        str: El PIN en texto plano si se generó ahora (solo esta vez).
        None: Si ya existía un PIN para hoy (ya no recuperable).
    """
    from bson import ObjectId
    try:
        usuario_oid = ObjectId(usuario_id)
    except Exception:
        usuario_oid = usuario_id

    # Verificar si ya tiene PIN para hoy
    hoy = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    coleccion = conexion_global.obtener_coleccion('pines_diarios')
    existente = coleccion.find_one({
        'usuario_id': usuario_oid,
        'fecha': hoy,
    })

    if existente is not None:
        return None  # Ya tiene PIN para hoy, no recuperable

    # Generar PIN de 6 dígitos
    pin = str(secrets.randbelow(900000) + 100000)
    pin_hash = hashear_contraseña(pin)

    coleccion.insert_one({
        'usuario_id': usuario_oid,
        'fecha': hoy,
        'pin_hash': pin_hash,
        'intentos_fallidos': 0,
    })

    return pin  # Se devuelve UNA sola vez, después solo existe el hash


def eliminar_pin_diario(usuario_id: str) -> bool:
    """
    Elimina el PIN del día para permitir generar uno nuevo.
    Útil si el usuario perdió el PIN y necesita uno nuevo.
    
    Returns:
        bool: True si se eliminó, False si no había PIN.
    """
    from bson import ObjectId
    try:
        usuario_oid = ObjectId(usuario_id)
    except Exception:
        usuario_oid = usuario_id

    hoy = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    coleccion = conexion_global.obtener_coleccion('pines_diarios')
    
    resultado = coleccion.delete_one({
        'usuario_id': usuario_oid,
        'fecha': hoy,
    })
    
    return resultado.deleted_count > 0


def verificar_pin_diario(usuario_id: str, pin_introducido: str) -> bool:
    """
    Verifica si el PIN introducido coincide con el del día.

    Returns:
        bool: True si es correcto
    """
    from bson import ObjectId
    try:
        usuario_oid = ObjectId(usuario_id)
    except Exception:
        usuario_oid = usuario_id

    hoy = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    coleccion = conexion_global.obtener_coleccion('pines_diarios')
    registro = coleccion.find_one({
        'usuario_id': usuario_oid,
        'fecha': hoy,
    })

    if registro is None:
        return False

    correcto = verificar_contraseña(pin_introducido, registro['pin_hash'])

    if not correcto:
        coleccion.update_one(
            {'_id': registro['_id']},
            {'$inc': {'intentos_fallidos': 1}}
        )

    return correcto