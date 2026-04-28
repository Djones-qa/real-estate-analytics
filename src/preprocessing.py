"""
preprocessing.py
=================
Data cleaning, outlier handling, missing value imputation, and type casting.
"""

import pandas as pd
import numpy as np


def clean_price_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    price_cols = [c for c in df.columns if "price" in c.lower() or "fee" in c.lower()]
    for col in price_cols:
        # Ensure columns are treated as strings for cleaning, then convert to numeric
        df[col] = (
            df[col].astype(str)
            .str.replace(r"[\$,]", "", regex=True)
            .replace(["", "nan", "None", "NaN"], np.nan)
        )
        df[col] = pd.to_numeric(df[col], errors='coerce')

    if "sale_price" in df.columns:
        df = df[df["sale_price"].gt(0)]
    return df


def handle_missing_values(df: pd.DataFrame, strategy: dict = None) -> pd.DataFrame:
    df = df.copy()
    if strategy is None:
        strategy = {}

    numeric_cols = df.select_dtypes(include=[np.number]).columns
    categorical_cols = df.select_dtypes(include=["object", "string", "category"]).columns

    for col in numeric_cols:
        if df[col].isna().any():
            method = strategy.get(col, "median")
            if method == "median":
                df[col] = df[col].fillna(df[col].median())
            elif method == "mean":
                df[col] = df[col].fillna(df[col].mean())
            elif method == "zero":
                df[col] = df[col].fillna(0)
            elif method == "drop":
                df = df.dropna(subset=[col])

    for col in categorical_cols:
        if df[col].isna().any():
            method = strategy.get(col, "mode")
            if method == "mode":
                mode_val = df[col].mode()
                if not mode_val.empty:
                    df[col] = df[col].fillna(mode_val[0])
            elif method == "unknown":
                df[col] = df[col].fillna("Unknown")
    return df


def remove_outliers_iqr(df: pd.DataFrame, columns: list = None, multiplier: float = 1.5) -> pd.DataFrame:
    df = df.copy()
    if columns is None:
        columns = ["sale_price", "square_feet"]
    columns = [c for c in columns if c in df.columns]

    for col in columns:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - multiplier * iqr
        upper = q3 + multiplier * iqr
        before = len(df)
        df = df[(df[col] >= lower) & (df[col] <= upper)]
        removed = before - len(df)
        if removed > 0:
            print(f"  {col}: removed {removed} outliers (range: {lower:,.0f} - {upper:,.0f})")
    return df


def cast_types(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    int_cols = ["bedrooms", "garage_spaces", "stories", "year_built", "days_on_market"]
    for col in int_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

    float_cols = ["bathrooms", "lot_size", "hoa_fee"]
    for col in float_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "zip_code" in df.columns:
        df["zip_code"] = df["zip_code"].astype(str).str.zfill(5)
    return df


def run_preprocessing_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    print("Starting preprocessing pipeline...")
    print(f"  Input: {len(df):,} rows")
    df = clean_price_columns(df)
    print(f"  After price cleaning: {len(df):,} rows")
    df = cast_types(df)
    df = handle_missing_values(df)
    print(f"  After imputation: {len(df):,} rows")
    df = remove_outliers_iqr(df)
    print(f"  After outlier removal: {len(df):,} rows")
    print("Preprocessing complete.")
    return df
