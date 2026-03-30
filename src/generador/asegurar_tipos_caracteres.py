"""
Módulo: asegurar_tipos_caracteres.py
Responsabilidad: Validar que la contraseña tenga al menos
1 carácter de cada tipo especificado en parámetros.
"""

import secrets
import string


def asegurar_tipos_caracteres(contraseña: list, parametros: dict) -> list:
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
    if not contraseña:
        raise ValueError("La contraseña no puede estar vacía")
    
    if not isinstance(contraseña, list):
        raise TypeError("La contraseña debe ser una lista de caracteres")
    
    # Contar cuántos tipos son requeridos
    tipos_requeridos = sum([
        parametros.get("usar_mayusculas", False),
        parametros.get("usar_numeros", False),
        parametros.get("usar_simbolos", False)
    ])
    
    # Validar que hay espacio suficiente
    if tipos_requeridos > len(contraseña):
        raise ValueError(
            f"Longitud insuficiente ({len(contraseña)}) "
            f"para garantizar {tipos_requeridos} tipos de caracteres"
        )
    
    # Determinar caracteres excluidos si aplica
    caracteres_excluidos = "0Ol1I" if parametros.get("excluir_ambiguos", False) else ""
    
    # Función auxiliar para seleccionar carácter de un tipo sin excluidos
    def elegir_mayuscula():
        """Elige una mayúscula sin caracteres ambiguos"""
        mayusculas = [c for c in string.ascii_uppercase 
                     if c not in caracteres_excluidos]
        return secrets.choice(mayusculas)
    
    def elegir_numero():
        """Elige un número sin caracteres ambiguos"""
        numeros = [c for c in string.digits 
                  if c not in caracteres_excluidos]
        return secrets.choice(numeros) if numeros else secrets.choice(string.digits)
    
    # Asegurar mayúsculas en posición 0
    if parametros.get("usar_mayusculas", False) and len(contraseña) > 0:
        if len(contraseña) >= 1:
            contraseña[0] = elegir_mayuscula()
    
    # Asegurar números en posición 1 (si existe espacio)
    if parametros.get("usar_numeros", False):
        if len(contraseña) > 1:
            contraseña[1] = elegir_numero()
        elif len(contraseña) == 1:
            # Si solo hay 1 espacio y se requiere número, sobrescribir
            contraseña[0] = elegir_numero()
    
    # Asegurar símbolos en posición 2 (si existe espacio)
    if parametros.get("usar_simbolos", False):
        if len(contraseña) > 2:
            contraseña[2] = secrets.choice(string.punctuation)
        elif len(contraseña) == 2:
            # Si solo hay 2 espacios y se requiere símbolo, usar posición 1
            contraseña[1] = secrets.choice(string.punctuation)
        elif len(contraseña) == 1:
            # Si solo hay 1 espacio, sobrescribir
            contraseña[0] = secrets.choice(string.punctuation)
    
    return contraseña
