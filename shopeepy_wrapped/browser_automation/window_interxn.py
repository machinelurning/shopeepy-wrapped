import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from shopeepy_wrapped.browser_automation.driver_setup import driver


def perform_keyboard_actions(input):
    action = ActionChains(driver)
    action.send_keys(input)
    action.perform()


def click_button(xpath):
    time.sleep(2)
    button = driver.find_element(By.XPATH, xpath)
    button.click()
