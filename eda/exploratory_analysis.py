"""
exploratory_analysis.py
========================
Automated EDA routines for the real estate dataset.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from src.utils import format_currency, print_summary  # noqa: E402


def univariate_summary(df, target="sale_price"):
    numeric = df.select_dtypes(include=[np.number])
    stats = numeric.describe().T
    stats["skew"] = numeric.skew()
    stats["kurtosis"] = numeric.kurtosis()
    stats["missing_pct"] = (numeric.isna().sum() / len(df) * 100).round(2)
    return stats.round(2)


def categorical_summary(df):
    cat_cols = df.select_dtypes(include=["object", "category"]).columns
    summaries = {}
    for col in cat_cols:
        vc = df[col].value_counts()
        summaries[col] = {
            "unique": df[col].nunique(),
            "top_value": vc.index[0] if len(vc) > 0 else None,
            "top_freq": vc.iloc[0] if len(vc) > 0 else 0,
            "top_pct": round(vc.iloc[0] / len(df) * 100, 1) if len(vc) > 0 else 0,
            "missing": df[col].isna().sum(),
        }
    return pd.DataFrame(summaries).T


def correlation_matrix(df, method="pearson"):
    numeric = df.select_dtypes(include=[np.number])
    return numeric.corr(method=method).round(3)


def top_correlations(df, target="sale_price", n=15):
    corr = correlation_matrix(df)
    if target not in corr.columns:
        return pd.DataFrame()
    target_corr = corr[target].drop(target, errors="ignore").abs().sort_values(ascending=False).head(n)
    return pd.DataFrame({
        "feature": target_corr.index,
        "abs_correlation": target_corr.values,
        "correlation": corr[target].loc[target_corr.index].values,
    })


def price_by_category(df, category, target="sale_price"):
    if category not in df.columns or target not in df.columns:
        return pd.DataFrame()
    return df.groupby(category)[target].agg(
        ["count", "mean", "median", "std", "min", "max"]
    ).round(0).sort_values("median", ascending=False)


def plot_price_distribution(df, target="sale_price", output_dir=None):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    axes[0].hist(df[target].dropna(), bins=50, color="#2196F3", edgecolor="white", alpha=0.8)
    axes[0].set_title("Sale Price Distribution", fontweight="bold")
    axes[0].set_xlabel("Sale Price ($)")
    axes[0].set_ylabel("Frequency")
    axes[0].axvline(df[target].median(), color="red", linestyle="--",
                    label=f"Median: {format_currency(df[target].median())}")
    axes[0].legend()
    axes[1].boxplot(df[target].dropna(), vert=True, patch_artist=True,
                    boxprops=dict(facecolor="#2196F3", alpha=0.6))
    axes[1].set_title("Sale Price Box Plot", fontweight="bold")
    axes[1].set_ylabel("Sale Price ($)")
    plt.tight_layout()
    if output_dir:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        plt.savefig(f"{output_dir}/price_distribution.png", dpi=150, bbox_inches="tight")
    plt.close()


def plot_correlation_heatmap(df, output_dir=None):
    corr = correlation_matrix(df)
    fig, ax = plt.subplots(figsize=(12, 10))
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="RdBu_r",
                center=0, square=True, linewidths=0.5, ax=ax)
    ax.set_title("Feature Correlation Heatmap", fontweight="bold")
    plt.tight_layout()
    if output_dir:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        plt.savefig(f"{output_dir}/correlation_heatmap.png", dpi=150, bbox_inches="tight")
    plt.close()


def run_full_eda(df, output_dir="visualizations/output"):
    print_summary(df, "Raw Dataset")
    print("\n--- Univariate Summary ---")
    print(univariate_summary(df).to_string())
    print("\n--- Categorical Summary ---")
    cat = categorical_summary(df)
    if not cat.empty:
        print(cat.to_string())
    print("\n--- Top Correlations with Sale Price ---")
    tc = top_correlations(df)
    if not tc.empty:
        print(tc.to_string(index=False))
    print("\n--- Price by Property Type ---")
    pbt = price_by_category(df, "property_type")
    if not pbt.empty:
        print(pbt.to_string())
    plot_price_distribution(df, output_dir=output_dir)
    plot_correlation_heatmap(df, output_dir=output_dir)
    print(f"\nEDA complete. Plots saved to {output_dir}/")
