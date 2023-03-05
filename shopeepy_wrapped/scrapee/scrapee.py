from typing import List, Any

from bs4 import BeautifulSoup

from shopeepy_wrapped.browser.action import scroll_to_bottom
from shopeepy_wrapped.browser.driver_setup import driver
from shopeepy_wrapped.browser.element_locator import element_id_generator
from shopeepy_wrapped.browser.wait import webdriverwait_by_config
from shopeepy_wrapped.config.core import config
from shopeepy_wrapped.scrapee.order import Order
from shopeepy_wrapped.ui.progress_bar import progress_bar


def scrape_orders(test: bool = False) -> List[Any]:
    driver.get(config.scrapee_config.PURCHASEPAGE_LINK)
    webdriverwait_by_config(config=config.scrapee_config.PURCHASES)

    if not test:
        scroll_to_bottom(waiting_time=3)

    soup = BeautifulSoup(driver.page_source, features="html.parser")

    order_elements = soup.find_all(
        *element_id_generator(config.scrapee_config.PURCHASES)
    )

    orders = []

    with progress_bar as p:
        for order_element in p.track(order_elements):
            orders.append(Order(order_element).order_parameters)

    return orders
