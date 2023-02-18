from typing import Any, Tuple

import pandas as pd

from shopeepy_wrapped.config.core import config


def clean_column_names(df: pd.DataFrame) -> Tuple[Any, ...]:
    return tuple(col.replace(" ", "_").replace("/", "_").lower() for col in df.columns)


def trim_cols_orders_df(df_orders: pd.DataFrame) -> pd.DataFrame:
    df_orders_clean_cols = clean_column_names(df_orders)
    df_orders.columns = df_orders_clean_cols
    return df_orders[config.data_cleaning_config.ORDERS_KEEP_COLS]


def trim_cols_products_df(df_products: pd.DataFrame) -> pd.DataFrame:
    df_products.columns = clean_column_names(df_products)
    return df_products