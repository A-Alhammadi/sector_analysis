#!/usr/bin/env python3

import os

# ----------------------------------------------------------------
# This script will generate a folder named 'my_project' and create
# the following Python files:
#
#   1. config.py
#   2. data_import.py
#   3. data_validation.py
#   4. data_processing.py
#   5. calculations.py
#   6. plots.py
#   7. main.py
#
# with the contents needed to:
#   - Download data for S&P 500, VIX, and sector ETFs
#   - Validate, process, and compute metrics
#   - Generate plots
# ----------------------------------------------------------------

PROJECT_NAME = "my_project"

files_content = {
    "config.py": """\"\"\"
config.py

Central configuration for tickers, date ranges, and global parameters.
\"\"\"

import datetime

# Tickers of interest
SECTOR_ETFS = [
    "XLY",   # Consumer Discretionary
    "XLP",   # Consumer Staples
    "XLE",   # Energy
    "XLF",   # Financials
    "XLV",   # Health Care
    "XLI",   # Industrials
    "XLB",   # Materials
    "XLK",   # Technology
    "XLC",   # Communication Services
    "XLRE",  # Real Estate
    "XLU"    # Utilities
]

SP500_TICKER = "^GSPC"
VIX_TICKER = "^VIX"

# Combine all tickers into one list
ALL_TICKERS = SECTOR_ETFS + [SP500_TICKER, VIX_TICKER]

# Date range (approximately 10 years back)
START_DATE_10YR = "2013-01-01"
END_DATE = datetime.datetime.today().strftime("%Y-%m-%d")

# Rolling window for correlation (in days)
ROLLING_WINDOW = 60

# Periods (in years) for metric calculations
PERIODS = {
    "10Y": 10,
    "5Y": 5,
    "3Y": 3,
    "1Y": 1,
}
""",
    "data_import.py": """\"\"\"
data_import.py

Fetch raw data from Yahoo Finance using yfinance.
\"\"\"

import yfinance as yf
import pandas as pd
from config import ALL_TICKERS, START_DATE_10YR, END_DATE

def fetch_data(tickers=None, start=None, end=None):
    \"\"\"
    Fetches daily adjusted close data from Yahoo Finance for the given tickers.
    \"\"\"
    if tickers is None:
        tickers = ALL_TICKERS

    if start is None:
        start = START_DATE_10YR
    
    if end is None:
        end = END_DATE

    data = yf.download(tickers, start=start, end=end)

    # By default, yfinance returns a multi-level column DataFrame
    # We'll reduce it to a single level with just the 'Adj Close' prices.
    if "Adj Close" in data:
        data = data["Adj Close"]
    else:
        # Fallback if 'Adj Close' is not in the data
        data = data["Close"]

    # Ensure data is a DataFrame (in case there's only 1 ticker)
    if isinstance(data, pd.Series):
        data = data.to_frame()
    
    return data
""",
    "data_validation.py": """\"\"\"
data_validation.py

Check data integrity: missing values, duplicates, etc.
\"\"\"

import pandas as pd

def validate_data(df: pd.DataFrame):
    \"\"\"
    Validate the DataFrame for missing values, duplicates, etc.
    \"\"\"
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
""",
    "data_processing.py": """\"\"\"
data_processing.py

Processes/cleans the data as needed (e.g. fill missing values, remove outliers).
\"\"\"

import pandas as pd

def process_data(df: pd.DataFrame):
    \"\"\"
    Process/clean the data, e.g. fill missing values, remove outliers, etc.
    \"\"\"
    # Forward fill then drop any remaining NaNs
    df = df.ffill().dropna()
    return df
""",
    "calculations.py": """\"\"\"
calculations.py

Core financial calculations: rolling correlations, performance, metrics, etc.
\"\"\"

import pandas as pd
import numpy as np
from config import SP500_TICKER, PERIODS, ROLLING_WINDOW

def calculate_daily_returns(df: pd.DataFrame) -> pd.DataFrame:
    \"\"\"
    Calculate daily percentage returns for each column.
    \"\"\"
    return df.pct_change().fillna(0)

def calculate_rolling_correlation(df_returns: pd.DataFrame, benchmark=SP500_TICKER, window=ROLLING_WINDOW) -> pd.DataFrame:
    \"\"\"
    Calculate rolling correlation of each ticker vs a benchmark (S&P 500).
    \"\"\"
    benchmark_returns = df_returns[benchmark]
    rolling_corr = df_returns.apply(lambda x: x.rolling(window).corr(benchmark_returns))
    return rolling_corr

def calculate_relative_performance(df: pd.DataFrame, benchmark=SP500_TICKER):
    \"\"\"
    Calculate the ratio of each ticker's price to the benchmark's price.
    \"\"\"
    return df.div(df[benchmark], axis=0)

def calculate_cumulative_returns(df_returns: pd.DataFrame) -> pd.DataFrame:
    \"\"\"
    Calculate cumulative returns from daily returns.
    \"\"\"
    # (1 + r).cumprod() - 1 for each ticker
    cumulative = (1 + df_returns).cumprod() - 1
    return cumulative

def metrics_for_period(df: pd.DataFrame, start_date, end_date):
    \"\"\"
    Calculate key metrics (total return, annualized return, volatility) over a date range.
    \"\"\"
    sliced = df.loc[start_date:end_date]
    if sliced.empty:
        return {
            "total_return": np.nan,
            "annualized_return": np.nan,
            "volatility": np.nan
        }
    daily_returns = sliced.pct_change().dropna()

    # Total return
    total_return = (sliced.iloc[-1] / sliced.iloc[0]) - 1

    # Annualized return (approx. 252 trading days)
    annualized_return = (1 + total_return) ** (252 / len(sliced)) - 1

    # Volatility (std dev of daily returns * sqrt(252))
    volatility = daily_returns.std() * np.sqrt(252)

    return {
        "total_return": total_return,
        "annualized_return": annualized_return,
        "volatility": volatility
    }

def generate_metrics_table(df: pd.DataFrame, reference_date):
    \"\"\"
    Generate a table of key metrics for each period in PERIODS (10Y, 5Y, etc.).
    \"\"\"
    results = {}
    end_date = df.index.max()
    
    for label, years in PERIODS.items():
        start_date = end_date - pd.DateOffset(years=years)
        metrics_dict = metrics_for_period(df, start_date, end_date)

        # Break down the dict into columns for each ticker
        total_returns = metrics_dict["total_return"]
        ann_returns = metrics_dict["annualized_return"]
        vols = metrics_dict["volatility"]

        combined_df = pd.DataFrame({
            "Total Return": total_returns,
            "Annualized Return": ann_returns,
            "Volatility": vols
        })
        results[label] = combined_df
    
    return results
""",
    "plots.py": """\"\"\"
plots.py

Generate the required plots: rolling correlation, relative performance,
cumulative performance, and correlation heatmaps.
\"\"\"

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from config import SP500_TICKER, SECTOR_ETFS, PERIODS
from calculations import calculate_daily_returns

def plot_rolling_correlation(rolling_corr: pd.DataFrame):
    \"\"\"
    Plot the rolling correlation of each ticker vs the S&P 500.
    \"\"\"
    plt.figure(figsize=(12, 8))
    for col in rolling_corr.columns:
        if col != SP500_TICKER:
            plt.plot(rolling_corr.index, rolling_corr[col], label=col)
    plt.title("Rolling Correlation with S&P 500")
    plt.xlabel("Date")
    plt.ylabel("Correlation")
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_relative_performance(relative_perf: pd.DataFrame):
    \"\"\"
    Plot the ratio of each ticker's price to the S&P 500 (relative performance).
    \"\"\"
    plt.figure(figsize=(12, 8))
    for col in relative_perf.columns:
        if col != SP500_TICKER:
            plt.plot(relative_perf.index, relative_perf[col], label=col)
    plt.title("Relative Performance vs. S&P 500")
    plt.xlabel("Date")
    plt.ylabel("Relative Performance")
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_cumulative_performance(cum_returns: pd.DataFrame):
    \"\"\"
    Plot cumulative performance for each ticker.
    \"\"\"
    plt.figure(figsize=(12, 8))
    for col in cum_returns.columns:
        plt.plot(cum_returns.index, cum_returns[col], label=col)
    plt.title("Cumulative Returns")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_correlation_heatmap(df: pd.DataFrame, label=""):
    \"\"\"
    Create a correlation heatmap for a given DataFrame slice.
    \"\"\"
    corr = df.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap="RdYlGn", fmt=".2f")
    plt.title(f"Correlation Heatmap {label}")
    plt.tight_layout()
    plt.show()

def plot_period_correlation_heatmaps(df: pd.DataFrame):
    \"\"\"
    Plot correlation heatmaps for each period (10Y, 5Y, 3Y, 1Y).
    \"\"\"
    end_date = df.index.max()
    for label, years in PERIODS.items():
        start_date = end_date - pd.DateOffset(years=years)
        sliced_df = df.loc[start_date:end_date]
        
        # We'll use daily returns for correlation
        returns_slice = calculate_daily_returns(sliced_df)
        plot_correlation_heatmap(returns_slice, label)
""",
    "main.py": """\"\"\"
main.py

Orchestrates the entire workflow:
- Fetch data
- Validate, process, and compute metrics
- Plot results
\"\"\"

import pandas as pd
from config import SP500_TICKER, END_DATE
from data_import import fetch_data
from data_validation import validate_data
from data_processing import process_data
from calculations import (
    calculate_daily_returns, 
    calculate_rolling_correlation,
    calculate_relative_performance,
    calculate_cumulative_returns,
    generate_metrics_table
)
from plots import (
    plot_rolling_correlation,
    plot_relative_performance,
    plot_cumulative_performance,
    plot_period_correlation_heatmaps
)

def main():
    # 1. Fetch the data
    raw_data = fetch_data()

    # 2. Validate the data
    validated_data = validate_data(raw_data)

    # 3. Process the data
    processed_data = process_data(validated_data)

    # 4. Perform calculations
    daily_returns = calculate_daily_returns(processed_data)
    
    # Rolling correlation vs. S&P 500
    rolling_corr = calculate_rolling_correlation(daily_returns, SP500_TICKER)
    
    # Relative performance vs. S&P 500
    relative_perf = calculate_relative_performance(processed_data, SP500_TICKER)
    
    # Cumulative performance
    cumulative_ret = calculate_cumulative_returns(daily_returns)
    
    # Generate metrics for different periods
    metrics_tables = generate_metrics_table(processed_data, END_DATE)
    for period_label, df_metrics in metrics_tables.items():
        print(f"\\n=== Metrics for {period_label} ===")
        print(df_metrics)
    
    # 5. Plot the results
    plot_rolling_correlation(rolling_corr)
    plot_relative_performance(relative_perf)
    plot_cumulative_performance(cumulative_ret)
    plot_period_correlation_heatmaps(processed_data)

if __name__ == "__main__":
    main()
"""
}

def create_project_structure():
    # Create main project directory
    os.makedirs(PROJECT_NAME, exist_ok=True)
    for filename, content in files_content.items():
        file_path = os.path.join(PROJECT_NAME, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
    print(f"Project '{PROJECT_NAME}' created with all script files.")

if __name__ == "__main__":
    create_project_structure()
