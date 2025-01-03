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

def calculate_sharpe_ratio(annualized_returns: pd.Series, volatilities: pd.Series) -> pd.Series:
    """
    Sharpe ratio = Annualized Return / Annualized Volatility
    """
    return annualized_returns / volatilities

def calculate_sortino_ratio(annualized_returns: pd.Series, daily_returns: pd.DataFrame) -> pd.Series:
    """
    Sortino Ratio = (Annualized Return - risk_free_rate) / DownsideDeviation
    For simplicity, assume risk_free_rate = 0
    DownsideDeviation is std dev of negative returns (annualized).
    """
    # We'll approximate annualization factor with sqrt(252)
    sortino_ratios = {}
    for ticker in daily_returns.columns:
        neg_returns = daily_returns[ticker][daily_returns[ticker] < 0]
        downside_std = neg_returns.std() * (252 ** 0.5)
        if downside_std == 0:
            sortino_ratios[ticker] = np.nan
        else:
            sortino_ratios[ticker] = annualized_returns[ticker] / downside_std
    return pd.Series(sortino_ratios)

def calculate_relative_return(df: pd.DataFrame, sp500_col=SP500_TICKER) -> pd.Series:
    """
    Calculate total return relative to the S&P 500: (ETF total return) - (SP500 total return).
    """
    total_ret = (df.iloc[-1] / df.iloc[0]) - 1
    sp500_return = total_ret[sp500_col]
    return total_ret - sp500_return

def metrics_for_period(df: pd.DataFrame, start_date, end_date):
    """
    Calculate key metrics (total return, annualized return, volatility, Sharpe, Sortino, relative return) over a date range.
    """
    sliced = df.loc[start_date:end_date]
    if sliced.empty:
        return {
            "total_return": np.nan,
            "annualized_return": np.nan,
            "volatility": np.nan,
            "sharpe_ratio": np.nan,
            "sortino_ratio": np.nan,
            "relative_return": np.nan
        }
    daily_prices = sliced
    daily_returns = daily_prices.pct_change().dropna()

    # Total return
    total_return = (daily_prices.iloc[-1] / daily_prices.iloc[0]) - 1

    # Annualized return (approx. 252 trading days)
    ann_return = (1 + total_return) ** (252 / len(daily_prices)) - 1

    # Volatility (std dev of daily returns * sqrt(252))
    volatility = daily_returns.std() * np.sqrt(252)

    # Sharpe ratio
    sharpe = calculate_sharpe_ratio(ann_return, volatility)

    # Sortino ratio
    sortino = calculate_sortino_ratio(ann_return, daily_returns)

    # Relative return (vs S&P 500)
    relative_ret = calculate_relative_return(daily_prices)

    return {
        "total_return": total_return,
        "annualized_return": ann_return,
        "volatility": volatility,
        "sharpe_ratio": sharpe,
        "sortino_ratio": sortino,
        "relative_return": relative_ret
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
        metrics_df = pd.DataFrame({
            "Total Return": metrics_dict["total_return"],
            "Annualized Return": metrics_dict["annualized_return"],
            "Volatility": metrics_dict["volatility"],
            "Sharpe Ratio": metrics_dict["sharpe_ratio"],
            "Sortino Ratio": metrics_dict["sortino_ratio"],
            "Relative Return vs SP500": metrics_dict["relative_return"]
        })
        results[label] = metrics_df
    
    return results
