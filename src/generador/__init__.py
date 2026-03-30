"""
Módulo: generador/__init__.py
Exporta todas las funciones del generador de contraseñas
"""

from .generar_contraseña import generar_contraseña
from .asegurar_tipos_caracteres import asegurar_tipos_caracteres

# Funciones por implementar (scaffolding):
# from .evaluar_fortaleza import evaluar_fortaleza
# from .detectar_patrones import detectar_patrones
# from .mezclar_contraseña import mezclar_contraseña
# from .construir_juego_caracteres import construir_juego_caracteres
# from .calcular_puntuacion import calcular_puntuacion

__all__ = [
    "generar_contraseña",
    "asegurar_tipos_caracteres",
]