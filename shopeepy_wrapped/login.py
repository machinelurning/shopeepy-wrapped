from shopeepy_wrapped.browser_automation.driver_setup import driver
# from shopeepy_wrapped.browser_automation.element_locator import element_id_generator
# from shopeepy_wrapped.browser_automation.window_interxn import (
#     click_button,
#     perform_keyboard_actions,
from shopeepy_wrapped.config.core import config

def login() -> None:
    driver.get(config.login_config.LOGINPAGE_LINK)
    done_login = input("Press \'Enter\' to continue...")
    print("Login successful!")

# def input_credentials() -> Tuple[str, str, str]:
#     username = input("Enter username: ")
#     password = getpass.getpass(prompt="Enter your password: ")
#     shopeepay_pin = getpass.getpass(
#         prompt="Enter your Shopeepay PIN (if you don't have it, enter 'N/A'): "
#     )
#
#     return username, password, shopeepay_pin
#
#
# def login_with_credentials(username: str, password: str) -> None:
#     WebDriverWait(driver, 10).until(
#         ec.presence_of_element_located(
#             (
#                 By.XPATH,
#                 element_id_generator(**config.login_config.USERNAME_INPUT, xpath=True),
#             )
#         )
#     )
#
#     username_input = driver.find_element(
#         By.XPATH, element_id_generator(**config.login_config.USERNAME_INPUT, xpath=True)
#     )
#     username_input.send_keys(username)
#
#     password_input = driver.find_element(
#         By.XPATH, element_id_generator(**config.login_config.PASSWORD_INPUT, xpath=True)
#     )
#     password_input.send_keys(password)
#
#     click_button(element_id_generator(**config.login_config.LOGIN_BUTTON, xpath=True))
#
#     time.sleep(5)
#
#     wrong_credentials = driver.find_element(
#         By.XPATH,
#         element_id_generator(**config.login_config.WRONG_CREDENTIALS, xpath=True),
#     )
#
#     if wrong_credentials:
#         raise Exception("Your account and/or password is incorrect, please try again.")
#
#
# def verify(shopeepay_pin: str) -> None:
#     if shopeepay_pin != "N/A":
#         click_button(
#             element_id_generator(**config.login_config.VERIFY_BY_SHOPEEPAY, xpath=True)
#         )
#
#         time.sleep(5)
#
#         perform_keyboard_actions(shopeepay_pin)
#
#         time.sleep(5)
#
#         perform_keyboard_actions(Keys.ENTER)
#
#     else:
#         click_button(
#             element_id_generator(**config.login_config.VERIFY_BY_EMAIL_OTP, xpath=True)
#         )
#         input(
#             "Click the link sent to your e-mail. Wait a few seconds and then press Enter. "
#         )
#
#
# def login() -> None:
#     driver.get(config.login_config.LOGINPAGE_LINK)
#
#     username, password, shopeepay_pin = input_credentials()
#     login_with_credentials(username, password)
#
#     try:
#         verify(shopeepay_pin)
#         time.sleep(5)
#
#     except NoSuchElementException:
#         time.sleep(5)
#
#     print("Login successful!")
