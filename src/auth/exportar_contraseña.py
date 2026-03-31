"""
Módulo: exportar_contraseña.py
Responsabilidad: Exportar contraseña del usuario a archivo JSON encriptado.
"""

import json
import os
from src.db.conexion import conexion_global
from src.seguridad.encriptacion import descifrar, cifrar


def exportar_contraseña(usuario_id: str, ruta_destino: str) -> str:
    """
    Exporta la contraseña del usuario a un archivo JSON encriptado.
    
    El archivo generado solo puede ser leído por la propia aplicación
    usando la misma clave Fernet.
    
    Args:
        usuario_id (str): ID del usuario
        ruta_destino (str): Ruta donde guardar el archivo
    
    Returns:
        str: Ruta del archivo creado
    
    Raises:
        TypeError: Si tipos son incorrectos
        ValueError: Si campos vacíos, ID inválido o ruta inválida
        Exception: Si usuario no encontrado o error de escritura
    """
    if not isinstance(usuario_id, str):
        raise TypeError(f"usuario_id debe ser string, recibido: {type(usuario_id).__name__}")
    if not isinstance(ruta_destino, str):
        raise TypeError(f"ruta_destino debe ser string, recibido: {type(ruta_destino).__name__}")
    
    if not usuario_id.strip():
        raise ValueError("usuario_id no puede estar vacío")
    if not ruta_destino.strip():
        raise ValueError("ruta_destino no puede estar vacía")
    
    from bson import ObjectId
    try:
        objeto_id = ObjectId(usuario_id)
    except Exception:
        raise ValueError(f"usuario_id inválido: '{usuario_id}'")
    
    # Verificar que el directorio existe
    directorio = os.path.dirname(ruta_destino)
    if directorio and not os.path.isdir(directorio):
        raise ValueError(f"El directorio no existe: {directorio}")
    
    coleccion = conexion_global.obtener_coleccion('usuarios')
    usuario = coleccion.find_one({'_id': objeto_id})
    
    if usuario is None:
        raise Exception("Usuario no encontrado")
    
    # Obtener y desencriptar la contraseña
    contraseña_encriptada = usuario.get('contraseña_encriptada', '')
    if not contraseña_encriptada:
        raise Exception("No hay contraseña encriptada para exportar")
    
    contraseña = descifrar(contraseña_encriptada)
    
    # Crear JSON con datos del usuario
    datos_exportacion = {
        'email': usuario.get('email', ''),
        'nombre': usuario.get('nombre', ''),
        'contraseña': contraseña,
        'parametros': usuario.get('parametros_contraseña', {}),
        'exportado_en': str(os.path.basename(ruta_destino))
    }
    
    json_texto = json.dumps(datos_exportacion, indent=2, ensure_ascii=False)
    
    # Encriptar el JSON completo
    json_cifrado = cifrar(json_texto)
    
    # Escribir archivo
    ruta_completa = ruta_destino
    if not ruta_completa.endswith('.enc'):
        ruta_completa += '.enc'
    
    with open(ruta_completa, 'w', encoding='utf-8') as archivo:
        archivo.write(json_cifrado)
    
    return ruta_completa
