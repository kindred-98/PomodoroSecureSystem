"""
Módulo: estados.py
Responsabilidad: Definir la máquina de estados del timer Pomodoro
y calcular la configuración de ciclos según el horario del trabajador.
"""

from datetime import datetime

# Estados del timer
ESTADO_INACTIVO = "INACTIVO"
ESTADO_TRABAJANDO = "TRABAJANDO"
ESTADO_DESCANSO_CORTO = "DESCANSO_CORTO"
ESTADO_DESCANSO_LARGO = "DESCANSO_LARGO"
ESTADO_PAUSADO = "PAUSADO"

# Transiciones válidas: {estado_origen: [estados_destino]}
TRANSICIONES_VALIDAS = {
    ESTADO_INACTIVO: [ESTADO_TRABAJANDO],
    ESTADO_TRABAJANDO: [
        ESTADO_DESCANSO_CORTO,
        ESTADO_DESCANSO_LARGO,
        ESTADO_PAUSADO,
        ESTADO_INACTIVO,
    ],
    ESTADO_DESCANSO_CORTO: [
        ESTADO_TRABAJANDO,
        ESTADO_DESCANSO_LARGO,
    ],
    ESTADO_DESCANSO_LARGO: [
        ESTADO_TRABAJANDO,
        ESTADO_INACTIVO,
    ],
    ESTADO_PAUSADO: [
        ESTADO_TRABAJANDO,
        ESTADO_DESCANSO_CORTO,
    ],
}


def obtener_transiciones_validas() -> dict:
    """
    Retorna el mapa de transiciones válidas de la máquina de estados.
    
    Returns:
        dict: {estado_origen: [estados_destino_permitidos]}
    """
    return TRANSICIONES_VALIDAS.copy()


def calcular_ciclos_jornada(
    horario_inicio: str,
    horario_fin: str,
    pomodoro_min: int = 25,
    descansos_cortos: list = None,
    descanso_largo: int = 30,
) -> dict:
    """
    Calcula cuántos ciclos Pomodoro caben en la jornada del trabajador.
    
    Adapta el número de ciclos al horario real, sin hardcodear nada.
    El Pomodoro es configurable por usuario.
    
    Args:
        horario_inicio (str): Hora inicio en formato "HH:MM"
        horario_fin (str): Hora fin en formato "HH:MM"
        pomodoro_min (int): Minutos por pomodoro de trabajo (default 25)
        descansos_cortos (list): Minutos por cada descanso corto (default [5,5,5,5])
        descanso_largo (int): Minutos del descanso largo (default 30)
    
    Returns:
        dict: {
            'inicio_jornada': str,
            'fin_jornada': str,
            'duracion_jornada_min': int,
            'pomodoro_trabajo_min': int,
            'descansos_cortos': list,
            'descanso_largo': int,
            'duracion_ciclo_min': int,
            'ciclos_completos': int,
            'minutos_sobrantes': int,
            'pomodoros_por_ciclo': int,
            'ciclo_reducido': bool,
            'pomodoros_ciclo_reducido': int,
        }
    
    Raises:
        TypeError: Si tipos son incorrectos
        ValueError: Si formato de hora es inválido o fin <= inicio
    """
    if not isinstance(horario_inicio, str):
        raise TypeError(
            f"horario_inicio debe ser string, "
            f"recibido: {type(horario_inicio).__name__}"
        )
    if not isinstance(horario_fin, str):
        raise TypeError(
            f"horario_fin debe ser string, "
            f"recibido: {type(horario_fin).__name__}"
        )
    
    if descansos_cortos is None:
        descansos_cortos = [5, 5, 5, 5]
    
    if not isinstance(descansos_cortos, list):
        raise TypeError(
            f"descansos_cortos debe ser list, "
            f"recibido: {type(descansos_cortos).__name__}"
        )
    
    # Parsear horas
    try:
        partes_inicio = horario_inicio.split(":")
        partes_fin = horario_fin.split(":")
        minutos_inicio = int(partes_inicio[0]) * 60 + int(partes_inicio[1])
        minutos_fin = int(partes_fin[0]) * 60 + int(partes_fin[1])
    except (ValueError, IndexError):
        raise ValueError(
            f"Formato de hora inválido. Use 'HH:MM'. "
            f"Recibido: inicio='{horario_inicio}', fin='{horario_fin}'"
        )
    
    if minutos_fin <= minutos_inicio:
        raise ValueError(
            f"horario_fin ({horario_fin}) debe ser posterior a "
            f"horario_inicio ({horario_inicio})"
        )
    
    duracion_jornada = minutos_fin - minutos_inicio
    pomodoros_por_ciclo = len(descansos_cortos)
    
    # Duración de un ciclo completo
    # Trabajo: pomodoro_min × pomodoros_por_ciclo
    # Descansos: sum(cortos) + largo
    banco_descansos = sum(descansos_cortos) + descanso_largo
    trabajo_por_ciclo = pomodoro_min * pomodoros_por_ciclo
    duracion_ciclo = trabajo_por_ciclo + banco_descansos
    
    # Cuántos ciclos completos caben
    ciclos_completos = duracion_jornada // duracion_ciclo
    minutos_sobrantes = duracion_jornada % duracion_ciclo
    
    # ¿Cabe un ciclo reducido?
    # Un ciclo reducido necesita al menos 2 pomodoros + 1 descanso corto
    minimo_ciclo_reducido = (pomodoro_min * 2) + min(descansos_cortos)
    ciclo_reducido = minutos_sobrantes >= minimo_ciclo_reducido
    
    pomodoros_ciclo_reducido = 0
    if ciclo_reducido:
        # Calcular cuántos pomodoros caben en el tiempo sobrante
        tiempo_disponible = minutos_sobrantes
        for i in range(pomodoros_por_ciclo):
            if tiempo_disponible >= pomodoro_min:
                pomodoros_ciclo_reducido += 1
                tiempo_disponible -= pomodoro_min
                # Después de cada pomodoro excepto el último quepa
                if i < pomodoros_por_ciclo - 1 and tiempo_disponible >= descansos_cortos[i]:
                    tiempo_disponible -= descansos_cortos[i]
                else:
                    break
            else:
                break
    
    return {
        'inicio_jornada': horario_inicio,
        'fin_jornada': horario_fin,
        'duracion_jornada_min': duracion_jornada,
        'pomodoro_trabajo_min': pomodoro_min,
        'descansos_cortos': descansos_cortos,
        'descanso_largo': descanso_largo,
        'duracion_ciclo_min': duracion_ciclo,
        'ciclos_completos': ciclos_completos,
        'minutos_sobrantes': minutos_sobrantes,
        'pomodoros_por_ciclo': pomodoros_por_ciclo,
        'ciclo_reducido': ciclo_reducido,
        'pomodoros_ciclo_reducido': pomodoros_ciclo_reducido,
    }
