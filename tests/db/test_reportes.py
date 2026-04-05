"""
Tests para el módulo de reportes de jornada.
"""

import pytest
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch
from bson import ObjectId

from src.db.reportes import (
    crear_reporte_jornada,
    crear_reporte_expiracion,
    obtener_reportes_para_supervisor,
    obtener_reportes_para_encargado,
    marcar_reporte_leido_supervisor,
    marcar_reporte_leido_encargado,
    _formatear_tiempo
)


class TestFormatearTiempo:
    """Tests para _formatear_tiempo (sin necesidad de BD)."""

    def test_segundos_solo(self):
        """Menos de un minuto."""
        assert _formatear_tiempo(45) == "45s"
        assert _formatear_tiempo(0) == "0s"

    def test_minutos(self):
        """Solo minutos (sin horas)."""
        assert _formatear_tiempo(60) == "1m"
        assert _formatear_tiempo(300) == "5m"
        assert _formatear_tiempo(2700) == "45m"

    def test_horas_y_minutos(self):
        """Horas y minutos."""
        assert _formatear_tiempo(3600) == "1h 0m"
        assert _formatear_tiempo(5400) == "1h 30m"
        assert _formatear_tiempo(7200) == "2h 0m"
        assert _formatear_tiempo(9000) == "2h 30m"

    def test_tiempo_largo(self):
        """Tiempo de una jornada completa."""
        assert _formatear_tiempo(28800) == "8h 0m"
        assert _formatear_tiempo(27900) == "7h 45m"


class TestCrearReporteJornada:
    """Tests para crear_reporte_jornada"""

    def test_crea_reporte_exitoso(self, mock_conexion_global):
        """Verifica que se cree un reporte correctamente"""
        usuario_id = str(ObjectId())
        fecha = datetime.now(timezone.utc)
        
        with patch('src.db.reportes.conexion_global', mock_conexion_global):
            reporte_id = crear_reporte_jornada(
                usuario_id=usuario_id,
                fecha=fecha,
                ciclos_iniciados=4,
                ciclos_completados=3,
                pomodoros_totales=12,
                tiempo_trabajado_segundos=7200,
                tiempo_descanso_segundos=900,
                pausas_utilizadas=2,
            )
        
        assert reporte_id is not None
        assert len(reporte_id) > 0
        
        coleccion = mock_conexion_global.obtener_coleccion('reportes_jornada')
        count = coleccion.count_documents({})
        assert count == 1

    def test_reporte_contiene_campos_esperados(self, mock_conexion_global):
        """Verifica que el reporte contenga todos los campos"""
        usuario_id = str(ObjectId())
        fecha = datetime.now(timezone.utc)
        
        with patch('src.db.reportes.conexion_global', mock_conexion_global):
            crear_reporte_jornada(
                usuario_id=usuario_id,
                fecha=fecha,
                ciclos_iniciados=4,
                ciclos_completados=3,
                pomodoros_totales=12,
                tiempo_trabajado_segundos=7200,
                tiempo_descanso_segundos=900,
                pausas_utilizadas=2,
            )
        
        coleccion = mock_conexion_global.obtener_coleccion('reportes_jornada')
        reporte = coleccion.find_one({})
        
        assert reporte is not None
        assert 'usuario_id' in reporte
        assert 'fecha_reporte' in reporte
        assert 'ciclos_iniciados' in reporte
        assert 'ciclos_completados' in reporte
        assert 'tiempo_trabajado_segundos' in reporte
        assert 'tiempo_trabajado_texto' in reporte
        assert 'tiempo_descanso_segundos' in reporte
        assert 'tiempo_descanso_texto' in reporte
        assert 'pausas_utilizadas' in reporte
        assert 'leido_supervisor' in reporte
        assert 'leido_encargado' in reporte

    def test_usuario_id_invalido_lanza_error(self, mock_conexion_global):
        """Verifica que se rechace usuario_id inválido"""
        with pytest.raises(ValueError):
            with patch('src.db.reportes.conexion_global', mock_conexion_global):
                crear_reporte_jornada(
                    usuario_id="id-invalido",
                    fecha=datetime.now(timezone.utc),
                    ciclos_iniciados=4,
                    ciclos_completados=3,
                    pomodoros_totales=12,
                    tiempo_trabajado_segundos=7200,
                    tiempo_descanso_segundos=900,
                    pausas_utilizadas=2,
                )

    def test_tiempo_formateado_correctamente(self, mock_conexion_global):
        """Verifica que los tiempos se formateen correctamente"""
        usuario_id = str(ObjectId())
        
        with patch('src.db.reportes.conexion_global', mock_conexion_global):
            crear_reporte_jornada(
                usuario_id=usuario_id,
                fecha=datetime.now(timezone.utc),
                ciclos_iniciados=4,
                ciclos_completados=3,
                pomodoros_totales=12,
                tiempo_trabajado_segundos=7200,
                tiempo_descanso_segundos=900,
                pausas_utilizadas=2,
            )
        
        coleccion = mock_conexion_global.obtener_coleccion('reportes_jornada')
        reporte = coleccion.find_one({})
        
        assert reporte['tiempo_trabajado_texto'] == "2h 0m"
        assert reporte['tiempo_descanso_texto'] == "15m"

    def test_jornada_reset_marca_correctamente(self, mock_conexion_global):
        """Verifica que jornada_reset se marque correctamente"""
        usuario_id = str(ObjectId())
        
        with patch('src.db.reportes.conexion_global', mock_conexion_global):
            crear_reporte_jornada(
                usuario_id=usuario_id,
                fecha=datetime.now(timezone.utc),
                ciclos_iniciados=4,
                ciclos_completados=3,
                pomodoros_totales=12,
                tiempo_trabajado_segundos=7200,
                tiempo_descanso_segundos=900,
                pausas_utilizadas=2,
                jornada_reset=True,
                motivo_reset="Fin de jornada laboral",
            )
        
        coleccion = mock_conexion_global.obtener_coleccion('reportes_jornada')
        reporte = coleccion.find_one({})
        
        assert reporte['jornada_reset'] is True
        assert reporte['motivo_reset'] == "Fin de jornada laboral"


class TestCrearReporteExpiracion:
    """Tests para crear_reporte_expiracion"""

    def test_crea_reporte_expiracion(self, mock_conexion_global):
        """Verifica que se cree un reporte de expiración"""
        usuario_id = str(ObjectId())
        estado_anterior = {
            'estado': 'TRABAJANDO',
            'pomodoro_actual': 2,
            'pomodoros_totales': 4,
            'ultima_actualizacion': datetime.now(timezone.utc),
        }
        
        with patch('src.db.reportes.conexion_global', mock_conexion_global):
            reporte_id = crear_reporte_expiracion(
                usuario_id=usuario_id,
                estado_anterior=estado_anterior,
                motivo="Sesión expirada: 15.0 horas de inactividad",
            )
        
        assert reporte_id is not None
        
        coleccion = mock_conexion_global.obtener_coleccion('reportes_jornada')
        reporte = coleccion.find_one({})
        
        assert reporte['tipo_reporte'] == 'expiracion_sesion'
        assert reporte['motivo'] == "Sesión expirada: 15.0 horas de inactividad"
        assert reporte['estado_anterior']['estado'] == 'TRABAJANDO'

    def test_usuario_id_invalido_lanza_error(self, mock_conexion_global):
        """Verifica que se rechace usuario_id inválido"""
        with pytest.raises(ValueError):
            with patch('src.db.reportes.conexion_global', mock_conexion_global):
                crear_reporte_expiracion(
                    usuario_id="id-invalido",
                    estado_anterior={},
                    motivo="test",
                )


class TestObtenerReportesParaSupervisor:
    """Tests para obtener_reportes_para_supervisor"""

    def test_retorna_reportes_no_leidos(self, mock_conexion_global):
        """Verifica que retorne solo reportes no leídos por supervisor"""
        coleccion = mock_conexion_global.obtener_coleccion('reportes_jornada')
        coleccion.insert_many([
            {'leido_supervisor': False, 'tipo_reporte': 'jornada', 'usuario_id': ObjectId()},
            {'leido_supervisor': False, 'tipo_reporte': 'expiracion', 'usuario_id': ObjectId()},
            {'leido_supervisor': True, 'tipo_reporte': 'jornada', 'usuario_id': ObjectId()},
        ])
        
        with patch('src.db.reportes.conexion_global', mock_conexion_global):
            reportes = obtener_reportes_para_supervisor()
        
        assert len(reportes) == 2

    def test_limita_resultados(self, mock_conexion_global):
        """Verifica que respete el límite"""
        coleccion = mock_conexion_global.obtener_coleccion('reportes_jornada')
        for i in range(100):
            coleccion.insert_one({'leido_supervisor': False, 'usuario_id': ObjectId()})
        
        with patch('src.db.reportes.conexion_global', mock_conexion_global):
            reportes = obtener_reportes_para_supervisor(limit=10)
        
        assert len(reportes) == 10


class TestObtenerReportesParaEncargado:
    """Tests para obtener_reportes_para_encargado"""

    def test_retorna_reportes_del_equipo(self, mock_conexion_global):
        """Verifica que retorne reportes del equipo del encargado"""
        coleccion_equipos = mock_conexion_global.obtener_coleccion('equipos')
        coleccion_reportes = mock_conexion_global.obtener_coleccion('reportes_jornada')
        
        encargado_id = ObjectId()
        equipo_id = ObjectId()
        coleccion_equipos.insert_one({
            '_id': equipo_id,
            'encargado_id': encargado_id,
        })
        
        coleccion_reportes.insert_many([
            {'team_id': equipo_id, 'leido_encargado': False, 'usuario_id': ObjectId()},
            {'team_id': ObjectId(), 'leido_encargado': False, 'usuario_id': ObjectId()},
        ])
        
        with patch('src.db.reportes.conexion_global', mock_conexion_global):
            reportes = obtener_reportes_para_encargado(str(encargado_id))
        
        assert len(reportes) == 1

    def test_encargado_id_invalido_retorna_lista_vacia(self, mock_conexion_global):
        """Verifica que retorne lista vacía si encargado no existe"""
        with patch('src.db.reportes.conexion_global', mock_conexion_global):
            reportes = obtener_reportes_para_encargado("id-invalido")
        
        assert reportes == []

    def test_sin_equipos_retorna_lista_vacia(self, mock_conexion_global):
        """Verifica que retorne lista vacía si no hay equipos"""
        with patch('src.db.reportes.conexion_global', mock_conexion_global):
            reportes = obtener_reportes_para_encargado(str(ObjectId()))
        
        assert reportes == []


class TestMarcarReporteLeido:
    """Tests para marcar reportes como leídos"""

    def test_marcar_leido_supervisor(self, mock_conexion_global):
        """Verifica que se marque como leído por supervisor"""
        coleccion = mock_conexion_global.obtener_coleccion('reportes_jornada')
        reporte_id = ObjectId()
        coleccion.insert_one({'_id': reporte_id, 'leido_supervisor': False})
        
        with patch('src.db.reportes.conexion_global', mock_conexion_global):
            resultado = marcar_reporte_leido_supervisor(str(reporte_id))
        
        assert resultado is True
        reporte = coleccion.find_one({'_id': reporte_id})
        assert reporte['leido_supervisor'] is True

    def test_marcar_leido_encargado(self, mock_conexion_global):
        """Verifica que se marque como leído por encargado"""
        coleccion = mock_conexion_global.obtener_coleccion('reportes_jornada')
        reporte_id = ObjectId()
        coleccion.insert_one({'_id': reporte_id, 'leido_encargado': False})
        
        with patch('src.db.reportes.conexion_global', mock_conexion_global):
            resultado = marcar_reporte_leido_encargado(str(reporte_id))
        
        assert resultado is True
        reporte = coleccion.find_one({'_id': reporte_id})
        assert reporte['leido_encargado'] is True

    def test_reporte_id_invalido_retorna_false(self, mock_conexion_global):
        """Verifica que retorne False si el ID es inválido"""
        with patch('src.db.reportes.conexion_global', mock_conexion_global):
            resultado = marcar_reporte_leido_supervisor("id-invalido")
        
        assert resultado is False
