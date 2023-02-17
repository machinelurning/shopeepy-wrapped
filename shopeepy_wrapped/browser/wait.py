from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from shopeepy_wrapped.browser.driver_setup import driver
from shopeepy_wrapped.config.core import Element
from shopeepy_wrapped.string_manipulation.xpath_manipulation import xpath_generator


def webdriverwait_by_config(config: Element, timeout_sec: int = 10) -> None:
    xpath = xpath_generator(config=config)
    try:
        WebDriverWait(driver, timeout_sec).until(
            ec.presence_of_element_located((By.XPATH, xpath))
        )

    except TimeoutException:
        raise TimeoutException


def webdriverwait_by_xpath(xpath: str, timeout_sec: int = 10) -> None:
    try:
        WebDriverWait(driver, timeout_sec).until(
            ec.presence_of_element_located((By.XPATH, xpath))
        )

    except TimeoutException:
        raise TimeoutException
