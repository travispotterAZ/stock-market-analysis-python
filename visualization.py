# visualization.py
# ─────────────────────────────────────────────
# All charting functions live here.
# Each function creates one (or a group of) plot(s).
# ─────────────────────────────────────────────

import os
import matplotlib.pyplot as plt
import pandas as pd

from config import OUTPUT_DIR


# ── Helpers ───────────────────────────────────────────────────────────────────

def _save_or_show(fig: plt.Figure, filename: str | None = None) -> None:
    """
    If OUTPUT_DIR is set and a filename is given, save the figure there.
    Otherwise (or additionally) call plt.show() so it pops up on screen.
    """
    if OUTPUT_DIR and filename:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        path = os.path.join(OUTPUT_DIR, filename)
        fig.savefig(path, bbox_inches="tight")
        print(f"  Saved chart → {path}")

    plt.show()
    plt.close(fig)


def _apply_common_labels(ax: plt.Axes, title: str, xlabel: str, ylabel: str) -> None:
    """Reusable label setter so we're not repeating ourselves."""
    ax.set_title(title, fontweight="bold")
    ax.set_xlabel(xlabel, fontweight="bold")
    ax.set_ylabel(ylabel, fontweight="bold")


# ── Chart functions ───────────────────────────────────────────────────────────

def plot_all_prices(close_prices: pd.DataFrame) -> None:
    """
    Single chart showing every ticker's closing price over time.
    Good for a quick side-by-side comparison.
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(close_prices, label=close_prices.columns.tolist())
    _apply_common_labels(ax, "All Stock Prices Over Time", "Date", "Price (USD)")
    ax.legend(title="Securities")
    _save_or_show(fig, "all_prices.png")


def plot_individual_prices(close_prices: pd.DataFrame) -> None:
    """
    One chart per ticker so price differences in scale don't squash smaller stocks.
    """
    for ticker in close_prices.columns:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(close_prices[ticker], color="steelblue")
        _apply_common_labels(ax, f"{ticker} — Daily Closing Price", "Date", "Price (USD)")
        _save_or_show(fig, f"price_{ticker}.png")


def plot_all_returns(daily_returns: pd.DataFrame) -> None:
    """
    All tickers' daily returns on a single chart.
    Helps spot whether they tend to move together (correlation).
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    for ticker in daily_returns.columns:
        ax.plot(daily_returns[ticker], label=ticker, alpha=0.8)
    _apply_common_labels(ax, "All Daily Returns Over Time", "Date", "Return")
    ax.axhline(0, color="black", linewidth=0.8, linestyle="--")   # zero line for reference
    ax.legend(title="Securities")
    _save_or_show(fig, "all_returns.png")


def plot_individual_returns(daily_returns: pd.DataFrame) -> None:
    """
    One chart per ticker for daily returns.
    The horizontal zero-line makes it easier to see positive vs negative days.
    """
    for ticker in daily_returns.columns:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(daily_returns[ticker], color="darkorange")
        ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
        _apply_common_labels(ax, f"{ticker} — Daily Returns", "Date", "Return")
        _save_or_show(fig, f"returns_{ticker}.png")


def plot_return_histograms(daily_returns: pd.DataFrame) -> None:
    """
    Histogram of daily returns per ticker.
    Shows the distribution — e.g. is it roughly bell-shaped? Are there fat tails?
    50 bins gives a good balance between detail and readability.
    """
    n = len(daily_returns.columns)
    fig, axes = plt.subplots(1, n, figsize=(7 * n, 5))

    # If there's only one ticker, axes won't be a list — wrap it so the loop works
    if n == 1:
        axes = [axes]

    for ax, ticker in zip(axes, daily_returns.columns):
        ax.hist(daily_returns[ticker], bins=50, color="mediumseagreen", edgecolor="white")
        _apply_common_labels(ax, f"{ticker} Return Distribution", "Daily Return", "Frequency")

    fig.suptitle("Histograms of Daily Returns", fontweight="bold", fontsize=14)
    plt.tight_layout()
    _save_or_show(fig, "return_histograms.png")


def plot_correlation_heatmap(daily_returns: pd.DataFrame) -> None:
    """
    Heatmap of pairwise return correlations.
    Values close to 1.0 mean the stocks move together; close to 0 means they're independent.
    Only shows up when there are at least 2 tickers — skipped otherwise.
    """
    if len(daily_returns.columns) < 2:
        print("  Skipping correlation heatmap (need at least 2 tickers).")
        return

    corr = daily_returns.corr()
    fig, ax = plt.subplots(figsize=(6, 5))

    # Draw the grid manually (no seaborn dependency)
    im = ax.imshow(corr, vmin=-1, vmax=1, cmap="coolwarm")
    fig.colorbar(im, ax=ax)

    tickers = corr.columns.tolist()
    ax.set_xticks(range(len(tickers)))
    ax.set_yticks(range(len(tickers)))
    ax.set_xticklabels(tickers)
    ax.set_yticklabels(tickers)

    # Annotate each cell with the correlation value
    for i in range(len(tickers)):
        for j in range(len(tickers)):
            ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", fontsize=12)

    ax.set_title("Return Correlation Heatmap", fontweight="bold")
    plt.tight_layout()
    _save_or_show(fig, "correlation_heatmap.png")


# ── Run directly to preview all charts ───────────────────────────────────────
if __name__ == "__main__":
    from data_sourcing import load_close_prices, load_daily_returns

    print("Loading saved data…")
    prices  = load_close_prices()
    returns = load_daily_returns()

    print("Generating all charts…")
    plot_all_prices(prices)
    plot_individual_prices(prices)
    plot_all_returns(returns)
    plot_individual_returns(returns)
    plot_return_histograms(returns)
    plot_correlation_heatmap(returns)
