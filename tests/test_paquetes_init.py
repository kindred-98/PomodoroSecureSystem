"""
Tests de integridad de los __all__ de los paquetes.

Regresión: al renombrar añadir_miembro a anadir_miembro, el __all__ de
src.db.equipos se quedó con el nombre antiguo y "from src.db.equipos import *"
pasó a lanzar AttributeError. Estos tests comprueban que cada entrada de
__all__ exista de verdad en el módulo, que es el modo de fallo que nos interesa.
"""

import importlib
import pkgutil

import pytest

import src

# Paquetes reales (tienen módulos dentro); los __init__.py vacíos son
# marcadores de sitio y no exportan nada.
PAQUETES = sorted(
    modulo.name
    for modulo in pkgutil.walk_packages(src.__path__, prefix="src.")
    if modulo.ispkg and not modulo.name.startswith("src.ui.componentes")
    and modulo.name not in ("src.anomalias", "src.notificaciones")
)


def _declarados(mod):
    """Entradas de __all__ del módulo, o None si no lo define."""
    return list(getattr(mod, "__all__", []))


def test_se_encuentra_algun_paquete():
    """Guardia: si el recorrido fallara, el resto de tests no probaría nada."""
    assert "src.db.equipos" in PAQUETES


@pytest.mark.parametrize("nombre", PAQUETES)
def test_entradas_de_all_existen(nombre):
    """Si el módulo define __all__, cada símbolo declarado debe existir."""
    mod = importlib.import_module(nombre)

    declarados = _declarados(mod)
    if not declarados:
        pytest.skip(f"{nombre} no define __all__, no hay nada que verificar")

    inexistentes = [s for s in declarados if not hasattr(mod, s)]
    assert not inexistentes, (
        f"{nombre}.__all__ declara {inexistentes} pero el módulo no los define"
    )


@pytest.mark.parametrize("nombre", PAQUETES)
def test_import_star_no_falla(nombre):
    """from <paquete> import * no debe lanzar AttributeError."""
    mod = importlib.import_module(nombre)
    declarados = _declarados(mod)

    for simbolo in declarados:
        assert getattr(mod, simbolo, None) is not None


def test_regresion_anadir_miembro():
    """El renombrado a ASCII no debe dejar el nombre antiguo en __all__."""
    mod = importlib.import_module("src.db.equipos")

    assert "anadir_miembro" in mod.__all__
    assert callable(mod.anadir_miembro)
    assert "añadir_miembro" not in vars(mod)


def test_imports_del_ci():
    """Reproduce el comando de verificación de imports del workflow de tests."""
    for nombre in (
        "src.generador", "src.db", "src.auth",
        "src.timer", "src.otp", "src.bloqueo",
    ):
        mod = importlib.import_module(nombre)
        declarados = _declarados(mod)
        for simbolo in declarados:
            assert hasattr(mod, simbolo), f"{nombre}.{simbolo} no existe"
