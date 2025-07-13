import yfinance as yf
import pandas as pd
from ta.trend import SMAIndicator, EMAIndicator, MACD
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import os

def process_and_train_stocks():
    # List of stock symbols to process
    stocks = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", 
              "LT", "BAJFINANCE", "SBIN", "HINDUNILVR", "MARUTI"]


    for stock in stocks:

        try:
            #* Download historical data from Yahoo Finance
            df = yf.download(stock + ".NS", start="2015-01-01", auto_adjust=False, progress=False)

            #* Keep only required columns
            df = df[["Open", "High", "Low", "Close", "Volume"]].copy()
            df.dropna(inplace=True)
            
            #* Save latest raw stock data (overwriting previous stock.csv)      
            df_raw = df.copy()
            df_raw.reset_index(inplace=True)
            df_raw.to_csv(f"data/{stock}.csv", index=False)

            
            #* Shape
            close_series = df['Close'].squeeze()

            #* Calculate technical indicators
            df["SMA_14"] = SMAIndicator(close_series, 14).sma_indicator()
            df["EMA_14"] = EMAIndicator(close_series, 14).ema_indicator()
            df["RSI"] = RSIIndicator(close_series, 14).rsi()

            macd = MACD(close_series)
            df["MACD"] = macd.macd()
            df["MACD_signal"] = macd.macd_signal()

            bb = BollingerBands(close_series)
            df["BB_upper"] = bb.bollinger_hband()
            df["BB_lower"] = bb.bollinger_lband()

            #* Create binary target column (1 if price goes up next day, else 0)
            df["Target"] = (df["Close"].shift(-1) > df["Close"]).astype(int)
            df.dropna(inplace=True)

            #* Save raw data to CSV
            os.makedirs("data", exist_ok=True)
            
            df.reset_index(inplace=True)  # Ensures 'Date' is a proper column
            df = df.iloc[1:]
            df.to_csv(f"data/{stock}_features.csv", index=False)



            #* Prepare training features and labels
            features = ["SMA_14", "EMA_14", "RSI", "MACD", "MACD_signal", "BB_upper", "BB_lower"]
            X = df[features]
            y = df["Target"]

            #* Scale features for training
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            #* Train/test split
            X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

            #* Train and save model
            model = RandomForestClassifier(random_state=42)
            model.fit(X_train, y_train)

            os.makedirs("models", exist_ok=True)
            joblib.dump(model, f"models/{stock}.pkl")
            joblib.dump(scaler, f"models/{stock}_scaler.pkl")

            print(f"✅ {stock} updated.")

        except Exception as e:
            print(f"❌ Exception in {stock}: {e}")

# Run the update process if script is executed directly
if __name__ == "__main__":
    process_and_train_stocks()
    if os.environ.get("USERNAME") == "VRAJ PATEL":
        input("\n🔚 Press Enter to exit...")
