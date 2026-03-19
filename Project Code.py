import yfinance as yf              # Data Source
import pandas as pd                # Data Manioulator & Analyzer
import matplotlib.pyplot as plt    # Data Visualization
import time                        # Used to slow down ticker request
#importing library as shorter terms makes for a more 

#↓↓↓Needed Securities tickers: (Google, Amazon, Tesla, Goldman Sachs, DAX index (German Market),  Bloomberg Bond Index
stock_ticker = ["GOOGL", "AMZN"] #,"TSLA", "GS", "^GDAXI", "BNDX"] 

#↓↓↓Data Source Time Range↓↓↓
start_date = "2024-01-01" #Starts after volatility due to COVID-19
end_date = "2024-09-01" #Ends before volatility due to U.S. Presidential Election Race

#↓↓↓Dowloads Data↓↓↓
#data = yf.download(stock_ticker, start=start_date, end=end_date)["Close"]
dfs = []
for t in stock_ticker:
    try:
        df = yf.download(t, start=start_date, end=end_date)["Close"]
        df.name = t
        dfs.append(df)
        print(f"Downloaded {t}")
    except Exception as e:
        print(f"Failed {t}: {e}")
    time.sleep(2)  # wait 2 seconds between calls
data = pd.concat(dfs, axis=1)
print("Final data shape:", data.shape)
print(data.head())
print(data.tail())

"""
This line accesses the yfinance database, assigning the variable 'data' with a pandas DataFrame containing the specified 'Close' value.
The Close value of a ticker is the price at market close for the day. A pandas DataFrame is similar to an excel sheet where:
(1) Rows represent trading days
(2) Columns correspond to a Close value
Tickers are specified in list 'stock_tickers'
Trading Days are specified in Data Source Time range defintions.
"""

#↓↓↓Save to CSV↓↓↓
data.to_csv("market_close.csv") #Final ticket dollar price USD. 
"""
This line will utlize the pandas library to save the pandas DataFrame, contained by variable 'data', as a CSV file 
(i.e. comma seperated values) named "market_close.csv" 
The CSV will be formatted as:
                                Date, TICKER
                                YYYY-MM-DD, PRICE
"""

#↓↓↓Read the data from CSV↓↓↓
data = pd.read_csv("market_close.csv", index_col=0, parse_dates=True)
"""
This line will utilize the pandas library to read the data contained on a CSV file back to a pandas DataFrame. This way the data can be
analyzed with the pandas library further. In this line, pandas is told to read the file "market_close.csv", index_col tells pandas to use
the first column (i.e Date) as the index for the data, and parse_dates=True tells pandas to identify strings that are dates to be treated as
'datetime' objects which permits the ability of plotting time series. 
"""

#↓↓↓Compute daily returns↓↓↓
daily_returns = data.pct_change(fill_method=None).dropna()
daily_returns.to_csv("daily_returns.csv")
"""
HUH?
CSV file is created to hold the dail returns data acquired from pct_change funtion applied to market_close (i.e. the csv file holding the
daily closing value of each ticket). The pct_change calculates the signed percentage changed of closing value from day to day.
"""

#↓↓↓Visualizations↓↓↓

#Daily Price Chart (Jan 1, 2021 --> Sep 1, 2024)
plt.figure(figsize=(12, 6))
plt.plot(data, label= stock_ticker) #Plots/Creates price chart, labels each data line accordingly 
plt.title("All Stock Prices Over Time", fontweight = 'bold') #Plot Title
plt.legend(title = "Securities") #Legend Title
plt.xlabel("Date", fontweight = 'bold') #Labels X-axis with 6-month intervals
plt.ylabel("Price", fontweight = 'bold') #Labels Y-axis with ***BAD INTERVAlS* ???More graphs needed??? Or seperate for lower values
plt.show() #Displays Price Chart

for i in daily_returns.columns:
    plt.figure(figsize=(9, 6))
    plt.plot(data[i])
    plt.title(i + " Daily Price", fontweight = 'bold')
    plt.xlabel("Date", fontweight = 'bold')
    plt.ylabel("Price", fontweight = 'bold')
    plt.show()

#Line Plot of Returns
plt.figure(figsize=(12, 6))
daily_returns.plot()
plt.title("All Daily Returns Over Time", fontweight = 'bold')
plt.xlabel("Date", fontweight = 'bold')
plt.ylabel("Return", fontweight = 'bold')
plt.legend(title = "Securities")
plt.show()


#Individual Line Plots of Returns
for i in daily_returns.columns:
    plt.figure(figsize=(8, 6))
    plt.plot(daily_returns[i])
    plt.title(i + " Daily Returns", fontweight = 'bold')
    plt.xlabel("Date", fontweight = 'bold')
    plt.ylabel("Return", fontweight = 'bold')
    plt.show()

#Histograms
plt.figure(figsize=(36, 18)) #Larger Size needed so lower histogram titles don't overlap
daily_returns.hist(bins=50, figsize=(12, 4))
plt.suptitle("Histograms of Daily Returns", fontweight = 'bold') #Title for grouping of Histograms Title
plt.tight_layout() #ensures spacing between histograms
plt.show() #Displays Histograms
"""
Alphabetical Order is automated
"""

#↓↓↓Summary Statistics↓↓↓
pd.set_option('display.float_format', '{:.2e}'.format)
print(daily_returns.describe())