"""
Módulo: registro.py
Responsabilidad: Flujo completo de registro de nuevos usuarios.
"""

from src.seguridad.encriptacion import hashear_contraseña, cifrar
from src.generador import generar_contraseña
from src.db.usuarios import crear_usuario
from src.db.conexion import conexion_global


def registrar_usuario(
    email: str,
    nombre: str,
    rol: str,
    parametros_contraseña: dict
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
    if not isinstance(email, str):
        raise TypeError(f"email debe ser string, recibido: {type(email).__name__}")
    if not isinstance(nombre, str):
        raise TypeError(f"nombre debe ser string, recibido: {type(nombre).__name__}")
    if not isinstance(rol, str):
        raise TypeError(f"rol debe ser string, recibido: {type(rol).__name__}")
    if not isinstance(parametros_contraseña, dict):
        raise TypeError(
            f"parametros_contraseña debe ser dict, "
            f"recibido: {type(parametros_contraseña).__name__}"
        )
    
    # Validación de valores
    import re
    
    email = email.strip().lower()
    nombre = nombre.strip()
    rol = rol.lower().strip()
    
    if not email:
        raise ValueError("email no puede estar vacío")
    
    # Validación de formato email
    if "@" not in email:
        raise ValueError("El email debe contener @")
    
    partes = email.split("@")
    if len(partes) != 2 or not partes[0] or not partes[1]:
        raise ValueError("El formato del email es inválido")
    
    local, dominio = partes
    
    # Local no puede empezar/terminar con punto
    if local.startswith(".") or local.endswith("."):
        raise ValueError("El email no puede empezar o terminar con punto")
    if ".." in local:
        raise ValueError("El email no puede tener puntos consecutivos")
    
    # Solo caracteres válidos en local
    if not re.match(r"^[a-zA-Z0-9._+-]+$", local):
        raise ValueError("El email contiene caracteres inválidos")
    
    # Dominio debe tener punto
    if "." not in dominio:
        raise ValueError("El dominio debe tener un punto")
    
    if dominio.startswith("."):
        raise ValueError("El dominio no puede empezar con punto")
    
    dominio_partes = dominio.rsplit(".", 1)
    if len(dominio_partes) != 2 or not dominio_partes[0]:
        raise ValueError("El dominio debe tener un TLD válido")
    
    tld = dominio_partes[1]
    if len(tld) < 2:
        raise ValueError("El TLD debe tener mínimo 2 caracteres")
    if len(tld) > 10:
        raise ValueError("El TLD debe tener máximo 10 caracteres")
    if not tld.isalpha():
        raise ValueError("El TLD solo puede contener letras")
    if not nombre:
        raise ValueError("nombre no puede estar vacío")
    
    # Verificar si es el primer usuario para forzar supervisor
    from src.db.conexion import conexion_global
    coleccion = conexion_global.obtener_coleccion('usuarios')
    es_primer_usuario = coleccion.count_documents({}) == 0
    
    if es_primer_usuario:
        rol = "supervisor"
    else:
        roles_validos = {"empleado"}
        if rol not in roles_validos:
            rol = "empleado"
    
    # Determinar tipo de contraseña: personalizada vs generada por sistema
    tipo = parametros_contraseña.get("tipo", "sistema")
    
    # Valores por defecto si params vacío
    params = {
        "longitud": parametros_contraseña.get("longitud", 16),
        "usar_mayusculas": parametros_contraseña.get("usar_mayusculas", True),
        "usar_numeros": parametros_contraseña.get("usar_numeros", True),
        "usar_simbolos": parametros_contraseña.get("usar_simbolos", True),
        "excluir_ambiguos": parametros_contraseña.get("excluir_ambiguos", False),
    }
    
    if tipo == "personalizada":
        contraseña_generada = parametros_contraseña.get("contraseña", "")
        if not contraseña_generada:
            raise ValueError("Contraseña personalizada no proporcionada")
    else:
        contraseña_generada = generar_contraseña(params)
    
    # Crear hash para verificación de login (no reversible)
    contraseña_hash = hashear_contraseña(contraseña_generada)
    
    # Encriptar para recuperación del usuario (reversible)
    contraseña_encriptada = cifrar(contraseña_generada)
    
    # Guardar en base de datos (inicialmente no verificado)
    usuario = crear_usuario(email, nombre, contraseña_hash, rol)
    
    # Campo email_verificado = False por defecto
    coleccion = conexion_global.obtener_coleccion('usuarios')
    coleccion.update_one(
        {'_id': usuario['_id']},
        {'$set': {'email_verificado': False, 'fecha_verificacion': None}}
    )
    usuario['email_verificado'] = False
    usuario['fecha_verificacion'] = None
    
    # Agregar campos de encriptación
    coleccion = conexion_global.obtener_coleccion('usuarios')
    coleccion.update_one(
        {'_id': usuario['_id']},
        {'$set': {
            'contraseña_encriptada': contraseña_encriptada,
            'parametros_contraseña': parametros_contraseña
        }}
    )
    usuario['contraseña_encriptada'] = contraseña_encriptada
    usuario['parametros_contraseña'] = parametros_contraseña
    
    return {
        'usuario': usuario,
        'contraseña_generada': contraseña_generada
    }
