from typing import Dict

from bs4.element import Tag

from shopeepy_wrapped.browser.element_locator import element_id_generator
from shopeepy_wrapped.config.core import config


class Product:
    def __init__(self, product_element: Tag) -> None:
        self.product_element = product_element
        # self.product_bread_crumb = None
        self.product_name: str | None = None
        self.product_price: str | None = None
        self.product_thumbnail: str | None = None

    # def bread_crumb_string(self, bread_crumbs):
    #     bread_crumb_levels = [
    #         bread_crumb_level.text for bread_crumb_level in bread_crumbs
    #     ]
    #     return " > ".join(bread_crumb_levels)
    #
    # def get_bread_crumbs(self, href):
    #     driver.get(href)
    #     try:
    #         webdriverwait(config.scrapee_config.BREAD_CRUMB)
    #         product_soup = BeautifulSoup(driver.page_source, features="html.parser")
    #         bread_crumb_element = product_soup.find(
    #             *element_id_generator(config.scrapee_config.BREAD_CRUMB_ELEMENT)
    #         )
    #
    #         bread_crumbs = bread_crumb_element.find_all(
    #             *element_id_generator(config.scrapee_config.BREAD_CRUMB)
    #         )
    #
    #         return self.bread_crumb_string(bread_crumbs)
    #
    #     except TimeoutException:
    #         print("Product does not exist anymore.")
    #         return np.nan
    #
    #     except AttributeError:
    #         return np.nan

    def get_product_names(self) -> str | None:
        try:
            name = self.product_element.find(
                *element_id_generator(config.scrapee_config.NAME)
            )
            return name.text
        except AttributeError:
            return None

    def get_product_prices(self) -> str | None:
        try:
            price = (
                self.product_element.find(
                    *element_id_generator(config.scrapee_config.PRICE)
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
                *element_id_generator(config.scrapee_config.THUMBNAIL)
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
        # product_link = append_site_prefix(self.product_element["href"])
        # self.product_bread_crumb = self.get_bread_crumbs(product_link)

    def get_product_details(self) -> Dict:
        product_details = {}

        self.get_product_parameters()

        for attr, value in self.__dict__.items():
            if attr != "product_element":
                product_details[attr] = value

        return product_details
