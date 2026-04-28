"""
utils.py
========
Shared utility functions: logging, config helpers, formatting, and diagnostics.
"""

import os
import yaml
import pandas as pd
from datetime import datetime


def get_project_root() -> Path:
    return Path(__file__).parent.parent


def load_config(config_path: str = None) -> dict:
    if config_path is None:
        config_path = get_project_root() / "config" / "config.yaml"
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def format_currency(value: float) -> str:
    if pd.isna(value):
        return "N/A"
    return f"${value:,.0f}"


def format_pct(value: float, decimals: int = 1) -> str:
    if pd.isna(value):
        return "N/A"
    return f"{value * 100:.{decimals}f}%"


def dataset_summary(df: pd.DataFrame) -> dict:
    total_cells = df.shape[0] * df.shape[1]
    missing_cells = df.isna().sum().sum()
    return {
        "rows": len(df),
        "columns": len(df.columns),
        "missing_pct": round(missing_cells / total_cells * 100, 2) if total_cells else 0,
        "dtypes": df.dtypes.value_counts().to_dict(),
        "memory_mb": round(df.memory_usage(deep=True).sum() / 1e6, 2),
        "duplicates": df.duplicated().sum(),
    }


def print_summary(df: pd.DataFrame, label: str = "Dataset"):
    info = dataset_summary(df)
    print(f"\n{'=' * 50}")fummary")
    print(f"{'=' * 50}")
    print(f"  Rows:        {i":     {info['columns']}")
    print(f"  Missing:     {info['missing_pct']}%")
    print(f"  Duplicates:  {info['duplicates']:,}")
    print(f"  Memory:      {info['memory_mb']} MB")
    print(f"{'=' * 50}\n")

ath: str):
    os.makedirs(path, exist_ok=True)


def timestamp_filename(base_name: str, extension: str = "csv") -> str:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base_name}_{ts}.{extension}"
