"""
tests/generador/test_generar_contraseña/test_aleatoriedad.py
Tests de aleatoriedad y stress para generar_contraseña()
"""

import pytest
from src.generador import generar_contraseña


class TestAleatoriedad:
    """Tests para validar la aleatoriedad de la generación"""
    
    def test_determinismo_no_existe(self, parametros_generador_defecto):
        """Test: Genera contraseñas distintas cada vez (aleatoriedad)"""
        contraseña1 = generar_contraseña(parametros_generador_defecto)
        contraseña2 = generar_contraseña(parametros_generador_defecto)
        # Muy improbable que genere dos iguales (1 entre 62^12)
        assert contraseña1 != contraseña2
    
    def test_distribucion_aleatoria_basica(self):
        """Test: Genera variedad en las contraseñas"""
        parametros = {
            "longitud": 12,
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True,
            "excluir_ambiguos": False
        }
        contraseñas = [generar_contraseña(parametros) for _ in range(10)]
        # Las 10 contraseñas deberían ser diferentes
        assert len(set(contraseñas)) >= 9  # Al menos 9 únicas de 10


class TestStress:
    """Tests de carga/stress para validar robustez"""
    
    def test_genera_50_contraseñas_sin_error(self, parametros_generador_defecto):
        """Test: Puede generar 50 contraseñas sin errores"""
        for _ in range(50):
            contraseña = generar_contraseña(parametros_generador_defecto)
            assert len(contraseña) == 12
    
    def test_genera_100_contraseñas_sin_error(self):
        """Test: Puede generar 100 contraseñas sin errores"""
        parametros = {
            "longitud": 10,
            "usar_mayusculas": True,
            "usar_numeros": True,
            "usar_simbolos": True,
            "excluir_ambiguos": False
        }
        for _ in range(100):
            contraseña = generar_contraseña(parametros)
            assert len(contraseña) == 10
    
    def test_todas_unicas_en_100_generaciones(self, parametros_generador_defecto):
        """Test: 100 generaciones produce contraseñas prácticamente todas únicas"""
        contraseñas = [generar_contraseña(parametros_generador_defecto) for _ in range(100)]
        unicidades = len(set(contraseñas))
        # Debería haber al menos 99 únicas de 100 (muy improbable colisión)
        assert unicidades >= 99
    
    def test_stress_longitudes_extremas(self):
        """Test: Genera sin error en longitudes extremas"""
        for longitud in [8, 16, 32, 64, 100, 128]:
            parametros = {
                "longitud": longitud,
                "usar_mayusculas": True,
                "usar_numeros": True,
                "usar_simbolos": True,
                "excluir_ambiguos": False
            }
            contraseña = generar_contraseña(parametros)
            assert len(contraseña) == longitud
    
    def test_stress_combinaciones_parametros(self):
        """Test: Genera sin error con múltiples combinaciones de parámetros"""
        combinaciones = [
            {"longitud": 8, "usar_mayusculas": True, "usar_numeros": False, 
             "usar_simbolos": False, "excluir_ambiguos": False},
            {"longitud": 12, "usar_mayusculas": True, "usar_numeros": True, 
             "usar_simbolos": False, "excluir_ambiguos": False},
            {"longitud": 16, "usar_mayusculas": False, "usar_numeros": True, 
             "usar_simbolos": True, "excluir_ambiguos": False},
            {"longitud": 20, "usar_mayusculas": True, "usar_numeros": True, 
             "usar_simbolos": True, "excluir_ambiguos": True},
        ]
        for parametros in combinaciones:
            contraseña = generar_contraseña(parametros)
            assert len(contraseña) == parametros["longitud"]
    
    def test_genera_correctamente_es_string(self, parametros_generador_defecto):
        """Test: El resultado es siempre string"""
        for _ in range(20):
            contraseña = generar_contraseña(parametros_generador_defecto)
            assert isinstance(contraseña, str)
