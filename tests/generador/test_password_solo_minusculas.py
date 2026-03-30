from src.generador import generar_password

def test_password_solo_minusculas():
    params = {
        "longitud": 10,
        "usar_mayusculas": False,
        "usar_numeros": False,
        "usar_simbolos": False,
        "excluir_ambiguos": False
    }

    password = generar_password(params)

    assert password.islower()
    