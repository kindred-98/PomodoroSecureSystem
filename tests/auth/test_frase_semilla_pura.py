"""Tests para frase_semilla - funciones puras."""

import pytest


class TestGenerarFraseSemilla:
    """Tests para generar_frase_semilla - función pura."""

    def test_genera_12_palabras(self):
        """Genera 12 palabras."""
        from src.auth.frase_semilla import generar_frase_semilla
        frase = generar_frase_semilla(12)
        assert len(frase.split()) == 12

    def test_genera_24_palabras(self):
        """Genera 24 palabras."""
        from src.auth.frase_semilla import generar_frase_semilla
        frase = generar_frase_semilla(24)
        assert len(frase.split()) == 24

    def test_rechaza_numero_invalido(self):
        """Rechaza número inválido."""
        from src.auth.frase_semilla import generar_frase_semilla
        with pytest.raises(ValueError):
            generar_frase_semilla(10)

    def test_palabras_no_se_repiten(self):
        """Palabras no se repiten."""
        from src.auth.frase_semilla import generar_frase_semilla
        frase = generar_frase_semilla(12)
        palabras = frase.split()
        assert len(palabras) == len(set(palabras))

    def test_retorna_string(self):
        """Retorna string."""
        from src.auth.frase_semilla import generar_frase_semilla
        resultado = generar_frase_semilla(12)
        assert isinstance(resultado, str)

    def test_palabras_en_lista(self):
        """Las palabras están en la lista."""
        from src.auth.frase_semilla import generar_frase_semilla, PALABRAS
        frase = generar_frase_semilla(12)
        for palabra in frase.split():
            assert palabra in PALABRAS


class TestPALABRAS:
    """Tests para la lista de palabras."""

    def test_no_hay_duplicados(self):
        """No hay duplicados."""
        from src.auth.frase_semilla import PALABRAS
        assert len(PALABRAS) == len(set(PALABRAS))

    def test_todas_son_strings(self):
        """Todas son strings."""
        from src.auth.frase_semilla import PALABRAS
        for p in PALABRAS:
            assert isinstance(p, str)

    def test_no_hay_vacias(self):
        """No hay palabras vacías."""
        from src.auth.frase_semilla import PALABRAS
        for p in PALABRAS:
            assert len(p) > 0

    def test_solo_minusculas(self):
        """Solo minúsculas."""
        from src.auth.frase_semilla import PALABRAS
        for p in PALABRAS:
            assert p == p.lower()
