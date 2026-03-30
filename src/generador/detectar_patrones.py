"""
Módulo: detectar_patrones.py
Responsabilidad: Detectar patrones débiles y predecibles en contraseñas.
"""


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
    
    # 1. Detectar secuencias consecutivas (abc, ABC, 123)
    for i in range(len(contraseña) - 2):
        subcadena = contraseña[i:i+3]
        # Verificar si son caracteres ASCII consecutivos
        if (ord(subcadena[1]) == ord(subcadena[0]) + 1 and 
            ord(subcadena[2]) == ord(subcadena[1]) + 1):
            resultados['secuencias_encontradas'].append(subcadena)
            resultados['tiene_secuencias_consecutivas'] = True
    
    # 2. Detectar repeticiones (aaa, 111)
    for i in range(len(contraseña) - 2):
        subcadena = contraseña[i:i+3]
        if subcadena[0] == subcadena[1] == subcadena[2]:
            resultados['repeticiones_encontradas'].append(subcadena)
            resultados['tiene_repeticiones'] = True
    
    # 3. Detectar patrones de teclado adyacente
    mapeo_teclado = {
        'q': 'w', 'w': 'qe', 'e': 'wrt', 'r': 'ert', 't': 'rty', 'y': 'tyu', 'u': 'yui', 'i': 'uio', 'o': 'iop', 'p': 'o',
        'a': 's', 's': 'adf', 'd': 'sdfg', 'f': 'dgh', 'g': 'fhj', 'h': 'gjk', 'j': 'hkl', 'k': 'jl', 'l': 'k',
        'z': 'x', 'x': 'zcv', 'c': 'xvb', 'v': 'cbn', 'b': 'vnm', 'n': 'bm', 'm': 'n',
        '1': '2', '2': '123', '3': '234', '4': '345', '5': '456', '6': '567', '7': '678', '8': '789', '9': '890', '0': '9',
    }
    
    for i in range(len(contraseña) - 2):
        subcadena = contraseña[i:i+3].lower()
        # Verificar si los caracteres son adyacentes en el teclado
        if (subcadena[0] in mapeo_teclado and 
            subcadena[1] in mapeo_teclado[subcadena[0]] and
            subcadena[2] in mapeo_teclado.get(subcadena[1], '')):
            resultados['adyacencias_encontradas'].append(subcadena)
            resultados['tiene_teclado_adyacente'] = True
    
    # 4. Detectar patrones crecientes (abcd, 1234)
    for i in range(len(contraseña) - 3):
        subcadena = contraseña[i:i+4]
        es_creciente = all(
            ord(subcadena[j+1]) == ord(subcadena[j]) + 1
            for j in range(len(subcadena) - 1)
        )
        if es_creciente:
            resultados['patrones_crecientes'].append(subcadena)
            resultados['tiene_patrones_crecientes'] = True
    
    # 5. Detectar patrones invertidos (dcba, 4321)
    for i in range(len(contraseña) - 3):
        subcadena = contraseña[i:i+4]
        es_invertido = all(
            ord(subcadena[j+1]) == ord(subcadena[j]) - 1
            for j in range(len(subcadena) - 1)
        )
        if es_invertido:
            resultados['patrones_invertidos'].append(subcadena)
            resultados['tiene_patrones_invertidos'] = True
    
    # Calcular fortaleza basada en patrones detectados
    # Debilidades: cada patrón debilita la puntuación
    debilidades = 0
    if resultados['tiene_secuencias_consecutivas']:
        debilidades += len(resultados['secuencias_encontradas']) * 0.05
    if resultados['tiene_repeticiones']:
        debilidades += len(resultados['repeticiones_encontradas']) * 0.20  # Aumentado de 0.16
    if resultados['tiene_teclado_adyacente']:
        debilidades += len(resultados['adyacencias_encontradas']) * 0.12
    if resultados['tiene_patrones_crecientes']:
        debilidades += len(resultados['patrones_crecientes']) * 0.15
    if resultados['tiene_patrones_invertidos']:
        debilidades += len(resultados['patrones_invertidos']) * 0.15
    
    # Fortaleza: inversión de debilidades, capped entre 0.0 y 1.0
    resultados['fortaleza_patron'] = max(0.0, 1.0 - debilidades)
    
    return resultados