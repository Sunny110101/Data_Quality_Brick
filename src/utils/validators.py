import pandas as pd
from typing import Dict, List, Any

def check_nulls(df: pd.DataFrame, threshold: float) -> Dict[str, float]:
    null_percentages = (df.isnull().sum() / len(df)) * 100
    return null_percentages[null_percentages > threshold].to_dict()

def check_duplicates(df: pd.DataFrame) -> int:
    return len(df[df.duplicated()])

def check_ranges(df: pd.DataFrame, ranges: Dict[str, List[float]]) -> Dict[str, int]:
    out_of_range = {}
    for col, (min_val, max_val) in ranges.items():
        if col in df.columns:
            mask = (df[col] < min_val) | (df[col] > max_val)
            out_of_range[col] = len(df[mask])
    return out_of_range
