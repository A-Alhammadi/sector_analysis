"""
plots.py

Generate the required plots: rolling correlation, relative performance,
cumulative performance, and correlation heatmaps.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from config import SP500_TICKER, SECTOR_ETFS, PERIODS
from calculations import calculate_daily_returns

def plot_rolling_correlation(rolling_corr: pd.DataFrame):
    """
    Plot the rolling correlation of each ticker vs the S&P 500.
    """
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
    """
    Plot the ratio of each ticker's price to the S&P 500 (relative performance).
    """
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
    """
    Plot cumulative performance for each ticker.
    """
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
    """
    Create a correlation heatmap for a given DataFrame slice.
    """
    corr = df.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap="RdYlGn", fmt=".2f")
    plt.title(f"Correlation Heatmap {label}")
    plt.tight_layout()
    plt.show()

def plot_period_correlation_heatmaps(df: pd.DataFrame):
    """
    Plot correlation heatmaps for each period (10Y, 5Y, 3Y, 1Y).
    """
    end_date = df.index.max()
    for label, years in PERIODS.items():
        start_date = end_date - pd.DateOffset(years=years)
        sliced_df = df.loc[start_date:end_date]
        
        # We'll use daily returns for correlation
        returns_slice = calculate_daily_returns(sliced_df)
        plot_correlation_heatmap(returns_slice, label)
