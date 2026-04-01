"""
Módulo: config_descansos_view.py
Responsabilidad: Configuración de descansos fijos de empresa (solo supervisor).
"""

import customtkinter as ctk
from src.config.colores import *


class ConfigDescansosView(ctk.CTkToplevel):
    """Ventana de configuración de descansos fijos de empresa."""

    def __init__(self, parent, usuario):
        super().__init__(parent)
        self.usuario = usuario
        self.title("Configurar Descansos Fijos")
        self.geometry("600x500")
        self.configure(fg_color=FONDO_PRINCIPAL)
        self._crear_widgets()
        self._cargar_descansos()

    def _crear_widgets(self):
        # Header
        ctk.CTkLabel(
            self, text="☕ Descansos Fijos de Empresa",
            font=("JetBrains Mono", 18, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(padx=20, pady=(20, 5))

        ctk.CTkLabel(
            self,
            text="Los descansos fijos son obligatorios y no pueden ser modificados por los empleados.",
            font=("JetBrains Mono", 11), text_color=TEXTO_SECUNDARIO,
            wraplength=550,
        ).pack(padx=20, pady=(0, 15))

        # Lista de descansos actuales
        self.frame_descansos = ctk.CTkScrollableFrame(
            self, fg_color=FONDO_CARD, corner_radius=12,
            scrollbar_button_color=BORDE,
        )
        self.frame_descansos.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        # Formulario para nuevo descanso
        form = ctk.CTkFrame(self, fg_color=FONDO_CARD, corner_radius=12)
        form.pack(fill="x", padx=20, pady=(0, 15))

        ctk.CTkLabel(
            form, text="➕ Nuevo descanso",
            font=("JetBrains Mono", 13, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(anchor="w", padx=15, pady=(10, 5))

        fila = ctk.CTkFrame(form, fg_color="transparent")
        fila.pack(fill="x", padx=15, pady=(0, 10))

        # Nombre
        ctk.CTkLabel(fila, text="Nombre:", font=("JetBrains Mono", 11),
                     text_color=TEXTO_SECUNDARIO).pack(side="left")
        self.entry_nombre = ctk.CTkEntry(
            fila, placeholder_text="Ej: Café mañana",
            font=("JetBrains Mono", 12), fg_color=FONDO_SECUNDARIO,
            text_color=TEXTO_PRINCIPAL, width=150, height=32, corner_radius=6,
        )
        self.entry_nombre.pack(side="left", padx=(5, 15))

        # Hora inicio
        ctk.CTkLabel(fila, text="Hora:", font=("JetBrains Mono", 11),
                     text_color=TEXTO_SECUNDARIO).pack(side="left")
        self.entry_hora = ctk.CTkEntry(
            fila, placeholder_text="10:30",
            font=("JetBrains Mono", 12), fg_color=FONDO_SECUNDARIO,
            text_color=TEXTO_PRINCIPAL, width=70, height=32, corner_radius=6,
        )
        self.entry_hora.pack(side="left", padx=(5, 15))

        # Duración
        ctk.CTkLabel(fila, text="Min:", font=("JetBrains Mono", 11),
                     text_color=TEXTO_SECUNDARIO).pack(side="left")
        self.entry_duracion = ctk.CTkEntry(
            fila, placeholder_text="15",
            font=("JetBrains Mono", 12), fg_color=FONDO_SECUNDARIO,
            text_color=TEXTO_PRINCIPAL, width=50, height=32, corner_radius=6,
        )
        self.entry_duracion.pack(side="left", padx=(5, 10))

        ctk.CTkButton(
            fila, text="Añadir",
            font=("JetBrains Mono", 11, "bold"),
            fg_color=BOTON_EXITO, hover_color=BOTON_EXITO_HOVER,
            text_color=TEXTO_PRINCIPAL, width=70, height=32, corner_radius=6,
            command=self._añadir_descanso,
        ).pack(side="right")

    def _cargar_descansos(self):
        """Carga descansos fijos actuales."""
        for widget in self.frame_descansos.winfo_children():
            widget.destroy()

        try:
            from src.db.conexion import conexion_global

            coleccion = conexion_global.obtener_coleccion('equipos')
            rol = self.usuario.get('rol', 'empleado')
            uid = self.usuario['_id']

            if rol == 'supervisor':
                equipo = coleccion.find_one()
                if equipo is None:
                    # Crear equipo por defecto para supervisor
                    equipo = {
                        'nombre': 'Equipo Principal',
                        'encargado_id': uid,
                        'miembros': [],
                        'descansos_fijos': [],
                        'horario': {'inicio': '09:00', 'fin': '16:00'},
                    }
                    resultado = coleccion.insert_one(equipo)
                    equipo['_id'] = resultado.inserted_id
            else:
                equipo = coleccion.find_one({'encargado_id': uid})

            if not equipo:
                ctk.CTkLabel(
                    self.frame_descansos,
                    text="No tienes un equipo asignado. Contacta a tu supervisor.",
                    font=("JetBrains Mono", 12), text_color=TEXTO_SECUNDARIO,
                ).pack(pady=20)
                self._equipo_actual = None
                return

            self._equipo_actual = equipo
            descansos = equipo.get('descansos_fijos', [])

            if not descansos:
                ctk.CTkLabel(
                    self.frame_descansos,
                    text="No hay descansos fijos. Usa el formulario de abajo para agregar.",
                    font=("JetBrains Mono", 12), text_color=TEXTO_SECUNDARIO,
                ).pack(pady=20)
                return

            for desc in descansos:
                frame = ctk.CTkFrame(self.frame_descansos, fg_color=FONDO_SECUNDARIO, corner_radius=6)
                frame.pack(fill="x", pady=2)

                ctk.CTkLabel(
                    frame,
                    text=f"{desc.get('nombre', '')}  |  {desc.get('hora_inicio', '')}  |  {desc.get('duracion_min', 0)} min",
                    font=("JetBrains Mono", 12), text_color=TEXTO_PRINCIPAL,
                ).pack(side="left", padx=10, pady=8)

        except Exception as e:
            ctk.CTkLabel(
                self.frame_descansos,
                text=f"Error: {e}",
                font=("JetBrains Mono", 12), text_color=PELIGRO,
            ).pack(pady=20)

    def _añadir_descanso(self):
        """Añade un nuevo descanso fijo al equipo."""
        nombre = self.entry_nombre.get().strip()
        hora = self.entry_hora.get().strip()
        duracion = self.entry_duracion.get().strip()

        if not nombre or not hora or not duracion:
            return

        try:
            duracion_int = int(duracion)
        except ValueError:
            return

        equipo = getattr(self, '_equipo_actual', None)
        if equipo is None:
            return

        nuevo = {
            'nombre': nombre,
            'hora_inicio': hora,
            'duracion_min': duracion_int,
        }

        from src.db.conexion import conexion_global
        coleccion = conexion_global.obtener_coleccion('equipos')

        descansos_actuales = list(equipo.get('descansos_fijos', []))
        descansos_actuales.append(nuevo)

        coleccion.update_one(
            {'_id': equipo['_id']},
            {'$set': {'descansos_fijos': descansos_actuales}}
        )

        # Actualizar cache local
        self._equipo_actual['descansos_fijos'] = descansos_actuales

        self.entry_nombre.delete(0, "end")
        self.entry_hora.delete(0, "end")
        self.entry_duracion.delete(0, "end")

        self._cargar_descansos()
