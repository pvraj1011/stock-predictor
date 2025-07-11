import yfinance as yf
import os

tickers = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS",
    "LT.NS", "BAJFINANCE.NS", "SBIN.NS", "HINDUNILVR.NS", "MARUTI.NS"
]

start_date = "2015-01-01"
end_date = None

os.makedirs("data", exist_ok=True)

for ticker in tickers:
    print(f"📥 Downloading {ticker}...")
    df = yf.download(ticker, start=start_date, end=end_date,auto_adjust=False)
    
    if not df.empty:
        df.reset_index(inplace=True)
        
        # Clean any accidental headers or bad rows from earlier
        if isinstance(df.columns[0], str) and df.columns[0] == "Date":
            df = df[df["Date"].notna()]
        
        # ✅ Save clean CSV with proper structure (no index column)
        df.to_csv(f"data/{ticker.replace('.NS', '')}.csv", index=False)
        print(f"✅ Saved to data/{ticker.replace('.NS', '')}.csv\n")
    else:
        print(f"❌ No data for {ticker}.\n")

