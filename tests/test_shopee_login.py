import pytest

from shopeepy_wrapped.config.core import InvalidCredentials
from shopeepy_wrapped.shopee_login.credentials import set_credentials, get_credentials
from shopeepy_wrapped.shopee_login.login import correct_credentials, login_success_watcher, login_with_credentials, verification_needed
from shopeepy_wrapped.browser.driver_setup import driver
from selenium.common.exceptions import TimeoutException


from keyring import set_password


def test_set_credentials_incorrect_type(dummy_shopee_account_wrong_type) -> None:
    match = "Username/password should be string type."

    # When / Then
    with pytest.raises(InvalidCredentials, match=match):
        set_credentials(**dummy_shopee_account_wrong_type)  # type: ignore


def test_set_credentials_happy(dummy_shopee_account) -> None:
    # Given
    set_password(dummy_shopee_account["app"], dummy_shopee_account["username"], dummy_shopee_account["password"])

    # When
    stored_password = get_credentials(username=dummy_shopee_account["username"], app=dummy_shopee_account["app"])

    # Then
    assert stored_password == dummy_shopee_account["password"]


def test_login_w_wrong_credentials_live(dummy_shopee_account):
    match = "Username and/or password are incorrect."
    set_password(dummy_shopee_account["app"], dummy_shopee_account["username"], dummy_shopee_account["password"])

    # When / Then
    with pytest.raises(InvalidCredentials, match=match):
        login_with_credentials(dummy_shopee_account["username"])


def test_verification_needed_fail():
    # Given
    driver.get("https://www.google.com")

    # When
    button_exists = verification_needed()

    # Then
    assert button_exists == False

def test_login_success_watcher_fail():
    # Given
    driver.get("https://www.google.com")
    match = "Maximum retries exceeded."

    # When / Then
    with pytest.raises(TimeoutException, match=match):
        login_success_watcher(retries=2)

def test_correct_credentials():
    # Given
    driver.get("https://www.google.com")

    # When
    no_incorrect_creds_banner = correct_credentials()

    # Then
    assert no_incorrect_creds_banner == True