import chromedriver_autoinstaller
from selenium import webdriver


def setup_chromedriver() -> webdriver:
    chromedriver_autoinstaller.install()

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")

    _driver = webdriver.Chrome(options=chrome_options)
    _driver.maximize_window()

    return _driver


driver = setup_chromedriver()
