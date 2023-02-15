import re

from bs4 import BeautifulSoup

from shopeepy_wrapped.browser_automation.driver_setup import driver
from shopeepy_wrapped.browser_automation.element_locator import element_id_generator
from shopeepy_wrapped.browser_automation.webdriverwait import webdriverwait
from shopeepy_wrapped.config.core import config
from shopeepy_wrapped.href_manipulation import append_site_prefix


class Product:
    def __init__(self, product_element):
        self.product_element = product_element
        self.product_bread_crumb = None
        self.product_name = None
        self.product_price = None

    def bread_crumb_string(self, bread_crumbs):
        bread_crumb_levels = [
            bread_crumb_level.text for bread_crumb_level in bread_crumbs
        ]
        return " > ".join(bread_crumb_levels)

    def get_bread_crumbs(self, href):
        driver.get(href)

        webdriverwait(config.scrapee_config.BREAD_CRUMB)

        product_soup = BeautifulSoup(driver.page_source, features="html.parser")
        bread_crumb_element = product_soup.find(*element_id_generator(**config.scrapee_config.BREAD_CRUMB_ELEMENT))

        bread_crumbs = bread_crumb_element.find_all(*element_id_generator(**config.scrapee_config.BREAD_CRUMB))

        return self.bread_crumb_string(bread_crumbs)

    def get_product_names(self):
        name = self.product_element.find(*element_id_generator(**config.scrapee_config.NAME))

        return name.text

    def get_product_prices(self):
        try:
            price = self.product_element.find(*element_id_generator(**config.scrapee_config.PRICE)).text.replace("₱",
                                                                                                                 "").replace(
                ",",
                "").strip()
            return price
        except AttributeError:
            return None

    def get_product_parameters(self):
        self.product_name = self.get_product_names()
        self.product_price = self.get_product_prices()

        product_link = append_site_prefix(self.product_element["href"])

        self.product_bread_crumb = self.get_bread_crumbs(product_link)

    def get_product_details(self):
        product_details = {}

        self.get_product_parameters()

        for attr, value in self.__dict__.items():
            if attr != "product_element":
                product_details[attr] = value

        return product_details


class Order:
    def __init__(self, order_element):
        self.order_element = order_element
        self.order_parameters = {}

    def select_order_href(self, href_elements):
        for href_element in href_elements:
            purchase_href = append_site_prefix(href_element["href"])
            if config.scrapee_config.USER_PURCHASE_STR in purchase_href:
                return purchase_href

    def get_href(self):
        try:
            purchase_href = self.select_order_href(self.order_element.find_all("a"))
            return purchase_href
        except AttributeError:
            return None

    def update_order_parameters(self, key_list, value_list):
        len_list = len(key_list)

        for i in range(len_list):
            self.order_parameters[key_list[i]] = value_list[i]

        return None

    def get_order_id(self, order_details_elements):
        possible_order_ids = order_details_elements.find_all("span")

        for possible_order_id in possible_order_ids:
            if "ORDER ID" in possible_order_id.text:
                return possible_order_id.text.replace("ORDER ID. ", "").upper().strip()

    def get_order_details(self, order_soup):
        order_details_elements = order_soup.find(*element_id_generator(**config.scrapee_config.ORDER_DETAILS))

        order_status = order_details_elements.find(
            *element_id_generator(**config.scrapee_config.ORDER_DETAILS_ELEMENTS)).text.upper()
        order_id = self.get_order_id(order_details_elements)

        self.update_order_parameters(["order_status", "order_id"], [order_status, order_id])

        return None

    def get_tracking_info(self, purchase_soup):
        tracking_stages = tuple(re.sub(r'\(.*?\)', "", stepper.text).strip() for stepper in
                                purchase_soup.find_all(*element_id_generator(**config.scrapee_config.TRACKING_STAGES)))
        tracking_timestamps = tuple(
            stepper.text for stepper in
            purchase_soup.find_all(*element_id_generator(**config.scrapee_config.TRACKING_TIMESTAMPS)))

        self.update_order_parameters(tracking_stages, tracking_timestamps)

        return None

    def get_price_breakdown(self, purchase_soup):
        price_breakdown = purchase_soup.find_all(*element_id_generator(**config.scrapee_config.PRICE_BREAKDOWN_ELEMENT))

        price_breakdown_category = tuple(
            row.find(*element_id_generator(**config.scrapee_config.PRICE_BREAKDOWN_CATEGORIES)).text for row in
            price_breakdown)
        price_breakdown_category = [re.sub(r'[0-9]+', '', category).replace("  ",
                                                                            " ") if "Coins" in category or "Coin" in category else category
                                    for category in price_breakdown_category]

        price_breakdown_value = tuple(
            row.find(*element_id_generator(**config.scrapee_config.PRICE_BREAKDOWN_VALUES)).text.replace("₱",
                                                                                                         "").replace(
                ",", "") for row in
            price_breakdown)

        self.update_order_parameters(price_breakdown_category, price_breakdown_value)

        return None

    def scrape_products(self, soup):
        product_elements = soup.find_all(*element_id_generator(**config.scrapee_config.PRODUCT))
        product_details = [Product(product_element).get_product_details() for product_element in product_elements]
        self.update_order_parameters(["products"], [product_details])

    def get_order_parameters(self):

        driver.get(self.get_href())

        webdriverwait(config.scrapee_config.ORDER_DETAILS)

        soup = BeautifulSoup(driver.page_source, features="html.parser")

        ################################
        #  Scrape Order-Level Details  #
        ################################

        self.get_order_details(soup)
        self.get_tracking_info(soup)
        self.get_price_breakdown(soup)

        ################################
        # Scrape Product-Level Details #
        ################################

        self.scrape_products(soup)

        return self.order_parameters
