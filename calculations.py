"""
calculations.py

Core financial calculations: rolling correlations, performance, metrics, etc.
"""

import pandas as pd
import numpy as np
from config import SP500_TICKER, PERIODS, ROLLING_WINDOW

def calculate_daily_returns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate daily percentage returns for each column.
    """
    return df.pct_change().fillna(0)

def calculate_rolling_correlation(df_returns: pd.DataFrame, benchmark=SP500_TICKER, window=ROLLING_WINDOW) -> pd.DataFrame:
    """
    Calculate rolling correlation of each ticker vs a benchmark (S&P 500).
    """
    benchmark_returns = df_returns[benchmark]
    rolling_corr = df_returns.apply(lambda x: x.rolling(window).corr(benchmark_returns))
    return rolling_corr

def calculate_relative_performance(df: pd.DataFrame, benchmark=SP500_TICKER):
    """
    Calculate the ratio of each ticker's price to the benchmark's price.
    """
    return df.div(df[benchmark], axis=0)

def calculate_cumulative_returns(df_returns: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate cumulative returns from daily returns.
    """
    # (1 + r).cumprod() - 1 for each ticker
    cumulative = (1 + df_returns).cumprod() - 1
    return cumulative

def metrics_for_period(df: pd.DataFrame, start_date, end_date):
    """
    Calculate key metrics (total return, annualized return, volatility) over a date range.
    """
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
    """
    Generate a table of key metrics for each period in PERIODS (10Y, 5Y, etc.).
    """
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
