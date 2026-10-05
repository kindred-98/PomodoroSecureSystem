"""
Módulo: mezclar_contraseña.py
Responsabilidad: Aplicar shuffling criptográficamente seguro
a contraseñas ya generadas.
"""

import secrets


def mezclar_contrasena(contrasena: str) -> str:
    """
    Mezcla (shuffle) una contraseña usando criptografía segura.
    
    Realiza un shuffle seguro de los caracteres para aumentar
    la aleatoriedad y dificultar análisis de patrones.
    
    Args:
        contraseña (str): Contraseña a mezclar
    
    Returns:
        str: Contraseña mezclada
        
    Raises:
        TypeError: Si contraseña no es string
        ValueError: Si contraseña está vacía
    """
    if not isinstance(contrasena, str):
        raise TypeError(f"La contraseña debe ser string, "
                       f"recibido: {type(contrasena).__name__}")
    
    if not contrasena:
        raise ValueError("La contraseña no puede estar vacía")
    
    # Convertir a lista para modificar
    caracteres = list(contrasena)
    
    # Fisher-Yates shuffle usando secrets (criptográficamente seguro)
    # Itera desde el final hacia el principio
    for i in range(len(caracteres) - 1, 0, -1):
        # Elegir índice aleatorio entre 0 e i (inclusive)
        indice_aleatorio = secrets.randbelow(i + 1)
        
        # Intercambiar
        caracteres[i], caracteres[indice_aleatorio] = \
            caracteres[indice_aleatorio], caracteres[i]
    
    return "".join(caracteres)


def mezclar_preservando_estructura(contrasena: str, preservar_inicio: bool = False) -> str:
    """
    Mezcla una contraseña preservando opcionalmente caracteres en posiciones iniciales.
    
    Útil para mantener estructura de tipos de caracteres sin comprometer
    la seguridad criptográfica.
    
    Args:
        contraseña (str): Contraseña a mezclar
        preservar_inicio (bool): Si True, preserva primer carácter intacto
    
    Returns:
        str: Contraseña mezclada (parcialmentesi se preserva inicio)
        
    Raises:
        TypeError: Si contraseña no es string
        ValueError: Si contraseña está vacía o es demasiado corta
    """
    if not isinstance(contrasena, str):
        raise TypeError(f"La contraseña debe ser string, "
                       f"recibido: {type(contrasena).__name__}")
    
    if not contrasena:
        raise ValueError("La contraseña no puede estar vacía")
    
    if preservar_inicio and len(contrasena) < 2:
        raise ValueError(
            "Se requiere contraseña de al menos 2 caracteres "
            "para preservar el inicio"
        )
    
    # Si se preserva el inicio, mezclar solo desde posición 1 en adelante
    if preservar_inicio:
        primer_char = contrasena[0]
        resto_mezclado = mezclar_contrasena(contrasena[1:])
        return primer_char + resto_mezclado
    
    return mezclar_contrasena(contrasena)
