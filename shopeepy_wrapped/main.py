from typing import Tuple

from bs4 import BeautifulSoup

from shopeepy_wrapped.browser.driver_setup import driver
from shopeepy_wrapped.browser.element_locator import element_id_generator
from shopeepy_wrapped.browser.scroll import scroll_to_bottom
from shopeepy_wrapped.browser.wait import webdriverwait_by_config
from shopeepy_wrapped.config.core import config
from shopeepy_wrapped.scrapee.order import Order


def main(test: bool = False) -> Tuple:
    driver.get(config.login_config.LOGINPAGE_LINK)

    input("Press Enter once you've logged in.")

    driver.get(config.scrapee_config.PURCHASEPAGE_LINK)

    webdriverwait_by_config(config.scrapee_config.PURCHASES)

    if not test:
        scroll_to_bottom(waiting_time=3)

    soup = BeautifulSoup(driver.page_source, features="html.parser")

    order_elements = soup.find_all(
        *element_id_generator(config.scrapee_config.PURCHASES)
    )

    orders = tuple(
        Order(order_element).order_parameters for order_element in order_elements
    )

    return orders
