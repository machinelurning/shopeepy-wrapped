from typing import Any, Dict, Tuple

import pandas as pd


def filter_products(order: Dict) -> Dict:
    return {key: order[key] for key in order.keys() if key != "products"}


def remove_products(orders: Tuple[Dict]) -> Tuple[Any, ...]:
    return tuple(filter_products(order) for order in orders)


def generate_orders_df(orders: Tuple[Dict]) -> pd.DataFrame:
    orders_no_products = remove_products(orders=orders)
    return pd.DataFrame(orders_no_products)
