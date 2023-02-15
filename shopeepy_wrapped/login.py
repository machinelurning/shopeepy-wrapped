from shopeepy_wrapped.browser_automation.driver_setup import driver
from shopeepy_wrapped.config.core import config

def login() -> None:
    driver.get(config.login_config.LOGINPAGE_LINK)
    done_login = input("Press \'Enter\' to continue...")
    print("Login successful!")