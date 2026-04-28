# Real Estate Analytics

![CI](https://github.com/Djones-qa/real-estate-analytics/actions/workflows/ci.yml/badge.svg)

A professional-grade data science pipeline for real estate market analysis and property price prediction. This project implements a modular architecture for data ingestion, cleaning, feature engineering, and automated model selection.

## Features

- **Automated EDA**: Generate univariate statistics, categorical summaries, and correlation heatmaps automatically.
- **Statistical Validation**: Built-in hypothesis testing including Shapiro-Wilk for normality and ANOVA/Kruskal-Wallis for group variance analysis.
- **Robust Preprocessing**: Pipeline for handling price formatting, missing value imputation, and IQR-based outlier removal.
- **Feature Engineering**: Advanced derivation of property age, price/sqft ratios, neighborhood-level median statistics, and geospatial clustering.
- **Model Training Pipeline**: Automated comparison across multiple regressors (Linear Regression, Random Forest, XGBoost, LightGBM) with Scikit-Learn pipelines.
- **CI/CD Integrated**: GitHub Actions workflow for automated testing and linting across multiple Python versions.

## Project Structure

```text
real-estate-analytics/
├── .github/workflows/      # CI/CD configuration
├── config/                 # YAML configuration for features and paths
├── eda/                    # Exploratory Data Analysis & Statistical Tests
│   ├── exploratory_analysis.py
│   └── statistical_tests.py
├── models/                 # Model training logic and saved models
│   └── train.py
├── src/                    # Core processing logic
│   ├── data_loader.py
│   ├── feature_engineering.py
│   ├── preprocessing.py
│   └── utils.py
└── requirements.txt        # Project dependencies
```

## Getting Started

### Installation

1. Ensure you have Python 3.10+ installed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

To run the full training pipeline and save the best performing model:
```bash
python models/train.py
```

## Testing

Run the test suite using `pytest`:
```bash
pytest tests/ -v
```