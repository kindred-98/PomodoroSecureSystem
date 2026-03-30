"""
Módulo: calcular_puntuacion.py
Responsabilidad: Calcular la puntuación de fortaleza de una contraseña
siguiendo el sistema de scoring documentado
"""


def calcular_puntuacion(contraseña: str) -> int:
    """
    Calcula la puntuación de fortaleza (0-100) de una contraseña.
    
    Scoring:
        - Longitud: 0-40 puntos
        - Diversidad: 0-50 puntos (mayús, números, símbolos)
        - Patrones: -20 puntos máximo (penalizaciones)
        
    Args:
        contraseña (str): Contraseña a puntuar
        
    Returns:
        int: Puntuación entre 0 y 100
    """
    # TODO: Implementar algoritmo de scoring completo
    pass