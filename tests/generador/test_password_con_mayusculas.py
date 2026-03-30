from src.generador import generar_password

def test_password_con_mayusculas():
    params = {
        "longitud": 12,
        "usar_mayusculas": True,
        "usar_numeros": False,
        "usar_simbolos": False,
        "excluir_ambiguos": False
    }

    password = generar_password(params)

    assert any(c.isupper() for c in password)