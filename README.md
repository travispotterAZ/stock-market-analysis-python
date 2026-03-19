# Stock Market Analysis

A Python project for downloading, analyzing, and visualizing historical stock data using Yahoo Finance.


---

## What it does

- Downloads daily closing prices for any set of tickers from Yahoo Finance
- Computes daily percentage returns
- Generates several charts (price history, return history, histograms, correlation heatmap)
- Prints summary statistics and highlights the best/worst trading days

---

## Project structure

```
stock-market-analysis/
│
├── main.py            # Entry point — run this to execute the full pipeline
├── config.py          # All settings in one place (tickers, dates, file paths)
├── data_sourcing.py   # Download data from Yahoo Finance and save/load CSVs
├── analysis.py        # Summary stats, cumulative returns, rolling volatility
├── visualization.py   # All chart/plot functions
│
├── data/              # Auto-created — holds the downloaded CSV files
│   ├── market_close.csv
│   └── daily_returns.csv
│
├── outputs/           # Auto-created — saved chart images (PNG)
│
├── requirements.txt
└── README.md
```

---

## Running the project

**Full pipeline (download + analyze + visualize):**

```bash
python main.py
```

On first run this downloads data from Yahoo Finance and caches it to `data/`. Subsequent runs load from the CSVs so it's fast and offline.

**Force a fresh download:**

```bash
python main.py --refresh
```

---

## Configuration

Open `config.py` to change:

| Setting | Default | Description |
|---|---|---|
| `TICKERS` | `["GOOGL", "AMZN"]` | List of Yahoo Finance ticker symbols |
| `START_DATE` | `"2024-01-01"` | Start of the analysis period |
| `END_DATE` | `"2024-09-01"` | End of the analysis period |
| `OUTPUT_DIR` | `"outputs"` | Where chart PNGs are saved |
| `DOWNLOAD_DELAY_SECS` | `2` | Pause between API calls (avoids rate limits) |

**Example — adding more tickers:**

```python
# config.py
TICKERS = ["GOOGL", "AMZN", "TSLA", "GS"]
```

**Finding ticker symbols:**  
Search for any company on [finance.yahoo.com](https://finance.yahoo.com) — the symbol shown in the URL/header is what you pass in. Indices use a `^` prefix (e.g. `^GDAXI` for the German DAX).

---

## Charts produced

| Chart | Description |
|---|---|
| All prices | All tickers on one chart — good for spotting overall trends |
| Individual prices | One chart per ticker — better for stocks with very different price scales |
| All returns | All daily returns overlaid — helps spot correlation between stocks |
| Individual returns | One chart per ticker, with a zero-reference line |
| Return histograms | Distribution of returns — are they bell-shaped? Are there fat tails? |
| Correlation heatmap | Pairwise correlation between all stocks (1.0 = move together, 0 = independent) |

---

## Key concepts

**Closing price** — The price of a stock at market close (4 PM ET). This is the standard reference price used in most financial analysis.

**Daily return** — The percentage change in closing price from one day to the next. Calculated as `(today - yesterday) / yesterday`. A return of `0.02` means the stock gained 2% that day.

**Cumulative return** — Total return over the entire period. Accounts for compounding: a 1% gain followed by a 1% loss is not zero (it's actually −0.01%).

**Rolling volatility** — Standard deviation of returns over a sliding window (default: 30 days). Higher volatility = more day-to-day price swings = more risk.

---

## Dependencies

| Library | Purpose |
|---|---|
| `yfinance` | Download historical data from Yahoo Finance |
| `pandas` | Store and manipulate data in tabular form (DataFrames) |
| `matplotlib` | Generate charts and plots |

---

## Possible extensions

- Add a `--tickers` command-line argument so you don't have to edit `config.py`
- Export a PDF report combining stats and charts
- Add a moving average overlay to the price charts
- Compare performance vs. the S&P 500 (`^GSPC`)
