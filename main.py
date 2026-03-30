"""
main.py - Punto de entrada de PomodoroSecureSystem

Este archivo es el punto de inicio de la aplicación.
Ejecutar: python main.py
"""

import sys
from pathlib import Path

# Agregar src al path para imports
ruta_proyecto = Path(__file__).parent
sys.path.insert(0, str(ruta_proyecto))

from src.generador.generar_contraseña import generar_contraseña
from src.generador.asegurar_tipos_caracteres import asegurar_tipos_caracteres


def principal():
    """Función principal - punto de entrada de la aplicación"""
    print("=" * 60)
    print("🍅🔐 POMODORO SECURE SYSTEM")
    print("=" * 60)
    print()
    
    # TODO: Aquí irá lógica de UI con CustomTkinter
    # Por ahora, demostración simple del generador
    
    print("✅ Aplicación iniciada correctamente")
    print()
    print("Estado: PRE-IMPLEMENTACIÓN")
    print("- Módulo generador: 20% (básico funcional)")
    print("- Módulos restantes: Por implementar")
    print()
    
    # Prueba simple del generador
    demostrar_generador()


def demostrar_generador():
    """Función auxiliar: Demostración del generador de contraseñas"""
    print("-" * 60)
    print("DEMOSTRACIÓN: Generador de Contraseñas")
    print("-" * 60)
    
    parametros = {
        "longitud": 12,
        "usar_mayusculas": True,
        "usar_numeros": True,
        "usar_simbolos": True,
        "excluir_ambiguos": False
    }
    
    try:
        contraseña_generada = generar_contraseña(parametros)
        print(f"✅ Contraseña generada: {contraseña_generada}")
        print(f"✅ Longitud: {len(contraseña_generada)}")
        print()
    except Exception as error:
        print(f"❌ Error al generar contraseña: {error}")
        print()


if __name__ == "__main__":
    principal()
