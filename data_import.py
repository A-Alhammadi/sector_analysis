"""
data_import.py

Fetch raw data from Yahoo Finance using yfinance.
"""

import yfinance as yf
import pandas as pd
from config import ALL_TICKERS, START_DATE_10YR, END_DATE

def fetch_data(tickers=None, start=None, end=None):
    """
    Fetches daily adjusted close data from Yahoo Finance for the given tickers.
    """
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
