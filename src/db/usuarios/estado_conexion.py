"""
Módulo: estado_conexion.py
Responsabilidad: Verificar si un usuario está actualmente conectado.
"""

from datetime import datetime, timezone, timedelta
from src.db.conexion import conexion_global


def obtener_estado_todos_los_usuarios() -> list:
    """
    Obtiene el estado de conexión de todos los usuarios activos.
    Se considera conectado si tiene un ciclo Pomodoro activo (no completado).
    
    Returns:
        list: Lista de dicts con {usuario_id, nombre, email, rol, conectado, ultima_conexion}
    """
    coleccion_ciclos = conexion_global.obtener_coleccion('ciclos_pomodoro')
    coleccion_usuarios = conexion_global.obtener_coleccion('usuarios')
    
    # Obtener ciclos activos (no completados)
    ciclos_activos = list(coleccion_ciclos.find({
        'completado': False
    }))
    
    # Crear set de usuarios conectados
    usuarios_conectados = set()
    for ciclo in ciclos_activos:
        uid = ciclo.get('usuario_id')
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
    Se considera conectado si tiene un ciclo Pomodoro activo.
    
    Args:
        usuario_id (str): ID del usuario
    
    Returns:
        bool: True si está conectado
    """
    try:
        from bson import ObjectId
        coleccion = conexion_global.obtener_coleccion('ciclos_pomodoro')
        
        ciclo_activo = coleccion.find_one({
            'usuario_id': ObjectId(usuario_id),
            'completado': False,
        })
        
        return ciclo_activo is not None
    except Exception:
        return False


def _buscar_ciclo(usuario_id: str, completado: bool):
    """Devuelve el ciclo del usuario filtrando por completado, o None."""
    from bson import ObjectId

    coleccion_ciclos = conexion_global.obtener_coleccion('ciclos_pomodoro')
    return coleccion_ciclos.find_one({
        'usuario_id': ObjectId(usuario_id),
        'completado': completado,
    })


def _estado_texto(ciclo) -> str:
    """Traduce el estado actual del ciclo a texto para la UI."""
    estado = ciclo.get('estado_actual', 'TRABAJANDO')
    if estado in ('DESCANSO_CORTO', 'DESCANSO_LARGO'):
        return "En descanso"
    return "Trabajando"


def _ultimo_ciclo_finalizado(usuario_id: str):
    """Devuelve el ciclo completado más reciente, o None."""
    from bson import ObjectId

    coleccion = conexion_global.obtener_coleccion('ciclos_pomodoro')
    return coleccion.find_one(
        {'usuario_id': ObjectId(usuario_id), 'completado': True},
        sort=[('fin_ciclo', -1)]
    )


def _asegurar_utc(valor):
    """Normaliza a UTC un datetime naive devuelto por MongoDB."""
    if hasattr(valor, 'tzinfo') and valor.tzinfo is None:
        return valor.replace(tzinfo=timezone.utc)
    return valor


def formatear_minutos_desconectado(minutos: int) -> str:
    """Convierte minutos desconectados en texto legible."""
    if minutos < 1:
        return "Hace menos de 1 minuto"
    if minutos < 60:
        return f"Hace {minutos} min"
    return f"Hace {minutos // 60}h {minutos % 60}m"


def obtener_tiempo_desconectado(usuario_id: str) -> str:
    """
    Obtiene el tiempo desde la última desconexión.
    
    Args:
        usuario_id (str): ID del usuario
    
    Returns:
        str: Texto con el tiempo desconectado o "Conectado"
    """
    try:
        ciclo_activo = _buscar_ciclo(usuario_id, False)
        if ciclo_activo:
            return _estado_texto(ciclo_activo)

        ultimo = _ultimo_ciclo_finalizado(usuario_id)
        if ultimo and 'fin_ciclo' in ultimo:
            ahora = _asegurar_utc(datetime.now(timezone.utc))
            fin = _asegurar_utc(ultimo['fin_ciclo'])
            minutos = int((ahora - fin).total_seconds() / 60)
            return formatear_minutos_desconectado(minutos)

        return "Sin actividad reciente"
    except Exception:
        return "Desconocido"
