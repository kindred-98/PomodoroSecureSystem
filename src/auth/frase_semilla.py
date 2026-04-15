"""
Módulo: frase_semilla.py
Responsabilidad: Generar y verificar frase semilla de recuperación.
similar a Bitcoin - 12 palabras que permiten recuperar la cuenta.
"""

import secrets
import os
from datetime import datetime, timezone
from src.db.conexion import conexion_global
from src.seguridad.encriptacion import hashear_contraseña

PALABRAS = [
    "agua", "aire", "alto", "amar", "angel", "arbol", "arte", "ave", "azul",
    "bajo", "ballena", "banco", "barco", "bello", "bien", "blanco", "boca", "brazo",
    "bueno", "buque", "caja", "calle", "calor", "cama", "campo", "canto",
    "carne", "carta", "casa", "caso", "cedro", "celeste", "centro", "cerca",
    "cielo", "cinco", "clase", "clima", "cobre", "coco", "colon", "color",
    "como", "copa", "corazon", "costa", "crema", "crudo", "cuarto", "cuatro",
    "cubo", "cuchillo", "cuello", "cuerpo", "cumbre", "curva", "danza",
    "debajo", "dentro", "despacio", "dia", "diferente", "dormir", "dulce",
    "duque", "echo", "edad", "elite", "ella", "enero", "epoca", "error",
    "escalera", "escena", "escuela", "espalda", "espejo", "estado", "esto",
    "estrella", "exterior", "facil", "faltar", "familia", "famoso", "favor",
    "febrero", "feliz", "feo", "fibra", "fiebre", "fiesta", "figura",
    "fin", "firma", "fisica", "flor", "fondo", "forma", "foto", "fraile",
    "freno", "fresa", "frio", "fuego", "fuente", "fuerza", "furia", "gala",
    "gallo", "game", "ganar", "gorra", "gota", "gozo", "gracias", "grado",
    "grafico", "grande", "grasa", "grifo", "gris", "grupo", "guapo", "guia",
    "guitarra", "haber", "hacer", "hada", "hallar", "hasta", "hecho", "helado",
    "herman", "hierba", "hijo", "historia", "hombre", "honesto", "hora", "hoy",
    "huevo", "humo", "idea", "iglesia", "igual", "isla", "jardin", "jefe",
    "joven", "joya", "juego", "juez", "junio", "junto", "juicio", "jurar",
    "labio", "lado", "lago", "largo", "lavar", "leche", "lecho", "leer",
    "legal", "lejos", "lengua", "leon", "letra", "ley", "libre", "libro",
    "liga", "limon", "limpio", "linea", "lista", "lobo", "loco", "lograr",
    "lucha", "lugar", "luz", "madre", "maestro", "magia", "maiz", "malo",
    "mama", "manana", "mano", "manta", "mar", "marca", "marzo", "mas",
    "masa", "matiz", "mayor", "medio", "mejor", "memoria", "menor", "menos",
    "mensaje", "mente", "mes", "mesa", "metal", "metro", "miedo", "miembro",
    "milla", "mismo", "mitodo", "modelo", "modo", "mono", "monte", "morir",
    "mostrar", "mover", "mucho", "muerte", "mujer", "mundo", "musica",
    "nacer", "nada", "nadie", "naranja", "nariz", "nave", "negro", "nervio",
    "ni", "nivel", "noche", "nombre", "norma", "norte", "nota", "novela",
    "nuage", "nube", "nulo", "nunca", "obra", "ocho", "odont", "oficial",
    "oido", "ojo", "ola", "olla", "olor", "olvidar", "once", "opera", "orden",
    "oreo", "oro", "oso", "otro", "padre", "pagar", "pais", "paja",
    "palabra", "palma", "pan", "panel", "papel", "par", "paraguas", "pareja",
    "paris", "parte", "pasar", "paso", "paz", "pecho", "pedir", "pelota",
    "pena", "penco", "perder", "perro", "pesca", "pez", "piano", "picar",
    "pico", "pie", "piedra", "piel", "pierna", "pieza", "piloto", "pino",
    "piso", "plan", "plano", "planta", "plata", "plato", "playa", "plaza",
    "pleno", "plomo", "pobre", "poco", "poder", "poeta", "polen", "pollo",
    "poniente", "portal", "posar", "postre", "pozo", "precio", "primavera",
    "primo", "prisa", "probar", "pronombre", "propio", "prorroga", "proteger",
    "proximo", "prueba", "publicar", "pueblo", "puerta", "pues", "puesto",
    "punto", "pura", "puro", "que", "quedar", "querer", "quien", "quinto",
    "radio", "raiz", "rama", "rana", "rapido", "raro", "rasgo", "rata",
    "raton", "rayo", "razon", "real", "recio", "red", "regio", "reino",
    "reloj", "renal", "renovar", "resto", "rey", "rico", "riego", "rio",
    "risue", "ritmo", "robar", "roca", "rodar", "rodilla", "rojo", "romper",
    "ronco", "rosa", "rostro", "rubio", "rueda", "rugir", "ruido", "rumbo",
    "rural", "ruta", "sacar", "sagrado", "sal", "salir", "salsa", "salud",
    "salvar", "samba", "san", "sano", "santo", "sarape", "secreto", "sed",
    "seguir", "seis", "selva", "semana", "senor", "sentir", "senales", "ser",
    "serio", "servir", "sexto", "siglo", "signo", "silbar", "similar", "simple",
    "sin", "sino", "sistema", "sitio", "sobre", "social", "sol", "solo",
    "sombra", "sonar", "sonreir", "soplar", "sorpresa", "subir", "suelo",
    "suerte", "suma", "super", "suponer", "sur", "surgir", "tal", "tallo",
    "tango", "tanque", "tarde", "tarea", "tasa", "taza", "techo", "tema",
    "temer", "tempo", "tender", "tener", "tenis", "teoria", "terco", "terreno",
    "tesis", "tibio", "tierra", "tipo", "tirar", "tiro", "titular", "tocar",
    "todavia", "todo", "tokio", "tomar", "tono", "tonto", "toque", "torre",
    "torta", "total", "toxina", "traer", "traje", "tramo", "tratar", "trauma",
    "traves", "tren", "tres", "trigo", "triste", "trono", "tropa", "trueque",
    "tumba", "tumor", "tunar", "turbio", "tus", "ultimo", "unico", "unir",
    "usar", "util", "uva", "vaca", "vago", "valer", "valiente", "valor",
    "vapor", "vario", "vaso", "vecino", "veinte", "vena", "venir",
    "ventana", "ver", "verano", "verdad", "verde", "verso", "vestir", "vez",
    "viaje", "vida", "viejo", "viento", "vino", "violin", "virtud", "vista",
    "vivir", "volar", "volver", "voto", "voz", "yate", "yema", "yoga",
    "yunque", "zapato", "zona", "zorro",
]


def generar_frase_semilla(palabras: int = 12) -> str:
    """
    Genera una frase semilla de recuperación.
    
    Args:
        palabras: Número de palabras (12 o 24). Por defecto 12.
    
    Returns:
        str: Frase semilla separada por espacios.
    """
    if palabras not in (12, 24):
        raise ValueError("Debe ser 12 o 24 palabras")
    
    seleccionadas = []
    disponibles = PALABRAS.copy()
    
    for _ in range(palabras):
        idx = secrets.randbelow(len(disponibles))
        palabra = disponibles.pop(idx)
        seleccionadas.append(palabra)
    
    return " ".join(seleccionadas)


def generar_frase_usuario(usuario_id: str) -> str | None:
    """
    Genera una frase semilla para un usuario.
    Solo se puede generar cada 90 días.
    
    Args:
        usuario_id: ID del usuario
    
    Returns:
        str: La frase (UNA sola vez) o None si ya existe reciente.
    """
    from bson import ObjectId
    from src.db.conexion import conexion_global
    
    try:
        usuario_oid = ObjectId(usuario_id)
    except Exception:
        usuario_oid = usuario_id
    
    coleccion = conexion_global.obtener_coleccion('frases_semilla')
    ahora = datetime.now(timezone.utc)
    
    # Verificar si ya hay frase reciente (90 días)
    hace_90 = ahora - timedelta(days=90)
    existente = coleccion.find_one({
        'usuario_id': usuario_oid,
        'generada_en': {'$gte': hace_90}
    })
    
    if existente:
        return None
    
    frase = generar_frase_semilla()
    frase_hash = hashear_contraseña(frase)
    
    # Guardar hash (para verificación)
    coleccion.insert_one({
        'usuario_id': usuario_oid,
        'frase_hash': frase_hash,
        'generada_en': ahora,
        'usada': False,
    })
    
    # Guardar frase encriptada en usuario para recuperación
    from src.seguridad.encriptacion import cifrar
    from src.db.conexion import conexion_global
    usuarios = conexion_global.obtener_coleccion('usuarios')
    usuarios.update_one(
        {'_id': usuario_oid},
        {'$set': {'frase_semilla_encriptada': cifrar(frase)}}
    )
    
    return frase


def conexion():
    from src.db.conexion import conexion_global
    return conexion_global

def verificar_frase_semilla(usuario_id: str, frase: str) -> bool:
    """
    Verifica una frase semilla.
    
    Args:
        usuario_id: ID del usuario
        frase: Frase a verificar
    
    Returns:
        bool: True si es correcta.
    """
    from bson import ObjectId
    from src.seguridad.encriptacion import verificar_contraseña
    
    try:
        usuario_oid = ObjectId(usuario_id)
    except Exception:
        usuario_oid = usuario_id
    
    coleccion = conexion_global.obtener_coleccion('frases_semilla')
    
    registro = coleccion.find_one({
        'usuario_id': usuario_oid,
        'usada': False,
    })
    
    if not registro:
        return False
    
    return verificar_contraseña(frase, registro['frase_hash'])


def marcar_frase_usada(usuario_id: str) -> bool:
    """
    Marca la frase种子 como usada (una vez).
    
    Returns:
        bool: True si se marcó.
    """
    from bson import ObjectId
    try:
        usuario_oid = ObjectId(usuario_id)
    except Exception:
        usuario_oid = usuario_id
    
    coleccion = conexion_global.obtener_coleccion('frases_semilla')
    
    resultado = coleccion.update_one(
        {'usuario_id': usuario_oid, 'usada': False},
        {'$set': {'usada': True}}
    )
    
    return resultado.modified_count > 0


def obtener_ultima_frase(usuario_id: str) -> dict | None:
    """
    Obtiene info de la última frase种子.
    
    Returns:
        dict: Información de la frase o None.
    """
    from bson import ObjectId
    try:
        usuario_oid = ObjectId(usuario_id)
    except Exception:
        usuario_oid = usuario_id
    
    coleccion = conexion_global.obtener_coleccion('frases_semilla')
    return coleccion.find_one({'usuario_id': usuario_oid})


from datetime import timedelta