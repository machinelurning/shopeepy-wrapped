from pathlib import Path

import pandas as pd

from shopeepy_wrapped.config.core import DATASET_DIR


def load_dataset(file_name: str) -> pd.DataFrame:
    dataframe = pd.read_csv(Path(f"{DATASET_DIR}/{file_name}"))
    return dataframe


def save_dataset(file_name: str, dataset: pd.DataFrame) -> None:
    dataset.to_csv(Path(f"{DATASET_DIR}/{file_name}"), index=False)
    return None
