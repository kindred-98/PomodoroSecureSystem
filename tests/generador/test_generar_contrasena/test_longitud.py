"""
tests/generador/test_generar_contrasena/test_longitud.py
Tests de validación de longitud para generar_contrasena()
"""

import pytest

from src.generador import generar_contrasena


def _parametros(longitud: int) -> dict:
    """Construye parámetros de generación con la longitud indicada."""
    return {
        "longitud": longitud,
        "usar_mayusculas": True,
        "usar_numeros": True,
        "usar_simbolos": True,
        "excluir_ambiguos": False,
    }


class TestLongitud:
    """Tests para validar la longitud de las contraseñas generadas"""

    def test_genera_con_longitud_correcta(self, parametros_generador_defecto):
        """Test: La contraseña generada tiene la longitud especificada"""
        contrasena = generar_contrasena(parametros_generador_defecto)
        assert len(contrasena) == parametros_generador_defecto["longitud"]

    @pytest.mark.parametrize("longitud", [8, 12, 20, 32, 64, 128])
    def test_genera_con_longitud_valida(self, longitud):
        """Test: Genera contraseña con una longitud dentro de los límites"""
        contrasena = generar_contrasena(_parametros(longitud))
        assert len(contrasena) == longitud

    @pytest.mark.parametrize("longitud", [7, 0, -5, 129, 1000])
    def test_rechaza_longitud_invalida(self, longitud):
        """Test: Rechaza longitudes fuera del rango permitido"""
        with pytest.raises(ValueError):
            generar_contrasena(_parametros(longitud))
