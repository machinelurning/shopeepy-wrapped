from pathlib import Path
from typing import Dict

from pydantic import BaseModel
from strictyaml import YAML, load

import shopeepy_wrapped

# Project Directories
PACKAGE_ROOT = Path(shopeepy_wrapped.__file__).resolve().parent
ROOT = PACKAGE_ROOT.parent
CONFIG_FILE_PATH = PACKAGE_ROOT / "config.yml"
DATASET_DIR = PACKAGE_ROOT / "datasets"
TRAINED_MODEL_DIR = PACKAGE_ROOT / "trained_models"


class LogInConfig(BaseModel):
    """
    Application-level config.
    """

    USERNAME_INPUT: Dict[str, str]
    PASSWORD_INPUT: Dict[str, str]
    LOGIN_BUTTON: Dict[str, str]
    VERIFY_BY_SHOPEEPAY: Dict[str, str]
    VERIFY_BY_EMAIL_OTP: Dict[str, str]
    LOGINPAGE_LINK: str


class Config(BaseModel):
    """Master config object."""

    login_config: LogInConfig
    # model_config: ModelConfig


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
        # model_config=ModelConfig(**parsed_config.data),
    )

    return _config


config = create_and_validate_config()
