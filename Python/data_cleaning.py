"""Clean the raw telecom churn dataset used in the notebook analysis."""

from pathlib import Path

import pandas as pd

try:
    from data_loading import DEFAULT_CLEANED_DATA_PATH, RAW_DATA_PATH, load_dataset
except ImportError:
    from .data_loading import DEFAULT_CLEANED_DATA_PATH, RAW_DATA_PATH, load_dataset


REQUIRED_COLUMNS = {"customerID", "tenure", "TotalCharges", "Churn"}


def clean_dataset(data: pd.DataFrame) -> pd.DataFrame:
    """Trim text, convert TotalCharges to numeric, fill zero-tenure blanks, and remove duplicates."""
    missing_columns = REQUIRED_COLUMNS.difference(data.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Dataset is missing required columns: {missing}")

    cleaned = data.copy()

    for column in cleaned.columns:
        if pd.api.types.is_string_dtype(cleaned[column].dtype):
            cleaned[column] = cleaned[column].str.strip()

    original_charges = cleaned["TotalCharges"]
    numeric_charges = pd.to_numeric(original_charges, errors="coerce")
    invalid_charges = numeric_charges.isna() & original_charges.notna() & original_charges.ne("")
    if invalid_charges.any():
        examples = original_charges[invalid_charges].head(3).tolist()
        raise ValueError(f"TotalCharges contains invalid numeric values: {examples}")

    cleaned["TotalCharges"] = numeric_charges.fillna(0)
    cleaned["tenure"] = pd.to_numeric(cleaned["tenure"], errors="raise")
    cleaned["Churn"] = cleaned["Churn"].astype(str).str.strip()
    cleaned = cleaned.drop_duplicates().reset_index(drop=True)
    return cleaned


def main() -> None:
    output_path: Path = DEFAULT_CLEANED_DATA_PATH
    raw_data = load_dataset(RAW_DATA_PATH)
    cleaned = clean_dataset(raw_data)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(output_path, index=False)
    print(f"Saved {len(cleaned):,} cleaned records to {output_path}")


if __name__ == "__main__":
    main()
