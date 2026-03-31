"""
Módulo: gestor_otp.py
Responsabilidad: Generar, verificar y gestionar códigos OTP
para validación de presencia del trabajador.
"""

import secrets
from datetime import datetime, timedelta, timezone
from ..seguridad.encriptacion import hashear_contraseña, verificar_contraseña
from ..db.conexion import conexion_global
from ..db.anomalias import registrar_anomalia

DURACION_OTP_SEGUNDOS = 420  # 7 minutos
MAXIMO_INTENTOS = 3


def generar_otp(usuario_id: str, ciclo_id: str = None) -> dict:
    """
    Genera un código OTP de 6 dígitos para validación de presencia.
    
    El código se genera con secrets (criptográficamente seguro),
    se hashea con bcrypt y se guarda en MongoDB.
    
    Args:
        usuario_id (str): ID del usuario
        ciclo_id (str, optional): ID del ciclo Pomodoro asociado
    
    Returns:
        dict: {
            'codigo': str (6 dígitos, solo visible esta vez),
            'expira_en_seg': int,
            'evento_id': str
        }
    
    Raises:
        TypeError: Si tipos son incorrectos
        ValueError: Si usuario_id está vacío o inválido
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
    
    # Generar código de 6 dígitos
    codigo = str(secrets.randbelow(900000) + 100000)
    
    # Hashear el código
    codigo_hash = hashear_contraseña(codigo)
    
    # Calcular expiración
    ahora = datetime.now(timezone.utc)
    expira = ahora + timedelta(seconds=DURACION_OTP_SEGUNDOS)
    
    # Preparar documento
    ciclo_oid = None
    if ciclo_id:
        try:
            ciclo_oid = ObjectId(ciclo_id)
        except Exception:
            pass
    
    evento = {
        'usuario_id': usuario_oid,
        'ciclo_id': ciclo_oid,
        'otp_hash': codigo_hash,
        'timestamp_generado': ahora,
        'timestamp_expira': expira,
        'intentos_fallidos': 0,
        'resuelto': False,
        'minutos_retraso': 0,
    }
    
    coleccion = conexion_global.obtener_coleccion('eventos_otp')
    resultado = coleccion.insert_one(evento)
    
    return {
        'codigo': codigo,
        'expira_en_seg': DURACION_OTP_SEGUNDOS,
        'evento_id': str(resultado.inserted_id),
    }


def verificar_otp(usuario_id: str, codigo_introducido: str) -> dict:
    """
    Verifica un código OTP introducido por el usuario.
    
    Maneja los 3 escenarios:
    - A) Correcto → reanuda sesión
    - B) 3 intentos fallidos → anomalía + requiere credenciales
    - C) Expirado → anomalía + minutos retraso
    
    Args:
        usuario_id (str): ID del usuario
        codigo_introducido (str): Código de 6 dígitos introducido
    
    Returns:
        dict: {
            'correcto': bool,
            'intentos_restantes': int,
            'expirado': bool,
            'requiere_credenciales': bool,
            'anomalia': dict or None
        }
    
    Raises:
        TypeError: Si tipos son incorrectos
        ValueError: Si usuario_id está vacío o inválido
    """
    if not isinstance(usuario_id, str):
        raise TypeError(f"usuario_id debe ser string, recibido: {type(usuario_id).__name__}")
    if not isinstance(codigo_introducido, str):
        raise TypeError(f"codigo_introducido debe ser string, recibido: {type(codigo_introducido).__name__}")
    if not usuario_id.strip():
        raise ValueError("usuario_id no puede estar vacío")
    
    from bson import ObjectId
    try:
        usuario_oid = ObjectId(usuario_id)
    except Exception:
        raise ValueError(f"usuario_id inválido: '{usuario_id}'")
    
    # Buscar OTP activo
    coleccion = conexion_global.obtener_coleccion('eventos_otp')
    evento = coleccion.find_one({
        'usuario_id': usuario_oid,
        'resuelto': False,
    })
    
    if evento is None:
        return {
            'correcto': False,
            'intentos_restantes': 0,
            'expirado': True,
            'requiere_credenciales': True,
            'anomalia': None,
            'mensaje': "No hay OTP activo",
        }
    
    # Verificar expiración
    ahora = datetime.now(timezone.utc)
    expira = evento['timestamp_expira']
    
    # Manejar datetime naive de mongomock
    if hasattr(expira, 'tzinfo') and expira.tzinfo is None:
        ahora = ahora.replace(tzinfo=None)
    
    if ahora > expira:
        # OTP expirado
        minutos_retraso = int((ahora - expira).total_seconds() / 60)
        
        coleccion.update_one(
            {'_id': evento['_id']},
            {'$set': {'minutos_retraso': minutos_retraso}}
        )
        
        anomalia = registrar_anomalia(
            usuario_id,
            'otp_expirado',
            f"OTP expiró sin validación. Retraso: {minutos_retraso} min.",
        )
        
        return {
            'correcto': False,
            'intentos_restantes': 0,
            'expirado': True,
            'requiere_credenciales': True,
            'anomalia': anomalia,
        }
    
    # Verificar código contra hash
    hash_almacenado = evento['otp_hash']
    codigo_correcto = verificar_contraseña(codigo_introducido, hash_almacenado)
    
    if codigo_correcto:
        # Correcto
        coleccion.update_one(
            {'_id': evento['_id']},
            {'$set': {'resuelto': True}}
        )
        
        return {
            'correcto': True,
            'intentos_restantes': MAXIMO_INTENTOS,
            'expirado': False,
            'requiere_credenciales': False,
            'anomalia': None,
        }
    
    # Incorrecto
    intentos_usados = evento['intentos_fallidos'] + 1
    intentos_restantes = MAXIMO_INTENTOS - intentos_usados
    
    coleccion.update_one(
        {'_id': evento['_id']},
        {'$set': {'intentos_fallidos': intentos_usados}}
    )
    
    if intentos_usados >= MAXIMO_INTENTOS:
        # 3 intentos fallidos → anomalía
        anomalia = registrar_anomalia(
            usuario_id,
            'tercer_intento_otp',
            f"3 intentos fallidos de OTP consecutivos.",
        )
        
        return {
            'correcto': False,
            'intentos_restantes': 0,
            'expirado': False,
            'requiere_credenciales': True,
            'anomalia': anomalia,
        }
    
    # Aún tiene intentos
    return {
        'correcto': False,
        'intentos_restantes': intentos_restantes,
        'expirado': False,
        'requiere_credenciales': False,
        'anomalia': None,
    }


def obtener_estado_otp(usuario_id: str) -> dict:
    """
    Retorna el estado del OTP activo del usuario.
    
    Args:
        usuario_id (str): ID del usuario
    
    Returns:
        dict: {
            'tiene_otp_activo': bool,
            'expira_en_seg': int,
            'intentos_usados': int,
            'intentos_restantes': int
        }
    
    Raises:
        TypeError: Si usuario_id no es string
        ValueError: Si usuario_id está vacío o inválido
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
    
    coleccion = conexion_global.obtener_coleccion('eventos_otp')
    evento = coleccion.find_one({
        'usuario_id': usuario_oid,
        'resuelto': False,
    })
    
    if evento is None:
        return {
            'tiene_otp_activo': False,
            'expira_en_seg': 0,
            'intentos_usados': 0,
            'intentos_restantes': MAXIMO_INTENTOS,
        }
    
    ahora = datetime.now(timezone.utc)
    expira = evento['timestamp_expira']
    
    # Manejar datetime naive
    if hasattr(expira, 'tzinfo') and expira.tzinfo is None:
        ahora = ahora.replace(tzinfo=None)
    
    diferencia = (expira - ahora).total_seconds()
    expira_en_seg = max(0, int(diferencia))
    
    return {
        'tiene_otp_activo': True,
        'expira_en_seg': expira_en_seg,
        'intentos_usados': evento.get('intentos_fallidos', 0),
        'intentos_restantes': MAXIMO_INTENTOS - evento.get('intentos_fallidos', 0),
    }


def cancelar_otp(usuario_id: str) -> bool:
    """
    Cancela el OTP activo del usuario.
    
    Args:
        usuario_id (str): ID del usuario
    
    Returns:
        bool: True si se canceló, False si no había OTP activo
    
    Raises:
        TypeError: Si usuario_id no es string
        ValueError: Si usuario_id está vacío o inválido
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
    
    coleccion = conexion_global.obtener_coleccion('eventos_otp')
    evento = coleccion.find_one({
        'usuario_id': usuario_oid,
        'resuelto': False,
    })
    
    if evento is None:
        return False
    
    coleccion.update_one(
        {'_id': evento['_id']},
        {'$set': {'resuelto': True}}
    )
    
    return True
