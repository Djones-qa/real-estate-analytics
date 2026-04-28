"""
train.py — Train and compare multiple regression models.
"""

import pandas as pd
import numpy as np
import joblib
import os
from pathlib import Path
from datetime import datetime
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import sys
from src.utils import load_config
sys.path.append(str(Path(__file__).parent.parent))


def prepare_features(df, config, target=None):
    if target is None:
        target = config["data"]["target_column"]
    numeric_features = [c for c in config["features"]["numeric"] if c in df.columns]
    categorical_features = [c for c in config["features"]["categorical"] if c in df.columns]
    engineered = ["property_age", "price_per_sqft", "bed_bath_ratio", "list_to_sale_ratio",
                  "sqft_per_bedroom", "lot_to_living_ratio", "neighborhood_median_price",
                  "neighborhood_avg_sqft", "neighborhood_sale_count",
                  "sale_year", "sale_month", "sale_quarter"]
    numeric_features += [c for c in engineered if c in df.columns]
    X = df[numeric_features + categorical_features].copy()
    y = df[target] if target in df.columns else None
    return X, y, numeric_features, categorical_features


def build_preprocessor(numeric_features, categorical_features):
    return ColumnTransformer(transformers=[
        ("num", Pipeline([("scaler", StandardScaler())]), numeric_features),
        ("cat", Pipeline([("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))]), categorical_features),
    ], remainder="drop")


def get_models():
    models = {
        "LinearRegression": LinearRegression(),
        "Ridge": Ridge(alpha=1.0),
        "Lasso": Lasso(alpha=1.0),
        "RandomForest": RandomForestRegressor(n_estimators=200, max_depth=15, min_samples_split=5, random_state=42, n_jobs=-1),
        "GradientBoosting": GradientBoostingRegressor(n_estimators=200, max_depth=5, learning_rate=0.1, random_state=42),
    }
    try:
        from xgboost import XGBRegressor
        models["XGBoost"] = XGBRegressor(n_estimators=200, max_depth=6, learning_rate=0.1, random_state=42, n_jobs=-1, verbosity=0)
    except ImportError:
        pass
    try:
        from lightgbm import LGBMRegressor
        models["LightGBM"] = LGBMRegressor(n_estimators=200, max_depth=6, learning_rate=0.1, random_state=42, n_jobs=-1, verbose=-1)
    except ImportError:
        pass
    return models


def train_and_compare(df, config=None, test_size=0.2, cv_folds=5, save_best=True):
    if config is None:
        config = load_config()
    X, y, num_feats, cat_feats = prepare_features(df, config)
    mask = y.notna()
    X, y = X[mask], y[mask]
    rs = config["model"]["random_state"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=rs)
    print(f"Train: {len(X_train):,} | Test: {len(X_test):,}")
    preprocessor = build_preprocessor(num_feats, cat_feats)
    models = get_models()
    results = []
    best_score, best_name, best_pipe = float("inf"), None, None

    for name, model in models.items():
        print(f"Training {name}...", end=" ")
        pipe = Pipeline([("preprocessor", preprocessor), ("model", model)])
        cv = cross_val_score(pipe, X_train, y_train, cv=cv_folds, scoring="neg_mean_absolute_error", n_jobs=-1)
        pipe.fit(X_train, y_train)
        y_pred = pipe.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        results.append({"model": name, "cv_mae": round(-cv.mean(), 2), "test_mae": round(mae, 2),
                        "test_rmse": round(rmse, 2), "test_r2": round(r2, 4)})
        print(f"MAE=${mae:,.0f} | R2={r2:.4f}")
        if mae < best_score:
            best_score, best_name, best_pipe = mae, name, pipe

    results_df = pd.DataFrame(results).sort_values("test_mae")
    print(f"\nBest: {best_name} (MAE=${best_score:,.0f})")
    if save_best and best_pipe:
        save_dir = "models/saved_models"
        os.makedirs(save_dir, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"{save_dir}/{best_name}_{ts}.joblib"
        joblib.dump(best_pipe, path)
        print(f"Saved to {path}")
    return results_df
