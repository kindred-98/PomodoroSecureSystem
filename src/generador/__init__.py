"""
Módulo: generador/__init__.py
Exporta todas las funciones del generador de contraseñas
"""

from src.generador.generar_contrasena import generar_contrasena, generar_contrasena_personalizada, generar_contrasena_segura
from src.generador.asegurar_tipos_caracteres import asegurar_tipos_caracteres
from src.generador.construir_juego_caracteres import construir_juego_caracteres
from src.generador.detectar_patrones import detectar_patrones
from src.generador.mezclar_contrasena import mezclar_contrasena, mezclar_preservando_estructura
from src.generador.evaluar_fortaleza import evaluar_fortaleza
from src.generador.calcular_puntuacion import calcular_puntuacion, generar_y_evaluar

__all__ = [
    # Funciones principales
    "generar_contrasena",
    "generar_contrasena_segura",
    "generar_contrasena_personalizada",
    "asegurar_tipos_caracteres",
    "construir_juego_caracteres",
    "detectar_patrones",
    "mezclar_contrasena",
    "mezclar_preservando_estructura",
    "evaluar_fortaleza",
    "calcular_puntuacion",
    "generar_y_evaluar",
]