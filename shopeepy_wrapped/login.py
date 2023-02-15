from shopeepy_wrapped.browser_automation.driver_setup import driver
from shopeepy_wrapped.config.core import config


def login() -> None:
    driver.get(config.login_config.LOGINPAGE_LINK)
    input("Press 'Enter' to continue...")
    # TODO: Add checker if user has really logged in already
    print("Login successful!")
