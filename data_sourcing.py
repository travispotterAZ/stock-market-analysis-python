# data_sourcing.py
# ─────────────────────────────────────────────
# Responsible for fetching stock data from Yahoo Finance
# and saving it locally as CSV files.
# ─────────────────────────────────────────────

import time
import os
import pandas as pd
import yfinance as yf

from config import (
    TICKERS,
    START_DATE,
    END_DATE,
    CLOSE_CSV,
    RETURNS_CSV,
    DOWNLOAD_DELAY_SECS,
    DATA_DIR,
)


def download_close_prices(tickers: list[str], start: str, end: str) -> pd.DataFrame:
    """
    Download daily closing prices for each ticker from Yahoo Finance.

    Args:
        tickers: List of ticker symbols, e.g. ["GOOGL", "AMZN"].
        start:   Start date string, e.g. "2024-01-01".
        end:     End date string,   e.g. "2024-09-01".

    Returns:
        A DataFrame where each column is one ticker and each row is a trading day.
    """
    frames = []

    for ticker in tickers:
        try:
            df = yf.download(ticker, start=start, end=end)["Close"]
            df.name = ticker
            frames.append(df)
            print(f"  ✓ Downloaded {ticker}")
        except Exception as e:
            print(f"  ✗ Failed to download {ticker}: {e}")

        # Be polite to the API — wait a couple seconds between requests
        time.sleep(DOWNLOAD_DELAY_SECS)

    if not frames:
        raise ValueError("No data was downloaded. Check your tickers and internet connection.")

    combined = pd.concat(frames, axis=1)
    print(f"\nDownloaded data shape: {combined.shape}  ({combined.shape[0]} trading days)")
    return combined


def compute_daily_returns(close_prices: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the day-over-day percentage change in closing price.

    A positive return means the stock went up that day; negative means it fell.
    The first row is dropped because there's no previous day to compare against.

    Args:
        close_prices: DataFrame of closing prices (output of download_close_prices).

    Returns:
        DataFrame of daily returns as decimals (e.g. 0.02 = +2%).
    """
    return close_prices.pct_change(fill_method=None).dropna()


def save_data(df: pd.DataFrame, filepath: str) -> None:
    """Save a DataFrame to CSV, creating the directory if needed."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath)
    print(f"  Saved → {filepath}")


def load_close_prices(filepath: str = CLOSE_CSV) -> pd.DataFrame:
    """
    Load closing prices from a saved CSV.

    Using index_col=0 keeps the Date column as the index,
    and parse_dates=True lets pandas treat it as real dates
    so plotting works correctly on the x-axis.
    """
    return pd.read_csv(filepath, index_col=0, parse_dates=True)


def load_daily_returns(filepath: str = RETURNS_CSV) -> pd.DataFrame:
    """Load daily returns from a saved CSV."""
    return pd.read_csv(filepath, index_col=0, parse_dates=True)


# ── Run directly to (re)download fresh data ──────────────────────────────────
if __name__ == "__main__":
    print("=== Downloading stock data ===")
    prices  = download_close_prices(TICKERS, START_DATE, END_DATE)
    returns = compute_daily_returns(prices)

    print("\n=== Saving to CSV ===")
    save_data(prices,  CLOSE_CSV)
    save_data(returns, RETURNS_CSV)

    print("\nFirst 5 rows of closing prices:")
    print(prices.head())
    print("\nFirst 5 rows of daily returns:")
    print(returns.head())
