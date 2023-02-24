from typing import List

import pandas as pd
from re import sub
from shopeepy_wrapped.config.core import DataTypes, config
from shopeepy_wrapped.data.data_manager import save_dataset


def keep_numericals(string_: str) -> float:
    return float(sub("[^0-9|.]", "", str(string_)))


def convert_datetime(dataframe: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    dataframe = dataframe.copy()

    for col in cols:
        dataframe[col] = pd.to_datetime(dataframe[col], format='%m/%d/%Y %H:%M')
    return dataframe


def convert_categorical(dataframe: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    dataframe = dataframe.copy()

    for col in cols:
        dataframe[col] = pd.Categorical(dataframe[col])

    return dataframe


def convert_float(dataframe: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    dataframe = dataframe.copy()

    for col in cols:
        dataframe[col].fillna("0", inplace=True)
        dataframe[col] = dataframe[col].apply(keep_numericals)
        dataframe[col] = dataframe[col].astype(float)

    return dataframe


def convert_object(dataframe: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    dataframe = dataframe.copy()

    for col in cols:
        dataframe[col] = dataframe[col].astype(str)

    return dataframe


def convert_data_types(dataframe: pd.DataFrame, data_type_dict: DataTypes) -> pd.DataFrame:
    for data_type in data_type_dict.keys():
        if data_type == 'datetime':
            dataframe = convert_datetime(dataframe=dataframe, cols=data_type_dict[data_type])
        elif data_type == 'categorical':
            dataframe = convert_categorical(dataframe=dataframe, cols=data_type_dict[data_type])
        elif data_type == 'float':
            dataframe = convert_float(dataframe=dataframe, cols=data_type_dict[data_type])
        elif data_type == 'string':
            dataframe = convert_object(dataframe=dataframe, cols=data_type_dict[data_type])
    return dataframe

def clean_dataset(dataframe: pd.DataFrame, order_type=True):
    if order_type:
        data_type_dict = config.data_config.ORDERS_DATA_TYPES
        file_name = config.data_config.CLEAN_ORDERS_DF_FILENAME
    else:
        data_type_dict = config.data_config.PRODUCTS_DATA_TYPES
        file_name = config.data_config.CLEAN_PRODUCTS_DF_FILENAME

    dataframe = convert_data_types(dataframe=dataframe, data_type_dict=data_type_dict)
    save_dataset(dataset=dataframe, file_name=file_name)

    return dataframe