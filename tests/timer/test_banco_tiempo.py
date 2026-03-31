"""Tests para timer/banco_tiempo.py"""

import pytest
from src.timer.banco_tiempo import (
    validar_configuracion_descansos,
    calcular_descanso_largo,
)


class TestValidarConfiguracion:
    """Tests para validar_configuracion_descansos"""
    
    def test_configuracion_estandar(self):
        """[5,5,5,5] debe ser válido, largo=30"""
        resultado = validar_configuracion_descansos([5, 5, 5, 5])
        assert resultado['valido'] is True
        assert resultado['descanso_largo'] == 30
        assert resultado['errores'] == []
    
    def test_configuracion_maxima_cortos(self):
        """[10,10,10,5] suma=35, largo=15, debe ser válido"""
        resultado = validar_configuracion_descansos([10, 10, 10, 5])
        assert resultado['valido'] is True
        assert resultado['descanso_largo'] == 15
    
    def test_configuracion_personalizada(self):
        """[7,7,7,7] suma=28, largo=22, debe ser válido"""
        resultado = validar_configuracion_descansos([7, 7, 7, 7])
        assert resultado['valido'] is True
        assert resultado['descanso_largo'] == 22
    
    def test_corto_por_debajo_minimo(self):
        """Corto < 5 debe ser inválido"""
        resultado = validar_configuracion_descansos([4, 5, 5, 5])
        assert resultado['valido'] is False
        assert any("mínimo" in e for e in resultado['errores'])
    
    def test_corto_por_encima_maximo(self):
        """Corto > 10 debe ser inválido"""
        resultado = validar_configuracion_descansos([11, 5, 5, 5])
        assert resultado['valido'] is False
        assert any("máximo" in e for e in resultado['errores'])
    
    def test_largo_muy_corto(self):
        """Si suma cortos es muy alta, largo < 15"""
        resultado = validar_configuracion_descansos([10, 10, 10, 10])
        assert resultado['valido'] is False
        assert any("largo" in e.lower() for e in resultado['errores'])
    
    def test_largo_muy_largo(self):
        """Si suma cortos es muy baja, largo > 30"""
        resultado = validar_configuracion_descansos([4, 4, 4, 4])
        assert resultado['valido'] is False
    
    def test_cantidad_incorrecta(self):
        """3 descansos en vez de 4 debe fallar"""
        resultado = validar_configuracion_descansos([5, 5, 5])
        assert resultado['valido'] is False
        assert any("4 descansos" in e for e in resultado['errores'])
    
    def test_cantidad_excesiva(self):
        """5 descansos en vez de 4 debe fallar"""
        resultado = validar_configuracion_descansos([5, 5, 5, 5, 5])
        assert resultado['valido'] is False
    
    def test_tipo_no_list(self):
        """Debe fallar si no es list"""
        with pytest.raises(TypeError, match="descansos_cortos debe ser list"):
            validar_configuracion_descansos("5,5,5,5")
    
    def test_banco_total_no_int(self):
        """Debe fallar si banco_total no es int"""
        with pytest.raises(TypeError, match="banco_total debe ser int"):
            validar_configuracion_descansos([5, 5, 5, 5], banco_total="50")
    
    def test_elemento_no_int(self):
        """Debe fallar si elementos no son int"""
        resultado = validar_configuracion_descansos([5, "5", 5, 5])
        assert resultado['valido'] is False
    
    def test_retorna_descansos_originales(self):
        """Debe retornar los descansos originales"""
        cortos = [5, 8, 7, 6]
        resultado = validar_configuracion_descansos(cortos)
        assert resultado['descansos_cortos'] == cortos
    
    def test_retorna_banco_total(self):
        """Debe retornar el banco total usado"""
        resultado = validar_configuracion_descansos([5, 5, 5, 5], banco_total=50)
        assert resultado['banco_total'] == 50


class TestCalcularDescansoLargo:
    """Tests para calcular_descanso_largo"""
    
    def test_calculo_estandar(self):
        """[5,5,5,5] banco=50 → largo=30"""
        assert calcular_descanso_largo([5, 5, 5, 5]) == 30
    
    def test_calculo_maximo(self):
        """[10,10,10,5] banco=50 → largo=15"""
        assert calcular_descanso_largo([10, 10, 10, 5]) == 15
    
    def test_calculo_personalizado(self):
        """[7,7,7,7] banco=50 → largo=22"""
        assert calcular_descanso_largo([7, 7, 7, 7]) == 22
    
    def test_banco_custom(self):
        """[5,5,5,5] banco=40 → largo=20"""
        assert calcular_descanso_largo([5, 5, 5, 5], banco_total=40) == 20
    
    def test_tipo_no_list(self):
        with pytest.raises(TypeError, match="descansos_cortos debe ser list"):
            calcular_descanso_largo("5,5,5,5")
    
    def test_banco_no_int(self):
        with pytest.raises(TypeError, match="banco_total debe ser int"):
            calcular_descanso_largo([5, 5, 5, 5], banco_total="50")
