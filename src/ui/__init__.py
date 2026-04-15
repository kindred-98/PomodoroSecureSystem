"""
Módulo: ui/__init__.py
Responsabilidad: Exportar vistas de la interfaz gráfica.
"""

from src.ui.splash import SplashView
from src.ui.login_view import LoginView
from src.ui.registro_view import RegistroView
from src.ui.dashboard_empleado import DashboardEmpleado
from src.ui.dashboard_encargado import DashboardEncargado
from src.ui.dashboard_supervisor import DashboardSupervisor
from src.ui.bloqueo_view import BloqueoView
from src.ui.password_view import PasswordView
from src.ui.historial_view import HistorialView
from src.ui.config_descansos_view import ConfigDescansosView
from src.ui.config_bloque_descansos import ConfigBloqueDescansos

__all__ = [
    "SplashView",
    "LoginView",
    "RegistroView",
    "DashboardEmpleado",
    "DashboardEncargado",
    "DashboardSupervisor",
    "BloqueoView",
    "PasswordView",
    "HistorialView",
    "ConfigDescansosView",
    "ConfigBloqueDescansos",
]

