"""
Módulo: crear_usuario.py
Responsabilidad: Crear un nuevo usuario en la base de datos.
"""

from datetime import datetime, timezone
from bson import ObjectId
from ..conexion import conexion_global


def crear_usuario(email: str, nombre: str, contraseña_hash: str, rol: str = "empleado") -> dict:
    """
    Crea un nuevo usuario en la base de datos.
    
    Args:
        email (str): Email único del usuario
        nombre (str): Nombre completo del usuario
        contraseña_hash (str): Hash bcrypt de la contraseña
        rol (str): Rol del usuario ("empleado"|"encargado"|"supervisor"). Default: "empleado"
    
    Returns:
        dict: Documento del usuario creado con _id
            {
                '_id': ObjectId,
                'email': str,
                'nombre': str,
                'contraseña_hash': str,
                'rol': str,
                'activo': True,
                'fecha_registro': datetime,
                'ultimo_acceso': None,
                'puntuacion_pomodoro': 0,
                'team_id': None,
                'metadata': {...}
            }
    
    Raises:
        ValueError: Si validación falla (email vacío, rol inválido)
        TypeError: Si tipos de parámetro son incorrectos
        Exception: Si el email ya existe (duplicado)
    """
    # Validación
    if not isinstance(email, str):
        raise TypeError(f"Email debe ser string, recibido: {type(email).__name__}")
    if not isinstance(nombre, str):
        raise TypeError(f"Nombre debe ser string, recibido: {type(nombre).__name__}")
    if not isinstance(contraseña_hash, str):
        raise TypeError(f"Contraseña_hash debe ser string, recibido: {type(contraseña_hash).__name__}")
    if not isinstance(rol, str):
        raise TypeError(f"Rol debe ser string, recibido: {type(rol).__name__}")
    
    email = email.strip()
    nombre = nombre.strip()
    rol = rol.lower().strip()
    
    if not email:
        raise ValueError("Email no puede estar vacío")
    if not nombre:
        raise ValueError("Nombre no puede estar vacío")
    if not contraseña_hash:
        raise ValueError("Contraseña_hash no puede estar vacía")
    
    roles_validos = {"empleado", "encargado", "supervisor"}
    if rol not in roles_validos:
        raise ValueError(f"Rol debe ser uno de {roles_validos}, recibido: {rol}")
    
    # Verificar que email no exista
    coleccion = conexion_global.obtener_coleccion('usuarios')
    if coleccion.find_one({'email': email}):
        raise Exception(f"El email '{email}' ya está registrado")
    
    # Crear documento
    usuario = {
        'email': email,
        'nombre': nombre,
        'contraseña_hash': contraseña_hash,
        'rol': rol,
        'activo': True,
        'fecha_registro': datetime.now(timezone.utc),
        'ultimo_acceso': None,
        'puntuacion_pomodoro': 0,
        'team_id': None,
        'metadata': {
            'ciclos_completados': 0,
            'pausas_utilizadas': 0,
            'anomalias_registradas': 0
        }
    }
    
    # Insertar en BD
    resultado = coleccion.insert_one(usuario)
    usuario['_id'] = resultado.inserted_id
    
    return usuario
