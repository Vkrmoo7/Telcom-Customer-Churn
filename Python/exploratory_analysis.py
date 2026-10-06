"""Summary and churn-rate calculations that mirror the notebook analysis."""

import pandas as pd


def summarize_dataset(data: pd.DataFrame) -> dict[str, object]:
    """Return dataset size, target balance, and a few descriptive metrics."""
    churn_counts = data["Churn"].value_counts().reindex(["No", "Yes"], fill_value=0)
    churn_rate = float(churn_counts["Yes"] / len(data)) if len(data) else 0.0
    return {
        "rows": int(len(data)),
        "columns": int(data.shape[1]),
        "churn_counts": churn_counts.to_dict(),
        "churn_rate": churn_rate,
        "median_tenure": float(data["tenure"].median()),
        "mean_monthly_charges": float(data["MonthlyCharges"].mean()),
    }


def target_distribution(data: pd.DataFrame) -> pd.Series:
    """Return the churn count distribution and proportions."""
    counts = data["Churn"].value_counts()
    return counts


def churn_rate_by(data: pd.DataFrame, column: str) -> pd.DataFrame:
    """Return customers and churn rate grouped by a categorical column."""
    if column not in data.columns:
        raise KeyError(f"Column not found in dataset: {column}")
    if "Churn" not in data.columns:
        raise KeyError("Column not found in dataset: Churn")

    return (
        data.groupby(column, dropna=False)["Churn"]
        .agg(customers="size", churn_rate=lambda values: values.eq("Yes").mean())
        .sort_values("churn_rate", ascending=False)
        .reset_index()
        .rename(columns={column: column})
        .set_index(column)
    )


def feature_churn_rates(data: pd.DataFrame, features: list[str]) -> dict[str, pd.DataFrame]:
    """Build churn-rate tables for multiple categorical features."""
    return {feature: churn_rate_by(data, feature) for feature in features}


def numeric_correlations(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate correlations using numeric columns and a binary churn indicator."""
    numeric_data = data.select_dtypes(include="number").copy()
    numeric_data["Churn_numeric"] = data["Churn"].map({"No": 0, "Yes": 1})
    return numeric_data.corr()
