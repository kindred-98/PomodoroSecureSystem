"""
Módulo: banco_tiempo.py
Responsabilidad: Validar y calcular la distribución de descansos
dentro del banco de tiempo de 50 minutos por ciclo Pomodoro.
"""

BANCO_TOTAL = 50
CANTIDAD_CORTOS = 4
MINIMO_CORTO = 5
MAXIMO_CORTO = 10
MINIMO_LARGO = 15
MAXIMO_LARGO = 30


def validar_configuracion_descansos(descansos_cortos: list, banco_total: int = BANCO_TOTAL) -> dict:
    """
    Valida que una configuración de descansos sea correcta.
    
    Reglas:
    - Exactamente 4 descansos cortos
    - Cada corto: entre 5 y 10 minutos
    - Suma de cortos: entre 20 y 35 minutos
    - Descanso largo = banco_total - suma(cortos)
    - Largo resultante: entre 15 y 30 minutos
    
    Args:
        descansos_cortos (list): Lista de 4 enteros con minutos por descanso corto
        banco_total (int): Total de minutos del banco (default 50)
    
    Returns:
        dict: {
            'valido': bool,
            'descansos_cortos': list,
            'descanso_largo': int,
            'banco_total': int,
            'errores': list
        }
    
    Raises:
        TypeError: Si descansos_cortos no es list o banco_total no es int
    """
    if not isinstance(descansos_cortos, list):
        raise TypeError(
            f"descansos_cortos debe ser list, "
            f"recibido: {type(descansos_cortos).__name__}"
        )
    if not isinstance(banco_total, int):
        raise TypeError(
            f"banco_total debe ser int, "
            f"recibido: {type(banco_total).__name__}"
        )
    
    errores = []
    
    # Validar cantidad de descansos
    if len(descansos_cortos) != CANTIDAD_CORTOS:
        errores.append(
            f"Se requieren exactamente {CANTIDAD_CORTOS} descansos cortos, "
            f"recibidos: {len(descansos_cortos)}"
        )
        return {
            'valido': False,
            'descansos_cortos': descansos_cortos,
            'descanso_largo': 0,
            'banco_total': banco_total,
            'errores': errores
        }
    
    # Validar tipos y rangos individuales
    for i, valor in enumerate(descansos_cortos):
        if not isinstance(valor, int):
            errores.append(f"Descanso {i + 1}: debe ser int, recibido {type(valor).__name__}")
            continue
        if valor < MINIMO_CORTO:
            errores.append(
                f"Descanso {i + 1}: {valor} min es menor al mínimo ({MINIMO_CORTO})"
            )
        if valor > MAXIMO_CORTO:
            errores.append(
                f"Descanso {i + 1}: {valor} min es mayor al máximo ({MAXIMO_CORTO})"
            )
    
    # Si hay errores individuales, no continuar
    if errores:
        return {
            'valido': False,
            'descansos_cortos': descansos_cortos,
            'descanso_largo': 0,
            'banco_total': banco_total,
            'errores': errores
        }
    
    # Calcular descanso largo
    suma_cortos = sum(descansos_cortos)
    descanso_largo = banco_total - suma_cortos
    
    # Validar suma de cortos (rango válido para que largo quede entre 15-30)
    # Si banco es 50: largo = 50 - suma
    # largo >= 15 → suma <= 35
    # largo <= 30 → suma >= 20
    max_suma_cortos = banco_total - MINIMO_LARGO
    min_suma_cortos = banco_total - MAXIMO_LARGO
    
    if suma_cortos < min_suma_cortos:
        errores.append(
            f"Suma de cortos ({suma_cortos}) es muy baja. "
            f"El descanso largo quedaría en {descanso_largo} min "
            f"(máximo {MAXIMO_LARGO}). Aumenta los descansos cortos."
        )
    if suma_cortos > max_suma_cortos:
        errores.append(
            f"Suma de cortos ({suma_cortos}) es muy alta. "
            f"El descanso largo quedaría en {descanso_largo} min "
            f"(mínimo {MINIMO_LARGO}). Reduce los descansos cortos."
        )
    
    return {
        'valido': len(errores) == 0,
        'descansos_cortos': descansos_cortos,
        'descanso_largo': descanso_largo if len(errores) == 0 else 0,
        'banco_total': banco_total,
        'errores': errores
    }


def calcular_descanso_largo(descansos_cortos: list, banco_total: int = BANCO_TOTAL) -> int:
    """
    Calcula los minutos del descanso largo dados los descansos cortos.
    
    Args:
        descansos_cortos (list): Lista de minutos por descanso corto
        banco_total (int): Total de minutos del banco (default 50)
    
    Returns:
        int: Minutos del descanso largo
    """
    if not isinstance(descansos_cortos, list):
        raise TypeError(
            f"descansos_cortos debe ser list, "
            f"recibido: {type(descansos_cortos).__name__}"
        )
    if not isinstance(banco_total, int):
        raise TypeError(
            f"banco_total debe ser int, "
            f"recibido: {type(banco_total).__name__}"
        )
    
    return banco_total - sum(descansos_cortos)
