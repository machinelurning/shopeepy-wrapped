import pytest

from shopeepy_wrapped.config.core import InvalidCredentials
from shopeepy_wrapped.shopee_login.credentials import set_credentials, get_credentials


# TODO Make test-accounts into conftest
def test_set_credentials_incorrect_type() -> None:
    # Given
    username = 123
    password = "test-password"
    app = "test-app"

    match = "Username/password should be string type."

    # When / Then
    with pytest.raises(InvalidCredentials, match=match):
        set_credentials(username=username, password=password, app=app)  # type: ignore


def test_set_credentials_happy() -> None:
    # Given
    username = "test-username"
    password = "test-password"
    app = "test-app"

    # When
    set_credentials(app=app, username=username, password=password)
    stored_password = get_credentials(app=app, username=username)

    # Then
    assert stored_password == password
