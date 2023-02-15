import numpy as np

from shopeepy_wrapped.browser_automation.element_locator import element_id_generator
from shopeepy_wrapped.config.core import config


class Product:
    def __init__(self, product_element):
        self.product_element = product_element
        # self.product_bread_crumb = None
        self.product_name = None
        self.product_price = None

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

    def get_product_names(self):
        try:
            name = self.product_element.find(
                *element_id_generator(config.scrapee_config.NAME)
            )
            print(name.text)
        except AttributeError:
            return np.nan

    def get_product_prices(self):
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
            return np.nan

    def get_product_parameters(self):
        self.product_name = self.get_product_names()
        self.product_price = self.get_product_prices()

        # product_link = append_site_prefix(self.product_element["href"])
        # self.product_bread_crumb = self.get_bread_crumbs(product_link)

    def get_product_details(self):
        product_details = {}

        self.get_product_parameters()

        for attr, value in self.__dict__.items():
            if attr != "product_element":
                product_details[attr] = value

        return product_details
