"""
Módulo: windows_lock.py
Responsabilidad: Wrapper thin para ctypes.windll.user32.LockWorkStation()
Separado para poder mockear en tests.
"""

import sys


def bloquear_escritorio() -> dict:
    """
    Bloquea el escritorio de Windows usando LockWorkStation().
    
    Solo funciona en Windows. En otros sistemas retorna error.
    
    Returns:
        dict: {
            'bloqueado': bool,
            'plataforma': str,
            'mensaje': str
        }
    """
    plataforma = sys.platform
    
    if plataforma != 'win32':
        return {
            'bloqueado': False,
            'plataforma': plataforma,
            'mensaje': f"LockWorkStation solo soportado en Windows. Plataforma: {plataforma}",
        }
    
    try:
        import ctypes
        resultado = ctypes.windll.user32.LockWorkStation()
        
        if resultado:
            return {
                'bloqueado': True,
                'plataforma': 'win32',
                'mensaje': "Escritorio bloqueado correctamente",
            }
        else:
            return {
                'bloqueado': False,
                'plataforma': 'win32',
                'mensaje': "LockWorkStation retornó 0 (error)",
            }
    except Exception as e:
        return {
            'bloqueado': False,
            'plataforma': 'win32',
            'mensaje': f"Error al bloquear escritorio: {e}",
        }
