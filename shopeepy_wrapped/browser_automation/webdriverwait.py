from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from shopeepy_wrapped.browser_automation.driver_setup import driver
from shopeepy_wrapped.browser_automation.element_locator import element_id_generator


def webdriverwait(config):
    WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.XPATH, element_id_generator(**config, xpath=True))))
