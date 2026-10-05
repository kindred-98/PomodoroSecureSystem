"""
Módulo: asegurar_tipos_caracteres.py
Responsabilidad: Validar que la contraseña tenga al menos
1 carácter de cada tipo especificado en parámetros.
"""

import secrets
import string

# Caracteres visualmente ambiguos (0/O, l/1/I)
_AMBIGUOS = "0Ol1I"

# Parámetros que indican si se debe garantizar cada tipo de carácter
_FLAGS_TIPO = {
    "mayusculas": "usar_mayusculas",
    "numeros": "usar_numeros",
    "simbolos": "usar_simbolos",
}


def _elegir_mayuscula(excluidos: str) -> str:
    """Elige una mayúscula evitando los caracteres ambiguos."""
    mayusculas = [c for c in string.ascii_uppercase if c not in excluidos]
    return secrets.choice(mayusculas)


def _elegir_numero(excluidos: str) -> str:
    """Elige un número evitando los caracteres ambiguos."""
    numeros = [c for c in string.digits if c not in excluidos]
    return secrets.choice(numeros) if numeros else secrets.choice(string.digits)


def _posicion_disponible(longitud: int, preferida: int) -> int:
    """Devuelve la posición a usar, recortando al final si no cabe la preferida."""
    return min(preferida, longitud - 1)


def _garantizar_mayusculas(contrasena: list, excluidos: str) -> None:
    """Coloca una mayúscula en la posición 0."""
    contrasena[0] = _elegir_mayuscula(excluidos)


def _garantizar_numero(contrasena: list, excluidos: str) -> None:
    """Coloca un número en la posición 1, o al final si la contraseña es más corta."""
    posicion = _posicion_disponible(len(contrasena), 1)
    contrasena[posicion] = _elegir_numero(excluidos)


def _garantizar_simbolo(contrasena: list) -> None:
    """Coloca un símbolo en la posición 2, o al final si la contraseña es más corta."""
    posicion = _posicion_disponible(len(contrasena), 2)
    contrasena[posicion] = secrets.choice(string.punctuation)


def asegurar_tipos_caracteres(contrasena: list, parametros: dict) -> list:
    """
    Garantiza que la contraseña contiene al menos 1 carácter
    de cada tipo seleccionado.
    
    Args:
        contraseña (list): Lista de caracteres generada
        parametros (dict): Configuración de tipos a incluir
        
    Returns:
        list: Contraseña modificada con tipos garantizados
        
    Raises:
        ValueError: Si longitud < número de tipos requeridos
    """
    # Validación propia
    if not contrasena:
        raise ValueError("La contraseña no puede estar vacía")
    
    if not isinstance(contrasena, list):
        raise TypeError("La contraseña debe ser una lista de caracteres")
    
    # Contar cuántos tipos son requeridos
    tipos_requeridos = sum(
        1 for flag in _FLAGS_TIPO.values() if parametros.get(flag, False)
    )

    # Validar que hay espacio suficiente
    if tipos_requeridos > len(contrasena):
        raise ValueError(
            f"Longitud insuficiente ({len(contrasena)}) "
            f"para garantizar {tipos_requeridos} tipos de caracteres"
        )

    excluidos = _AMBIGUOS if parametros.get("excluir_ambiguos", False) else ""

    garantizadores = {
        _FLAGS_TIPO["mayusculas"]: lambda: _garantizar_mayusculas(contrasena, excluidos),
        _FLAGS_TIPO["numeros"]: lambda: _garantizar_numero(contrasena, excluidos),
        _FLAGS_TIPO["simbolos"]: lambda: _garantizar_simbolo(contrasena),
    }

    for flag, garantizar in garantizadores.items():
        if parametros.get(flag, False):
            garantizar()

    return contrasena
