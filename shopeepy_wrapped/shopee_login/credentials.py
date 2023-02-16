from keyring import get_password, set_password


def set_credentials(username: str, password: str) -> None:
    set_password("shopeepay-wrapped", username, password)


def get_credentials(username: str) -> str:
    return get_password("shopeepay-wrapped", username)
