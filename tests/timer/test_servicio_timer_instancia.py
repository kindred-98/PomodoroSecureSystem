"""Tests adicionales para servicio_timer."""

import pytest
from bson import ObjectId
from unittest.mock import patch


class TestServicioTimerInstancia:
    """Tests para la instancia del servicio."""

    def test_es_singleton(self):
        """Es singleton."""
        from src.timer.servicio_timer import ServicioTimer
        i1 = ServicioTimer()
        i2 = ServicioTimer()
        assert i1 is i2

    def test_estado_inicial(self):
        """Estado inicial es inactivo."""
        from src.timer.servicio_timer import ServicioTimer
        from src.timer.estados import ESTADO_INACTIVO
        svc = ServicioTimer()
        assert svc.estado == ESTADO_INACTIVO

    def test_obtener_estado_retorna_dict(self):
        """Obtener estado retorna dict."""
        from src.timer.servicio_timer import ServicioTimer
        svc = ServicioTimer()
        estado = svc.obtener_estado()
        assert isinstance(estado, dict)

    def test_obtener_estado_tiene_campos(self):
        """Tiene campos esperados."""
        from src.timer.servicio_timer import ServicioTimer
        svc = ServicioTimer()
        estado = svc.obtener_estado()
        assert 'estado' in estado
        assert 'segundos_restantes' in estado
        assert 'pomodoro_actual' in estado
        assert 'pomodoros_totales' in estado
        assert 'pausas_usadas' in estado
        assert 'ciclo_activo' in estado
        assert 'descansos_restantes' in estado
        assert 'descanso_largo' in estado
        assert 'pausas_maximas' in estado


class TestParsearOid:
    """Tests para _parsear_oid."""

    def test_string_a_objectid(self):
        """String a ObjectId."""
        from src.timer.servicio_timer import ServicioTimer
        svc = ServicioTimer()
        resultado = svc._parsear_oid(str(ObjectId()))
        assert isinstance(resultado, ObjectId)

    def test_objectid_pasa(self):
        """ObjectId pasa."""
        from src.timer.servicio_timer import ServicioTimer
        svc = ServicioTimer()
        oid = ObjectId()
        resultado = svc._parsear_oid(oid)
        assert resultado == oid

    def test_string_invalido_pasa(self):
        """String inválido pasa."""
        from src.timer.servicio_timer import ServicioTimer
        svc = ServicioTimer()
        resultado = svc._parsear_oid("invalid")
        assert resultado == "invalid"

    def test_none_pasa(self):
        """None pasa."""
        from src.timer.servicio_timer import ServicioTimer
        svc = ServicioTimer()
        resultado = svc._parsear_oid(None)
        assert resultado is None or isinstance(resultado, ObjectId)


class TestConstantes:
    """Tests para constantes."""

    def test_horas_maximas_sesion(self):
        """Horas máximas sesión."""
        from src.timer.servicio_timer import HORAS_MAXIMAS_SESION
        assert HORAS_MAXIMAS_SESION == 12
        assert isinstance(HORAS_MAXIMAS_SESION, int)

    def test_horas_maximas_positivo(self):
        """Horas máximas positivo."""
        from src.timer.servicio_timer import HORAS_MAXIMAS_SESION
        assert HORAS_MAXIMAS_SESION > 0


class TestEstadoInicial:
    """Tests para estado inicial."""

    def test_segundos_inicial(self):
        """Segundos iniciales."""
        from src.timer.servicio_timer import ServicioTimer
        svc = ServicioTimer()
        assert svc.segundos_restantes == 0

    def test_pomodoro_actual(self):
        """Pomodoro actual."""
        from src.timer.servicio_timer import ServicioTimer
        svc = ServicioTimer()
        assert svc.pomodoro_actual == 0

    def test_pomodoros_totales(self):
        """Pomodoros totales."""
        from src.timer.servicio_timer import ServicioTimer
        svc = ServicioTimer()
        assert svc.pomodoros_totales == 4

    def test_pausas_usadas(self):
        """Pausas usadas."""
        from src.timer.servicio_timer import ServicioTimer
        svc = ServicioTimer()
        assert svc.pausas_usadas == 0

    def test_usuario_id_none(self):
        """Usuario ID none."""
        from src.timer.servicio_timer import ServicioTimer
        svc = ServicioTimer()
        assert svc.usuario_id is None

    def test_ciclo_activo_false(self):
        """Ciclo activo false."""
        from src.timer.servicio_timer import ServicioTimer
        svc = ServicioTimer()
        assert svc.ciclo_activo is False


class TestConfiguracion:
    """Tests para configuración."""

    def test_configuracion_vacia(self):
        """Configuración vacía."""
        from src.timer.servicio_timer import ServicioTimer
        svc = ServicioTimer()
        assert svc._configuracion == {}

    def test_descansos_vacio(self):
        """Descansos vacío."""
        from src.timer.servicio_timer import ServicioTimer
        svc = ServicioTimer()
        assert svc._descansos_restantes == []

    def test_descanso_largo_default(self):
        """Descanso largo default."""
        from src.timer.servicio_timer import ServicioTimer
        svc = ServicioTimer()
        assert svc._descanso_largo == 30
