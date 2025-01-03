"""
data_validation.py

Check data integrity: missing values, duplicates, etc.
"""

import pandas as pd

def validate_data(df: pd.DataFrame):
    """
    Validate the DataFrame for missing values, duplicates, etc.
    """
    # Check for duplicates
    if df.index.duplicated().any():
        print("Warning: There are duplicated dates in the index.")
    
    # Check for missing values
    missing_values = df.isnull().sum()
    total_missing = missing_values.sum()
    if total_missing > 0:
        print("Warning: There are missing values in the DataFrame:")
        print(missing_values[missing_values > 0])
    else:
        print("Data validation passed with no missing values.")
    
    return df
