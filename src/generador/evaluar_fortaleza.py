"""
Módulo: evaluar_fortaleza.py
Responsabilidad: Evaluar y calificar la fortaleza de una contraseña
usando un sistema de puntuación integrado.
"""

import math
from src.generador.detectar_patrones import detectar_patrones

# Escala de puntos por longitud mínima alcanzada
_ESCALA_LONGITUD = ((20, 30), (16, 24), (12, 18), (10, 12), (8, 6), (6, 2))

# Puntos por número de tipos de carácter presentes (índice = tipos - 1)
_ESCALA_DIVERSIDAD = (2, 10, 20, 30)

# Factor multiplicador según diversidad (índice = tipos - 1)
_FACTOR_DIVERSIDAD = (0.15, 0.5, 0.85, 1.0)

# Factor multiplicador según longitud máxima
_ESCALA_FACTOR_LONGITUD = ((6, 0.1), (8, 0.4), (12, 0.7))

# Tamaño del espacio de caracteres que aporta cada tipo de carácter
_APORTE_CHARSET = (
    ('tiene_minusculas', 26),
    ('tiene_mayusculas', 26),
    ('tiene_numeros', 10),
    ('tiene_simbolos', 32),
)

# Traducción de hallazgos a claves de penalización
_CLAVES_PENALIZACION = (
    ('tiene_secuencias_consecutivas', 'secuencias_encontradas', 'secuencias'),
    ('tiene_repeticiones', 'repeticiones_encontradas', 'repeticiones'),
    ('tiene_teclado_adyacente', 'adyacencias_encontradas', 'teclado'),
    ('tiene_patrones_crecientes', 'patrones_crecientes', 'crecientes'),
    ('tiene_patrones_invertidos', 'patrones_invertidos', 'invertidos'),
)

# Umbrales de puntuación final para cada nivel
_UMBRALES_NIVEL = ((30, "Débil"), (60, "Normal"), (80, "Fuerte"))


def _escala_longitud(longitud: int) -> int:
    """Devuelve los puntos base por longitud."""
    for minimo, puntos in _ESCALA_LONGITUD:
        if longitud >= minimo:
            return puntos
    return 0


def _factor_longitud(longitud: int) -> float:
    """Devuelve el factor multiplicador por longitud."""
    for minimo, factor in _ESCALA_FACTOR_LONGITUD:
        if longitud < minimo:
            return factor
    return 1.0


def _analizar_tipos(contrasena: str) -> dict:
    """Indica qué tipos de carácter contiene la contraseña."""
    return {
        'tiene_mayusculas': any(c.isupper() for c in contrasena),
        'tiene_minusculas': any(c.islower() for c in contrasena),
        'tiene_numeros': any(c.isdigit() for c in contrasena),
        'tiene_simbolos': any(not c.isalnum() for c in contrasena),
    }


def _puntos_diversidad(tipos_presentes: int) -> int:
    """Devuelve los puntos por número de tipos de carácter."""
    if tipos_presentes == 0:
        return 0
    return _ESCALA_DIVERSIDAD[tipos_presentes - 1]


def _factor_diversidad(tipos_presentes: int) -> float:
    """Devuelve el factor multiplicador por diversidad."""
    if tipos_presentes == 0:
        return _FACTOR_DIVERSIDAD[0]
    return _FACTOR_DIVERSIDAD[tipos_presentes - 1]


def _calcular_entropia(contrasena: str, tipos: dict) -> float:
    """Aproxima los bits de entropía a partir del espacio de caracteres."""
    tamano_charset = sum(
        aporte for clave, aporte in _APORTE_CHARSET if tipos[clave]
    )
    if tamano_charset == 0:
        return 0
    return len(contrasena) * math.log2(tamano_charset)


def _penalizaciones(analisis_patrones: dict) -> dict:
    """Resume los patrones detectados como penalizaciones por tipo."""
    penalizacion = {}
    for clave_bool, clave_lista, etiqueta in _CLAVES_PENALIZACION:
        if analisis_patrones[clave_bool]:
            penalizacion[etiqueta] = len(analisis_patrones[clave_lista])
    return penalizacion


def _determinar_nivel(puntuacion: int) -> str:
    """Traduce la puntuación final a un nivel legible."""
    for umbral, nivel in _UMBRALES_NIVEL:
        if puntuacion < umbral:
            return nivel
    return "Muy Fuerte"


def evaluar_fortaleza(contrasena: str) -> dict:
    """
    Evalúa la fortaleza de una contraseña usando sistema de puntuación integral.
    
    Criterios de evaluación:
    - Longitud (máx 30 pts)
    - Diversidad de caracteres (máx 30 pts)
    - Entropía (máx 20 pts)
    - Ausencia de patrones débiles (máx 20 pts)
    
    Args:
        contraseña (str): Contraseña a evaluar
        
    Returns:
        dict: {
            'puntuacion': int (0-100),
            'nivel': str ("Débil"|"Normal"|"Fuerte"|"Muy Fuerte"),
            'detalles': {
                'longitud': int,
                'tiene_mayusculas': bool,
                'tiene_minusculas': bool,
                'tiene_numeros': bool,
                'tiene_simbolos': bool,
                'entropia_bits': float,
                'puntos_longitud': int,
                'puntos_diversidad': int,
                'puntos_entropia': int,
                'puntos_patrones': int,
                'penalizacion_patrones': dict
            }
        }
        
    Raises:
        TypeError: Si contraseña no es string
        ValueError: Si contraseña está vacía
    """
    if not isinstance(contrasena, str):
        raise TypeError(f"La contraseña debe ser string, "
                       f"recibido: {type(contrasena).__name__}")
    
    if not contrasena:
        raise ValueError("La contraseña no puede estar vacía")

    longitud = len(contrasena)

    # ==================== CRITERIO 1: LONGITUD ====================
    tipos = _analizar_tipos(contrasena)
    tipos_presentes = sum(tipos.values())

    # Factores penalizadores aplicados a longitud, entropía y patrones
    factor_diversidad = _factor_diversidad(tipos_presentes)
    factor_long = _factor_longitud(longitud)
    penalizacion_combinada = factor_diversidad * factor_long

    puntos_longitud = int(
        _escala_longitud(longitud) * penalizacion_combinada
    )
    puntos_diversidad = _puntos_diversidad(tipos_presentes)

    # ==================== CRITERIO 3: ENTROPÍA ====================
    entropia_bits = _calcular_entropia(contrasena, tipos)
    puntos_entropia = int(
        min(20, int(entropia_bits / 5)) * penalizacion_combinada
    )

    # ==================== CRITERIO 4: PATRONES ====================
    analisis_patrones = detectar_patrones(contrasena)
    puntos_patrones = int(
        analisis_patrones['fortaleza_patron'] * 20 * factor_long
    )

    puntos_totales = puntos_longitud + puntos_diversidad + puntos_entropia + puntos_patrones

    detalles = {
        'longitud': longitud,
        **tipos,
        'entropia_bits': round(entropia_bits, 2),
        'puntos_longitud': puntos_longitud,
        'puntos_diversidad': puntos_diversidad,
        'puntos_entropia': puntos_entropia,
        'puntos_patrones': puntos_patrones,
        'penalizacion_patrones': _penalizaciones(analisis_patrones),
    }

    # ==================== PUNTUACIÓN FINAL ====================
    puntuacion_final = min(100, max(0, puntos_totales))

    return {
        'puntuacion': puntuacion_final,
        'nivel': _determinar_nivel(puntuacion_final),
        'detalles': detalles
    }
