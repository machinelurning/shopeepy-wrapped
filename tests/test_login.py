import pytest

from shopeepy_wrapped.login import login_with_credentials
from shopeepy_wrapped.config.core import config
from shopeepy_wrapped.browser_automation.driver_setup import driver
def test_login_w_wrong_credentials() -> None:
    driver.get(config.login_config.LOGINPAGE_LINK)

    username = "wrong_username"
    password = "wrong_password"

    expected_exc_info = "Your account and/or password is incorrect, please try again."

    with pytest.raises(Exception) as exc_info:
        login_with_credentials(username=username, password=password)

    assert str(exc_info.value) == expected_exc_info
