from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from shopeepy_wrapped.browser.driver_setup import driver
from shopeepy_wrapped.browser.xpath import xpath_generator
from shopeepy_wrapped.config.core import Element


def webdriverwait_by_config(config: Element) -> None:
    xpath = xpath_generator(config=config)
    try:
        WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH, xpath))
        )

    except TimeoutException:
        raise TimeoutException


def webdriverwait_by_xpath(xpath: str) -> None:
    try:
        WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH, xpath))
        )

    except TimeoutException:
        raise TimeoutException
