"""
Módulo: ui/__init__.py
Responsabilidad: Exportar vistas de la interfaz gráfica.
"""

from .splash import SplashView
from .login_view import LoginView
from .registro_view import RegistroView
from .dashboard_empleado import DashboardEmpleado
from .dashboard_encargado import DashboardEncargado
from .dashboard_supervisor import DashboardSupervisor
from .bloqueo_view import BloqueoView
from .password_view import PasswordView
from .historial_view import HistorialView
from .config_descansos_view import ConfigDescansosView

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
]
