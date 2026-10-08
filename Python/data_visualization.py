"""Generate the notebook-style telecom churn charts and report."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages

try:
    from data_cleaning import clean_dataset
    from data_loading import DEFAULT_CLEANED_DATA_PATH, PROJECT_ROOT, load_dataset
    from exploratory_analysis import churn_rate_by, numeric_correlations, summarize_dataset
except ImportError:
    from .data_cleaning import clean_dataset
    from .data_loading import DEFAULT_CLEANED_DATA_PATH, PROJECT_ROOT, load_dataset
    from .exploratory_analysis import churn_rate_by, numeric_correlations, summarize_dataset


VISUALIZATION_DIR = PROJECT_ROOT / "Visualizations"
REPORT_PATH = PROJECT_ROOT / "Documentation" / "Project_Report.pdf"
IMPORTANT_PLOT_FILENAMES = (
    "customer_churn_distribution.png",
    "contract_churn.png",
    "tenure_churn_boxplot.png",
    "monthly_charges_churn.png",
    "internet_service_churn.png",
    "payment_method_churn.png",
    "correlation_matrix.png",
)

sns.set_theme(style="whitegrid")


def _save_figure(fig: plt.Figure, filename: str) -> Path:
    path = VISUALIZATION_DIR / filename
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)
    return path


def create_visualizations(data: pd.DataFrame) -> list[Path]:
    """Create the same main EDA visuals used in the notebook."""
    VISUALIZATION_DIR.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []

    fig, ax = plt.subplots(figsize=(6, 4))
    sns.countplot(data=data, x="Churn", ax=ax)
    ax.set_title("Customer Churn Distribution")
    ax.set_xlabel("Churn")
    ax.set_ylabel("Number of Customers")
    fig.tight_layout()
    paths.append(_save_figure(fig, "customer_churn_distribution.png"))

    fig, ax = plt.subplots(figsize=(7, 5))
    sns.countplot(data=data, x="gender", hue="Churn", ax=ax)
    ax.set_title("Gender vs Customer Churn")
    ax.set_xlabel("Gender")
    ax.set_ylabel("Number of Customers")
    fig.tight_layout()
    paths.append(_save_figure(fig, "gender_churn.png"))

    fig, ax = plt.subplots(figsize=(7, 5))
    sns.countplot(data=data, x="SeniorCitizen", hue="Churn", ax=ax)
    ax.set_title("Senior Citizen vs Customer Churn")
    ax.set_xlabel("Senior Citizen")
    ax.set_ylabel("Number of Customers")
    fig.tight_layout()
    paths.append(_save_figure(fig, "senior_churn.png"))

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(data=data, x="Contract", hue="Churn", ax=ax)
    ax.set_title("Contract Type vs Customer Churn")
    ax.set_xlabel("Contract Type")
    ax.set_ylabel("Number of Customers")
    ax.tick_params(axis="x", rotation=15)
    fig.tight_layout()
    paths.append(_save_figure(fig, "contract_churn.png"))

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=data, x="Churn", y="tenure", ax=ax)
    ax.set_title("Tenure vs Customer Churn")
    ax.set_xlabel("Churn")
    ax.set_ylabel("Tenure (Months)")
    fig.tight_layout()
    paths.append(_save_figure(fig, "tenure_churn_boxplot.png"))

    fig, ax = plt.subplots(figsize=(9, 5))
    sns.histplot(data=data, x="tenure", hue="Churn", bins=30, kde=True, ax=ax)
    ax.set_title("Tenure Distribution by Churn")
    ax.set_xlabel("Tenure (Months)")
    ax.set_ylabel("Number of Customers")
    fig.tight_layout()
    paths.append(_save_figure(fig, "tenure_distribution_by_churn.png"))

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=data, x="Churn", y="MonthlyCharges", ax=ax)
    ax.set_title("Monthly Charges vs Customer Churn")
    ax.set_xlabel("Churn")
    ax.set_ylabel("Monthly Charges")
    fig.tight_layout()
    paths.append(_save_figure(fig, "monthly_charges_churn.png"))

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=data, x="Churn", y="TotalCharges", ax=ax)
    ax.set_title("Total Charges vs Customer Churn")
    ax.set_xlabel("Churn")
    ax.set_ylabel("Total Charges")
    fig.tight_layout()
    paths.append(_save_figure(fig, "total_charges_churn.png"))

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(data=data, x="InternetService", hue="Churn", ax=ax)
    ax.set_title("Internet Service vs Customer Churn")
    ax.set_xlabel("Internet Service")
    ax.set_ylabel("Number of Customers")
    fig.tight_layout()
    paths.append(_save_figure(fig, "internet_service_churn.png"))

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.countplot(data=data, x="PaymentMethod", hue="Churn", ax=ax)
    ax.set_title("Payment Method vs Customer Churn")
    ax.set_xlabel("Payment Method")
    ax.set_ylabel("Number of Customers")
    ax.tick_params(axis="x", rotation=25)
    fig.tight_layout()
    paths.append(_save_figure(fig, "payment_method_churn.png"))

    fig, ax = plt.subplots(figsize=(7, 5))
    sns.countplot(data=data, x="Partner", hue="Churn", ax=ax)
    ax.set_title("Partner Status vs Customer Churn")
    ax.set_xlabel("Partner")
    ax.set_ylabel("Number of Customers")
    fig.tight_layout()
    paths.append(_save_figure(fig, "partner_churn.png"))

    fig, ax = plt.subplots(figsize=(7, 5))
    sns.countplot(data=data, x="Dependents", hue="Churn", ax=ax)
    ax.set_title("Dependents vs Customer Churn")
    ax.set_xlabel("Dependents")
    ax.set_ylabel("Number of Customers")
    fig.tight_layout()
    paths.append(_save_figure(fig, "dependents_churn.png"))

    fig, ax = plt.subplots(figsize=(7, 5))
    sns.countplot(data=data, x="PhoneService", hue="Churn", ax=ax)
    ax.set_title("Phone Service vs Customer Churn")
    ax.set_xlabel("Phone Service")
    ax.set_ylabel("Number of Customers")
    fig.tight_layout()
    paths.append(_save_figure(fig, "phone_service_churn.png"))

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(data=data, x="MultipleLines", hue="Churn", ax=ax)
    ax.set_title("Multiple Lines vs Customer Churn")
    ax.set_xlabel("Multiple Lines")
    ax.set_ylabel("Number of Customers")
    fig.tight_layout()
    paths.append(_save_figure(fig, "multiple_lines_churn.png"))

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(data=data, x="OnlineSecurity", hue="Churn", ax=ax)
    ax.set_title("Online Security vs Customer Churn")
    ax.set_xlabel("Online Security")
    ax.set_ylabel("Number of Customers")
    ax.tick_params(axis="x", rotation=15)
    fig.tight_layout()
    paths.append(_save_figure(fig, "online_security_churn.png"))

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(data=data, x="TechSupport", hue="Churn", ax=ax)
    ax.set_title("Technical Support vs Customer Churn")
    ax.set_xlabel("Tech Support")
    ax.set_ylabel("Number of Customers")
    fig.tight_layout()
    paths.append(_save_figure(fig, "tech_support_churn.png"))

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    sns.countplot(data=data, x="StreamingTV", hue="Churn", ax=axes[0])
    axes[0].set_title("Streaming TV vs Churn")
    axes[0].tick_params(axis="x", rotation=15)
    sns.countplot(data=data, x="StreamingMovies", hue="Churn", ax=axes[1])
    axes[1].set_title("Streaming Movies vs Churn")
    axes[1].tick_params(axis="x", rotation=15)
    plt.tight_layout()
    paths.append(_save_figure(fig, "streaming_services_churn.png"))

    churn_numeric = data["Churn"].map({"Yes": 1, "No": 0})
    correlation = data[["SeniorCitizen", "tenure", "MonthlyCharges", "TotalCharges"]].copy()
    correlation["Churn_numeric"] = churn_numeric
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(correlation.corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    ax.set_title("Correlation Matrix")
    fig.tight_layout()
    paths.append(_save_figure(fig, "correlation_matrix.png"))

    important_paths = filter_important_chart_paths(paths)
    important_filenames = {path.name for path in important_paths}
    for path in VISUALIZATION_DIR.glob("*.png"):
        if path.name not in important_filenames:
            path.unlink()
    return important_paths


def filter_important_chart_paths(chart_paths: list[Path]) -> list[Path]:
    """Keep the seven most useful charts for the visualization folder and report."""
    paths_by_name = {path.name: path for path in chart_paths}
    return [paths_by_name[filename] for filename in IMPORTANT_PLOT_FILENAMES]


def create_report(data: pd.DataFrame, chart_paths: list[Path]) -> Path:
    """Write a PDF report with summary text and the main chart pages."""
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    summary = summarize_dataset(data)
    churn_rates = {column: churn_rate_by(data, column) for column in ("Contract", "InternetService")}
    with PdfPages(REPORT_PATH) as pdf:
        fig, ax = plt.subplots(figsize=(8.27, 11.69))
        ax.axis("off")
        lines = [
            "Telecom Customer Churn Analysis",
            "",
            f"Customers analyzed: {summary['rows']:,}",
            f"Overall churn rate: {summary['churn_rate']:.1%}",
            f"Median tenure: {summary['median_tenure']:.0f} months",
            f"Mean monthly charges: ${summary['mean_monthly_charges']:.2f}",
            "",
            "Key observations",
            f"- Month-to-month churn rate: {churn_rates['Contract'].loc['Month-to-month', 'churn_rate']:.1%}",
            f"- One-year contract churn rate: {churn_rates['Contract'].loc['One year', 'churn_rate']:.1%}",
            f"- Two-year contract churn rate: {churn_rates['Contract'].loc['Two year', 'churn_rate']:.1%}",
            "",
            "The patterns shown are descriptive associations, not evidence of causation.",
            "Review the selected charts on the following pages for churn, contract, tenure, billing, service, payment, and correlation detail.",
        ]
        ax.text(0.08, 0.92, "\n".join(lines), va="top", fontsize=13, linespacing=1.5)
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

        for chart_path in chart_paths:
            image = plt.imread(chart_path)
            fig, ax = plt.subplots(figsize=(11, 7))
            ax.imshow(image)
            ax.axis("off")
            pdf.savefig(fig, bbox_inches="tight")
            plt.close(fig)

    return REPORT_PATH


def main() -> None:
    if DEFAULT_CLEANED_DATA_PATH.is_file():
        data = load_dataset(DEFAULT_CLEANED_DATA_PATH)
    else:
        data = clean_dataset(load_dataset())
        DEFAULT_CLEANED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        data.to_csv(DEFAULT_CLEANED_DATA_PATH, index=False)

    chart_paths = create_visualizations(data)
    report_path = create_report(data, chart_paths)
    print(f"Created {len(chart_paths)} charts in {VISUALIZATION_DIR}")
    print(f"Created report at {report_path}")


if __name__ == "__main__":
    main()
