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

# Configuración de expiración de sesión
HORAS_MAXIMAS_SESION = 12  # Una jornada laboral típica


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
        # Forzar reset del estado (ciclos residuales se cierran en ciclo_pomodoro)
        self._inicializar()

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
        Calcula tiempo restante desde timestamp real (persistente).
        Verifica expiración de sesión (>12 horas).
        """
        evento = None

        if not self.ciclo_activo:
            return {'evento': None, **self.obtener_estado()}

        if self.estado == ESTADO_PAUSADO:
            return {'evento': None, **self.obtener_estado()}

        # Verificar expiración de sesión (>12 horas)
        if self._inicio_estado and self.usuario_id:
            verificacion = self.verificar_sesion_expirada(self.usuario_id)
            if verificacion['expirada']:
                self.forzar_reset_por_expiracion(
                    self.usuario_id,
                    verificacion['motivo']
                )
                return {
                    'evento': 'sesion_expirada',
                    'motivo': verificacion['motivo'],
                    **self.obtener_estado()
                }

        # Calcular segundos restantes desde timestamp real
        if self._inicio_estado:
            ahora = datetime.now(timezone.utc)
            inicio = self._inicio_estado
            # Manejar datetime naive
            if hasattr(inicio, 'tzinfo') and inicio.tzinfo is None and hasattr(ahora, 'tzinfo') and ahora.tzinfo is not None:
                ahora = ahora.replace(tzinfo=None)
            elapsed = (ahora - inicio).total_seconds()
            self.segundos_restantes = max(0, int(self.segundos_totales - elapsed))

        if self.segundos_restantes <= 0:
            evento = self._manejar_fin_estado()

        self._guardar_estado_bd()

        return {'evento': evento, **self.obtener_estado()}

    def _guardar_estado_bd(self):
        """Guarda el estado actual del timer en MongoDB."""
        if not self.usuario_id:
            return
        try:
            coleccion = conexion_global.obtener_coleccion('timer_estado')
            coleccion.update_one(
                {'usuario_id': self._parsear_oid(self.usuario_id)},
                {'$set': {
                    'estado': self.estado,
                    'segundos_totales': self.segundos_totales,
                    'pomodoro_actual': self.pomodoro_actual,
                    'pomodoros_totales': self.pomodoros_totales,
                    'pausas_usadas': self.pausas_usadas,
                    'ciclo_activo': self.ciclo_activo,
                    'inicio_estado': self._inicio_estado,
                    'configuracion': self._configuracion,
                    'descansos_restantes': self._descansos_restantes,
                    'descanso_largo': self._descanso_largo,
                    'ciclo_id': self._ciclo_id,
                    'ultima_actualizacion': datetime.now(timezone.utc),
                }},
                upsert=True,
            )
        except Exception:  # nosec
            pass

    def restaurar_desde_bd(self, usuario_id: str) -> bool:
        """
        Restaura el estado del timer desde MongoDB.
        Llamar al hacer login. Retorna True si había estado guardado.
        
        Si la sesión está expirada, fuerza un reset y retorna False.
        """
        try:
            # Primero verificar si la sesión no está expirada
            verificacion = self.verificar_sesion_expirada(usuario_id)
            
            if verificacion['expirada']:
                # Sesión expirada, forzar reset
                self.forzar_reset_por_expiracion(
                    usuario_id, 
                    verificacion['motivo']
                )
                return False
            
            coleccion = conexion_global.obtener_coleccion('timer_estado')
            doc = coleccion.find_one({
                'usuario_id': self._parsear_oid(usuario_id)
            })

            if doc is None or not doc.get('ciclo_activo', False):
                return False

            self.usuario_id = usuario_id
            self._ciclo_id = doc.get('ciclo_id')
            self.estado = doc.get('estado', ESTADO_INACTIVO)
            self.segundos_totales = doc.get('segundos_totales', 1500)
            self.pomodoro_actual = doc.get('pomodoro_actual', 1)
            self.pomodoros_totales = doc.get('pomodoros_totales', 4)
            self.pausas_usadas = doc.get('pausas_usadas', 0)
            self.ciclo_activo = doc.get('ciclo_activo', False)
            self._inicio_estado = doc.get('inicio_estado')
            self._configuracion = doc.get('configuracion', {})
            self._descansos_restantes = doc.get('descansos_restantes', [])
            self._descanso_largo = doc.get('descanso_largo', 30)

            # Recalcular segundos restantes desde timestamp
            if self._inicio_estado and self.estado != ESTADO_PAUSADO:
                ahora = datetime.now(timezone.utc)
                inicio = self._inicio_estado
                if hasattr(inicio, 'tzinfo') and inicio.tzinfo is None:
                    ahora = ahora.replace(tzinfo=None)
                elapsed = (ahora - inicio).total_seconds()
                self.segundos_restantes = max(0, int(self.segundos_totales - elapsed))

                if self.segundos_restantes <= 0:
                    # El estado terminó mientras estaba desconectado
                    self._manejar_fin_estado()
            else:
                self.segundos_restantes = self.segundos_totales

            return True
        except Exception:
            return False

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

    def verificar_sesion_expirada(self, usuario_id: str) -> dict:
        """
        Verifica si la sesión guardada en BD está expirada.
        
        Una sesión se considera expirada si:
        - Han pasado más de HORAS_MAXIMAS_SESION desde la última actualización
        - El estado es inconsistente (ej: descanso con días de antigüedad)
        
        Args:
            usuario_id (str): ID del usuario
            
        Returns:
            dict: {
                'expirada': bool,
                'motivo': str,
                'horas_transcurridas': float,
                'estado_anterior': dict
            }
        """
        try:
            coleccion = conexion_global.obtener_coleccion('timer_estado')
            doc = coleccion.find_one({
                'usuario_id': self._parsear_oid(usuario_id)
            })
            
            if doc is None:
                return {
                    'expirada': False,
                    'motivo': 'sin_sesion',
                    'horas_transcurridas': 0,
                    'estado_anterior': None
                }
            
            ultima_actualizacion = doc.get('ultima_actualizacion')
            
            if ultima_actualizacion is None:
                return {
                    'expirada': False,
                    'motivo': 'sin_timestamp',
                    'horas_transcurridas': 0,
                    'estado_anterior': None
                }
            
            ahora = datetime.now(timezone.utc)
            
            # Manejar timezone aware/unaware
            if hasattr(ultima_actualizacion, 'tzinfo') and ultima_actualizacion.tzinfo is None:
                ultima_actualizacion = ultima_actualizacion.replace(tzinfo=timezone.utc)
                ahora = ahora.replace(tzinfo=None)
            
            horas_transcurridas = (ahora - ultima_actualizacion).total_seconds() / 3600
            
            # Verificar si excede el límite
            if horas_transcurridas > HORAS_MAXIMAS_SESION:
                return {
                    'expirada': True,
                    'motivo': f'Sesión expirada: {horas_transcurridas:.1f} horas de inactividad',
                    'horas_transcurridas': horas_transcurridas,
                    'estado_anterior': {
                        'estado': doc.get('estado'),
                        'pomodoro_actual': doc.get('pomodoro_actual'),
                        'pomodoros_totales': doc.get('pomodoros_totales'),
                        'ultima_actualizacion': doc.get('ultima_actualizacion'),
                    }
                }
            
            # Verificar estado inconsistente (descanso con más de 2 horas)
            estado = doc.get('estado')
            segundos_totales = doc.get('segundos_totales', 0)
            
            if estado in (ESTADO_DESCANSO_CORTO, ESTADO_DESCANSO_LARGO):
                # Un descanso no debería durar más de 2 horas
                if horas_transcurridas > 2 and segundos_totales <= 3600:
                    return {
                        'expirada': True,
                        'motivo': f'Descanso con {horas_transcurridas:.1f} horas de antigüedad',
                        'horas_transcurridas': horas_transcurridas,
                        'estado_anterior': {
                            'estado': estado,
                            'pomodoro_actual': doc.get('pomodoro_actual'),
                            'pomodoros_totales': doc.get('pomodoros_totales'),
                            'ultima_actualizacion': doc.get('ultima_actualizacion'),
                        }
                    }
            
            return {
                'expirada': False,
                'motivo': 'sesion_valida',
                'horas_transcurridas': horas_transcurridas,
                'estado_anterior': None
            }
            
        except Exception as e:
            return {
                'expirada': False,
                'motivo': f'Error verificando: {str(e)}',
                'horas_transcurridas': 0,
                'estado_anterior': None
            }

    def forzar_reset_por_expiracion(self, usuario_id: str, motivo: str) -> bool:
        """
        Fuerza un reset de la sesión por expiración.
        
        Genera un reporte para el supervisor/encargado y limpia el estado.
        
        Args:
            usuario_id (str): ID del usuario
            motivo (str): Razón del reset
            
        Returns:
            bool: True si se realizó el reset correctamente
        """
        try:
            # Obtener estado actual antes del reset
            verificacion = self.verificar_sesion_expirada(usuario_id)
            
            if not verificacion['expirada']:
                return False
            
            # Generar reporte de expiración
            try:
                from src.db.reportes import crear_reporte_expiracion
                crear_reporte_expiracion(
                    usuario_id=usuario_id,
                    estado_anterior=verificacion['estado_anterior'],
                    motivo=motivo
                )
            except Exception:  # nosec - no fallar si el reporte no se puede crear
                pass
            
            # Limpiar el estado en BD
            coleccion = conexion_global.obtener_coleccion('timer_estado')
            coleccion.delete_one({'usuario_id': self._parsear_oid(usuario_id)})
            
            # Marcar ciclos incompletos como completados
            coleccion_ciclos = conexion_global.obtener_coleccion('ciclos_pomodoro')
            coleccion_ciclos.update_many(
                {'usuario_id': self._parsear_oid(usuario_id), 'completado': False},
                {'$set': {
                    'completado': True,
                    'estado_actual': ESTADO_INACTIVO,
                    'fin_ciclo': datetime.now(timezone.utc),
                    'reset_por_expiracion': True,
                }}
            )
            
            # Resetear el servicio
            self._inicializar()
            
            return True
            
        except Exception:
            return False

    def fin_jornada_laboral(self, usuario_id: str) -> dict:
        """
        Termina la jornada laboral del usuario.
        
        Resetea todos los contadores y genera un reporte final.
        
        Args:
            usuario_id (str): ID del usuario
            
        Returns:
            dict: Resumen de la jornada
        """
        try:
            # Obtener datos del ciclo actual
            coleccion = conexion_global.obtener_coleccion('timer_estado')
            estado_doc = coleccion.find_one({
                'usuario_id': self._parsear_oid(usuario_id)
            })
            
            coleccion_ciclos = conexion_global.obtener_coleccion('ciclos_pomodoro')
            
            # Contar ciclos completados y pomodoros
            ciclos = list(coleccion_ciclos.find({
                'usuario_id': self._parsear_oid(usuario_id)
            }))
            
            ciclos_iniciados = len(ciclos)
            ciclos_completados = sum(1 for c in ciclos if c.get('completado', False))
            pomodoros_totales = sum(c.get('pomodoros_completados', 0) for c in ciclos)
            
            # Calcular tiempo (aproximado basado en configuración)
            tiempo_trabajado = ciclos_completados * 25 * 60  # Minutos de trabajo
            tiempo_descanso = ciclos_completados * 5 * 60    # Minutos de descanso corto
            
            # Generar reporte
            try:
                from src.db.reportes import crear_reporte_jornada
                crear_reporte_jornada(
                    usuario_id=usuario_id,
                    fecha=datetime.now(timezone.utc),
                    ciclos_iniciados=ciclos_iniciados,
                    ciclos_completados=ciclos_completados,
                    pomodoros_totales=pomodoros_totales,
                    tiempo_trabajado_segundos=tiempo_trabajado,
                    tiempo_descanso_segundos=tiempo_descanso,
                    pausas_utilizadas=estado_doc.get('pausas_usadas', 0) if estado_doc else 0,
                    jornada_reset=True,
                    motivo_reset='Fin de jornada laboral',
                )
            except Exception:  # nosec
                pass
            
            # Marcar ciclos como completados
            coleccion_ciclos.update_many(
                {'usuario_id': self._parsear_oid(usuario_id), 'completado': False},
                {'$set': {
                    'completado': True,
                    'estado_actual': ESTADO_INACTIVO,
                    'fin_ciclo': datetime.now(timezone.utc),
                    'reset_manual': True,
                }}
            )
            
            # Limpiar timer_estado
            coleccion.delete_one({'usuario_id': self._parsear_oid(usuario_id)})
            
            # Resetear pausas de hoy
            try:
                from src.pausas.gestor_pausas import resetear_pausas_jornada
                resetear_pausas_jornada(usuario_id)
            except Exception:  # nosec
                pass
            
            # Resetear el servicio
            self._inicializar()
            
            return {
                'exito': True,
                'resumen': {
                    'ciclos_iniciados': ciclos_iniciados,
                    'ciclos_completados': ciclos_completados,
                    'pomodoros_totales': pomodoros_totales,
                    'tiempo_trabajado': _formatear_tiempo(tiempo_trabajado),
                    'tiempo_descanso': _formatear_tiempo(tiempo_descanso),
                }
            }
            
        except Exception as e:
            return {
                'exito': False,
                'error': str(e)
            }


def _formatear_tiempo(segundos: int) -> str:
    """Formatea segundos a texto legible."""
    if segundos < 60:
        return f"{segundos}s"
    
    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    
    if horas > 0:
        return f"{horas}h {minutos}m"
    else:
        return f"{minutos}m"


# Instancia global
servicio_timer = ServicioTimer()
