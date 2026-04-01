"""
Módulo: config_bloque_descansos.py
Responsabilidad: Popup para configurar descansos por bloque (50 min banco).
Se muestra al supervisor la primera vez que inicia sesión.
"""

import customtkinter as ctk
from src.config.colores import *


class ConfigBloqueDescansos(ctk.CTkToplevel):
    """Popup modal para configurar descansos por bloque."""

    def __init__(self, parent, usuario, on_completo=None):
        super().__init__(parent)
        self.usuario = usuario
        self.on_completo = on_completo

        self.title("Configura tus descansos por bloque")
        self.geometry("520x480")
        self.configure(fg_color=FONDO_PRINCIPAL)
        self.resizable(False, False)

        # Hacer modal
        self.transient(parent)
        self.grab_set()

        self._crear_widgets()

    def _crear_widgets(self):
        ctk.CTkLabel(
            self, text="Configura tus descansos por bloque",
            font=("JetBrains Mono", 16, "bold"), text_color=TEXTO_PRINCIPAL,
        ).pack(padx=20, pady=(20, 5))

        ctk.CTkLabel(
            self,
            text="Tienes 50 minutos de descanso por ciclo.\nRepartelos como prefieras (4 cortos + 1 largo).",
            font=("JetBrains Mono", 11), text_color=TEXTO_SECUNDARIO,
            justify="center",
        ).pack(padx=20, pady=(0, 10))

        # Presets
        presets_frame = ctk.CTkFrame(self, fg_color="transparent")
        presets_frame.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkLabel(
            presets_frame, text="Presets:",
            font=("JetBrains Mono", 12), text_color=TEXTO_SECUNDARIO,
        ).pack(anchor="w")

        presets = [
            ("5+5+5+5 + 30", [5, 5, 5, 5], 30),
            ("7+7+7+7 + 22", [7, 7, 7, 7], 22),
            ("10+10+10+5 + 15", [10, 10, 10, 5], 15),
            ("8+8+8+8 + 18", [8, 8, 8, 8], 18),
        ]

        self.preset_var = ctk.StringVar(value="5+5+5+5 + 30")

        for texto, cortos, largo in presets:
            ctk.CTkRadioButton(
                presets_frame, text=texto,
                variable=self.preset_var, value=texto,
                font=("JetBrains Mono", 11), text_color=TEXTO_SECUNDARIO,
                fg_color=TRABAJO_ACTIVO, hover_color=BOTON_PRIMARIO_HOVER,
            ).pack(anchor="w", pady=1)

        # Separador
        ctk.CTkFrame(self, fg_color=BORDE, height=1).pack(fill="x", padx=20, pady=10)

        # Personalizado
        ctk.CTkLabel(
            self, text="O personaliza:",
            font=("JetBrains Mono", 12), text_color=TEXTO_SECUNDARIO,
        ).pack(anchor="w", padx=20)

        custom_frame = ctk.CTkFrame(self, fg_color="transparent")
        custom_frame.pack(fill="x", padx=20, pady=(5, 5))

        ctk.CTkLabel(custom_frame, text="Corto 1:", font=("JetBrains Mono", 10),
                     text_color=TEXTO_SECUNDARIO).grid(row=0, column=0, padx=3)
        self.e1 = ctk.CTkEntry(custom_frame, width=45, height=28, font=("JetBrains Mono", 11),
                               fg_color=FONDO_SECUNDARIO, text_color=TEXTO_PRINCIPAL)
        self.e1.grid(row=0, column=1, padx=3)
        self.e1.insert(0, "5")

        ctk.CTkLabel(custom_frame, text="Corto 2:", font=("JetBrains Mono", 10),
                     text_color=TEXTO_SECUNDARIO).grid(row=0, column=2, padx=3)
        self.e2 = ctk.CTkEntry(custom_frame, width=45, height=28, font=("JetBrains Mono", 11),
                               fg_color=FONDO_SECUNDARIO, text_color=TEXTO_PRINCIPAL)
        self.e2.grid(row=0, column=3, padx=3)
        self.e2.insert(0, "5")

        ctk.CTkLabel(custom_frame, text="Corto 3:", font=("JetBrains Mono", 10),
                     text_color=TEXTO_SECUNDARIO).grid(row=0, column=4, padx=3)
        self.e3 = ctk.CTkEntry(custom_frame, width=45, height=28, font=("JetBrains Mono", 11),
                               fg_color=FONDO_SECUNDARIO, text_color=TEXTO_PRINCIPAL)
        self.e3.grid(row=0, column=5, padx=3)
        self.e3.insert(0, "5")

        ctk.CTkLabel(custom_frame, text="Corto 4:", font=("JetBrains Mono", 10),
                     text_color=TEXTO_SECUNDARIO).grid(row=0, column=6, padx=3)
        self.e4 = ctk.CTkEntry(custom_frame, width=45, height=28, font=("JetBrains Mono", 11),
                               fg_color=FONDO_SECUNDARIO, text_color=TEXTO_PRINCIPAL)
        self.e4.grid(row=0, column=7, padx=3)
        self.e4.insert(0, "5")

        self.label_info = ctk.CTkLabel(
            self, text="",
            font=("JetBrains Mono", 11), text_color=TEXTO_SECUNDARIO,
        )
        self.label_info.pack(pady=(5, 5))

        # Botones
        botones = ctk.CTkFrame(self, fg_color="transparent")
        botones.pack(fill="x", padx=20, pady=(5, 15))

        ctk.CTkButton(
            botones, text="Usar preset seleccionado",
            font=("JetBrains Mono", 12, "bold"),
            fg_color=BOTON_PRIMARIO, hover_color=BOTON_PRIMARIO_HOVER,
            text_color=TEXTO_PRINCIPAL, height=40, corner_radius=8,
            command=self._usar_preset,
        ).pack(side="left", padx=(0, 5), expand=True, fill="x")

        ctk.CTkButton(
            botones, text="Usar personalizado",
            font=("JetBrains Mono", 12),
            fg_color=BOTON_SECUNDARIO, hover_color=BOTON_SECUNDARIO_HOVER,
            text_color=TEXTO_PRINCIPAL, height=40, corner_radius=8,
            command=self._usar_custom,
        ).pack(side="left", padx=5, expand=True, fill="x")

    def _usar_preset(self):
        """Aplica el preset seleccionado."""
        presets = {
            "5+5+5+5 + 30": ([5, 5, 5, 5], 30),
            "7+7+7+7 + 22": ([7, 7, 7, 7], 22),
            "10+10+10+5 + 15": ([10, 10, 10, 5], 15),
            "8+8+8+8 + 18": ([8, 8, 8, 8], 18),
        }
        seleccion = self.preset_var.get()
        cortos, largo = presets.get(seleccion, ([5, 5, 5, 5], 30))
        self._guardar(cortos, largo)

    def _usar_custom(self):
        """Aplica la configuración personalizada."""
        try:
            cortos = [
                int(self.e1.get()),
                int(self.e2.get()),
                int(self.e3.get()),
                int(self.e4.get()),
            ]
        except ValueError:
            self.label_info.configure(text="Valores deben ser numeros", text_color=PELIGRO)
            return

        largo = 50 - sum(cortos)

        from src.timer.banco_tiempo import validar_configuracion_descansos
        resultado = validar_configuracion_descansos(cortos)

        if not resultado['valido']:
            self.label_info.configure(
                text=" | ".join(resultado['errores']),
                text_color=PELIGRO,
            )
            return

        self._guardar(cortos, largo)

    def _guardar(self, cortos, largo):
        """Guarda la configuración y cierra."""
        try:
            from src.db.conexion import conexion_global
            from src.db.usuarios import buscar_por_id

            coleccion = conexion_global.obtener_coleccion('usuarios')
            coleccion.update_one(
                {'_id': self.usuario['_id']},
                {'$set': {
                    'config_descansos': {
                        'descansos_cortos': cortos,
                        'descanso_largo': largo,
                        'banco_total': 50,
                    }
                }}
            )

            if self.on_completo:
                self.on_completo(cortos, largo)
            self.destroy()
        except Exception as e:
            self.label_info.configure(text=str(e), text_color=PELIGRO)
