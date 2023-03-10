from typing import Dict

from bs4.element import Tag

from shopeepy_wrapped.browser.element_locator import element_id_generator
from shopeepy_wrapped.config.core import config


class Product:
    def __init__(self, product_element: Tag) -> None:
        self.product_element = product_element
        self.product_name: str | None = None
        self.product_price: str | None = None
        self.product_thumbnail: str | None = None
        self.product_details: Dict = {}
        self.get_product_details()

    def get_product_names(self) -> str | None:
        try:
            name = self.product_element.find(
                *element_id_generator(config=config.scrapee_config.NAME)
            )
            return name.text
        except AttributeError:
            return None

    def get_product_prices(self) -> str | None:
        try:
            price = (
                self.product_element.find(
                    *element_id_generator(config=config.scrapee_config.PRICE)
                )
                .text.replace("₱", "")
                .replace(",", "")
                .strip()
            )
            return price

        except AttributeError:
            return None

    def get_product_thumbnail(self) -> str | None:
        try:
            thumbnail_href = self.product_element.find(
                *element_id_generator(config=config.scrapee_config.THUMBNAIL)
            )

            thumbnail_href = thumbnail_href["style"]
            thumbnail_href = thumbnail_href[
                thumbnail_href.find("(") + 1 : thumbnail_href.find(")")
            ]
            return thumbnail_href

        except AttributeError:
            return None

    def get_product_parameters(self) -> None:
        self.product_name = self.get_product_names()
        self.product_price = self.get_product_prices()
        self.product_thumbnail = self.get_product_thumbnail()

    def get_product_details(self) -> None:
        self.get_product_parameters()

        for attr, value in self.__dict__.items():
            if attr not in ["product_details", "product_element"]:
                self.product_details[attr] = value
