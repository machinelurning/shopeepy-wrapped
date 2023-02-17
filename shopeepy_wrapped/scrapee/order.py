import re
from typing import Any, Dict, Tuple

from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag

from shopeepy_wrapped.browser.driver_setup import driver
from shopeepy_wrapped.browser.element_locator import element_id_generator
from shopeepy_wrapped.browser.wait import webdriverwait_by_config
from shopeepy_wrapped.config.core import config
from shopeepy_wrapped.scrapee.product import Product
from shopeepy_wrapped.string_manipulation.href_manipulation import append_site_prefix


class Order:
    def __init__(self, order_element: Tag) -> None:
        self.order_element = order_element
        self.order_parameters: Dict = {}
        self.get_order_parameters()

    def select_order_href(self, href_elements: ResultSet) -> str | None:
        for href_element in href_elements:
            possible_purchase_href = append_site_prefix(
                incomplete_href=href_element["href"]
            )
            if config.scrapee_config.USER_PURCHASE_STR in possible_purchase_href:
                purchase_href = append_site_prefix(incomplete_href=href_element["href"])
                break

        return purchase_href

    def get_href(self) -> str | None:
        try:
            purchase_href = self.select_order_href(
                href_elements=self.order_element.find_all("a")
            )
            return purchase_href
        except AttributeError:
            return None

    def update_order_parameters(
            self, key_list: Tuple[Any, ...], value_list: Tuple[Any, ...]
    ) -> None:
        len_list = len(key_list)

        for i in range(len_list):
            self.order_parameters[key_list[i]] = value_list[i]

        return None

    def get_order_id(self, order_details_elements: Tag) -> str:
        possible_order_ids = order_details_elements.find_all("span")

        for possible_order_id in possible_order_ids:
            if "ORDER ID" in possible_order_id.text:
                order_id = (
                    possible_order_id.text.replace("ORDER ID. ", "").upper().strip()
                )
                break

        return order_id

    def get_order_details(self, order_soup: BeautifulSoup) -> None:
        order_details_elements = order_soup.find(
            *element_id_generator(config=config.scrapee_config.ORDER_DETAILS)
        )

        order_status = order_details_elements.find(
            *element_id_generator(config=config.scrapee_config.ORDER_DETAILS_ELEMENTS)
        ).text.upper()
        order_id = self.get_order_id(order_details_elements)

        self.update_order_parameters(
            key_list=("order_status", "order_id"), value_list=(order_status, order_id)
        )

        return None

    def get_tracking_info(self, order_soup: BeautifulSoup) -> None:
        tracking_stages = tuple(
            re.sub(r"\(.*?\)", "", stepper.text).strip()
            for stepper in order_soup.find_all(
                *element_id_generator(config=config.scrapee_config.TRACKING_STAGES)
            )
        )
        tracking_timestamps = tuple(
            stepper.text
            for stepper in order_soup.find_all(
                *element_id_generator(config=config.scrapee_config.TRACKING_TIMESTAMPS)
            )
        )

        self.update_order_parameters(
            key_list=tracking_stages, value_list=tracking_timestamps
        )

        return None

    def get_price_breakdown(self, order_soup: BeautifulSoup) -> None:
        price_breakdown = order_soup.find_all(
            *element_id_generator(config=config.scrapee_config.PRICE_BREAKDOWN_ELEMENT)
        )

        price_breakdown_category = tuple(
            row.find(
                *element_id_generator(
                    config=config.scrapee_config.PRICE_BREAKDOWN_CATEGORIES
                )
            ).text
            for row in price_breakdown
        )
        price_breakdown_category = tuple(
            re.sub(r"[0-9]+", "", category).replace("  ", " ")
            if "Coins" in category or "Coin" in category
            else category
            for category in price_breakdown_category
        )

        price_breakdown_value = tuple(
            row.find(
                *element_id_generator(
                    config=config.scrapee_config.PRICE_BREAKDOWN_VALUES
                )
            )
            .text.replace("₱", "")
            .replace(",", "")
            for row in price_breakdown
        )

        self.update_order_parameters(
            key_list=price_breakdown_category, value_list=price_breakdown_value
        )

        return None

    def scrape_products(self, order_soup: BeautifulSoup) -> None:
        product_elements = order_soup.find_all(
            *element_id_generator(config=config.scrapee_config.PRODUCT)
        )

        product_details = tuple(
            Product(product_element=product_element).product_details
            for product_element in product_elements
        )

        self.update_order_parameters(
            key_list=("products",), value_list=(product_details,)
        )

    def get_order_parameters(self) -> None:
        driver.get(self.get_href())

        webdriverwait_by_config(config=config.scrapee_config.ORDER_DETAILS)

        soup = BeautifulSoup(driver.page_source, features="html.parser")

        #  Scrape Order-Level Details
        self.get_order_details(order_soup=soup)
        self.get_tracking_info(order_soup=soup)
        self.get_price_breakdown(order_soup=soup)

        # Scrape Product-Level Details
        self.scrape_products(order_soup=soup)
