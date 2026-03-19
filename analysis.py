# analysis.py
# ─────────────────────────────────────────────
# Summary statistics and basic analytical functions.
# Nothing is printed automatically — call the functions
# you want from main.py (or a notebook).
# ─────────────────────────────────────────────

import pandas as pd


def print_summary_statistics(daily_returns: pd.DataFrame) -> None:
    """
    Print descriptive statistics for daily returns.

    Includes count, mean, std deviation, min/max, and quartiles.
    Numbers are shown in scientific notation so they line up neatly
    (returns are small decimals like 0.002, so 2e-3 is easier to scan).
    """
    pd.set_option("display.float_format", "{:.4f}".format)

    print("=" * 50)
    print("  SUMMARY STATISTICS — Daily Returns")
    print("=" * 50)
    print(daily_returns.describe())
    print()


def print_top_days(daily_returns: pd.DataFrame, n: int = 5) -> None:
    """
    Print the best and worst single trading days for each ticker.

    Args:
        daily_returns: DataFrame of daily returns.
        n:             How many top/bottom days to show (default 5).
    """
    for ticker in daily_returns.columns:
        series = daily_returns[ticker].sort_values()

        print(f"── {ticker} ──")
        print(f"  Worst {n} days:")
        for date, val in series.head(n).items():
            print(f"    {date.date()}  {val:+.2%}")

        print(f"  Best {n} days:")
        for date, val in series.tail(n).sort_values(ascending=False).items():
            print(f"    {date.date()}  {val:+.2%}")
        print()


def compute_rolling_volatility(daily_returns: pd.DataFrame, window: int = 30) -> pd.DataFrame:
    """
    Calculate rolling standard deviation of returns (a simple volatility estimate).

    A 30-day window is common — it smooths out noise while still reacting
    to changing market conditions within a few weeks.

    Args:
        daily_returns: DataFrame of daily returns.
        window:        Rolling window size in trading days (default 30).

    Returns:
        DataFrame of rolling volatility values (same shape as input, NaN for the first window-1 rows).
    """
    return daily_returns.rolling(window=window).std()


def compute_cumulative_returns(daily_returns: pd.DataFrame) -> pd.DataFrame:
    """
    Convert daily returns into cumulative returns from the start of the period.

    Formula: cumulative = (1 + r1) * (1 + r2) * … - 1

    This tells you: "If I invested $1 at the start, what is it worth now?"
    A value of 0.15 means +15% total gain over the whole period.

    Args:
        daily_returns: DataFrame of daily returns.

    Returns:
        DataFrame of cumulative returns.
    """
    return (1 + daily_returns).cumprod() - 1


# ── Run directly to see a quick report ───────────────────────────────────────
if __name__ == "__main__":
    from data_sourcing import load_daily_returns

    returns = load_daily_returns()

    print_summary_statistics(returns)
    print_top_days(returns)

    cum = compute_cumulative_returns(returns)
    print("Cumulative return over the full period:")
    print(cum.iloc[-1].map("{:.2%}".format))
