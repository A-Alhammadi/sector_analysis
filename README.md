# Sector Analysis Program

## Overview

This program analyzes sector ETFs, the S&P 500, and the VIX, fetching 10+ years of data from Yahoo Finance. It computes metrics like total return, annualized return, Sharpe Ratio, Sortino Ratio, and relative return vs. the S&P 500. The program generates:

- **Excel file**: Metrics sorted by various criteria.
- **Plots**: Rolling correlations, relative performance, cumulative returns, and correlation heatmaps.

Results are saved in a timestamped folder under `results`.

---

## Configurations

You can customize the program by editing `config.py`:

- **Sector ETFs**: Add or remove ETFs in the `SECTOR_ETFS` list.
  ```python
  SECTOR_ETFS = [
      "XLY",  # Consumer Discretionary
      "XLP",  # Consumer Staples
      "XLE",  # Energy
      "XLF",  # Financials
      "XLV",  # Health Care
      "XLI",  # Industrials
      "XLB",  # Materials
      "XLK",  # Technology
      "XLC",  # Communication Services
      "XLRE", # Real Estate
      "XLU"   # Utilities
  ]
  ```
- **Date Range**: Adjust `START_DATE_10YR` for a different start date.
  ```python
  START_DATE_10YR = "2013-01-01"
  ```
- **Rolling Window**: Change `ROLLING_WINDOW` to modify correlation granularity.
  ```python
  ROLLING_WINDOW = 60  # Days
  ```
- **Metric Periods**: Modify the `PERIODS` dictionary to adjust analysis periods.
  ```python
  PERIODS = {
      "10Y": 10,
      "5Y": 5,
      "3Y": 3,
      "1Y": 1,
  }
  ```

---

## Requirements

Install the required libraries:

```bash
pip install yfinance pandas matplotlib seaborn openpyxl
```

---

## How to Run

Run the program with:

```bash
python main.py
```

Results (metrics and plots) will be saved in the `results` folder.

