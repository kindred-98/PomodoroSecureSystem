"""
Módulo: fuentes.py
Responsabilidad: Definición de fuentes/tipografía para toda la UI.
"""

# ============================================
# FUENTES DEL SISTEMA
# ============================================
FUENTE_PRINCIPAL = "Comic Sans MS"
FUENTE_ALTERNATIVA = "Segoe UI"
FUENTE_MONOESPACIADA = "JetBrains Mono"
FUENTE_EMOJI = "Segoe UI Emoji"

# ============================================
# TAMAÑOS DE FUENTE
# ============================================
TAMANO_TITULO_GRANDE = 26
TAMANO_TITULO = 22
TAMANO_SUBTITULO = 20
TAMANO_CABECERA = 18
TAMANO_NORMAL = 16
TAMANO_NORMAL_PEQUENO = 14
TAMANO_PEQUENO = 13
TAMANO_MINIMO = 12
TAMANO_FOOTER = 11

# ============================================
# ICONOS (EMOJIS)
# ============================================
ICONO_LOGO = "🍅🔐"
ICONO_CHECK = "✅"
ICONO_ADVERTENCIA = "⚠️"
ICONO_COPIAR = "📋"

# ============================================
# ESTILOS DE TEXTO (tuplas para CTk)
# ============================================
def crear_fuente(tamano=14, peso="normal"):
    """Crea una tupla de fuente."""
    return (FUENTE_PRINCIPAL, tamano, peso)


def crear_fuente_mono(tamano=14, peso="normal"):
    """Crea una tupla de fuente monoespaciada."""
    return (FUENTE_MONOESPACIADA, tamano, peso)


def crear_fuente_emoji(tamano=14, peso="normal"):
    """Crea una tupla de fuente para emojis."""
    return (FUENTE_EMOJI, tamano, peso)


TITULO = crear_fuente(TAMANO_TITULO, "bold")
SUBTITULO = crear_fuente(TAMANO_SUBTITULO, "bold")
CABECERA = crear_fuente(TAMANO_CABECERA, "bold")
NORMAL = crear_fuente(TAMANO_NORMAL)
NORMAL_NEGRITA = crear_fuente(TAMANO_NORMAL, "bold")
PEQUENO = crear_fuente(TAMANO_PEQUENO)
MINIMO = crear_fuente(TAMANO_MINIMO)
FOOTER = crear_fuente(TAMANO_FOOTER)