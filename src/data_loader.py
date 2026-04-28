"""
data_loader.py
==============
Load raw datasets from CSV/Parquet, validate schema, and return clean DataFrames.
"""

import os
import pandas as pd
import yaml


def load_config(config_path: str = "config/config.yaml") -> dict:
    """Load project configuration from YAML."""
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def load_raw_data(file_name: str, config: dict = None, file_type: str = "csv") -> pd.DataFrame:
    if config is None:
        config = load_config()

    raw_dir = config["data"]["raw_dir"]
    file_path = os.path.join(raw_dir, file_name)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    if file_type == "csv":
        df = pd.read_csv(file_path, parse_dates=[config["data"]["date_column"]])
    elif file_type == "parquet":
        df = pd.read_parquet(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

    print(f"Loaded {len(df):,} rows x {len(df.columns)} columns from {file_path}")
    return df


def validate_schema(df: pd.DataFrame, config: dict = None) -> dict:
    if config is None:
        config = load_config()

    expected_cols = (
        config["features"]["numeric"]
        + config["features"]["categorical"]
        + config["features"]["geospatial"]
        + [config["data"]["target_column"], config["data"]["date_column"]]
    )

    actual_cols = set(df.columns)
    expected_set = set(expected_cols)
    missing = expected_set - actual_cols
    extra = actual_cols - expected_set

    result = {"valid": len(missing) == 0, "missing": sorted(missing), "extra": sorted(extra)}

    if missing:
        print(f"WARNING: Missing {len(missing)} expected columns: {result['missing']}")
    else:
        print("Schema validation passed.")
    return result


def save_processed(df: pd.DataFrame, file_name: str, config: dict = None):
    if config is None:
        config = load_config()

    out_dir = config["data"]["processed_dir"]
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, file_name)

    if file_name.endswith(".parquet"):
        df.to_parquet(out_path, index=False)
    else:
        df.to_csv(out_path, index=False)
    print(f"Saved {len(df):,} rows to {out_path}")


if __name__ == "__main__":
    config = load_config()
    print(f"Project: {config['project']['name']}")
    print(f"Raw data directory: {config['data']['raw_dir']}")
    print("Data loader ready.")
