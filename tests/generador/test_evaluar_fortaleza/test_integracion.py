"""
tests/generador/test_evaluar_fortaleza/test_integracion.py
Tests de integración y comportamientos generales
"""

import pytest
from src.generador import evaluar_fortaleza, generar_contraseña


class TestGeneradasYEvaluadas:
    """Tests de contraseñas generadas y evaluadas"""
    
    def test_generada_16_chars_evaluada(self):
        """Test: Contraseña generada de 16 chars obtiene puntuación"""
        parametros = {
            'longitud': 16,
            'usar_mayusculas': True,
            'usar_numeros': True,
            'usar_simbolos': True,
            'excluir_ambiguos': False
        }
        contraseña = generar_contraseña(parametros)
        resultado = evaluar_fortaleza(contraseña)
        
        assert resultado['puntuacion'] > 50
        assert resultado['nivel'] in {"Normal", "Fuerte", "Muy Fuerte"}
    
    def test_generada_32_chars_fuerte(self):
        """Test: Contraseña generada de 32 chars es fuerte"""
        parametros = {
            'longitud': 32,
            'usar_mayusculas': True,
            'usar_numeros': True,
            'usar_simbolos': True,
            'excluir_ambiguos': False
        }
        contraseña = generar_contraseña(parametros)
        resultado = evaluar_fortaleza(contraseña)
        
        assert resultado['puntuacion'] >= 70
        assert resultado['nivel'] in {"Fuerte", "Muy Fuerte"}


class TestComparacionesRelativas:
    """Tests de comparaciones relativas entre contraseñas"""
    
    def test_mas_larga_mejor(self):
        """Test: Contraseña más larga es generalmente mejor"""
        corta = evaluar_fortaleza("Abc12!@#")
        larga = evaluar_fortaleza("Abc12!@#Def45$%^Ghi78*()Jkl")
        
        assert larga['puntuacion'] > corta['puntuacion']
    
    def test_mas_diversa_mejor(self):
        """Test: Más diversidad de tipos = mejor puntuación"""
        solo_min = evaluar_fortaleza("abcdefghijklmnopqrst")
        min_may_num = evaluar_fortaleza("abcdefghijklABCDEFG1234567890")
        
        assert min_may_num['puntuacion'] > solo_min['puntuacion']
    
    def test_patrones_debilitan(self):
        """Test: Patrones debilitan la puntuación"""
        sin_patrones = evaluar_fortaleza("XyZ9Bw!q#pK")
        con_patrones = evaluar_fortaleza("abcdef123456")
        
        assert sin_patrones['puntuacion'] > con_patrones['puntuacion']


class TestConsistencia:
    """Tests de consistencia del algoritmo"""
    
    def test_misma_entrada_mismo_resultado(self):
        """Test: Misma entrada siempre da mismo resultado"""
        contraseña = "MyPa$$w0rd!"
        resultado1 = evaluar_fortaleza(contraseña)
        resultado2 = evaluar_fortaleza(contraseña)
        
        assert resultado1['puntuacion'] == resultado2['puntuacion']
        assert resultado1['nivel'] == resultado2['nivel']
    
    def test_contraseñas_similares_similar_puntuacion(self):
        """Test: Contraseñas similares dan puntuaciones similares"""
        resultado1 = evaluar_fortaleza("Abc12!@#XYZ")
        resultado2 = evaluar_fortaleza("Abc12!@#ZYX")  # Solo último diferente
        
        # Deberían estar cerca en puntuación
        diferencia = abs(resultado1['puntuacion'] - resultado2['puntuacion'])
        assert diferencia < 20
    
    def test_todo_tipo_contraseña_evaluable(self):
        """Test: Cualquier contraseña es evaluable"""
        contraseñas = [
            "a",
            "password",
            "P@ssw0rd",
            "x" * 128,
            "!@#$%^&*()",
            "Ésté€$"
        ]
        
        for contraseña in contraseñas:
            resultado = evaluar_fortaleza(contraseña)
            assert 0 <= resultado['puntuacion'] <= 100
            assert resultado['nivel'] in {"Débil", "Normal", "Fuerte", "Muy Fuerte"}
