# config.py
# ─────────────────────────────────────────────
# Central place for all project settings.
# Change things here instead of hunting through every file.
# ─────────────────────────────────────────────

# Stocks to analyze (Yahoo Finance ticker symbols)
# Examples: "TSLA", "GS", "^GDAXI" (DAX index), "BNDX" (Bloomberg Bond ETF)
TICKERS = ["GOOGL", "AMZN"]

# Date range for historical data
START_DATE = "2024-01-01"   # Chosen after COVID-19 volatility settled
END_DATE   = "2024-09-01"   # Chosen before U.S. Presidential Election volatility

# File paths
DATA_DIR              = "data"
CLOSE_CSV             = f"{DATA_DIR}/market_close.csv"
RETURNS_CSV           = f"{DATA_DIR}/daily_returns.csv"

# Download settings
DOWNLOAD_DELAY_SECS = 2     # Pause between yfinance requests to avoid rate limits

# Chart output directory (set to None to just show charts, don't save them)
OUTPUT_DIR = "outputs"
