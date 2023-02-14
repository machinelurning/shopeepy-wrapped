import chromedriver_autoinstaller
from selenium import webdriver


def setup_chromedriver():
    chromedriver_autoinstaller.install()

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")

    driver_ = webdriver.Chrome(options=chrome_options)
    driver_.maximize_window()

    return driver_


driver = setup_chromedriver()
