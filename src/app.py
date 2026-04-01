"""
Módulo: app.py
Responsabilidad: Controlador principal de la aplicación.
Gestiona navegación entre vistas y estado global.
"""

import customtkinter as ctk
from src.config.colores import *
from src.ui.splash import SplashView
from src.ui.login_view import LoginView
from src.ui.registro_view import RegistroView
from src.ui.dashboard_empleado import DashboardEmpleado
from src.ui.dashboard_encargado import DashboardEncargado
from src.ui.dashboard_supervisor import DashboardSupervisor
from src.ui.password_view import PasswordView
from src.ui.historial_view import HistorialView


class PomodoroSecureApp(ctk.CTk):
    """Ventana principal de la aplicación."""

    def __init__(self):
        super().__init__()
        aplicar_tema()
        self._configurar_ventana()
        self.usuario_actual = None
        self.vista_actual = None
        self._mostrar_splash()

    def _configurar_ventana(self):
        self.title("PomodoroSecure")
        self.geometry("1280x720")
        self.minsize(1024, 600)
        self.configure(fg_color=FONDO_PRINCIPAL)

    def _limpiar_vista(self):
        if self.vista_actual:
            self.vista_actual.destroy()
            self.vista_actual = None

    def _mostrar_splash(self):
        self._limpiar_vista()
        vista = SplashView(self, on_complete=self._mostrar_login)
        vista.pack(fill="both", expand=True)
        self.vista_actual = vista
        vista.iniciar_animacion()

    def _mostrar_login(self):
        self._limpiar_vista()
        vista = LoginView(
            self,
            on_login=self._on_login,
            on_ir_registro=self._mostrar_registro,
        )
        vista.pack(fill="both", expand=True)
        self.vista_actual = vista

    def _mostrar_registro(self):
        self._limpiar_vista()
        vista = RegistroView(
            self,
            on_registro_completo=self._on_registro_completo,
            on_ir_login=self._mostrar_login,
        )
        vista.pack(fill="both", expand=True)
        self.vista_actual = vista

    def _mostrar_dashboard(self):
        """Muestra el dashboard según el rol del usuario."""
        self._limpiar_vista()
        rol = self.usuario_actual.get('rol', 'empleado')

        if rol == 'supervisor':
            vista = DashboardSupervisor(
                self,
                usuario=self.usuario_actual,
                on_logout=self._on_logout,
                on_ver_contraseña=self._mostrar_password,
                on_ver_historial=self._mostrar_historial,
            )
        elif rol == 'encargado':
            vista = DashboardEncargado(
                self,
                usuario=self.usuario_actual,
                on_logout=self._on_logout,
                on_ver_contraseña=self._mostrar_password,
                on_ver_historial=self._mostrar_historial,
            )
        else:
            vista = DashboardEmpleado(
                self,
                usuario=self.usuario_actual,
                on_logout=self._on_logout,
                on_ver_contraseña=self._mostrar_password,
            )
        vista.pack(fill="both", expand=True)
        self.vista_actual = vista

    def _mostrar_historial(self):
        self._limpiar_vista()
        vista = HistorialView(
            self,
            usuario=self.usuario_actual,
            on_volver=self._mostrar_dashboard,
        )
        vista.pack(fill="both", expand=True)
        self.vista_actual = vista

    def _mostrar_password(self):
        self._limpiar_vista()
        vista = PasswordView(
            self,
            usuario=self.usuario_actual,
            on_volver=self._mostrar_dashboard,
        )
        vista.pack(fill="both", expand=True)
        self.vista_actual = vista

    def _on_login(self, email, contraseña):
        """Callback cuando el usuario intenta login."""
        from src.auth import iniciar_sesion
        try:
            resultado = iniciar_sesion(email, contraseña)
            self.usuario_actual = resultado['usuario']
            self._mostrar_dashboard()

            # Verificar si necesita configurar descansos
            self.after(500, self._verificar_config_descansos)
        except Exception as e:
            if hasattr(self.vista_actual, 'mostrar_error'):
                self.vista_actual.mostrar_error(str(e))
            raise

    def _verificar_config_descansos(self):
        """Muestra popup de descansos si no están configurados."""
        try:
            from src.db.conexion import conexion_global
            coleccion = conexion_global.obtener_coleccion('usuarios')
            usuario = coleccion.find_one({'_id': self.usuario_actual['_id']})

            if not usuario.get('config_descansos'):
                from src.ui.config_bloque_descansos import ConfigBloqueDescansos
                popup = ConfigBloqueDescansos(self, self.usuario_actual)
                popup.grab_set()
        except Exception:
            pass

    def _on_logout(self):
        """Callback cuando el usuario cierra sesión."""
        if self.usuario_actual:
            try:
                from src.db.conexion import conexion_global
                coleccion = conexion_global.obtener_coleccion('sesiones_auth')
                coleccion.update_many(
                    {'usuario_id': self.usuario_actual['_id'], 'activa': True},
                    {'$set': {'activa': False}},
                )
            except Exception:
                pass
        self.usuario_actual = None
        self._mostrar_login()

    def _on_registro_completo(self):
        """Callback cuando el registro termina."""
        self._mostrar_login()
