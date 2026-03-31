"""
Módulo: calcular_puntuacion.py
Responsabilidad: Wrapper final que integra todas las funciones
de evaluación de contraseñas en un sistema de puntuación unificado.
"""

import math
from src.generador.generar_contraseña import generar_contraseña
from src.generador.detectar_patrones import detectar_patrones
from src.generador.evaluar_fortaleza import evaluar_fortaleza
from src.generador.mezclar_contraseña import mezclar_contraseña as mezclar


def calcular_puntuacion(contraseña: str, incluir_analisis: bool = False) -> dict:
    """
    Calcula puntuación integral de una contraseña de forma rápida.
    
    Realiza evaluación simplificada para obtener resultado rápido.
    
    Args:
        contraseña (str): Contraseña a evaluar
        incluir_analisis (bool): Si True, incluye análisis detallado de patrones
    
    Returns:
        dict: {
            'puntuacion': int (0-100),
            'nivel': str,
            'es_segura': bool (True si puntuacion >= 70),
            'tiempo_cracken_segundos': float (estimado),
            'analisis_patrones': dict (opcional, solo si incluir_analisis=True)
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
    
    # Evaluar fortaleza
    resultado_fortaleza = evaluar_fortaleza(contraseña)
    puntuacion = resultado_fortaleza['puntuacion']
    nivel = resultado_fortaleza['nivel']
    
    # Estimar tiempo de crackeo (modelo exponencial simplificado)
    # Basado en puntuación y longitud
    tamaño_charset = 95  # ASCII imprimibles
    longitud = len(contraseña)
    
    # promedio_intentos = (tamaño_charset ^ longitud) / 2
    promedio_intentos = (tamaño_charset ** longitud) / 2
    
    # Suponiendo 1 millón de intentos por segundo
    tiempo_segundos = promedio_intentos / 1_000_000
    
    # Convertir a unidad legible
    if tiempo_segundos < 1:
        tiempo_legible = f"{tiempo_segundos * 1000:.2f}ms"
    elif tiempo_segundos < 60:
        tiempo_legible = f"{tiempo_segundos:.2f}s"
    elif tiempo_segundos < 3600:
        tiempo_legible = f"{tiempo_segundos / 60:.2f}min"
    elif tiempo_segundos < 86400:
        tiempo_legible = f"{tiempo_segundos / 3600:.2f}h"
    else:
        tiempo_legible = f"{tiempo_segundos / 86400:.2f}días"
    
    resultado = {
        'puntuacion': puntuacion,
        'nivel': nivel,
        'es_segura': puntuacion >= 70,
        'tiempo_crack_estimado': tiempo_legible,
        'tiempo_crack_segundos': tiempo_segundos
    }
    
    # Incluir análisis de patrones si se solicita
    if incluir_analisis:
        resultado['analisis_patrones'] = detectar_patrones(contraseña)
    
    return resultado


def generar_y_evaluar(parametros: dict, mezclar_resultado: bool = False) -> dict:
    """
    Genera una contraseña y calcula su puntuación automáticamente.
    
    Workflow completo de generación + evaluación en una llamada.
    
    Args:
        parametros (dict): Parámetros para generar_contraseña
        mezclar_resultado (bool): Si True, mezcla la contraseña generada
    
    Returns:
        dict: {
            'contraseña': str,
            'puntuacion': int (0-100),
            'nivel': str,
            'es_segura': bool,
            'tiempo_crack_estimado': str,
            'detalles_generacion': dict
        }
        
    Raises:
        ValueError: Si los parámetros son inválidos
        TypeError: Si parametros no es dict
    """
    if not isinstance(parametros, dict):
        raise TypeError("Los parámetros deben ser un diccionario")
    
    # Generar contraseña
    contraseña = generar_contraseña(parametros)
    
    # Mezclar si se solicita
    if mezclar_resultado:
        contraseña = mezclar(contraseña)
    
    # Evaluar
    evaluacion = evaluar_fortaleza(contraseña)
    puntuacion = evaluacion['puntuacion']
    
    # Estimar tiempo de crackeo
    tamaño_charset = 95
    longitud = len(contraseña)
    promedio_intentos = (tamaño_charset ** longitud) / 2
    tiempo_segundos = promedio_intentos / 1_000_000
    
    return {
        'contraseña': contraseña,
        'puntuacion': puntuacion,
        'nivel': evaluacion['nivel'],
        'es_segura': puntuacion >= 70,
        'tiempo_crack_segundos': tiempo_segundos,
        'detalles_evaluacion': evaluacion['detalles']
    }
