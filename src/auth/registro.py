"""
Módulo: registro.py
Responsabilidad: Flujo completo de registro de nuevos usuarios.
"""

from src.seguridad.encriptacion import hashear_contraseña, cifrar
from src.generador import generar_contraseña
from src.db.usuarios import crear_usuario
from src.db.conexion import conexion_global
from src.auth.audit import audit_registro


import re

# Longitud mínima y máxima permitida para el TLD del dominio
_TLD_MINIMO = 2
_TLD_MAXIMO = 10

# Roles que puede solicitar el usuario en el registro
_ROLES_SOLICITABLES = {"empleado"}


_NOMBRES_TIPO = {str: "string", dict: "dict"}


def _validar_tipo(campo: str, valor, tipo_esperado: type) -> None:
    """Lanza TypeError si el valor no es del tipo esperado."""
    if not isinstance(valor, tipo_esperado):
        nombre_esperado = _NOMBRES_TIPO.get(tipo_esperado, tipo_esperado.__name__)
        raise TypeError(
            f"{campo} debe ser {nombre_esperado}, "
            f"recibido: {type(valor).__name__}"
        )


def _validar_tld(tld: str) -> None:
    """Valida el TLD del dominio: longitud y solo letras."""
    if len(tld) < _TLD_MINIMO:
        raise ValueError("El TLD debe tener mínimo 2 caracteres")
    if len(tld) > _TLD_MAXIMO:
        raise ValueError("El TLD debe tener máximo 10 caracteres")
    if not tld.isalpha():
        raise ValueError("El TLD solo puede contener letras")


def _validar_parte_local(local: str) -> None:
    """Valida la parte previa al @ del email."""
    if local.startswith(".") or local.endswith("."):
        raise ValueError("El email no puede empezar o terminar con punto")
    if ".." in local:
        raise ValueError("El email no puede tener puntos consecutivos")
    if not re.match(r"^[a-zA-Z0-9._+-]+$", local):
        raise ValueError("El email contiene caracteres inválidos")


def _validar_dominio(dominio: str) -> None:
    """Valida el dominio del email y su TLD."""
    if "." not in dominio:
        raise ValueError("El dominio debe tener un punto")
    if dominio.startswith("."):
        raise ValueError("El dominio no puede empezar con punto")

    dominio_partes = dominio.rsplit(".", 1)
    if len(dominio_partes) != 2 or not dominio_partes[0]:
        raise ValueError("El dominio debe tener un TLD válido")

    _validar_tld(dominio_partes[1])


def _validar_email(email: str) -> str:
    """Valida el formato completo del email y lo devuelve normalizado."""
    email = email.strip().lower()

    if not email:
        raise ValueError("email no puede estar vacío")
    if "@" not in email:
        raise ValueError("El email debe contener @")

    partes = email.split("@")
    if len(partes) != 2 or not partes[0] or not partes[1]:
        raise ValueError("El formato del email es inválido")

    local, dominio = partes
    _validar_parte_local(local)
    _validar_dominio(dominio)

    return email


def _resolver_rol(rol: str, es_primer_usuario: bool) -> str:
    """El primer usuario siempre es supervisor; el resto se limita a empleado."""
    if es_primer_usuario:
        return "supervisor"
    return rol if rol in _ROLES_SOLICITABLES else "empleado"


def registrar_usuario(
    email: str,
    nombre: str,
    rol: str,
    parametros_contrasena: dict
) -> dict:
    """
    Registra un nuevo usuario con contraseña generada por el sistema.
    
    Flujo de 4 pasos:
    1. Valida datos personales
    2. Genera contraseña con los parámetros proporcionados
    3. Crea hash (bcrypt) + encripta (Fernet)
    4. Guarda en base de datos
    
    Args:
        email (str): Email único del usuario
        nombre (str): Nombre completo
        rol (str): "empleado" | "encargado" | "supervisor"
        parametros_contraseña (dict): Parámetros para generar contraseña:
            - longitud (int): 8-128
            - usar_mayusculas (bool)
            - usar_numeros (bool)
            - usar_simbolos (bool)
            - excluir_ambiguos (bool)
    
    Returns:
        dict: {
            'usuario': dict (documento del usuario creado),
            'contraseña_generada': str (solo visible una vez)
        }
    
    Raises:
        TypeError: Si tipos de parámetro son incorrectos
        ValueError: Si validación falla
    """
    # Validación de tipos
    _validar_tipo("email", email, str)
    _validar_tipo("nombre", nombre, str)
    _validar_tipo("rol", rol, str)
    _validar_tipo("parametros_contraseña", parametros_contrasena, dict)

    # Validación de valores
    email = _validar_email(email)
    nombre = nombre.strip()
    rol = rol.lower().strip()

    if not nombre:
        raise ValueError("nombre no puede estar vacío")

    # Verificar si es el primer usuario para forzar supervisor
    coleccion = conexion_global.obtener_coleccion('usuarios')
    es_primer_usuario = coleccion.count_documents({}) == 0

    rol = _resolver_rol(rol, es_primer_usuario)

    # Determinar tipo de contraseña: personalizada vs generada por sistema
    tipo = parametros_contrasena.get("tipo", "sistema")

    # Valores por defecto si params vacío
    params = {
        "longitud": parametros_contrasena.get("longitud", 16),
        "usar_mayusculas": parametros_contrasena.get("usar_mayusculas", True),
        "usar_numeros": parametros_contrasena.get("usar_numeros", True),
        "usar_simbolos": parametros_contrasena.get("usar_simbolos", True),
        "excluir_ambiguos": parametros_contrasena.get("excluir_ambiguos", False),
    }

    if tipo == "personalizada":
        contrasena_generada = parametros_contrasena.get("contraseña", "")
        if not contrasena_generada:
            raise ValueError("Contraseña personalizada no proporcionada")
    else:
        contrasena_generada = generar_contraseña(params)

    # Crear hash para verificación de login (no reversible)
    contrasena_hash = hashear_contraseña(contrasena_generada)

    # Encriptar para recuperación del usuario (reversible)
    contrasena_encriptada = cifrar(contrasena_generada)

    # Guardar en base de datos (inicialmente no verificado)
    usuario = crear_usuario(email, nombre, contrasena_hash, rol)

    # Actualizar campos en una sola operación
    coleccion.update_one(
        {'_id': usuario['_id']},
        {'$set': {
            'email_verificado': False,
            'fecha_verificacion': None,
            'contraseña_encriptada': contrasena_encriptada,
            'parametros_contraseña': params
        }}
    )
    usuario['email_verificado'] = False
    usuario['fecha_verificacion'] = None
    usuario['contraseña_encriptada'] = contrasena_encriptada
    usuario['parametros_contraseña'] = params

    audit_registro(email, True)

    return {
        'usuario': usuario,
        'contraseña_generada': contrasena_generada
    }
