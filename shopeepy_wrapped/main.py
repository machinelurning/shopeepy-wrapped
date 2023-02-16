from typing import Tuple

from bs4 import BeautifulSoup

from shopeepy_wrapped.browser.driver_setup import driver
from shopeepy_wrapped.browser.element_locator import element_id_generator
from shopeepy_wrapped.browser.scroll import scroll_to_bottom
from shopeepy_wrapped.browser.webdriver_wait import webdriverwait
from shopeepy_wrapped.config.core import config
from shopeepy_wrapped.login import login
from shopeepy_wrapped.scrapee.order import Order


def main(test: bool = False) -> Tuple:
    login()

    driver.get(config.scrapee_config.PURCHASEPAGE_LINK)

    webdriverwait(config.scrapee_config.PURCHASES)

    if not test:
        scroll_to_bottom()

    soup = BeautifulSoup(driver.page_source, features="html.parser")
    order_elements = soup.find_all(
        *element_id_generator(config.scrapee_config.PURCHASES)
    )

    orders = tuple(
        Order(order_element).get_order_parameters() for order_element in order_elements
    )

    return orders
