"""
Módulo: servicio_timer.py
Responsabilidad: Estado centralizado del timer Pomodoro.
Sobrevive a la navegación entre vistas.
"""

import threading
import time as time_module
from datetime import datetime, timezone
from src.timer.estados import (
    ESTADO_INACTIVO,
    ESTADO_TRABAJANDO,
    ESTADO_DESCANSO_CORTO,
    ESTADO_DESCANSO_LARGO,
    ESTADO_PAUSADO,
)
from src.db.conexion import conexion_global
from src.pausas.gestor_pausas import MAXIMO_PAUSAS


class ServicioTimer:
    """Servicio singleton que mantiene el estado del timer Pomodoro."""

    _instancia = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instancia is None:
                cls._instancia = super().__new__(cls)
                cls._instancia._inicializar()
            return cls._instancia

    def _inicializar(self):
        """Inicializa el estado del timer."""
        self.estado = ESTADO_INACTIVO
        self.segundos_restantes = 0
        self.segundos_totales = 0
        self.pomodoro_actual = 0
        self.pomodoros_totales = 4
        self.pausas_usadas = 0
        self.usuario_id = None
        self.ciclo_activo = False
        self._configuracion = {}
        self._ciclo_id = None
        self._descansos_restantes = []
        self._descanso_largo = 30
        self._inicio_estado = None
        self._pausa_inicio = None

    @staticmethod
    def _parsear_oid(usuario_id):
        """Convierte string a ObjectId de forma segura."""
        from bson import ObjectId
        try:
            return ObjectId(usuario_id)
        except Exception:
            return usuario_id

    def obtener_estado(self) -> dict:
        """Retorna el estado actual del timer."""
        return {
            'estado': self.estado,
            'segundos_restantes': max(0, self.segundos_restantes),
            'segundos_totales': self.segundos_totales,
            'pomodoro_actual': self.pomodoro_actual,
            'pomodoros_totales': self.pomodoros_totales,
            'pausas_usadas': self.pausas_usadas,
            'pausas_maximas': MAXIMO_PAUSAS,
            'ciclo_activo': self.ciclo_activo,
            'descansos_restantes': list(self._descansos_restantes),
            'descanso_largo': self._descanso_largo,
        }

    def iniciar(self, usuario_id: str, configuracion: dict = None):
        """Inicia un nuevo ciclo Pomodoro."""
        # Verificar si el ciclo en memoria es real o residual de sesión anterior
        if self.ciclo_activo:
            coleccion = conexion_global.obtener_coleccion('ciclos_pomodoro')
            ciclo_real = coleccion.find_one({
                'usuario_id': self._parsear_oid(usuario_id),
                'completado': False,
            })
            if ciclo_real is None:
                # Ciclo fantasma en memoria, resetear
                self._inicializar()
            else:
                raise Exception("Ya hay un ciclo Pomodoro activo")

        if configuracion is None:
            configuracion = {}

        pomodoro_min = configuracion.get('pomodoro_min', 25)
        descansos = configuracion.get('descansos_cortos', [5, 5, 5, 5])
        descanso_largo = configuracion.get('descanso_largo', 30)

        from src.timer.ciclo_pomodoro import iniciar_ciclo
        resultado = iniciar_ciclo(usuario_id, configuracion)

        self.usuario_id = usuario_id
        self._ciclo_id = resultado.get('ciclo_id')
        self._configuracion = {
            'pomodoro_min': pomodoro_min,
            'descansos_cortos': list(descansos),
            'descanso_largo': descanso_largo,
        }
        self._descansos_restantes = list(descansos)
        self._descanso_largo = descanso_largo
        self.pomodoros_totales = len(descansos)
        self.pomodoro_actual = 1
        self.pausas_usadas = 0
        self.ciclo_activo = True
        self.estado = ESTADO_TRABAJANDO
        self.segundos_restantes = pomodoro_min * 60
        self.segundos_totales = pomodoro_min * 60
        self._inicio_estado = datetime.now(timezone.utc)

    def tick(self) -> dict:
        """
        Avanza el timer 1 segundo.
        Retorna el evento ocurrido (si lo hay) y el estado actual.
        """
        evento = None

        if not self.ciclo_activo:
            return {'evento': None, **self.obtener_estado()}

        if self.estado == ESTADO_PAUSADO:
            return {'evento': None, **self.obtener_estado()}

        if self.segundos_restantes > 0:
            self.segundos_restantes -= 1
        else:
            evento = self._manejar_fin_estado()

        return {'evento': evento, **self.obtener_estado()}

    def _manejar_fin_estado(self) -> str:
        """Maneja la transición cuando un estado llega a 0."""
        from src.timer.ciclo_pomodoro import manejar_evento_timer

        if self.estado == ESTADO_TRABAJANDO:
            try:
                resultado = manejar_evento_timer(self.usuario_id, "pomodoro_completado")
                accion = resultado.get('accion', '')
                duracion = resultado.get('datos_extra', {}).get('duracion_min', 5)

                if 'largo' in accion:
                    self.estado = ESTADO_DESCANSO_LARGO
                else:
                    self.estado = ESTADO_DESCANSO_CORTO

                self.segundos_restantes = duracion * 60
                self.segundos_totales = duracion * 60
                self._inicio_estado = datetime.now(timezone.utc)
                return self.estado

            except Exception as e:
                self.ciclo_activo = False
                self.estado = ESTADO_INACTIVO
                return 'error'

        elif self.estado in (ESTADO_DESCANSO_CORTO, ESTADO_DESCANSO_LARGO):
            try:
                resultado = manejar_evento_timer(self.usuario_id, "descanso_completado")
                accion = resultado.get('accion', '')

                if accion == 'nuevo_ciclo':
                    self.pomodoro_actual = 1
                    self._descansos_restantes = list(self._configuracion.get('descansos_cortos', [5, 5, 5, 5]))
                elif accion == 'fin_jornada':
                    self.ciclo_activo = False
                    self.estado = ESTADO_INACTIVO
                    return 'ciclo_completado'
                else:
                    self.pomodoro_actual = resultado.get('pomodoro_actual', self.pomodoro_actual + 1)

                pomodoro_min = self._configuracion.get('pomodoro_min', 25)
                self.estado = ESTADO_TRABAJANDO
                self.segundos_restantes = pomodoro_min * 60
                self.segundos_totales = pomodoro_min * 60
                self._inicio_estado = datetime.now(timezone.utc)
                return ESTADO_TRABAJANDO

            except Exception as e:
                self.ciclo_activo = False
                self.estado = ESTADO_INACTIVO
                return 'error'

        return None

    def pausar(self):
        """Pausa el timer."""
        if self.estado == ESTADO_PAUSADO:
            raise Exception("El timer ya está pausado")
        if not self.ciclo_activo:
            raise Exception("No hay ciclo activo para pausar")

        from src.pausas import iniciar_pausa
        iniciar_pausa(self.usuario_id)

        self.estado_anterior = self.estado
        self.estado = ESTADO_PAUSADO
        self._pausa_inicio = datetime.now(timezone.utc)
        self.pausas_usadas += 1

    def reanudar(self):
        """Reanuda el timer después de una pausa."""
        if self.estado != ESTADO_PAUSADO:
            raise Exception("El timer no está pausado")

        from src.pausas import finalizar_pausa
        finalizar_pausa(self.usuario_id)

        self.estado = getattr(self, 'estado_anterior', ESTADO_TRABAJANDO)
        self._pausa_inicio = None

    def destruir(self):
        """Resetea el servicio (logout)."""
        self._inicializar()


# Instancia global
servicio_timer = ServicioTimer()
