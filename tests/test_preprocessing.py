import pandas as pd
import numpy as np
import pytest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from src.preprocessing import clean_price_columns, handle_missing_values

def test_clean_price_columns():
    data = {
        "sale_price": ["$500,000", "450,000", "0", "nan"],
        "hoa_fee": ["$100", None, "50", "20.50"]
    }
    df = pd.DataFrame(data)
    cleaned_df = clean_price_columns(df)
    
    # Should remove $ and , and convert to float
    assert cleaned_df["sale_price"].iloc[0] == 500000.0
    # Should filter out non-positive sale prices (0 and nan)
    assert len(cleaned_df) == 2
    assert cleaned_df["hoa_fee"].iloc[0] == 100.0

def test_handle_missing_values():
    df = pd.DataFrame({"bedrooms": [3, 4, np.nan], "property_type": ["Single Family", None, "Condo"]})
    fixed_df = handle_missing_values(df)
    assert fixed_df["bedrooms"].isna().sum() == 0
    assert fixed_df["property_type"].isna().sum() == 0