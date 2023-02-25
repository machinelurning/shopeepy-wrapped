import chromedriver_autoinstaller
from selenium import webdriver


def setup_chromedriver() -> webdriver:
    chromedriver_autoinstaller.install()

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--headless")

    _driver = webdriver.Chrome(options=chrome_options)

    return _driver


driver = setup_chromedriver()
