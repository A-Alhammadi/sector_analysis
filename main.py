"""
main.py

Orchestrates the entire workflow:
- Fetch data
- Validate, process, and compute metrics
- Plot results
"""

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
        print(f"\n=== Metrics for {period_label} ===")
        print(df_metrics)
    
    # 5. Plot the results
    plot_rolling_correlation(rolling_corr)
    plot_relative_performance(relative_perf)
    plot_cumulative_performance(cumulative_ret)
    plot_period_correlation_heatmaps(processed_data)

if __name__ == "__main__":
    main()
