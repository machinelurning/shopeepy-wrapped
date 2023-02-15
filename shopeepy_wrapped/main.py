from bs4 import BeautifulSoup

from login import login
from shopeepy_wrapped.browser_automation.driver_setup import driver
from shopeepy_wrapped.browser_automation.element_locator import element_id_generator
from shopeepy_wrapped.browser_automation.scroll import scroll_to_bottom
from shopeepy_wrapped.browser_automation.webdriverwait import webdriverwait
from shopeepy_wrapped.config.core import config
from shopeepy_wrapped.scrapee import Order


def main():
    login()

    driver.get(config.scrapee_config.PURCHASEPAGE_LINK)

    webdriverwait(config.scrapee_config.PURCHASES)

    scroll_to_bottom()

    soup = BeautifulSoup(driver.page_source, features="html.parser")
    order_elements = soup.find_all(*element_id_generator(**config.scrapee_config.PURCHASES))

    orders = [Order(order_element).get_order_parameters() for order_element in order_elements]
    return orders


main()
