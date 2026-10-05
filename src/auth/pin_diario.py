"""
Módulo: pin_diario.py
Responsabilidad: Generar y verificar PIN diario de 6 dígitos.
Se genera al login o desde gestión de contraseña.
Se hashea con bcrypt. Solo se devuelve en texto plano en el momento de creación.
"""

import secrets
from datetime import datetime, timezone

from bson import ObjectId
from bson.errors import InvalidId

from src.seguridad.encriptacion import hashear_contrasena, verificar_contrasena
from src.db.conexion import conexion_global


def _validar_usuario_id(usuario_id: str) -> str:
    """Valida que usuario_id sea un string no vacío."""
    if not isinstance(usuario_id, str):
        raise TypeError(
            f"usuario_id debe ser string, recibido: {type(usuario_id).__name__}"
        )
    if not usuario_id.strip():
        raise ValueError("usuario_id no puede estar vacío")
    return usuario_id


def _validar_pin(pin_introducido: str) -> str:
    """Valida que el PIN sea un string no vacío."""
    if not isinstance(pin_introducido, str):
        raise TypeError(
            f"pin debe ser string, recibido: {type(pin_introducido).__name__}"
        )
    if not pin_introducido.strip():
        raise ValueError("pin no puede estar vacío")
    return pin_introducido


def _a_object_id(usuario_id: str):
    """Convierte a ObjectId; si no es válido, devuelve el valor original."""
    try:
        return ObjectId(usuario_id)
    except (InvalidId, TypeError):
        return usuario_id


def _coleccion_hoy():
    """Devuelve la colección de PINes junto con la fecha de hoy."""
    hoy = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return conexion_global.obtener_coleccion('pines_diarios'), hoy


def generar_pin_diario(usuario_id: str) -> str | None:
    """
    Genera un PIN de 6 dígitos para el día de hoy.
    Se llama al hacer login o desde la pantalla de gestión de contraseña.
    Solo se guarda su hash en BD.

    Returns:
        str: El PIN en texto plano si se generó ahora (solo esta vez).
        None: Si ya existía un PIN para hoy (ya no recuperable).
    """
    usuario_oid = _a_object_id(_validar_usuario_id(usuario_id))

    # Verificar si ya tiene PIN para hoy
    coleccion, hoy = _coleccion_hoy()
    existente = coleccion.find_one({
        'usuario_id': usuario_oid,
        'fecha': hoy,
    })

    if existente is not None:
        return None  # Ya tiene PIN para hoy, no recuperable

    # Generar PIN de 6 dígitos
    pin = str(secrets.randbelow(900000) + 100000)
    pin_hash = hashear_contrasena(pin)

    ahora = datetime.now(timezone.utc)
    coleccion.insert_one({
        'usuario_id': usuario_oid,
        'fecha': hoy,
        'pin_hash': pin_hash,
        'intentos_fallidos': 0,
        'ultimo_intento': ahora,
    })

    return pin  # Se devuelve UNA sola vez, después solo existe el hash


def eliminar_pin_diario(usuario_id: str) -> bool:
    """
    Elimina el PIN del día para permitir generar uno nuevo.
    Útil si el usuario perdió el PIN y necesita uno nuevo.

    Returns:
        bool: True si se eliminó, False si no había PIN.
    """
    usuario_oid = _a_object_id(_validar_usuario_id(usuario_id))
    coleccion, hoy = _coleccion_hoy()

    resultado = coleccion.delete_one({
        'usuario_id': usuario_oid,
        'fecha': hoy,
    })

    return resultado.deleted_count > 0


def obtener_ultimo_pin(usuario_id: str) -> dict | None:
    """
    Obtiene el registro del último PIN generado hoy.

    Returns:
        dict: Registro del PIN o None.
    """
    usuario_oid = _a_object_id(_validar_usuario_id(usuario_id))
    coleccion, hoy = _coleccion_hoy()

    return coleccion.find_one({
        'usuario_id': usuario_oid,
        'fecha': hoy,
    })


def verificar_pin_diario(usuario_id: str, pin_introducido: str) -> bool:
    """
    Verifica si el PIN introducido coincide con el del día.

    Returns:
        bool: True si es correcto
    """
    usuario_oid = _a_object_id(_validar_usuario_id(usuario_id))
    pin_introducido = _validar_pin(pin_introducido)

    coleccion, hoy = _coleccion_hoy()
    registro = coleccion.find_one({
        'usuario_id': usuario_oid,
        'fecha': hoy,
    })

    if registro is None:
        return False

    correcto = verificar_contrasena(pin_introducido, registro['pin_hash'])

    if not correcto:
        coleccion.update_one(
            {'_id': registro['_id']},
            {'$inc': {'intentos_fallidos': 1}}
        )

    return correcto
