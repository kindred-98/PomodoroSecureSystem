"""
Módulo: reportes.py
Responsabilidad: Generar reportes de actividad del usuario para supervisor/encargado.
"""

from datetime import datetime, timezone
from src.db.conexion import conexion_global


def crear_reporte_jornada(
    usuario_id: str,
    fecha: datetime,
    ciclos_iniciados: int,
    ciclos_completados: int,
    pomodoros_totales: int,
    tiempo_trabajado_segundos: int,
    tiempo_descanso_segundos: int,
    pausas_utilizadas: int,
    jornada_reset: bool = False,
    motivo_reset: str = None,
) -> str:
    """
    Crea un reporte de la jornada laboral del usuario.
    
    Este reporte es enviado al supervisor y encargado del equipo.
    
    Args:
        usuario_id (str): ID del usuario
        fecha (datetime): Fecha y hora del reporte
        ciclos_iniciados (int): Número de ciclos iniciados
        ciclos_completados (int): Número de ciclos completados
        pomodoros_totales (int): Total de pomodoros completados
        tiempo_trabajado_segundos (int): Tiempo total trabajado
        tiempo_descanso_segundos (int): Tiempo total en descansos
        pausas_utilizadas (int): Pausas manuales usadas
        jornada_reset (bool): Si la jornada fue reseteada manualmente
        motivo_reset (str): Motivo del reset si aplica
    
    Returns:
        str: ID del reporte creado
    """
    from bson import ObjectId
    
    coleccion_reportes = conexion_global.obtener_coleccion('reportes_jornada')
    coleccion_usuarios = conexion_global.obtener_coleccion('usuarios')
    
    try:
        usuario_oid = ObjectId(usuario_id)
    except Exception:
        raise ValueError(f"usuario_id inválido: '{usuario_id}'")
    
    # Obtener datos del usuario para saber quién es su supervisor/encargado
    usuario = coleccion_usuarios.find_one({'_id': usuario_oid})
    
    reporte = {
        'usuario_id': usuario_oid,
        'usuario_nombre': usuario.get('nombre', 'Desconocido') if usuario else 'Desconocido',
        'usuario_email': usuario.get('email', '') if usuario else '',
        'fecha_reporte': datetime.now(timezone.utc),
        'fecha_jornada': fecha,
        'ciclos_iniciados': ciclos_iniciados,
        'ciclos_completados': ciclos_completados,
        'pomodoros_totales': pomodoros_totales,
        'tiempo_trabajado_segundos': tiempo_trabajado_segundos,
        'tiempo_trabajado_texto': _formatear_tiempo(tiempo_trabajado_segundos),
        'tiempo_descanso_segundos': tiempo_descanso_segundos,
        'tiempo_descanso_texto': _formatear_tiempo(tiempo_descanso_segundos),
        'pausas_utilizadas': pausas_utilizadas,
        'jornada_reset': jornada_reset,
        'motivo_reset': motivo_reset,
        'leido_supervisor': False,
        'leido_encargado': False,
    }
    
    # Si el usuario pertenece a un equipo, agregar info del equipo
    if usuario and usuario.get('team_id'):
        reporte['team_id'] = usuario['team_id']
    
    resultado = coleccion_reportes.insert_one(reporte)
    return str(resultado.inserted_id)


def crear_reporte_expiracion(
    usuario_id: str,
    estado_anterior: dict,
    motivo: str,
) -> str:
    """
    Crea un reporte especial cuando una sesión expira por inactividad.
    
    Args:
        usuario_id (str): ID del usuario
        estado_anterior (dict): Estado del timer antes del reset
        motivo (str): Razón de la expiración
    
    Returns:
        str: ID del reporte creado
    """
    from bson import ObjectId
    
    coleccion_reportes = conexion_global.obtener_coleccion('reportes_jornada')
    
    try:
        usuario_oid = ObjectId(usuario_id)
    except Exception:
        raise ValueError(f"usuario_id inválido: '{usuario_id}'")
    
    reporte = {
        'usuario_id': usuario_oid,
        'fecha_reporte': datetime.now(timezone.utc),
        'tipo_reporte': 'expiracion_sesion',
        'motivo': motivo,
        'estado_anterior': {
            'estado': estado_anterior.get('estado', 'DESCONOCIDO'),
            'pomodoro_actual': estado_anterior.get('pomodoro_actual', 0),
            'pomodoros_totales': estado_anterior.get('pomodoros_totales', 0),
            'ultima_actualizacion': estado_anterior.get('ultima_actualizacion'),
        },
        'leido_supervisor': False,
        'leido_encargado': False,
    }
    
    resultado = coleccion_reportes.insert_one(reporte)
    return str(resultado.inserted_id)


def obtener_reportes_para_supervisor(limit: int = 50) -> list:
    """
    Obtiene los reportes pendientes para el supervisor.
    
    Args:
        limit (int): Máximo número de reportes a retornar
    
    Returns:
        list: Lista de reportes no leídos
    """
    coleccion_reportes = conexion_global.obtener_coleccion('reportes_jornada')
    
    reportes = list(
        coleccion_reportes.find({'leido_supervisor': False})
        .sort('fecha_reporte', -1)
        .limit(limit)
    )
    
    # Convertir ObjectId a string para serialización
    for reporte in reportes:
        reporte['_id'] = str(reporte['_id'])
        reporte['usuario_id'] = str(reporte['usuario_id'])
        if reporte.get('team_id'):
            reporte['team_id'] = str(reporte['team_id'])
    
    return reportes


def obtener_reportes_para_encargado(encargado_id: str, limit: int = 50) -> list:
    """
    Obtiene los reportes de los equipos del encargado.
    
    Args:
        encargado_id (str): ID del encargado
        limit (int): Máximo número de reportes a retornar
    
    Returns:
        list: Lista de reportes de sus equipos
    """
    from bson import ObjectId
    
    coleccion_reportes = conexion_global.obtener_coleccion('reportes_jornada')
    coleccion_equipos = conexion_global.obtener_coleccion('equipos')
    
    try:
        encargado_oid = ObjectId(encargado_id)
    except Exception:
        return []
    
    # Obtener IDs de los equipos del encargado
    equipos = list(coleccion_equipos.find({'encargado_id': encargado_oid}))
    team_ids = [eq['_id'] for eq in equipos]
    
    if not team_ids:
        return []
    
    # Obtener reportes de usuarios en esos equipos
    reportes = list(
        coleccion_reportes.find({
            'team_id': {'$in': team_ids},
            'leido_encargado': False,
        })
        .sort('fecha_reporte', -1)
        .limit(limit)
    )
    
    for reporte in reportes:
        reporte['_id'] = str(reporte['_id'])
        reporte['usuario_id'] = str(reporte['usuario_id'])
        reporte['team_id'] = str(reporte['team_id'])
    
    return reportes


def marcar_reporte_leido_supervisor(reporte_id: str) -> bool:
    """Marca un reporte como leído por el supervisor."""
    from bson import ObjectId
    
    try:
        reporte_oid = ObjectId(reporte_id)
    except Exception:
        return False
    
    coleccion_reportes = conexion_global.obtener_coleccion('reportes_jornada')
    resultado = coleccion_reportes.update_one(
        {'_id': reporte_oid},
        {'$set': {'leido_supervisor': True}}
    )
    return resultado.modified_count > 0


def marcar_reporte_leido_encargado(reporte_id: str) -> bool:
    """Marca un reporte como leído por el encargado."""
    from bson import ObjectId
    
    try:
        reporte_oid = ObjectId(reporte_id)
    except Exception:
        return False
    
    coleccion_reportes = conexion_global.obtener_coleccion('reportes_jornada')
    resultado = coleccion_reportes.update_one(
        {'_id': reporte_oid},
        {'$set': {'leido_encargado': True}}
    )
    return resultado.modified_count > 0


def _formatear_tiempo(segundos: int) -> str:
    """
    Formatea segundos a texto legible.
    
    Args:
        segundos (int): Segundos a formatear
    
    Returns:
        str: Tiempo formateado (ej: "2h 30m" o "45m")
    """
    if segundos < 60:
        return f"{segundos}s"
    
    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    
    if horas > 0:
        return f"{horas}h {minutos}m"
    else:
        return f"{minutos}m"
