from src.generador import generar_password

def test_genera_password_con_longitud_correcta():
    params = {
        "longitud": 12,
        "usar_mayusculas": True,
        "usar_numeros": True,
        "usar_simbolos": True,
        "excluir_ambiguos": False
    }

    password = generar_password(params)

    assert len(password) == 12