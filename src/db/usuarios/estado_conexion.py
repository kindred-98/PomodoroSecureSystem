"""
Módulo: estado_conexion.py
Responsabilidad: Verificar si un usuario está actualmente conectado.
"""

from datetime import datetime, timezone, timedelta
from src.db.conexion import conexion_global


def obtener_estado_todos_los_usuarios() -> list:
    """
    Obtiene el estado de conexión de todos los usuarios activos.
    
    Returns:
        list: Lista de dicts con {usuario_id, nombre, email, rol, conectado, ultima_conexion}
    """
    coleccion_sesiones = conexion_global.obtener_coleccion('sesiones')
    coleccion_usuarios = conexion_global.obtener_coleccion('usuarios')
    
    # Obtener sesiones activas (no cerradas)
    sesiones_activas = list(coleccion_sesiones.find({
        'fin': None
    }))
    
    # Crear set de usuarios conectados
    usuarios_conectados = set()
    for sesion in sesiones_activas:
        uid = sesion.get('usuario_id')
        if uid:
            usuarios_conectados.add(str(uid))
    
    # Obtener todos los usuarios activos
    usuarios = list(coleccion_usuarios.find({'activo': True}))
    
    resultado = []
    for u in usuarios:
        uid = str(u['_id'])
        conectado = uid in usuarios_conectados
        
        resultado.append({
            'usuario_id': uid,
            'nombre': u.get('nombre', 'Sin nombre'),
            'email': u.get('email', ''),
            'rol': u.get('rol', 'empleado'),
            'conectado': conectado,
            'ultima_conexion': u.get('ultimo_acceso'),
        })
    
    return resultado


def esta_conectado(usuario_id: str) -> bool:
    """
    Verifica si un usuario está actualmente conectado.
    
    Args:
        usuario_id (str): ID del usuario
    
    Returns:
        bool: True si está conectado
    """
    try:
        from bson import ObjectId
        coleccion = conexion_global.obtener_coleccion('sesiones')
        
        sesion_activa = coleccion.find_one({
            'usuario_id': ObjectId(usuario_id),
            'fin': None,
        })
        
        return sesion_activa is not None
    except Exception:
        return False


def obtener_tiempo_desconectado(usuario_id: str) -> str:
    """
    Obtiene el tiempo desde la última desconexión.
    
    Args:
        usuario_id (str): ID del usuario
    
    Returns:
        str: Texto con el tiempo desconectado o "Conectado"
    """
    try:
        coleccion = conexion_global.obtener_coleccion('sesiones')
        from bson import ObjectId
        
        sesion = coleccion.find_one({
            'usuario_id': ObjectId(usuario_id),
            'fin': None,
        })
        
        if sesion:
            return "Conectado"
        
        # Buscar última sesión cerrada
        ultima = coleccion.find_one(
            {'usuario_id': ObjectId(usuario_id), 'fin': {'$ne': None}},
            sort=[('fin', -1)]
        )
        
        if ultima and 'fin' in ultima:
            ahora = datetime.now(timezone.utc)
            fin = ultima['fin']
            
            if hasattr(fin, 'tzinfo') and fin.tzinfo is None:
                fin = fin.replace(tzinfo=timezone.utc)
            if hasattr(ahora, 'tzinfo') and ahora.tzinfo is None:
                ahora = ahora.replace(tzinfo=timezone.utc)
            
            diferencia = ahora - fin
            minutos = int(diferencia.total_seconds() / 60)
            
            if minutos < 1:
                return "Hace menos de 1 minuto"
            elif minutos < 60:
                return f"Hace {minutos} min"
            else:
                horas = minutos // 60
                mins = minutos % 60
                return f"Hace {horas}h {mins}m"
        
        return "Sin actividad reciente"
    except Exception:
        return "Desconocido"
