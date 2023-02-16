import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from shopeepy_wrapped.browser.driver_setup import driver


def perform_keyboard_actions(_input: str) -> None:
    action = ActionChains(driver)
    action.send_keys(_input)
    action.perform()


def click_button(xpath: str) -> None:
    time.sleep(2)
    button = driver.find_element(By.XPATH, xpath)
    button.click()
