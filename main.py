"""
main.py

Orchestrates the entire workflow:
- Fetch data
- Validate, process, and compute metrics
- Plot results
- Save results (CSV and images) in a timestamped folder
"""

import os
import pandas as pd
from datetime import datetime
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
import matplotlib.pyplot as plt


def create_results_folder():
    """
    Creates a timestamped folder inside the 'results' directory.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    results_dir = os.path.join("results", timestamp)
    os.makedirs(results_dir, exist_ok=True)
    return results_dir


def main():
    # Create results folder
    results_dir = create_results_folder()
    print(f"Results will be saved in: {results_dir}")

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
    
    # Print metrics for each period
    for period_label, df_metrics in metrics_tables.items():
        print(f"\n=== Metrics for {period_label} ===")
        print(df_metrics)

    # 5. Export sorted metrics to CSV file in the results folder
    if "10Y" in metrics_tables:
        df_10y = metrics_tables["10Y"].copy()

        # Create sorted DataFrames
        sort_by_total_return = df_10y.sort_values(by="Total Return", ascending=False)
        sort_by_annualized_return = df_10y.sort_values(by="Annualized Return", ascending=False)
        sort_by_sharpe = df_10y.sort_values(by="Sharpe Ratio", ascending=False)  # Volatility-adjusted return
        sort_by_sortino = df_10y.sort_values(by="Sortino Ratio", ascending=False)  # Downside risk-adjusted return
        sort_by_relative_return = df_10y.sort_values(by="Relative Return vs SP500", ascending=False)

        # Save to a single CSV file with multiple sheets (requires pandas >= 1.4.0)
        output_csv_path = os.path.join(results_dir, "metrics_sorts.xlsx")
        with pd.ExcelWriter(output_csv_path) as writer:
            sort_by_total_return.to_excel(writer, sheet_name="Sorted by Total Return")
            sort_by_annualized_return.to_excel(writer, sheet_name="Sorted by Annual Return")
            sort_by_sharpe.to_excel(writer, sheet_name="Sorted by Sharpe")
            sort_by_sortino.to_excel(writer, sheet_name="Sorted by Sortino")
            sort_by_relative_return.to_excel(writer, sheet_name="Sorted by Relative")

        print(f"\nExported sorted metrics (10Y) to: {output_csv_path}")
    else:
        print("\nNo 10Y metrics found to export.")

        # 6. Save plots in the results folder
    plt.figure(figsize=(12, 8))
    plot_rolling_correlation(rolling_corr)
    plt.savefig(os.path.join(results_dir, "rolling_correlation.png"))
    plt.close()

    plt.figure(figsize=(12, 8))
    plot_relative_performance(relative_perf)
    plt.savefig(os.path.join(results_dir, "relative_performance.png"))
    plt.close()

    plt.figure(figsize=(12, 8))
    plot_cumulative_performance(cumulative_ret)
    plt.savefig(os.path.join(results_dir, "cumulative_performance.png"))
    plt.close()

    # Save individual heatmaps for each period
    plot_period_correlation_heatmaps(processed_data, save_dir=results_dir)

    print(f"All plots have been saved in: {results_dir}")

if __name__ == "__main__":
    main()
