from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_DIR = PROJECT_ROOT / "data" / "movie-recommendation-hackathon-2026"


def _resolve_data_dir(data_dir: str | Path | None = None) -> Path:
    return Path(data_dir) if data_dir is not None else DEFAULT_DATA_DIR


def load_train_data(data_dir: str | Path | None = None) -> pd.DataFrame:
    data_path = _resolve_data_dir(data_dir) / "train.csv"
    return pd.read_csv(data_path)


def load_test_data(data_dir: str | Path | None = None) -> pd.DataFrame:
    data_path = _resolve_data_dir(data_dir) / "test.csv"
    return pd.read_csv(data_path)


def load_movies_data(data_dir: str | Path | None = None) -> pd.DataFrame:
    data_path = _resolve_data_dir(data_dir) / "movies.csv"
    return pd.read_csv(data_path)


def load_sample_submission(data_dir: str | Path | None = None) -> pd.DataFrame:
    data_path = _resolve_data_dir(data_dir) / "sample_submission.csv"
    return pd.read_csv(data_path)