"""
Módulo: gestion_equipos_view.py
Responsabilidad: Vista para gestionar equipos (crear, editar, asignar miembros).
"""

import customtkinter as ctk
from src.config.colores import *


class GestionEquiposView(ctk.CTkToplevel):
    """Vista de gestión de equipos."""

    def __init__(self, parent, usuario):
        super().__init__(parent, fg_color=FONDO_PRINCIPAL)
        self.usuario = usuario
        self.title("Gestión de Equipos")
        self.geometry("900x600")
        self.transient(parent)
        self.grab_set()

        x = (self.winfo_screenwidth() // 2) - (900 // 2)
        y = (self.winfo_screenheight() // 2) - (600 // 2)
        self.geometry(f"900x600+{x}+{y}")

        self._crear_widgets()
        self._cargar_equipos()

    def _crear_widgets(self):
        # Header
        header = ctk.CTkFrame(self, fg_color=FONDO_SECUNDARIO, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header, text="👥 Gestión de Equipos",
            font=("JetBrains Mono", 18, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(side="left", padx=20, pady=12)

        ctk.CTkButton(
            header, text="+ Crear Equipo",
            font=("JetBrains Mono", 12),
            fg_color=BOTON_PRIMARIO, hover_color=BOTON_PRIMARIO_HOVER,
            text_color=TEXTO_PRINCIPAL, width=120, height=36, corner_radius=8,
            command=self._crear_equipo,
        ).pack(side="right", padx=20, pady=12)

        # Body
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=20, pady=20)

        # Panel izquierdo: lista de equipos
        lista_frame = ctk.CTkFrame(body, fg_color=FONDO_SECUNDARIO, width=300, corner_radius=12)
        lista_frame.pack(side="left", fill="y", padx=(0, 15))
        lista_frame.pack_propagate(False)

        ctk.CTkLabel(
            lista_frame, text="Equipos",
            font=("JetBrains Mono", 14, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(anchor="w", padx=15, pady=(15, 10))

        self.frame_equipos = ctk.CTkScrollableFrame(
            lista_frame, fg_color="transparent",
            scrollbar_button_color=BORDE,
        )
        self.frame_equipos.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Panel derecho: detalle del equipo
        self.panel_detalle = ctk.CTkFrame(body, fg_color="transparent")
        self.panel_detalle.pack(side="right", fill="both", expand=True)

        self.label_detalle_vacio = ctk.CTkLabel(
            self.panel_detalle,
            text="Selecciona un equipo para ver sus detalles",
            font=("JetBrains Mono", 14),
            text_color=TEXTO_SECUNDARIO,
        )
        self.label_detalle_vacio.pack(pady=50)

        self._equipo_seleccionado = None

    def _cargar_equipos(self):
        """Carga la lista de equipos."""
        for widget in self.frame_equipos.winfo_children():
            widget.destroy()

        try:
            from src.db.equipos import listar_todos
            equipos = listar_todos()

            if not equipos:
                ctk.CTkLabel(
                    self.frame_equipos,
                    text="No hay equipos creados.\nUsa el botón 'Crear Equipo'",
                    font=("JetBrains Mono", 11),
                    text_color=TEXTO_SECUNDARIO,
                ).pack(pady=20)
                return

            for equipo in equipos:
                frame = ctk.CTkFrame(
                    self.frame_equipos, fg_color=FONDO_CARD, corner_radius=8
                )
                frame.pack(fill="x", pady=3)

                nombre = equipo.get('nombre', 'Sin nombre')
                miembros = equipo.get('miembros', [])
                encargado = equipo.get('encargado_id')

                btn = ctk.CTkButton(
                    frame, text=f"📁 {nombre}",
                    font=("JetBrains Mono", 11),
                    fg_color="transparent", hover_color=FONDO_CARD,
                    text_color=TEXTO_PRINCIPAL, height=36, corner_radius=6,
                    command=lambda e=equipo: self._seleccionar_equipo(e),
                    anchor="w",
                )
                btn.pack(fill="x", padx=5, pady=2)

                info = ctk.CTkLabel(
                    frame, text=f"{len(miembros)} miembros" + (f" | Con encargado" if encargado else " | Sin encargado"),
                    font=("JetBrains Mono", 9),
                    text_color=TEXTO_SECUNDARIO,
                    anchor="w",
                )
                info.pack(anchor="w", padx=15, pady=(0, 5))

        except Exception as e:
            ctk.CTkLabel(
                self.frame_equipos,
                text=f"Error: {e}",
                font=("JetBrains Mono", 11),
                text_color=PELIGRO,
            ).pack(pady=20)

    def _seleccionar_equipo(self, equipo):
        """Muestra los detalles del equipo seleccionado."""
        self._equipo_seleccionado = equipo
        self.label_detalle_vacio.pack_forget()

        for widget in self.panel_detalle.winfo_children():
            widget.destroy()

        # Card de detalle
        detalle_card = ctk.CTkFrame(self.panel_detalle, fg_color=FONDO_CARD, corner_radius=12)
        detalle_card.pack(fill="both", expand=True, padx=10, pady=10)

        # Nombre del equipo
        nombre_frame = ctk.CTkFrame(detalle_card, fg_color="transparent")
        nombre_frame.pack(fill="x", padx=20, pady=(20, 5))

        ctk.CTkLabel(
            nombre_frame, text="Nombre:",
            font=("JetBrains Mono", 12), text_color=TEXTO_SECUNDARIO,
            width=100,
        ).pack(side="left")

        self.entry_nombre = ctk.CTkEntry(
            nombre_frame,
            font=("JetBrains Mono", 12),
            fg_color=FONDO_SECUNDARIO, text_color=TEXTO_PRINCIPAL,
            height=36, corner_radius=8,
        )
        self.entry_nombre.pack(side="left", fill="x", expand=True, padx=(5, 10))
        self.entry_nombre.insert(0, equipo.get('nombre', ''))

        ctk.CTkButton(
            nombre_frame, text="Guardar",
            font=("JetBrains Mono", 11),
            fg_color=BOTON_EXITO, hover_color=BOTON_EXITO_HOVER,
            text_color=TEXTO_PRINCIPAL, width=80, height=32, corner_radius=6,
            command=self._guardar_nombre,
        ).pack(side="right")

        # Encargado
        encargado_frame = ctk.CTkFrame(detalle_card, fg_color="transparent")
        encargado_frame.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(
            encargado_frame, text="Encargado:",
            font=("JetBrains Mono", 12), text_color=TEXTO_SECUNDARIO,
            width=100,
        ).pack(side="left")

        self._cargar_encargados_disponibles(encargado_frame, equipo)

        # Miembros
        miembros_label = ctk.CTkLabel(
            detalle_card, text="Miembros del equipo:",
            font=("JetBrains Mono", 12, "bold"), text_color=TEXTO_PRINCIPAL,
        )
        miembros_label.pack(anchor="w", padx=20, pady=(15, 5))

        frame_miembros = ctk.CTkScrollableFrame(
            detalle_card, fg_color="transparent",
            height=150, scrollbar_button_color=BORDE,
        )
        frame_miembros.pack(fill="x", padx=20, pady=(0, 10))

        self._cargar_miembros_equipo(frame_miembros, equipo)

        # Agregar miembro
        agregar_frame = ctk.CTkFrame(detalle_card, fg_color="transparent")
        agregar_frame.pack(fill="x", padx=20, pady=(0, 10))

        self.entry_agregar = ctk.CTkEntry(
            agregar_frame, placeholder_text="ID o email del usuario...",
            font=("JetBrains Mono", 11),
            fg_color=FONDO_SECUNDARIO, text_color=TEXTO_PRINCIPAL,
            height=36, corner_radius=8,
        )
        self.entry_agregar.pack(side="left", fill="x", expand=True, padx=(0, 10))

        ctk.CTkButton(
            agregar_frame, text="+ Agregar",
            font=("JetBrains Mono", 11),
            fg_color=BOTON_PRIMARIO, hover_color=BOTON_PRIMARIO_HOVER,
            text_color=TEXTO_PRINCIPAL, width=100, height=36, corner_radius=8,
            command=self._agregar_miembro,
        ).pack(side="right")

        # Botón eliminar equipo
        btn_eliminar = ctk.CTkButton(
            detalle_card, text="🗑 Eliminar Equipo",
            font=("JetBrains Mono", 12),
            fg_color=BOTON_PELIGRO, hover_color=BOTON_PELIGRO_HOVER,
            text_color=TEXTO_PRINCIPAL, height=40, corner_radius=8,
            command=self._eliminar_equipo,
        )
        btn_eliminar.pack(pady=(20, 10))

    def _cargar_encargados_disponibles(self, parent, equipo):
        """Carga los encargados disponibles para asignar."""
        try:
            from src.db.conexion import conexion_global
            coleccion = conexion_global.obtener_coleccion('usuarios')
            usuarios = list(coleccion.find({'rol': 'encargado', 'activo': True}))

            valores = ["-- Sin asignar --"]
            self._encargados_map = {"-- Sin asignar --": None}
            for u in usuarios:
                nombre = u.get('nombre', 'Sin nombre')
                email = u.get('email', '')
                valores.append(f"{nombre} ({email})")
                self._encargados_map[f"{nombre} ({email})"] = str(u['_id'])

            self.combo_encargado = ctk.CTkComboBox(
                parent,
                values=valores,
                font=("JetBrains Mono", 11),
                fg_color=FONDO_SECUNDARIO, text_color=TEXTO_PRINCIPAL,
                button_color=BORDE, width=200,
            )
            self.combo_encargado.pack(side="left", fill="x", expand=True, padx=(5, 10))

            # Seleccionar encargado actual
            encargado_actual = equipo.get('encargado_id')
            if encargado_actual:
                for k, v in self._encargados_map.items():
                    if v and str(v) == str(encargado_actual):
                        self.combo_encargado.set(k)
                        break

            ctk.CTkButton(
                parent, text="Asignar",
                font=("JetBrains Mono", 11),
                fg_color=BOTON_SECUNDARIO, hover_color=BOTON_SECUNDARIO_HOVER,
                text_color=TEXTO_PRINCIPAL, width=80, height=32, corner_radius=6,
                command=self._asignar_encargado,
            ).pack(side="right")

        except Exception as e:
            ctk.CTkLabel(
                parent, text=f"Error: {e}",
                font=("JetBrains Mono", 10),
                text_color=PELIGRO,
            ).pack(side="left")

    def _cargar_miembros_equipo(self, parent, equipo):
        """Carga los miembros del equipo."""
        try:
            from src.db.equipos import obtener_miembros
            miembros = obtener_miembros(str(equipo['_id']))

            if not miembros:
                ctk.CTkLabel(
                    parent, text="No hay miembros en este equipo",
                    font=("JetBrains Mono", 11),
                    text_color=TEXTO_SECUNDARIO,
                ).pack(pady=10)
                return

            for m in miembros:
                frame = ctk.CTkFrame(parent, fg_color=FONDO_SECUNDARIO, corner_radius=6)
                frame.pack(fill="x", pady=2)

                nombre = m.get('nombre', 'Sin nombre')
                rol = m.get('rol', 'empleado').title()
                email = m.get('email', '')

                ctk.CTkLabel(
                    frame, text=f"👤 {nombre}",
                    font=("JetBrains Mono", 11), text_color=TEXTO_PRINCIPAL,
                    anchor="w",
                ).pack(side="left", padx=10, pady=8)

                ctk.CTkLabel(
                    frame, text=rol,
                    font=("JetBrains Mono", 9),
                    text_color=AVISO,
                ).pack(side="left", padx=5)

                ctk.CTkButton(
                    frame, text="Quitar",
                    font=("JetBrains Mono", 9),
                    fg_color=BOTON_PELIGRO, hover_color=BOTON_PELIGRO_HOVER,
                    text_color=TEXTO_PRINCIPAL, width=60, height=24, corner_radius=4,
                    command=lambda mm=m: self._quitar_miembro(mm),
                ).pack(side="right", padx=10, pady=4)

        except Exception as e:
            ctk.CTkLabel(
                parent, text=f"Error: {e}",
                font=("JetBrains Mono", 10),
                text_color=PELIGRO,
            ).pack(pady=10)

    def _guardar_nombre(self):
        """Guarda el nuevo nombre del equipo."""
        if not self._equipo_seleccionado:
            return

        nuevo_nombre = self.entry_nombre.get().strip()
        if not nuevo_nombre:
            return

        try:
            from src.db.equipos import editar_nombre
            editar_nombre(str(self._equipo_seleccionado['_id']), nuevo_nombre)
            self._cargar_equipos()
        except Exception as e:
            pass

    def _asignar_encargado(self):
        """Asigna un encargado al equipo."""
        if not self._equipo_seleccionado:
            return

        valor = self.combo_encargado.get()
        if valor == "-- Sin asignar --":
            return

        encargado_id = self._encargados_map.get(valor)
        if not encargado_id:
            return

        try:
            from src.db.equipos import asignar_encargado
            asignar_encargado(str(self._equipo_seleccionado['_id']), encargado_id)
            self._cargar_equipos()
        except Exception:
            pass

    def _agregar_miembro(self):
        """Agrega un miembro al equipo."""
        if not self._equipo_seleccionado:
            return

        texto = self.entry_agregar.get().strip()
        if not texto:
            return

        try:
            from src.db.equipos import añadir_miembro
            from src.db.conexion import conexion_global

            coleccion = conexion_global.obtener_coleccion('usuarios')

            # Buscar por ID o email
            from bson import ObjectId
            try:
                usuario = coleccion.find_one({'_id': ObjectId(texto)})
            except Exception:
                usuario = coleccion.find_one({'email': {'$regex': texto, '$options': 'i'}})

            if not usuario:
                return

            añadir_miembro(str(self._equipo_seleccionado['_id']), str(usuario['_id']))
            self.entry_agregar.delete(0, "end")
            self._seleccionar_equipo(self._equipo_seleccionado)
        except Exception:
            pass

    def _quitar_miembro(self, miembro):
        """Quita un miembro del equipo."""
        if not self._equipo_seleccionado:
            return

        try:
            from src.db.equipos import quitar_miembro
            quitar_miembro(str(self._equipo_seleccionado['_id']), str(miembro['_id']))
            self._seleccionar_equipo(self._equipo_seleccionado)
        except Exception:
            pass

    def _eliminar_equipo(self):
        """Elimina el equipo seleccionado."""
        if not self._equipo_seleccionado:
            return

        try:
            from src.db.equipos import eliminar_equipo
            eliminar_equipo(str(self._equipo_seleccionado['_id']))

            # Limpiar panel y recargar
            for widget in self.panel_detalle.winfo_children():
                widget.destroy()
            self.label_detalle_vacio.pack(pady=50)
            self._equipo_seleccionado = None
            self._cargar_equipos()
        except Exception:
            pass

    def _crear_equipo(self):
        """Abre diálogo para crear un nuevo equipo."""
        dialogo = ctk.CTkToplevel(self)
        dialogo.title("Crear Equipo")
        dialogo.geometry("400x200")
        dialogo.transient(self)
        dialogo.grab_set()

        x = (dialogo.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialogo.winfo_screenheight() // 2) - (200 // 2)
        dialogo.geometry(f"400x200+{x}+{y}")

        ctk.CTkLabel(
            dialogo, text="Nombre del nuevo equipo:",
            font=("JetBrains Mono", 14), text_color=TEXTO_PRINCIPAL,
        ).pack(pady=20)

        entry_nombre = ctk.CTkEntry(
            dialogo, placeholder_text="Ej: Equipo de Frontend",
            font=("JetBrains Mono", 13),
            fg_color=FONDO_SECUNDARIO, text_color=TEXTO_PRINCIPAL,
            height=40, corner_radius=8,
        )
        entry_nombre.pack(padx=40, fill="x", pady=(0, 20))

        def confirmar():
            nombre = entry_nombre.get().strip()
            if not nombre:
                return

            try:
                from src.db.equipos import crear_equipo
                crear_equipo(nombre, str(self.usuario['_id']))
                dialogo.destroy()
                self._cargar_equipos()
            except Exception:
                pass

        ctk.CTkButton(
            dialogo, text="Crear",
            font=("JetBrains Mono", 12, "bold"),
            fg_color=BOTON_PRIMARIO, hover_color=BOTON_PRIMARIO_HOVER,
            text_color=TEXTO_PRINCIPAL, height=40, corner_radius=8,
            command=confirmar,
        ).pack(padx=40, fill="x")
