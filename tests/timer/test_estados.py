"""Tests para timer/estados.py"""

import pytest
from src.timer.estados import (
    calcular_ciclos_jornada,
    obtener_transiciones_validas,
    ESTADO_INACTIVO,
    ESTADO_TRABAJANDO,
    ESTADO_DESCANSO_CORTO,
    ESTADO_DESCANSO_LARGO,
    ESTADO_PAUSADO,
)


class TestObtenerTransiciones:
    """Tests para obtener_transiciones_validas"""
    
    def test_retorna_dict(self):
        transiciones = obtener_transiciones_validas()
        assert isinstance(transiciones, dict)
    
    def test_tiene_5_estados(self):
        transiciones = obtener_transiciones_validas()
        assert len(transiciones) == 5
    
    def test_inactivo_solo_va_a_trabajando(self):
        transiciones = obtener_transiciones_validas()
        assert transiciones[ESTADO_INACTIVO] == [ESTADO_TRABAJANDO]
    
    def test_trabajando_puede_pausar(self):
        transiciones = obtener_transiciones_validas()
        assert ESTADO_PAUSADO in transiciones[ESTADO_TRABAJANDO]
    
    def test_pausado_vuelve_a_trabajando(self):
        transiciones = obtener_transiciones_validas()
        assert ESTADO_TRABAJANDO in transiciones[ESTADO_PAUSADO]
    
    def test_descanso_corto_va_a_largo(self):
        transiciones = obtener_transiciones_validas()
        assert ESTADO_DESCANSO_LARGO in transiciones[ESTADO_DESCANSO_CORTO]


class TestCalcularCiclosJornada:
    """Tests para calcular_ciclos_jornada"""
    
    def test_jornada_7h_estandar(self):
        """09:00-16:00 = 420 min, ciclo=150, 2 ciclos + 120 sobran"""
        resultado = calcular_ciclos_jornada("09:00", "16:00")
        assert resultado['duracion_jornada_min'] == 420
        assert resultado['ciclos_completos'] == 2
        assert resultado['minutos_sobrantes'] == 120
    
    def test_jornada_8h(self):
        """08:00-16:00 = 480 min, 3 ciclos + 30 sobran"""
        resultado = calcular_ciclos_jornada("08:00", "16:00")
        assert resultado['duracion_jornada_min'] == 480
        assert resultado['ciclos_completos'] == 3
    
    def test_jornada_6h(self):
        """08:00-14:00 = 360 min, 2 ciclos + 60 sobran"""
        resultado = calcular_ciclos_jornada("08:00", "14:00")
        assert resultado['duracion_jornada_min'] == 360
        assert resultado['ciclos_completos'] == 2
        assert resultado['minutos_sobrantes'] == 60
    
    def test_pomodoro_configurable(self):
        """Pomodoro de 30 min cambia el cálculo"""
        resultado = calcular_ciclos_jornada("09:00", "16:00", pomodoro_min=30)
        assert resultado['pomodoro_trabajo_min'] == 30
        # ciclo = 4×30 + 50 = 170, 420/170 = 2 ciclos + 80
        assert resultado['ciclos_completos'] == 2
    
    def test_descansos_custom(self):
        """Descansos [8,8,8,8] cambian banco"""
        resultado = calcular_ciclos_jornada(
            "09:00", "16:00",
            descansos_cortos=[8, 8, 8, 8],
            descanso_largo=18
        )
        # banco = 32+18=50, ciclo = 100+50=150, igual
        assert resultado['duracion_ciclo_min'] == 150
    
    def test_ciclo_reducido(self):
        """Con 60 min sobrantes, ciclo reducido es posible"""
        resultado = calcular_ciclos_jornada("08:00", "14:00")
        # 60 min sobran, minimo ciclo reducido = 2×25+5 = 55
        assert resultado['ciclo_reducido'] is True
        assert resultado['pomodoros_ciclo_reducido'] >= 2
    
    def test_formato_hora_invalido(self):
        """Formato sin ':' debe fallar"""
        with pytest.raises(ValueError, match="Formato de hora inválido"):
            calcular_ciclos_jornada("0900", "1600")
    
    def test_fin_anterior_a_inicio(self):
        """Fin <= inicio debe fallar"""
        with pytest.raises(ValueError, match="posterior"):
            calcular_ciclos_jornada("16:00", "09:00")
    
    def test_inicio_no_string(self):
        with pytest.raises(TypeError, match="horario_inicio debe ser string"):
            calcular_ciclos_jornada(9, "16:00")
    
    def test_fin_no_string(self):
        with pytest.raises(TypeError, match="horario_fin debe ser string"):
            calcular_ciclos_jornada("09:00", 16)
    
    def test_descansos_no_list(self):
        with pytest.raises(TypeError, match="descansos_cortos debe ser list"):
            calcular_ciclos_jornada("09:00", "16:00", descansos_cortos="5,5,5,5")
    
    def test_retorna_campos_correctos(self):
        """Debe retornar todos los campos esperados"""
        resultado = calcular_ciclos_jornada("09:00", "16:00")
        assert 'inicio_jornada' in resultado
        assert 'fin_jornada' in resultado
        assert 'duracion_jornada_min' in resultado
        assert 'pomodoro_trabajo_min' in resultado
        assert 'descansos_cortos' in resultado
        assert 'descanso_largo' in resultado
        assert 'duracion_ciclo_min' in resultado
        assert 'ciclos_completos' in resultado
        assert 'pomodoros_por_ciclo' in resultado
