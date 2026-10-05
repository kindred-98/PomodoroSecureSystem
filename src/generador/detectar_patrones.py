"""
Módulo: detectar_patrones.py
Responsabilidad: Detectar patrones débiles y predecibles en contraseñas.
"""


_MAPEO_TECLADO = {
    'q': 'w', 'w': 'qe', 'e': 'wrt', 'r': 'ert', 't': 'rty', 'y': 'tyu', 'u': 'yui', 'i': 'uio', 'o': 'iop', 'p': 'o',
    'a': 's', 's': 'adf', 'd': 'sdfg', 'f': 'dgh', 'g': 'fhj', 'h': 'gjk', 'j': 'hkl', 'k': 'jl', 'l': 'k',
    'z': 'x', 'x': 'zcv', 'c': 'xvb', 'v': 'cbn', 'b': 'vnm', 'n': 'bm', 'm': 'n',
    '1': '2', '2': '123', '3': '234', '4': '345', '5': '456', '6': '567', '7': '678', '8': '789', '9': '890', '0': '9',
}

# Penalización aplicada por cada aparición de cada tipo de patrón
_PESO_DEBILIDAD = {
    'secuencias_encontradas': 0.05,
    'repeticiones_encontradas': 0.20,
    'adyacencias_encontradas': 0.12,
    'patrones_crecientes': 0.15,
    'patrones_invertidos': 0.15,
}


def _es_consecutiva(subcadena: str, paso: int) -> bool:
    """Indica si los caracteres avanzan (paso=1) o retroceden (paso=-1) de uno en uno."""
    return all(
        ord(subcadena[i + 1]) == ord(subcadena[i]) + paso
        for i in range(len(subcadena) - 1)
    )


def _ventanas(contraseña: str, largo: int):
    """Genera las subcadenas consecutivas de largo fijo."""
    for i in range(len(contraseña) - largo + 1):
        yield contraseña[i:i + largo]


def _es_teclado_adyacente(subcadena: str) -> bool:
    """Indica si la subcadena (ya en minúsculas) es adyacente en el teclado."""
    primero, segundo, tercero = subcadena[0], subcadena[1], subcadena[2]
    return (
        primero in _MAPEO_TECLADO
        and segundo in _MAPEO_TECLADO[primero]
        and tercero in _MAPEO_TECLADO.get(segundo, '')
    )


def _registrar(resultados: dict, clave_lista: str, clave_bool: str, valor) -> None:
    """Añade un hallazgo y activa su indicador booleano."""
    resultados[clave_lista].append(valor)
    resultados[clave_bool] = True


def _detectar_secuencias(contraseña: str, resultados: dict) -> None:
    """Detecta secuencias ASCII consecutivas de 3 caracteres."""
    for sub in _ventanas(contraseña, 3):
        if _es_consecutiva(sub, 1):
            _registrar(resultados, 'secuencias_encontradas',
                       'tiene_secuencias_consecutivas', sub)


def _detectar_repeticiones(contraseña: str, resultados: dict) -> None:
    """Detecta triples de caracteres idénticos."""
    for sub in _ventanas(contraseña, 3):
        if sub[0] == sub[1] == sub[2]:
            _registrar(resultados, 'repeticiones_encontradas',
                       'tiene_repeticiones', sub)


def _detectar_teclado(contraseña: str, resultados: dict) -> None:
    """Detecta tríos adyacentes en el teclado QWERTY."""
    for sub in _ventanas(contraseña, 3):
        sub = sub.lower()
        if _es_teclado_adyacente(sub):
            _registrar(resultados, 'adyacencias_encontradas',
                       'tiene_teclado_adyacente', sub)


def _detectar_crecientes(contraseña: str, resultados: dict) -> None:
    """Detecta patrones crecientes de 4 caracteres (abcd, 1234)."""
    for sub in _ventanas(contraseña, 4):
        if _es_consecutiva(sub, 1):
            _registrar(resultados, 'patrones_crecientes',
                       'tiene_patrones_crecientes', sub)


def _detectar_invertidos(contraseña: str, resultados: dict) -> None:
    """Detecta patrones invertidos de 4 caracteres (dcba, 4321)."""
    for sub in _ventanas(contraseña, 4):
        if _es_consecutiva(sub, -1):
            _registrar(resultados, 'patrones_invertidos',
                       'tiene_patrones_invertidos', sub)


def _calcular_fortaleza(resultados: dict) -> float:
    """Invierte las debilidades detectadas en una puntuación 0.0-1.0."""
    debilidades = sum(
        len(resultados[clave]) * peso
        for clave, peso in _PESO_DEBILIDAD.items()
    )
    return max(0.0, 1.0 - debilidades)


def detectar_patrones(contraseña: str) -> dict:
    """
    Detecta patrones débiles y predecibles en una contraseña.
    
    Detecta:
    - Secuencias consecutivas (abc, 123, ABC)
    - Caracteres repetidos (aaa, 111)
    - Teclado adyacente (qwerty, asdf, 123)
    - Patrones crecientes (abcd, 1234)
    - Secuencias invertidas (dcba, 4321)
    
    Args:
        contraseña (str): Contraseña a analizar
    
    Returns:
        dict: Análisis de patrones con estructura:
            {
                'tiene_secuencias_consecutivas': bool,
                'secuencias_encontradas': list[str],
                'tiene_repeticiones': bool,
                'repeticiones_encontradas': list[str],
                'tiene_teclado_adyacente': bool,
                'adyacencias_encontradas': list[str],
                'tiene_patrones_crecientes': bool,
                'patrones_crecientes': list[str],
                'tiene_patrones_invertidos': bool,
                'patrones_invertidos': list[str],
                'fortaleza_patron': float  # 0.0 (muy débil) a 1.0 (muy fuerte)
            }
        
    Raises:
        TypeError: Si contraseña no es string
        ValueError: Si contraseña está vacía
    """
    if not isinstance(contraseña, str):
        raise TypeError(f"La contraseña debe ser string, "
                       f"recibido: {type(contraseña).__name__}")
    
    if not contraseña:
        raise ValueError("La contraseña no puede estar vacía")
    
    resultados = {
        'tiene_secuencias_consecutivas': False,
        'secuencias_encontradas': [],
        'tiene_repeticiones': False,
        'repeticiones_encontradas': [],
        'tiene_teclado_adyacente': False,
        'adyacencias_encontradas': [],
        'tiene_patrones_crecientes': False,
        'patrones_crecientes': [],
        'tiene_patrones_invertidos': False,
        'patrones_invertidos': [],
    }
    
    _detectar_secuencias(contraseña, resultados)
    _detectar_repeticiones(contraseña, resultados)
    _detectar_teclado(contraseña, resultados)
    _detectar_crecientes(contraseña, resultados)
    _detectar_invertidos(contraseña, resultados)

    resultados['fortaleza_patron'] = _calcular_fortaleza(resultados)

    return resultados