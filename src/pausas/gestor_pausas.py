"""
Módulo: gestor_pausas.py
Responsabilidad: Gestionar pausas manuales del trabajador.
Reglas: máximo 2 pausas por jornada, máximo 10 min cada una.
"""

from datetime import datetime, timezone
from bson import ObjectId
from src.db.conexion import conexion_global

MAXIMO_PAUSAS = 2
MAXIMO_DURACION_MIN = 10


def limpiar_pausa_huerfana(usuario_id: str) -> bool:
    """
    Limpia pausas huérfanas (activa en BD pero sin timer activo).
    Esto puede pasar si el programa se cerró durante una pausa.
    Función pública para usar desde otros módulos.
    
    Args:
        usuario_id (str): ID del usuario
    
    Returns:
        bool: True si se limpió una pausa huérfana
    """
    try:
        from bson import ObjectId
        usuario_oid = ObjectId(usuario_id)
    except Exception:
        return False
    
    coleccion_pausas = conexion_global.obtener_coleccion('pausas_manuales')
    
    pausa_huerfana = coleccion_pausas.find_one({
        'usuario_id': usuario_oid,
        'activa': True,
    })
    
    if pausa_huerfana:
        ahora = datetime.now(timezone.utc)
        inicio = pausa_huerfana.get('inicio')
        
        if hasattr(inicio, 'tzinfo') and inicio.tzinfo is None and hasattr(ahora, 'tzinfo') and ahora.tzinfo is not None:
            ahora = ahora.replace(tzinfo=None)
        
        duracion = int((ahora - inicio).total_seconds() / 60) if inicio else 0
        
        coleccion_pausas.update_one(
            {'_id': pausa_huerfana['_id']},
            {'$set': {
                'fin': ahora,
                'duracion_minutos': duracion,
                'activa': False,
                'excedida': duracion > MAXIMO_DURACION_MIN,
                'limpieza_automatica': True,
            }}
        )
        return True
    
    return False


def iniciar_pausa(usuario_id: str) -> dict:
    """
    Inicia una pausa manual para el usuario.
    
    Reglas:
    - Debe haber un ciclo activo
    - No puede haber otra pausa activa
    - Máximo 2 pausas por jornada
    
    Args:
        usuario_id (str): ID del usuario
    
    Returns:
        dict: {
            'pausa_id': str,
            'inicio': datetime,
            'pausas_usadas': int,
            'pausas_restantes': int,
        }
    
    Raises:
        TypeError: Si usuario_id no es string
        ValueError: Si usuario_id vacío
        Exception: Si no cumple las reglas de pausas
    """
    if not isinstance(usuario_id, str):
        raise TypeError(f"usuario_id debe ser string, recibido: {type(usuario_id).__name__}")
    if not usuario_id.strip():
        raise ValueError("usuario_id no puede estar vacío")
    
    from bson import ObjectId
    try:
        usuario_oid = ObjectId(usuario_id)
    except Exception:
        raise ValueError(f"usuario_id inválido: '{usuario_id}'")
    
    # Verificar ciclo activo
    coleccion_ciclos = conexion_global.obtener_coleccion('ciclos_pomodoro')
    ciclo_activo = coleccion_ciclos.find_one({
        'usuario_id': usuario_oid,
        'completado': False,
    })
    
    if ciclo_activo is None:
        raise RuntimeError("No hay ciclo Pomodoro activo. Inicia un ciclo primero.")
    
    # Limpiar pausa huérfana si existe (timer no está en estado pausado pero hay pausa en BD)
    limpiar_pausa_huerfana(usuario_id)
    
    # Verificar que no hay pausa activa
    coleccion_pausas = conexion_global.obtener_coleccion('pausas_manuales')
    pausa_activa = coleccion_pausas.find_one({
        'usuario_id': usuario_oid,
        'activa': True,
    })
    
    if pausa_activa is not None:
        raise RuntimeError("Ya tienes una pausa activa. Finalízala antes de iniciar otra.")
    
    # Contar pausas de hoy
    hoy_inicio = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    pausas_hoy = coleccion_pausas.count_documents({
        'usuario_id': usuario_oid,
        'inicio': {'$gte': hoy_inicio},
    })
    
    if pausas_hoy >= MAXIMO_PAUSAS:
        raise ValueError(
            f"Máximo de pausas alcanzado ({MAXIMO_PAUSAS}/{MAXIMO_PAUSAS}). "
            f"Ya no puedes tomar más pausas hoy."
        )
    
    # Registrar pausa
    ahora = datetime.now(timezone.utc)
    pausa = {
        'usuario_id': usuario_oid,
        'ciclo_id': ciclo_activo['_id'],
        'inicio': ahora,
        'fin': None,
        'duracion_minutos': None,
        'activa': True,
        'excedida': False,
    }
    
    resultado = coleccion_pausas.insert_one(pausa)
    pausa['_id'] = resultado.inserted_id
    
    pausas_usadas = pausas_hoy + 1
    
    return {
        'pausa_id': str(pausa['_id']),
        'inicio': ahora,
        'pausas_usadas': pausas_usadas,
        'pausas_restantes': MAXIMO_PAUSAS - pausas_usadas,
    }


def finalizar_pausa(usuario_id: str) -> dict:
    """
    Finaliza la pausa activa del usuario.
    
    Si la pausa supera los 10 minutos, registra una anomalía.
    
    Args:
        usuario_id (str): ID del usuario
    
    Returns:
        dict: {
            'pausa_id': str,
            'duracion_minutos': int,
            'excedida': bool,
            'anomalia': dict or None,
            'pausas_usadas': int,
        }
    
    Raises:
        TypeError: Si usuario_id no es string
        ValueError: Si usuario_id vacío
        Exception: Si no hay pausa activa
    """
    if not isinstance(usuario_id, str):
        raise TypeError(f"usuario_id debe ser string, recibido: {type(usuario_id).__name__}")
    if not usuario_id.strip():
        raise ValueError("usuario_id no puede estar vacío")
    
    from bson import ObjectId
    try:
        usuario_oid = ObjectId(usuario_id)
    except Exception:
        raise ValueError(f"usuario_id inválido: '{usuario_id}'")
    
    coleccion_pausas = conexion_global.obtener_coleccion('pausas_manuales')
    pausa_activa = coleccion_pausas.find_one({
        'usuario_id': usuario_oid,
        'activa': True,
    })
    
    if pausa_activa is None:
        raise RuntimeError("No hay pausa activa para finalizar")
    
    # Limpiar pausa huérfana si el timer no está en estado pausado
    
    ahora = datetime.now(timezone.utc)
    inicio = pausa_activa['inicio']
    
    # Manejar datetime naive de mongomock
    if hasattr(inicio, 'tzinfo') and inicio.tzinfo is None and hasattr(ahora, 'tzinfo') and ahora.tzinfo is not None:
        ahora_naive = ahora.replace(tzinfo=None)
        duracion_segundos = (ahora_naive - inicio).total_seconds()
    else:
        duracion_segundos = (ahora - inicio).total_seconds()
    
    duracion_minutos = int(duracion_segundos / 60)
    excedida = duracion_minutos > MAXIMO_DURACION_MIN
    
    # Actualizar pausa
    pausa_actualizada = coleccion_pausas.find_one_and_update(
        {'_id': pausa_activa['_id']},
        {'$set': {
            'fin': ahora,
            'duracion_minutos': duracion_minutos,
            'activa': False,
            'excedida': excedida,
        }},
        return_document=True
    )
    
    # Crear reporte para supervisor y encargado
    try:
        _crear_reporte_pausa(usuario_id, pausa_actualizada, duracion_minutos)
    except Exception:
        pass
    
    anomalia_registrada = None
    
    if excedida:
        # Registrar anomalía
        from src.db.anomalias import registrar_anomalia
        anomalia_registrada = registrar_anomalia(
            str(usuario_oid),
            'pausa_excedida',
            f"Pausa manual excedió {MAXIMO_DURACION_MIN} min. "
            f"Duración real: {duracion_minutos} min."
        )
    
    # Contar pausas totales hoy
    hoy_inicio = ahora.replace(hour=0, minute=0, second=0, microsecond=0)
    pausas_hoy = coleccion_pausas.count_documents({
        'usuario_id': usuario_oid,
        'inicio': {'$gte': hoy_inicio},
    })
    
    return {
        'pausa_id': str(pausa_activa['_id']),
        'duracion_minutos': duracion_minutos,
        'excedida': excedida,
        'anomalia': anomalia_registrada,
        'pausas_usadas': pausas_hoy,
    }


def resetear_pausas_jornada(usuario_id: str) -> bool:
    """
    Resetea las pausas de la jornada actual.
    Se llama cuando el usuario presiona 'Fin de Jornada'.
    
    Args:
        usuario_id (str): ID del usuario
    
    Returns:
        bool: True si se reseteó correctamente
    """
    try:
        usuario_oid = ObjectId(usuario_id)
    except Exception:
        return False
    
    coleccion_pausas = conexion_global.obtener_coleccion('pausas_manuales')
    
    # Eliminar todas las pausas de hoy
    hoy_inicio = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    coleccion_pausas.delete_many({
        'usuario_id': usuario_oid,
        'inicio': {'$gte': hoy_inicio},
    })
    
    return True


def _obtener_usuario_info(usuario_id: str) -> dict:
    """Obtiene información del usuario (nombre, email, rol)."""
    try:
        from bson import ObjectId
        coleccion = conexion_global.obtener_coleccion('usuarios')
        usuario = coleccion.find_one({'_id': ObjectId(usuario_id)})
        if usuario:
            return {
                'nombre': usuario.get('nombre', 'Sin nombre'),
                'email': usuario.get('email', ''),
                'rol': usuario.get('rol', 'empleado'),
            }
    except Exception:
        pass
    return {}


def _obtener_supervisor_encargado(usuario_id: str) -> tuple:
    """
    Obtiene el ID del supervisor y encargado del equipo del usuario.
    
    Returns:
        tuple: (supervisor_id, encargado_id)
    """
    try:
        from bson import ObjectId
        coleccion_equipos = conexion_global.obtener_coleccion('equipos')
        
        # Buscar equipo que contenga al usuario
        equipo = coleccion_equipos.find_one({
            'miembros': ObjectId(usuario_id)
        })
        
        if equipo:
            return (str(equipo.get('supervisor_id', '')), str(equipo.get('encargado_id', '')))
    except Exception:
        pass
    return (None, None)


def _crear_reporte_pausa(usuario_id: str, pausa_doc: dict, duracion_min: int):
    """
    Crea un reporte de pausa para supervisor y encargado.
    
    Args:
        usuario_id (str): ID del usuario
        pausa_doc (dict): Documento de la pausa
        duracion_min (int): Duración en minutos
    """
    try:
        usuario_info = _obtener_usuario_info(usuario_id)
        supervisor_id, encargado_id = _obtener_supervisor_encargado(usuario_id)
        
        if not supervisor_id and not encargado_id:
            return
        
        reporte = {
            'usuario_id': ObjectId(usuario_id),
            'tipo': 'pausa',
            'nombre_usuario': usuario_info.get('nombre', 'Sin nombre'),
            'email_usuario': usuario_info.get('email', ''),
            'pausa_id': pausa_doc.get('_id'),
            'inicio': pausa_doc.get('inicio'),
            'fin': pausa_doc.get('fin'),
            'duracion_minutos': duracion_min,
            'excedida': pausa_doc.get('excedida', False),
            'fecha_registro': datetime.now(timezone.utc),
            'leido': False,
            'destinatarios': [sid for sid in [supervisor_id, encargado_id] if sid],
        }
        
        coleccion = conexion_global.obtener_coleccion('reportes_pausas')
        coleccion.insert_one(reporte)
    except Exception:
        pass
