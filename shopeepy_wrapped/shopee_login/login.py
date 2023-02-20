import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from shopeepy_wrapped.browser.action import click_button
from shopeepy_wrapped.browser.driver_setup import driver
from shopeepy_wrapped.browser.wait import (
    webdriverwait_by_config,
    webdriverwait_by_xpath,
)
from shopeepy_wrapped.config.core import InvalidCredentials, config
from shopeepy_wrapped.shopee_login.credentials import get_credentials
from shopeepy_wrapped.string_manipulation.xpath_manipulation import xpath_generator


def correct_credentials() -> bool:
    try:
        webdriverwait_by_config(config=config.login_config.WRONG_CREDENTIALS)
    except TimeoutException:
        return True
    return False


def login_success_watcher(retries: int = 50) -> bool:
    for i in range(retries):
        try:
            webdriverwait_by_config(
                config=config.login_config.LOGIN_CONFIRM, timeout_sec=2
            )
            return True
        except TimeoutException:
            pass

    raise TimeoutException("Maximum retries exceeded.")


def verification_needed() -> bool:
    time.sleep(10)

    try:
        webdriverwait_by_xpath(xpath=config.login_config.VERIFY_BY_EMAIL_LINK)
    except TimeoutException:
        return False

    return True


def verify_by_email_link() -> bool:
    if not verification_needed():
        return login_success_watcher()

    click_button(config.login_config.VERIFY_BY_EMAIL_LINK)
    return login_success_watcher()


def login_with_credentials(username: str) -> bool:
    driver.get(config.login_config.LOGINPAGE_LINK)

    password = get_credentials(username=username)

    webdriverwait_by_config(config=config.login_config.USERNAME_INPUT)

    username_input = driver.find_element(
        By.XPATH, xpath_generator(config=config.login_config.USERNAME_INPUT)
    )
    username_input.send_keys(username)

    password_input = driver.find_element(
        By.XPATH, xpath_generator(config=config.login_config.PASSWORD_INPUT)
    )
    password_input.send_keys(password)

    click_button(xpath_generator(config=config.login_config.LOGIN_BUTTON))

    if not correct_credentials():
        raise InvalidCredentials("Username and/or password are incorrect.")

    return True
