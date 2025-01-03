"""
data_processing.py

Processes/cleans the data as needed (e.g. fill missing values, remove outliers).
"""

import pandas as pd

def process_data(df: pd.DataFrame):
    """
    Process/clean the data, e.g. fill missing values, remove outliers, etc.
    """
    # Forward fill then drop any remaining NaNs
    df = df.ffill().dropna()
    return df
