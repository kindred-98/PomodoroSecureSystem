"""
Tests para src.generador.calcular_puntuacion
Módulo: Cálculo de puntuación integral de contraseñas
"""

import pytest
from unittest.mock import patch, MagicMock

from src.generador.calcular_puntuacion import (
    calcular_puntuacion,
    generar_y_evaluar
)


class TestCalcularPuntuacion:
    """Tests para la función calcular_puntuacion"""

    def test_contraseña_debil_retorna_baja_puntuacion(self):
        """Verifica que contraseñas debiles tengan baja puntuación"""
        resultado = calcular_puntuacion("abc")
        
        assert resultado['puntuacion'] < 70
        assert resultado['es_segura'] is False

    def test_contraseña_fuerte_retorna_alta_puntuacion(self):
        """Verifica que contraseñas fuertes tengan alta puntuación"""
        resultado = calcular_puntuacion("Kx9#mP2$vL5@nQ8!")
        
        assert resultado['puntuacion'] >= 70
        assert resultado['es_segura'] is True

    def test_retorna_todos_los_campos_requeridos(self):
        """Verifica que se retornen todos los campos esperados"""
        resultado = calcular_puntuacion("Test123!")
        
        assert 'puntuacion' in resultado
        assert 'nivel' in resultado
        assert 'es_segura' in resultado
        assert 'tiempo_crack_estimado' in resultado
        assert 'tiempo_crack_segundos' in resultado

    def test_puntuacion_en_rango_0_100(self):
        """Verifica que la puntuación esté entre 0 y 100"""
        resultado = calcular_puntuacion("TestPassword123!")
        
        assert 0 <= resultado['puntuacion'] <= 100

    def test_nivel_es_string_valido(self):
        """Verifica que el nivel sea un string válido"""
        resultado = calcular_puntuacion("Test123!")
        
        assert isinstance(resultado['nivel'], str)
        assert resultado['nivel'] in ['debil', 'normal', 'fuerte', 'muy_fuerte', 'Débil', 'Normal', 'Fuerte', 'Muy fuerte']

    def test_tiempo_crack_mas_largo_para_contraseñas_largas(self):
        """Verifica que contraseñas más largas tengan mayor tiempo de crack"""
        corta = calcular_puntuacion("Abc1!")
        larga = calcular_puntuacion("Abc1!XyZ2@Wv3#Qm5$")
        
        assert larga['tiempo_crack_segundos'] > corta['tiempo_crack_segundos']

    def test_sin_analisis_no_incluye_patrones(self):
        """Verifica que sin incluir_analisis no venga analisis_patrones"""
        resultado = calcular_puntuacion("Test123!", incluir_analisis=False)
        
        assert 'analisis_patrones' not in resultado

    def test_con_analisis_incluye_patrones(self):
        """Verifica que con incluir_analisis=True venga analisis_patrones"""
        resultado = calcular_puntuacion("Test123!", incluir_analisis=True)
        
        assert 'analisis_patrones' in resultado

    def test_contraseña_no_string_lanza_typeerror(self):
        """Verifica que se rechace contraseña no string"""
        with pytest.raises(TypeError):
            calcular_puntuacion(123)

    def test_contraseña_none_lanza_typeerror(self):
        """Verifica que se rechace contraseña None"""
        with pytest.raises(TypeError):
            calcular_puntuacion(None)

    def test_contraseña_vacia_lanza_valueerror(self):
        """Verifica que se rechace contraseña vacía"""
        with pytest.raises(ValueError):
            calcular_puntuacion("")

    def test_contraseña_lista_lanza_typeerror(self):
        """Verifica que se rechace contraseña tipo lista"""
        with pytest.raises(TypeError):
            calcular_puntuacion(["a", "b", "c"])

    def test_tiempo_legible_formato_correcto(self):
        """Verifica que el tiempo tenga formato legible"""
        resultado = calcular_puntuacion("TestPassword123!")
        
        assert isinstance(resultado['tiempo_crack_estimado'], str)
        assert len(resultado['tiempo_crack_estimado']) > 0

    def test_contraseñas_similares_puntuacion_diferente_por_longitud(self):
        """Verifica que longitud diferente afecte puntuación"""
        corta = calcular_puntuacion("Aa1!")
        larga = calcular_puntuacion("Aa1!Bb2Cc3Dd4")
        
        assert corta['puntuacion'] != larga['puntuacion']

    def test_diversdad_aumenta_puntuacion(self):
        """Verifica que más tipos de caracteres aumenten puntuación"""
        solo_minus = calcular_puntuacion("abcdefghijklmnop")
        con_todo = calcular_puntuacion("Abc123!@#Def456")
        
        assert con_todo['puntuacion'] > solo_minus['puntuacion']

    def test_es_segura_true_solo_si_puntuacion_mayor_o_igual_70(self):
        """Verifica el umbral de seguridad"""
        debil = calcular_puntuacion("abc")
        fuerte = calcular_puntuacion("Str0ng!P@ssw0rd#2024")
        
        assert debil['es_segura'] is False
        assert fuerte['es_segura'] is True


class TestGenerarYEvaluar:
    """Tests para la función generar_y_evaluar"""

    def test_genera_contraseña_valida(self):
        """Verifica que genere una contraseña"""
        parametros = {
            "longitud": 16,
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True,
            "excluir_ambiguos": False
        }
        
        resultado = generar_y_evaluar(parametros)
        
        assert 'contraseña' in resultado
        assert len(resultado['contraseña']) == 16

    def test_retorna_puntuacion(self):
        """Verifica que retorne puntuación"""
        parametros = {
            "longitud": 16,
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True,
            "excluir_ambiguos": False
        }
        
        resultado = generar_y_evaluar(parametros)
        
        assert 'puntuacion' in resultado
        assert 0 <= resultado['puntuacion'] <= 100

    def test_retorna_nivel(self):
        """Verifica que retorne nivel"""
        parametros = {
            "longitud": 16,
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True,
            "excluir_ambiguos": False
        }
        
        resultado = generar_y_evaluar(parametros)
        
        assert 'nivel' in resultado
        assert resultado['nivel'] in ['debil', 'normal', 'fuerte', 'muy_fuerte', 'Débil', 'Normal', 'Fuerte', 'Muy fuerte', 'Muy Fuerte']

    def test_retorna_es_segura(self):
        """Verifica que retorne es_segura"""
        parametros = {
            "longitud": 16,
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True,
            "excluir_ambiguos": False
        }
        
        resultado = generar_y_evaluar(parametros)
        
        assert 'es_segura' in resultado
        assert isinstance(resultado['es_segura'], bool)

    def test_con_mezclar_cambia_contraseña(self):
        """Verifica que mezclar_resultado=True mezcle la contraseña"""
        parametros = {
            "longitud": 16,
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True,
            "excluir_ambiguos": False
        }
        
        resultado1 = generar_y_evaluar(parametros, mezclar_resultado=False)
        resultado2 = generar_y_evaluar(parametros, mezclar_resultado=True)
        
        assert resultado1['contraseña'] != resultado2['contraseña']

    def test_parametros_no_dict_lanza_typeerror(self):
        """Verifica que se rechace parámetros no dict"""
        with pytest.raises(TypeError):
            generar_y_evaluar("parametros_string")

    def test_parametros_none_lanza_typeerror(self):
        """Verifica que se rechace parámetros None"""
        with pytest.raises(TypeError):
            generar_y_evaluar(None)

    def test_parametros_lista_lanza_typeerror(self):
        """Verifica que se rechace parámetros como lista"""
        with pytest.raises(TypeError):
            generar_y_evaluar([{"longitud": 16}])

    def test_genera_longitud_personalizada(self):
        """Verifica que genere con la longitud especificada"""
        longitud = 20
        parametros = {
            "longitud": longitud,
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True,
            "excluir_ambiguos": False
        }
        
        resultado = generar_y_evaluar(parametros)
        
        assert len(resultado['contraseña']) == longitud

    def test_genera_contraseña_fuerte_por_defecto(self):
        """Verifica que genere contraseñas seguras por defecto"""
        parametros = {
            "longitud": 16,
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True,
            "excluir_ambiguos": False
        }
        
        resultado = generar_y_evaluar(parametros)
        
        assert resultado['es_segura'] is True

    def test_retorna_detalles_evaluacion(self):
        """Verifica que retorne detalles de evaluación"""
        parametros = {
            "longitud": 16,
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True,
            "excluir_ambiguos": False
        }
        
        resultado = generar_y_evaluar(parametros)
        
        assert 'detalles_evaluacion' in resultado
