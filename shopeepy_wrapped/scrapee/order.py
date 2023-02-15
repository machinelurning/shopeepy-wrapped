from bs4 import BeautifulSoup

from shopeepy_wrapped.browser_automation.driver_setup import driver
from shopeepy_wrapped.browser_automation.element_locator import element_id_generator
from shopeepy_wrapped.browser_automation.webdriverwait import webdriverwait
from shopeepy_wrapped.config.core import config
from shopeepy_wrapped.href.href_manipulation import append_site_prefix


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
