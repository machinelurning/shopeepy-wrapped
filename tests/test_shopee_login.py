import pytest

from shopeepy_wrapped.config.core import InvalidCredentials
from shopeepy_wrapped.shopee_login.credentials import set_credentials, get_credentials
from shopeepy_wrapped.shopee_login.login import login_with_credentials


def test_set_credentials_incorrect_type(dummy_shopee_account_wrong_type) -> None:
    match = "Username/password should be string type."

    # When / Then
    with pytest.raises(InvalidCredentials, match=match):
        set_credentials(**dummy_shopee_account_wrong_type)  # type: ignore


def test_set_credentials_happy(dummy_shopee_account) -> None:
    # When
    set_credentials(**dummy_shopee_account)
    stored_password = get_credentials(username=dummy_shopee_account["username"], app=dummy_shopee_account["app"])

    # Then
    assert stored_password == dummy_shopee_account["password"]


def test_login_w_wrong_credentials_live(dummy_shopee_account):
    match = "Username and/or password are incorrect."
    set_credentials(**dummy_shopee_account)

    # When / Then
    with pytest.raises(InvalidCredentials, match=match):
        login_with_credentials(dummy_shopee_account["username"])