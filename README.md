# Telecom Customer Churn Analysis

A modular exploratory data analysis project for the Telco customer churn dataset.
It loads the raw CSV, cleans the charge fields, summarizes churn patterns, and writes
four visualizations plus a PDF report.

## Project structure

```text
Telcom Customer Churn/
├── README.md
├── requirements.txt
├── Dataset/
│   ├── raw_dataset.csv
│   └── cleaned_dataset.csv          # generated
├── Notebook/
│   └── Data_Analysis_EDA.ipynb
├── Python/
│   ├── data_loading.py
│   ├── data_cleaning.py
│   ├── exploratory_analysis.py
│   └── data_visualization.py
├── Visualizations/                  # generated PNG charts
├── Documentation/
│   └── Project_Report.pdf            # generated report
└── .ipynb_checkpoints/              # optional Jupyter metadata
```

## Setup and run

From the project root, install the dependencies and run the analysis:

```bash
python -m pip install -r requirements.txt
python Python/data_cleaning.py
python Python/data_visualization.py
```

The cleaning step writes `Dataset/cleaned_dataset.csv`. The visualization step
creates `distribution_analysis.png`, `trend_analysis.png`,
`category_analysis.png`, and `correlation_analysis.png` in `Visualizations/`,
and assembles them into `Documentation/Project_Report.pdf`.

Run the notebook from Jupyter or VS Code for an interactive walkthrough. The
notebook auto-detects the project root by locating the `Python` and `Dataset`
folders, so it works even when the project folder name differs from the original
example structure.

## Data notes

The raw dataset has 7,043 customer records and 21 columns. `TotalCharges` is
stored as text in the source CSV; its 11 blank values belong to customers with
zero months of tenure and are converted to numeric zero during cleaning.
Exact duplicate records are removed if present. Customer IDs are retained for
traceability but are not included in the numeric correlation analysis.

## Analysis scope

- Churn distribution and tenure patterns
- Churn rate by contract, internet service, and payment method
- Correlations among numeric measures and the binary churn indicator
- A concise PDF report with the generated charts

This is descriptive exploratory analysis, not a causal or predictive model.
