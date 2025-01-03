"""
config.py

Central configuration for tickers, date ranges, and global parameters.
"""

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

SECTOR_NAMES = {
    "XLY": "Consumer Discretionary",
    "XLP": "Consumer Staples",
    "XLE": "Energy",
    "XLF": "Financials",
    "XLV": "Health Care",
    "XLI": "Industrials",
    "XLB": "Materials",
    "XLK": "Technology",
    "XLC": "Communication Services",
    "XLRE": "Real Estate",
    "XLU": "Utilities",
}

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
