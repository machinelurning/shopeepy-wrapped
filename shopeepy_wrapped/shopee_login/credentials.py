from keyring import get_password, set_password

from shopeepy_wrapped.config.core import InvalidCredentials


def set_credentials(
        username: str, password: str, app: str = "shopeepay-wrapped"
) -> None:
    if not isinstance(username, str) or not isinstance(password, str):
        raise InvalidCredentials("Username/password should be string type.")

    set_password(app, username, password)


def get_credentials(username: str, app: str = "shopeepay-wrapped") -> str:
    return get_password(app, username)
