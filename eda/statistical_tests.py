"""
statistical_tests.py
=====================
Hypothesis testing and statistical validation for real estate features.
"""

import pandas as pd
import numpy as np
from scipy import stats


def test_normality(series, alpha=0.05):
    clean = series.dropna()
    if len(clean) < 8:
        return {"test_name": "insufficient_data", "statistic": None, "p_value": None, "is_normal": None}
    if len(clean) < 5000:
        stat, p = stats.shapiro(clean)
        test_name = "Shapiro-Wilk"
    else:
        stat, p = stats.normaltest(clean)
        test_name = "DAgostino-Pearson"
    return {"test_name": test_name, "statistic": round(stat, 4), "p_value": round(p, 6), "is_normal": p > alpha}


def test_price_by_group(df, group_col, target="sale_price", alpha=0.05):
    groups = [g[target].dropna().values for _, g in df.groupby(group_col) if len(g) >= 5]
    if len(groups) < 2:
        return {"test_name": "insufficient_groups", "statistic": None, "p_value": None, "significant": None}
    largest = max(groups, key=len)
    norm_result = test_normality(pd.Series(largest))
    if norm_result.get("is_normal", False):
        stat, p = stats.f_oneway(*groups)
        test_name = "One-Way ANOVA"
    else:
        stat, p = stats.kruskal(*groups)
        test_name = "Kruskal-Wallis"
    return {"test_name": test_name, "statistic": round(stat, 4), "p_value": round(p, 6),
            "significant": p < alpha, "group_count": len(groups)}


def test_correlation_significance(df, feature, target="sale_price", method="pearson"):
    clean = df[[feature, target]].dropna()
    if len(clean) < 10:
        return {"correlation": None, "p_value": None, "significant": None, "n": len(clean)}
    if method == "pearson":
        corr, p = stats.pearsonr(clean[feature], clean[target])
    else:
        corr, p = stats.spearmanr(clean[feature], clean[target])
    return {"correlation": round(corr, 4), "p_value": round(p, 6), "significant": p < 0.05, "n": len(clean)}


def test_seasonal_effect(df, target="sale_price"):
    if "sale_quarter" not in df.columns:
        if "sale_date" in df.columns:
            df = df.copy()
            df["sale_quarter"] = pd.to_datetime(df["sale_date"]).dt.quarter
        else:
            return {"error": "No sale_quarter or sale_date column found"}
    return test_price_by_group(df, "sale_quarter", target)


def run_all_tests(df):
    results = []
    norm = test_normality(df.get("sale_price", pd.Series()))
    results.append({"test": "Normality (sale_price)", **norm})
    for col in ["property_type", "condition", "neighborhood", "zoning"]:
        if col in df.columns:
            results.append({"test": f"Group diff ({col})", **test_price_by_group(df, col)})
    for col in ["square_feet", "lot_size", "bedrooms", "bathrooms", "year_built", "garage_spaces"]:
        if col in df.columns:
            results.append({"test": f"Correlation ({col})", **test_correlation_significance(df, col)})
    results.append({"test": "Seasonal effect", **test_seasonal_effect(df)})
    return pd.DataFrame(results)
