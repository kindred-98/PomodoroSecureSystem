"""
Módulo: historial_view.py
Responsabilidad: Vista de historial de sesiones Pomodoro.
"""

import customtkinter as ctk
from src.config.colores import *


class HistorialView(ctk.CTkFrame):
    """Pantalla de historial de sesiones del usuario."""

    def __init__(self, parent, usuario, on_volver, es_supervisor=False):
        super().__init__(parent, fg_color=FONDO_PRINCIPAL)
        self.usuario = usuario
        self.on_volver = on_volver
        self.es_supervisor = es_supervisor
        self._crear_widgets()
        self._cargar_sesiones()

    def _crear_widgets(self):
        # Header
        header = ctk.CTkFrame(self, fg_color=FONDO_SECUNDARIO, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkButton(
            header, text="← Volver",
            font=("Comic Sans MS", 12),
            fg_color=BOTON_SECUNDARIO, hover_color=BOTON_SECUNDARIO_HOVER,
            text_color=TEXTO_PRINCIPAL, width=100, height=36, corner_radius=8,
            command=self.on_volver,
        ).pack(side="left", padx=20, pady=12)

        titulo = "📋 Historial de Sesiones" if not self.es_supervisor else "📋 Historial del Equipo"
        ctk.CTkLabel(
            header, text=titulo,
            font=("Comic Sans MS", 16, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(side="left", padx=20)

        # Contenido
        contenido = ctk.CTkFrame(self, fg_color="transparent")
        contenido.pack(fill="both", expand=True, padx=20, pady=15)

        # Card de resumen
        self.card_resumen = ctk.CTkFrame(contenido, fg_color=FONDO_CARD, corner_radius=12)
        self.card_resumen.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            self.card_resumen, text="📊 Resumen",
            font=("Comic Sans MS", 14, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(anchor="w", padx=20, pady=(15, 5))

        self.label_resumen = ctk.CTkLabel(
            self.card_resumen, text="Cargando...",
            font=("Comic Sans MS", 12), text_color=TEXTO_SECUNDARIO,
        )
        self.label_resumen.pack(anchor="w", padx=20, pady=(0, 15))

        # Tabs para supervisor
        if self.es_supervisor:
            self.tabs = ctk.CTkTabview(contenido, fg_color=FONDO_CARD)
            self.tabs.pack(fill="both", expand=True, pady=(15, 0))
            
            self.tab_sesiones = self.tabs.add("🍅 Sesiones")
            self.tab_pausas = self.tabs.add("⏸️ Pausas")
            
            self.frame_sesiones = ctk.CTkScrollableFrame(
                self.tab_sesiones, fg_color="transparent",
                scrollbar_button_color=BORDE,
            )
            self.frame_sesiones.pack(fill="both", expand=True)
            
            self.frame_pausas = ctk.CTkScrollableFrame(
                self.tab_pausas, fg_color="transparent",
                scrollbar_button_color=BORDE,
            )
            self.frame_pausas.pack(fill="both", expand=True)
        else:
            ctk.CTkLabel(
                contenido, text="Sesiones recientes",
                font=("Comic Sans MS", 13, "bold"), text_color=TEXTO_PRINCIPAL,
            ).pack(anchor="w", pady=(0, 5))

            self.frame_sesiones = ctk.CTkScrollableFrame(
                contenido, fg_color=FONDO_CARD, corner_radius=12,
                scrollbar_button_color=BORDE,
            )
            self.frame_sesiones.pack(fill="both", expand=True)

    def _cargar_sesiones(self):
        """Carga las sesiones del usuario desde BD."""
        try:
            from src.db.conexion import conexion_global
            from src.db.usuarios.buscar_por_id import buscar_por_id
            from bson import ObjectId

            # Obtener miembros del equipo del supervisor
            usuario_id = str(self.usuario['_id'])
            
            if self.es_supervisor:
                self._cargar_historial_supervisor()
            else:
                coleccion = conexion_global.obtener_coleccion('sesiones')
                sesiones = list(coleccion.find(
                    {'usuario_id': self.usuario['_id']}
                ).sort('inicio', -1).limit(50))

                self._mostrar_sesiones(sesiones)

        except Exception as e:
            self.label_resumen.configure(text=f"Error: {e}")

    def _cargar_historial_supervisor(self):
        """Carga el historial completo del equipo para el supervisor."""
        try:
            from src.db.conexion import conexion_global
            from src.db.equipos import listar_todos
            from bson import ObjectId

            # Obtener todos los equipos
            equipos = listar_todos()
            
            # Recolectar todos los usuario_ids de los equipos
            todos_usuarios = set()
            for eq in equipos:
                for miembros in eq.get('miembros', []):
                    todos_usuarios.add(miembros)
            
            # Cargar sesiones de todos los usuarios
            coleccion_sesiones = conexion_global.obtener_coleccion('sesiones')
            sesiones = list(coleccion_sesiones.find(
                {'usuario_id': {'$in': list(todos_usuarios)}}
            ).sort('inicio', -1).limit(100))
            
            # Cargar usuarios para mostrar nombres
            coleccion_usuarios = conexion_global.obtener_coleccion('usuarios')
            usuarios_map = {}
            for u in coleccion_usuarios.find({'_id': {'$in': list(todos_usuarios)}}):
                usuarios_map[u['_id']] = u.get('nombre', 'Desconocido')
            
            # Resumen
            total_pomodoros = sum(1 for s in sesiones if s.get('tipo_sesion') == 'pomodoro')
            total_segundos = sum(s.get('duracion_segundos', 0) for s in sesiones)
            total_usuarios = len(set(s.get('usuario_id') for s in sesiones))
            
            self.label_resumen.configure(
                text=f"Usuarios: {total_usuarios} | Pomodoros: {total_pomodoros} | Tiempo: {total_segundos//3600}h"
            )
            
            # Limpiar y mostrar sesiones
            for widget in self.frame_sesiones.winfo_children():
                widget.destroy()
            
            for sesion in sesiones:
                nombre = usuarios_map.get(sesion.get('usuario_id'), 'Desconocido')
                tipo = sesion.get('tipo_sesion', 'pomodoro')
                emoji = "🍅" if tipo == "pomodoro" else "☕"
                color = TRABAJO_ACTIVO if tipo == "pomodoro" else TIMER_DESCANSO_CORTO
                
                frame = ctk.CTkFrame(self.frame_sesiones, fg_color=FONDO_SECUNDARIO, corner_radius=6)
                frame.pack(fill="x", pady=2)
                
                ctk.CTkLabel(frame, text=emoji, font=("Segoe UI Emoji", 16), text_color=color).pack(side="left", padx=(10, 5), pady=6)
                
                info = ctk.CTkFrame(frame, fg_color="transparent")
                info.pack(side="left", fill="x", expand=True, pady=6)
                
                duracion_min = sesion.get('duracion_segundos', 0) // 60
                ciclo = sesion.get('numero_ciclo', '?')
                pom = sesion.get('pomodoro_numero', '?')
                
                ctk.CTkLabel(info, text=f"{nombre} - Ciclo {ciclo} - Pom {pom} - {duracion_min} min", font=("Comic Sans MS", 11), text_color=TEXTO_PRINCIPAL, anchor="w").pack(fill="x")
                
                inicio = sesion.get('inicio', '')
                if hasattr(inicio, 'strftime'):
                    fecha = inicio.strftime("%d/%m/%Y %H:%M")
                else:
                    fecha = str(inicio)[:16]
                ctk.CTkLabel(info, text=fecha, font=("Comic Sans MS", 10), text_color=TEXTO_SECUNDARIO, anchor="w").pack(fill="x")
            
            # Cargar pausas
            self._cargar_pausas_historial(usuarios_map)

        except Exception as e:
            print(f"Error cargando historial supervisor: {e}")

    def _cargar_pausas_historial(self, usuarios_map):
        """Carga el historial de pausas."""
        try:
            from src.db.conexion import conexion_global
            
            coleccion = conexion_global.obtener_coleccion('pausas_manuales')
            pausas = list(coleccion.find().sort('inicio', -1).limit(50))
            
            for widget in self.frame_pausas.winfo_children():
                widget.destroy()
            
            if not pausas:
                ctk.CTkLabel(self.frame_pausas, text="No hay pausas registradas", font=("Comic Sans MS", 12), text_color=TEXTO_SECUNDARIO).pack(pady=30)
                return
            
            for pausa in pausas:
                usuario_nombre = usuarios_map.get(pausa.get('usuario_id'), 'Desconocido')
                duracion = pausa.get('duracion_minutos', 0)
                excedida = pausa.get('excedida', False)
                
                frame = ctk.CTkFrame(self.frame_pausas, fg_color=FONDO_SECUNDARIO, corner_radius=6)
                frame.pack(fill="x", pady=2)
                
                emoji = "⏸️" if not excedida else "⚠️"
                color = TIMER_PAUSADO if not excedida else PELIGRO
                
                ctk.CTkLabel(frame, text=emoji, font=("Segoe UI Emoji", 16), text_color=color).pack(side="left", padx=(10, 5), pady=6)
                
                info = ctk.CTkFrame(frame, fg_color="transparent")
                info.pack(side="left", fill="x", expand=True, pady=6)
                
                ctk.CTkLabel(info, text=f"{usuario_nombre} - {duracion} min{' (EXCEDIDA)' if excedida else ''}", font=("Comic Sans MS", 11), text_color=TEXTO_PRINCIPAL, anchor="w").pack(fill="x")
                
                inicio = pausa.get('inicio', '')
                if hasattr(inicio, 'strftime'):
                    fecha = inicio.strftime("%d/%m/%Y %H:%M")
                else:
                    fecha = str(inicio)[:16]
                ctk.CTkLabel(info, text=fecha, font=("Comic Sans MS", 10), text_color=TEXTO_SECUNDARIO, anchor="w").pack(fill="x")
        
        except Exception as e:
            print(f"Error cargando pausas: {e}")

    def _mostrar_sesiones(self, sesiones):
        """Muestra las sesiones en el frame."""
        # Resumen
        total_pomodoros = sum(
            1 for s in sesiones if s.get('tipo_sesion') == 'pomodoro'
        )
        total_segundos = sum(
            s.get('duracion_segundos', 0) for s in sesiones
        )
        horas = total_segundos // 3600
        minutos = (total_segundos % 3600) // 60

        self.label_resumen.configure(
            text=f"Total Pomodoros: {total_pomodoros} | Tiempo trabajado: {horas}h {minutos}m"
        )

        # Limpiar
        for widget in self.frame_sesiones.winfo_children():
            widget.destroy()

        if not sesiones:
            ctk.CTkLabel(
                self.frame_sesiones,
                text="No hay sesiones registradas",
                font=("Comic Sans MS", 12), text_color=TEXTO_SECUNDARIO,
            ).pack(pady=30)
            return

        for sesion in sesiones:
            frame = ctk.CTkFrame(self.frame_sesiones, fg_color=FONDO_SECUNDARIO, corner_radius=6)
            frame.pack(fill="x", pady=2)

            # Tipo
            tipo = sesion.get('tipo_sesion', 'pomodoro')
            emoji = "🍅" if tipo == "pomodoro" else "☕"
            color = TRABAJO_ACTIVO if tipo == "pomodoro" else TIMER_DESCANSO_CORTO

            ctk.CTkLabel(
                frame, text=emoji,
                font=("Segoe UI Emoji", 16), text_color=color,
            ).pack(side="left", padx=(10, 5), pady=6)

            # Info
            info = ctk.CTkFrame(frame, fg_color="transparent")
            info.pack(side="left", fill="x", expand=True, pady=6)

            duracion_min = sesion.get('duracion_segundos', 0) // 60
            ciclo = sesion.get('numero_ciclo', '?')
            pom = sesion.get('pomodoro_numero', '?')

            ctk.CTkLabel(
                info,
                text=f"Ciclo {ciclo} — Pomodoro {pom} — {duracion_min} min",
                font=("Comic Sans MS", 11), text_color=TEXTO_PRINCIPAL,
                anchor="w",
            ).pack(fill="x")

            inicio = sesion.get('inicio', '')
            if hasattr(inicio, 'strftime'):
                fecha = inicio.strftime("%d/%m/%Y %H:%M")
            else:
                fecha = str(inicio)[:16]
            ctk.CTkLabel(
                info, text=fecha,
                font=("Comic Sans MS", 10), text_color=TEXTO_SECUNDARIO,
                anchor="w",
            ).pack(fill="x")

