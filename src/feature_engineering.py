"""
feature_engineering.py
=======================
Derive new features from raw columns to improve model performance.
"""

import pandas as pd
import numpy as np


def add_temporal_features(df: pd.DataFrame, date_col: str = "sale_date") -> pd.DataFrame:
    df = df.copy()
    if date_col in df.columns:
        dt = pd.to_datetime(df[date_col])
        df["sale_year"] = dt.dt.year
        df["sale_month"] = dt.dt.month
        df["sale_quarter"] = dt.dt.quarter
        df["sale_day_of_week"] = dt.dt.dayofweek
        df["is_weekend"] = dt.dt.dayofweek.ge(5).astype(int)
    return df


def add_property_age(df: pd.DataFrame, reference_col: str = "sale_date") -> pd.DataFrame:
    df = df.copy()
    if "year_built" in df.columns and reference_col in df.columns:
        ref_year = pd.to_datetime(df[reference_col]).dt.year
        df["property_age"] = ref_year - df["year_built"]
        df["property_age"] = df["property_age"].clip(lower=0)
        bins = [0, 5, 15, 30, 50, 100, 200]
        labels = ["New (0-5)", "Recent (6-15)", "Established (16-30)",
                  "Mature (31-50)", "Historic (51-100)", "Antique (100+)"]
        df["age_bucket"] = pd.cut(df["property_age"], bins=bins, labels=labels, right=True)
    return df


def add_ratio_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "sale_price" in df.columns and "square_feet" in df.columns:
        df["price_per_sqft"] = (df["sale_price"] / df["square_feet"]).round(2)
    if "bedrooms" in df.columns and "bathrooms" in df.columns:
        df["bed_bath_ratio"] = (df["bedrooms"] / df["bathrooms"].replace(0, np.nan)).round(2)
    if "list_price" in df.columns and "sale_price" in df.columns:
        df["list_to_sale_ratio"] = (df["sale_price"] / df["list_price"].replace(0, np.nan)).round(4)
    if "square_feet" in df.columns and "bedrooms" in df.columns:
        df["sqft_per_bedroom"] = (df["square_feet"] / df["bedrooms"].replace(0, np.nan)).round(0)
    if "lot_size" in df.columns and "square_feet" in df.columns:
        df["lot_to_living_ratio"] = ((df["lot_size"] * 43560) / df["square_feet"].replace(0, np.nan)).round(2)
    return df


def add_neighborhood_stats(df: pd.DataFrame, group_col: str = "neighborhood") -> pd.DataFrame:
    df = df.copy()
    if group_col in df.columns and "sale_price" in df.columns:
        aggs = df.groupby(group_col).agg(
            neighborhood_median_price=("sale_price", "median"),
            neighborhood_avg_sqft=("square_feet", "mean"),
            neighborhood_sale_count=("sale_price", "count"),
        ).reset_index()
        df = df.merge(aggs, on=group_col, how="left")
        df["price_vs_neighborhood_median"] = (
            df["sale_price"] / df["neighborhood_median_price"].replace(0, np.nan)
        ).round(4)
    return df


def add_geospatial_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "latitude" in df.columns and "longitude" in df.columns:
        df["lat_rounded"] = df["latitude"].round(2)
        df["lon_rounded"] = df["longitude"].round(2)
        df["geo_cluster"] = df["lat_rounded"].astype(str) + "_" + df["lon_rounded"].astype(str)
    return df


def run_feature_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    print("Starting feature engineering pipeline...")
    initial_cols = len(df.columns)
    df = add_temporal_features(df)
    df = add_property_age(df)
    df = add_ratio_features(df)
    df = add_neighborhood_stats(df)
    df = add_geospatial_features(df)
    new_cols = len(df.columns) - initial_cols
    print(f"  Added {new_cols} engineered features ({initial_cols} -> {len(df.columns)} total)")
    print("Feature engineering complete.")
    return df
