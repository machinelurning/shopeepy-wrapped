from typing import Dict, List, Tuple

import pandas as pd


def get_products(orders: Tuple[Dict]) -> List[Dict]:
    products = []

    for order in orders:
        products_list = order["products"]
        order_id = order["order_id"]
        for product in products_list:
            product["order_id"] = order_id
            products.append(product)

    return products


def generate_products_df(orders: Tuple[Dict]) -> pd.DataFrame:
    return pd.DataFrame(get_products(orders))
