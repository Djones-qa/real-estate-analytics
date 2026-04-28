"""
predict.py — Load trained models and generate predictions.
"""

import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from glob import glob
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from src.utils import load_config, format_currency  # noqa: E402


def load_latest_model(model_dir="models/saved_models"):
    model_files = sorted(glob(f"{model_dir}/*.joblib"))
    if not model_files:
        raise FileNotFoundError(f"No saved models in {model_dir}/")
    latest = model_files[-1]
    pipeline = joblib.load(latest)
    print(f"Loaded model: {latest}")
    return pipeline, latest


def predict_single(pipeline, property_data, config=None):
    if config is None:
        config = load_config()
    df = pd.DataFrame([property_data])
    prediction = pipeline.predict(df)[0]
    return {"predicted_price": round(prediction, 0), "formatted": format_currency(prediction),
            "input_features": property_data}


def predict_batch(pipeline, df, output_col="predicted_price"):
    df = df.copy()
    predictions = pipeline.predict(df)
    df[output_col] = np.round(predictions, 0)
    print(f"Generated {len(predictions):,} predictions")
    print(f"  Mean: {format_currency(predictions.mean())} | Median: {format_currency(np.median(predictions))}")
    return df


def compare_predictions(df, actual_col="sale_price", predicted_col="predicted_price"):
    df = df.copy()
    if actual_col in df.columns and predicted_col in df.columns:
        df["prediction_error"] = df[predicted_col] - df[actual_col]
        df["abs_error"] = df["prediction_error"].abs()
        df["pct_error"] = (df["prediction_error"] / df[actual_col] * 100).round(2)
        print(f"Mean Abs Error: {format_currency(df['abs_error'].mean())}")
        print(f"Mean % Error: {df['pct_error'].mean():.2f}%")
    return df
