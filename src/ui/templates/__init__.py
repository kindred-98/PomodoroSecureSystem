"""
Módulo: __init__.py
Responsabilidad: Exportar todos los componentes de templates.
"""

# Theme (colores)
from src.ui.templates.theme import (
    FONDO_PRINCIPAL, FONDO_CARD, FONDO_SECUNDARIO,
    TEXTO_PRINCIPAL, TEXTO_SECUNDARIO, PELIGRO, INFORMACION, AVISO, COMPLETADO,
    TRABAJO_ACTIVO,
    BLOQUEO_CORTO, BLOQUEO_LARGO, BLOQUEO_FIJO,
    TIMER_TRABAJO, TIMER_DESCANSO_CORTO, TIMER_DESCANSO_LARGO, TIMER_PAUSADO,
    BORDE, BORDE_ACTIVO,
    BOTON_PRIMARIO, BOTON_PRIMARIO_HOVER,
    BOTON_SECUNDARIO, BOTON_SECUNDARIO_HOVER,
    BOTON_PELIGRO, BOTON_PELIGRO_HOVER,
    BOTON_EXITO, BOTON_EXITO_HOVER,
)

# Fuentes
from src.ui.templates.fuentes import (
    FUENTE_PRINCIPAL, TAMANO_TITULO_GRANDE, TAMANO_TITULO, TAMANO_SUBTITULO,
    TAMANO_CABECERA, TAMANO_NORMAL, TAMANO_NORMAL_PEQUENO, TAMANO_PEQUENO,
    TAMANO_MINIMO, TAMANO_FOOTER,
    ICONO_LOGO, ICONO_CHECK, ICONO_ADVERTENCIA, ICONO_COPIAR,
    crear_fuente, TITULO, SUBTITULO, CABECERA, NORMAL, NORMAL_NEGRITA,
    PEQUENO, MINIMO, FOOTER
)

# Componentes
from src.ui.templates.componentes import (
    BotonPrimario, BotonSecundario, BotonPeligro,
    InputTexto, InputPassword,
    LabelTitulo, LabelNormal, LabelError,
    Card, FrameContenido,
    Checkbox, Radio,
    ProgressBar
)