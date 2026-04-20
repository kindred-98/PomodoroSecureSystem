"""
Módulo: app.py
Responsabilidad: Controlador principal de la aplicación.
Gestiona navegación entre vistas y estado global.
"""

import customtkinter as ctk
from src.ui.templates import FONDO_PRINCIPAL, COMPLETADO
from src.config.colores import aplicar_tema
from src.ui.splash import SplashView
from src.ui.login_view import LoginView
from src.ui.registro_view import RegistroView
from src.ui.verificar_email_view import VerificarEmailView
from src.ui.registro_resultado_view import RegistroResultadoView
from src.ui.dashboard_empleado import DashboardEmpleado
from src.ui.dashboard_encargado import DashboardEncargado
from src.ui.dashboard_supervisor import DashboardSupervisor
from src.ui.password_view import PasswordView
from src.ui.historial_view import HistorialView


class PomodoroSecureApp(ctk.CTk):
    """Ventana principal de la aplicación."""

    def __init__(self):
        super().__init__()

        from src.config.colores import aplicar_tema
        aplicar_tema("dark")

        from src.db.conexion import conexion_global
        conexion_global.conectar()

        self._configurar_ventana()
        self.usuario_actual = None
        self.vista_actual = None
        self.tema_actual = "dark"
        self._mostrar_splash()

    def _configurar_ventana(self):
        from src.ui.templates import FONDO_PRINCIPAL
        self.title("PomodoroSecure")
        self.geometry("1200x1000")
        self.resizable(False, False)
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
        vista.set_login_frase_callback(self._on_login_frase)
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

    def _mostrar_verificar_email(self, email, on_verificado):
        self._email_verificado = email
        self._limpiar_vista()
        vista = VerificarEmailView(
            self,
            email=email,
            on_verificado=on_verificado,
            on_volver=self._mostrar_login,
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
        es_supervisor = self.usuario_actual.get('rol') == 'supervisor'
        vista = HistorialView(
            self,
            usuario=self.usuario_actual,
            on_volver=self._mostrar_dashboard,
            es_supervisor=es_supervisor,
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

            # Restaurar timer desde BD (si había ciclo activo)
            from src.timer.servicio_timer import servicio_timer
            servicio_timer.restaurar_desde_bd(str(self.usuario_actual['_id']))

            # Vincular empleado a equipo si no tiene
            self._vincular_a_equipo()

            # Verificar si necesita configurar descansos
            self.after(500, self._verificar_config_descansos)
        except Exception as e:
            if hasattr(self.vista_actual, 'mostrar_error'):
                self.vista_actual.mostrar_error(str(e))
            raise

    def _on_login_frase(self, email, usuario_data):
        """Login con frase semilla - sin contraseña."""
        try:
            self.usuario_actual = usuario_data
            self._mostrar_dashboard()

            # Restaurar timer desde BD
            from src.timer.servicio_timer import servicio_timer
            servicio_timer.restaurar_desde_bd(str(self.usuario_actual['_id']))

            # Vincular empleado a equipo
            self._vincular_a_equipo()

            # Verificar descansos
            self.after(500, self._verificar_config_descansos)
        except Exception as e:
            if hasattr(self.vista_actual, 'mostrar_error'):
                self.vista_actual.mostrar_error(str(e))
            raise

    def _vincular_a_equipo(self):
        """Vincula el usuario al equipo del supervisor si no tiene equipo."""
        try:
            from src.db.conexion import conexion_global
            coleccion_equipos = conexion_global.obtener_coleccion('equipos')

            # Verificar si ya está en algún equipo
            equipo_existente = coleccion_equipos.find_one({
                'miembros': self.usuario_actual['_id']
            })
            if equipo_existente:
                return

            # Buscar equipo del supervisor
            if self.usuario_actual.get('rol') == 'supervisor':
                # Supervisor crea su propio equipo si no tiene
                equipo = coleccion_equipos.find_one({
                    'encargado_id': self.usuario_actual['_id']
                })
                if not equipo:
                    coleccion_equipos.insert_one({
                        'nombre': f"Equipo {self.usuario_actual.get('nombre', 'Principal')}",
                        'encargado_id': self.usuario_actual['_id'],
                        'miembros': [self.usuario_actual['_id']],
                        'descansos_fijos': [],
                        'horario': {'inicio': '09:00', 'fin': '16:00'},
                    })
            else:
                # Empleado/encargado se vincula al primer equipo disponible
                equipo = coleccion_equipos.find_one()
                if equipo:
                    coleccion_equipos.update_one(
                        {'_id': equipo['_id']},
                        {'$addToSet': {'miembros': self.usuario_actual['_id']}}
                    )
        except Exception:  # nosec
            pass

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
        except Exception:  # nosec
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
            except Exception:  # nosec
                pass
        self.usuario_actual = None
        self._mostrar_login()

    def _on_registro_completo(self, email):
        """Callback cuando el registro termina - va a verificación."""
        self._mostrar_verificar_email(email, self._on_email_verificado)

    def _on_email_verificado(self):
        """Callback después de verificar email - mostrar paso 3."""
        self._mostrar_registro_verificado(self._email_verificado)

    def _mostrar_registro_verificado(self, email):
        """Muestra el paso 3 del registro después de verificación."""
        self._limpiar_vista()

        from src.ui.registro_resultado_view import RegistroResultadoView
        vista = RegistroResultadoView(
            self,
            email=email,
            on_login=self._mostrar_login,
        )
        vista.pack(fill="both", expand=True)
        self.vista_actual = vista
