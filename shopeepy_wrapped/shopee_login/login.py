import time

from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from shopeepy_wrapped.browser.action import click_button
from shopeepy_wrapped.browser.driver_setup import driver
from shopeepy_wrapped.browser.wait import (
    webdriverwait_by_config,
    webdriverwait_by_xpath,
)
from shopeepy_wrapped.browser.xpath import xpath_generator
from shopeepy_wrapped.config.core import config
from shopeepy_wrapped.shopee_login.credentials import get_credentials


class IncorrectCredentials(Exception):
    pass


def correct_credentials() -> bool:
    try:
        webdriverwait_by_config(config=config.login_config.WRONG_CREDENTIALS)
        return False
    except TimeoutException:
        return True


def login_success_watcher(retries: int = 50) -> bool:
    for i in range(retries):
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, features="html.parser")
        logged_in = soup.find(config.login_config.LOGIN_CONFIRM)
        print(logged_in)

        if logged_in:
            return True

    raise TimeoutException


def verify_by_email_link() -> bool:
    try:
        webdriverwait_by_xpath(config.login_config.VERIFY_BY_EMAIL_LINK)
    except TimeoutException:
        return True

    click_button(config.login_config.VERIFY_BY_EMAIL_LINK)

    verified_by_email = login_success_watcher()

    return verified_by_email


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
        raise IncorrectCredentials

    return True
