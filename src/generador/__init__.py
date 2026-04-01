"""
Módulo: generador/__init__.py
Exporta todas las funciones del generador de contraseñas
"""

from src.generador.generar_contraseña import generar_contraseña, generar_contraseña_personalizada
from src.generador.asegurar_tipos_caracteres import asegurar_tipos_caracteres
from src.generador.construir_juego_caracteres import construir_juego_caracteres
from src.generador.detectar_patrones import detectar_patrones
from src.generador.mezclar_contraseña import mezclar_contraseña, mezclar_preservando_estructura
from src.generador.evaluar_fortaleza import evaluar_fortaleza
from src.generador.calcular_puntuacion import calcular_puntuacion, generar_y_evaluar

__all__ = [
    # Funciones principales
    "generar_contraseña",
    "generar_contraseña_personalizada",
    "asegurar_tipos_caracteres",
    "construir_juego_caracteres",
    "detectar_patrones",
    "mezclar_contraseña",
    "mezclar_preservando_estructura",
    "evaluar_fortaleza",
    "calcular_puntuacion",
    "generar_y_evaluar",
]