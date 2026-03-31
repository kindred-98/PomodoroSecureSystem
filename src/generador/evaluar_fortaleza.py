"""
Módulo: evaluar_fortaleza.py
Responsabilidad: Evaluar y calificar la fortaleza de una contraseña
usando un sistema de puntuación integrado.
"""

import math
from .detectar_patrones import detectar_patrones


def evaluar_fortaleza(contraseña: str) -> dict:
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
    if not isinstance(contraseña, str):
        raise TypeError(f"La contraseña debe ser string, "
                       f"recibido: {type(contraseña).__name__}")
    
    if not contraseña:
        raise ValueError("La contraseña no puede estar vacía")
    
    detalles = {}
    puntos_totales = 0
    
    # ==================== CRITERIO 1: LONGITUD ====================
    detalles['longitud'] = len(contraseña)
    puntos_longitud = 0
    
    # Escala más estricta para longitud
    if len(contraseña) >= 20:
        puntos_longitud = 30
    elif len(contraseña) >= 16:
        puntos_longitud = 24
    elif len(contraseña) >= 12:
        puntos_longitud = 18
    elif len(contraseña) >= 10:
        puntos_longitud = 12
    elif len(contraseña) >= 8:
        puntos_longitud = 6  # Reducido de 10
    elif len(contraseña) >= 6:
        puntos_longitud = 2
    # Menos de 6 = 0 puntos
    
    puntos_totales += puntos_longitud
    detalles['puntos_longitud'] = puntos_longitud
    
    # ==================== CRITERIO 2: DIVERSIDAD ====================
    tiene_mayusculas = any(c.isupper() for c in contraseña)
    tiene_minusculas = any(c.islower() for c in contraseña)
    tiene_numeros = any(c.isdigit() for c in contraseña)
    tiene_simbolos = any(not c.isalnum() for c in contraseña)
    
    detalles['tiene_mayusculas'] = tiene_mayusculas
    detalles['tiene_minusculas'] = tiene_minusculas
    detalles['tiene_numeros'] = tiene_numeros
    detalles['tiene_simbolos'] = tiene_simbolos
    
    # Escala más estricta para diversidad
    puntos_diversidad = 0
    tipos_presentes = sum([tiene_mayusculas, tiene_minusculas, 
                           tiene_numeros, tiene_simbolos])
    
    if tipos_presentes == 4:
        puntos_diversidad = 30  # Todos los 4 tipos
    elif tipos_presentes == 3:
        puntos_diversidad = 20  # 3 tipos
    elif tipos_presentes == 2:
        puntos_diversidad = 10  # 2 tipos
    elif tipos_presentes == 1:
        puntos_diversidad = 2   # Solo 1 tipo (reducido de 7)
    # 0 tipos = 0 puntos
    
    puntos_totales += puntos_diversidad
    detalles['puntos_diversidad'] = puntos_diversidad
    
    # ========== FACTOR MULTIPLICADOR POR DIVERSIDAD ==========
    # Penaliza contraseñas con baja diversidad (ej: solo minúsculas, solo números)
    factor_diversidad = 1.0
    if tipos_presentes == 1:
        factor_diversidad = 0.15  # Muy baja: solo 1 tipo
    elif tipos_presentes == 2:
        factor_diversidad = 0.5   # Baja: 2 tipos
    elif tipos_presentes == 3:
        factor_diversidad = 0.85  # Media-alta: 3 tipos
    # Si tipos_presentes == 4, factor = 1.0
    
    # ========== FACTOR MULTIPLICADOR POR LONGITUD ==========
    # Penaliza contraseñas muy cortas incluso con diversidad completa
    factor_longitud = 1.0
    if len(contraseña) < 6:
        factor_longitud = 0.1   # < 6: muy corta
    elif len(contraseña) < 8:
        factor_longitud = 0.4   # 6-7: corta
    elif len(contraseña) < 12:
        factor_longitud = 0.7   # 8-11: corta-media
    # Si >= 12, factor = 1.0
    
    # Re-aplicar factor a puntos de longitud y entropía
    puntos_longitud = int(puntos_longitud * factor_diversidad * factor_longitud)
    puntos_totales = puntos_totales - detalles['puntos_longitud'] + puntos_longitud
    detalles['puntos_longitud'] = puntos_longitud
    
    # ==================== CRITERIO 3: ENTROPÍA ====================
    # Aproximación de bits de entropía basada en espacio de caracteres
    tamaño_charset = 0
    if tiene_minusculas:
        tamaño_charset += 26
    if tiene_mayusculas:
        tamaño_charset += 26
    if tiene_numeros:
        tamaño_charset += 10
    if tiene_simbolos:
        tamaño_charset += 32  # Aproximado para puntuación
    
    if tamaño_charset > 0:
        entropia_bits = len(contraseña) * math.log2(tamaño_charset)
    else:
        entropia_bits = 0
    
    detalles['entropia_bits'] = round(entropia_bits, 2)
    
    # Puntos por entropía: 1 punto por cada 5 bits (max 20)
    puntos_entropia = min(20, int(entropia_bits / 5))
    puntos_entropia = int(puntos_entropia * factor_diversidad * factor_longitud)  # Aplicar ambos factores
    puntos_totales += puntos_entropia
    detalles['puntos_entropia'] = puntos_entropia
    
    # ==================== CRITERIO 4: PATRONES ====================
    analisis_patrones = detectar_patrones(contraseña)
    fortaleza_patron = analisis_patrones['fortaleza_patron']
    
    # Si no hay patrones débiles, gana puntos extra (pero reducido para contraseñas muy cortas)
    puntos_patrones = int(fortaleza_patron * 20 * factor_longitud)  # Aplicar factor de longitud
    puntos_totales += puntos_patrones
    detalles['puntos_patrones'] = puntos_patrones
    
    # Registrar penalizaciones
    penalizacion = {}
    if analisis_patrones['tiene_secuencias_consecutivas']:
        penalizacion['secuencias'] = len(analisis_patrones['secuencias_encontradas'])
    if analisis_patrones['tiene_repeticiones']:
        penalizacion['repeticiones'] = len(analisis_patrones['repeticiones_encontradas'])
    if analisis_patrones['tiene_teclado_adyacente']:
        penalizacion['teclado'] = len(analisis_patrones['adyacencias_encontradas'])
    if analisis_patrones['tiene_patrones_crecientes']:
        penalizacion['crecientes'] = len(analisis_patrones['patrones_crecientes'])
    if analisis_patrones['tiene_patrones_invertidos']:
        penalizacion['invertidos'] = len(analisis_patrones['patrones_invertidos'])
    
    detalles['penalizacion_patrones'] = penalizacion
    
    # ==================== PUNTUACIÓN FINAL ====================
    puntuacion_final = min(100, max(0, puntos_totales))
    
    # Determinar nivel
    if puntuacion_final < 30:
        nivel = "Débil"
    elif puntuacion_final < 60:
        nivel = "Normal"
    elif puntuacion_final < 80:
        nivel = "Fuerte"
    else:
        nivel = "Muy Fuerte"
    
    return {
        'puntuacion': puntuacion_final,
        'nivel': nivel,
        'detalles': detalles
    }
