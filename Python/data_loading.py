"""Load the telecom customer churn dataset from the project folders."""

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_DIR = PROJECT_ROOT / "Dataset"
RAW_DATA_PATH = DATASET_DIR / "raw_dataset.csv"
DEFAULT_CLEANED_DATA_PATH = DATASET_DIR / "cleaned_dataset.csv"


def find_project_root(start_path: str | Path | None = None) -> Path:
    """Locate the project root by walking upward until both project folders exist."""
    search_root = Path(start_path).resolve() if start_path is not None else Path.cwd()

    for candidate in (search_root, *search_root.parents):
        if (candidate / "Python").is_dir() and (candidate / "Dataset").is_dir():
            return candidate

    raise FileNotFoundError(
        "Project root not found. Start from the project folder or one of its parent directories."
    )


def load_dataset(path: str | Path = RAW_DATA_PATH) -> pd.DataFrame:
    """Read a CSV dataset and return it as a DataFrame."""
    dataset_path = Path(path)
    if not dataset_path.is_file():
        fallback_candidates = [
            PROJECT_ROOT / "Dataset" / dataset_path.name,
            PROJECT_ROOT / dataset_path.name,
        ]
        for candidate in fallback_candidates:
            if candidate.is_file():
                dataset_path = candidate
                break
        else:
            raise FileNotFoundError(f"Dataset file does not exist: {dataset_path}")

    return pd.read_csv(dataset_path)
