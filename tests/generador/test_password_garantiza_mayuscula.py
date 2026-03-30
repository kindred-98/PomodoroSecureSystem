from src.generador import generar_password

def test_password_garantiza_mayuscula():
    params = {
        "longitud": 8,
        "usar_mayusculas": True,
        "usar_numeros": False,
        "usar_simbolos": False,
        "excluir_ambiguos": False
    }

    # ejecutamos varias veces para detectar aleatoriedad
    for _ in range(50):
        password = generar_password(params)
        assert any(c.isupper() for c in password)