"""
Módulo: generador/__init__.py
Exporta todas las funciones del generador de contraseñas
"""

from .generar_contraseña import generar_contraseña
from .asegurar_tipos_caracteres import asegurar_tipos_caracteres
from .construir_juego_caracteres import construir_juego_caracteres
from .detectar_patrones import detectar_patrones
from .mezclar_contraseña import mezclar_contraseña, mezclar_preservando_estructura
from .evaluar_fortaleza import evaluar_fortaleza
from .calcular_puntuacion import calcular_puntuacion, generar_y_evaluar

__all__ = [
    # Funciones principales
    "generar_contraseña",
    "asegurar_tipos_caracteres",
    "construir_juego_caracteres",
    "detectar_patrones",
    "mezclar_contraseña",
    "mezclar_preservando_estructura",
    "evaluar_fortaleza",
    "calcular_puntuacion",
    "generar_y_evaluar",
]