from pathlib import Path
from typing import List

from pydantic import BaseModel
from strictyaml import YAML, load
from typing_extensions import NotRequired, TypedDict

import shopeepy_wrapped

# Project Directories
PACKAGE_ROOT = Path(shopeepy_wrapped.__file__).resolve().parent
ROOT = PACKAGE_ROOT.parent
CONFIG_FILE_PATH = PACKAGE_ROOT / "config.yml"
DATASET_DIR = PACKAGE_ROOT / "datasets"


class InvalidCredentials(Exception):
    pass


class Element(TypedDict):
    element_tag: str
    attribute: NotRequired[str]
    attribute_value: NotRequired[List[str]]


class DataTypes(TypedDict):
    datetime: NotRequired[List[str]]
    categorical: NotRequired[List[str]]
    float: NotRequired[List[str]]
    string: NotRequired[List[str]]


class LogInConfig(BaseModel):
    """
    Application-level config.
    """

    LOGINPAGE_LINK: str
    VERIFY_BY_EMAIL_LINK: str
    USERNAME_INPUT: Element
    PASSWORD_INPUT: Element
    LOGIN_BUTTON: Element
    LOGIN_CONFIRM: Element
    WRONG_CREDENTIALS: Element


class ScrapeeConfig(BaseModel):
    """
    Scraping config.
    """

    USER_PURCHASE_STR: str
    PURCHASEPAGE_LINK: str
    PURCHASES: Element
    NAME: Element
    PRICE: Element
    STORE: Element
    STATUS: Element
    HREF: Element
    BUNDLE: Element
    PRODUCT: Element
    BREAD_CRUMB_ELEMENT: Element
    BREAD_CRUMB: Element
    ORDER_ID: Element
    ORDER_DETAILS: Element
    ORDER_DETAILS_ELEMENTS: Element
    TRACKING_STAGES: Element
    TRACKING_TIMESTAMPS: Element
    PRICE_BREAKDOWN_ELEMENT: Element
    PRICE_BREAKDOWN_CATEGORIES: Element
    PRICE_BREAKDOWN_VALUES: Element
    THUMBNAIL: Element


class DataConfig(BaseModel):
    ORDERS_KEEP_COLS: List[str]
    ORDERS_UNCLEANED_FILENAME: str
    PRODUCTS_UNCLEANED_FILENAME: str
    ORDERS_DATA_TYPES: DataTypes
    PRODUCTS_DATA_TYPES: DataTypes
    CLEAN_PRODUCTS_DF_FILENAME: str
    CLEAN_ORDERS_DF_FILENAME: str


class Config(BaseModel):
    """Master config object."""

    login_config: LogInConfig
    scrapee_config: ScrapeeConfig
    data_config: DataConfig


def find_config_file() -> Path:
    """
    Locate the configuration file.
    """

    if CONFIG_FILE_PATH.is_file():
        return CONFIG_FILE_PATH
    raise Exception(f"Config not found at {CONFIG_FILE_PATH!r}")


def fetch_config_from_yaml(cfg_path: Path = None) -> YAML:
    """
    Parse YAML containing the package configuration.
    """

    if not cfg_path:
        cfg_path = find_config_file()

    if cfg_path:
        with open(cfg_path, "r") as conf_file:
            parsed_config = load(conf_file.read())
            return parsed_config
    raise OSError(f"Did not find config file at path: {cfg_path}")


def create_and_validate_config(parsed_config: YAML = None) -> Config:
    """
    Run validation on config values.
    """

    if parsed_config is None:
        parsed_config = fetch_config_from_yaml()

    # specify the data attribute from the strictyaml YAML type.
    _config = Config(
        login_config=LogInConfig(**parsed_config.data),
        scrapee_config=ScrapeeConfig(**parsed_config.data),
        data_config=DataConfig(**parsed_config.data),
    )

    return _config


config = create_and_validate_config()
