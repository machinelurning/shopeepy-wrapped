from re import sub
from typing import List

import pandas as pd

from shopeepy_wrapped.config.core import DataTypes, config
from shopeepy_wrapped.data.trimming import trim_cols_orders_df, trim_cols_products_df


def keep_numericals(string_: str) -> float:
    return float(sub("[^0-9|.]", "", str(string_)))


def convert_datetime(dataframe: pd.DataFrame, convert_cols: List[str]) -> pd.DataFrame:
    dataframe = dataframe.copy()

    cols = [col for col in dataframe.columns if col in convert_cols]

    for col in cols:
        dataframe[col] = pd.to_datetime(dataframe[col], format="%m/%d/%Y %H:%M")
    return dataframe


def convert_categorical(dataframe: pd.DataFrame, convert_cols: List[str]) -> pd.DataFrame:
    dataframe = dataframe.copy()

    cols = [col for col in dataframe.columns if col in convert_cols]

    for col in cols:
        dataframe[col] = pd.Categorical(dataframe[col])

    return dataframe


def convert_float(dataframe: pd.DataFrame, convert_cols: List[str]) -> pd.DataFrame:
    dataframe = dataframe.copy()

    cols = [col for col in dataframe.columns if col in convert_cols]

    for col in cols:
        dataframe[col].fillna("0", inplace=True)
        dataframe[col] = dataframe[col].apply(keep_numericals)
        dataframe[col] = dataframe[col].astype(float)

    return dataframe


def convert_object(dataframe: pd.DataFrame, convert_cols: List[str]) -> pd.DataFrame:
    dataframe = dataframe.copy()

    cols = [col for col in dataframe.columns if col in convert_cols]

    for col in cols:
        dataframe[col] = dataframe[col].astype(str)

    return dataframe


def convert_data_types(
        dataframe: pd.DataFrame, data_type_dict: DataTypes
) -> pd.DataFrame:
    for data_type in data_type_dict.keys():
        if data_type == "datetime":
            dataframe = convert_datetime(
                dataframe=dataframe, convert_cols=data_type_dict[data_type]  # type: ignore
            )
        elif data_type == "categorical":
            dataframe = convert_categorical(
                dataframe=dataframe, convert_cols=data_type_dict[data_type]  # type: ignore
            )
        elif data_type == "float":
            dataframe = convert_float(
                dataframe=dataframe, convert_cols=data_type_dict[data_type]  # type: ignore
            )
        elif data_type == "string":
            dataframe = convert_object(
                dataframe=dataframe, convert_cols=data_type_dict[data_type]  # type: ignore
            )
    return dataframe


def clean_dataset(dataframe: pd.DataFrame, order_type: bool = True) -> pd.DataFrame:
    if order_type:
        data_type_dict = config.data_config.ORDERS_DATA_TYPES
        dataframe = trim_cols_orders_df(df_orders=dataframe)
    else:
        data_type_dict = config.data_config.PRODUCTS_DATA_TYPES
        dataframe = trim_cols_products_df(df_products=dataframe)

    dataframe = convert_data_types(dataframe=dataframe, data_type_dict=data_type_dict)
    return dataframe
