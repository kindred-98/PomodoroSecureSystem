"""
Módulo: pin_diario.py
Responsabilidad: Generar y verificar PIN diario de 6 dígitos.
Se genera al login, se hashea con bcrypt, nunca se muestra de nuevo.
"""

import secrets
from datetime import datetime, timezone
from src.seguridad.encriptacion import hashear_contraseña, verificar_contraseña
from src.db.conexion import conexion_global


def generar_pin_diario(usuario_id: str) -> None:
    """
    Genera un PIN de 6 dígitos para el día de hoy.
    Se llama al hacer login. El PIN nunca se muestra al usuario.
    Solo se guarda su hash en BD.
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
        return  # Ya tiene PIN para hoy

    # Generar PIN de 6 dígitos
    pin = str(secrets.randbelow(900000) + 100000)
    pin_hash = hashear_contraseña(pin)

    coleccion.insert_one({
        'usuario_id': usuario_oid,
        'fecha': hoy,
        'pin_hash': pin_hash,
        'intentos_fallidos': 0,
    })


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
