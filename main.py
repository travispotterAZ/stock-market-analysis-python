# main.py
# ─────────────────────────────────────────────
# Entry point — run this file to execute the full pipeline:
#   1. Download (or load cached) stock data
#   2. Run analysis
#   3. Generate all charts
#
# Usage:
#   python main.py            # uses cached CSVs if they exist
#   python main.py --refresh  # re-downloads data from Yahoo Finance
# ─────────────────────────────────────────────

import os
import sys

from config import CLOSE_CSV, RETURNS_CSV, TICKERS, START_DATE, END_DATE

from data_sourcing import (
    download_close_prices,
    compute_daily_returns,
    save_data,
    load_close_prices,
    load_daily_returns,
)
from analysis import (
    print_summary_statistics,
    print_top_days,
    compute_cumulative_returns,
    compute_rolling_volatility,
)
from visualization import (
    plot_all_prices,
    plot_individual_prices,
    plot_all_returns,
    plot_individual_returns,
    plot_return_histograms,
    plot_correlation_heatmap,
)


def run(refresh: bool = False) -> None:
    """
    Full analysis pipeline.

    Args:
        refresh: If True, re-download data even if CSVs already exist.
    """

    # ── Step 1: Data ──────────────────────────────────────────────────────────
    data_exists = os.path.exists(CLOSE_CSV) and os.path.exists(RETURNS_CSV)

    if refresh or not data_exists:
        print(f"\n[1/3] Downloading data for: {TICKERS}  ({START_DATE} → {END_DATE})")
        prices  = download_close_prices(TICKERS, START_DATE, END_DATE)
        returns = compute_daily_returns(prices)
        save_data(prices,  CLOSE_CSV)
        save_data(returns, RETURNS_CSV)
    else:
        print(f"\n[1/3] Loading cached data from CSV  (run with --refresh to re-download)")
        prices  = load_close_prices()
        returns = load_daily_returns()

    # ── Step 2: Analysis ──────────────────────────────────────────────────────
    print("\n[2/3] Running analysis")

    print_summary_statistics(returns)
    print_top_days(returns, n=3)

    cum_returns = compute_cumulative_returns(returns)
    print("Cumulative return over the full period:")
    print(cum_returns.iloc[-1].map("{:.2%}".format))
    print()

    # ── Step 3: Visualization ─────────────────────────────────────────────────
    print("[3/3] Generating charts  (close each window to continue)\n")

    plot_all_prices(prices)
    plot_individual_prices(prices)
    plot_all_returns(returns)
    plot_individual_returns(returns)
    plot_return_histograms(returns)
    plot_correlation_heatmap(returns)

    print("\nDone! Charts saved to the 'outputs/' folder.")


if __name__ == "__main__":
    refresh_flag = "--refresh" in sys.argv
    run(refresh=refresh_flag)
