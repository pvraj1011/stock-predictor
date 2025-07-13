import streamlit as st
import pandas as pd
import joblib
import os
import base64
import subprocess
from datetime import date, timedelta
import matplotlib.pyplot as plt
from PIL import Image

# ----------------------------
# Stock Logo + Navigation
# ----------------------------
def show_logo(stock):
    logo_path = f"logos/{stock}.png"
    if os.path.exists(logo_path):
        logo = Image.open(logo_path)
        st.image(logo, width=80)

def stock_logo_button(stock):
    logo_path = f"logos/{stock}.png"
    if os.path.exists(logo_path):
        img_bytes = open(logo_path, "rb").read()
        b64_img = base64.b64encode(img_bytes).decode()
        if st.button(" ", key=f"btn_{stock}"):
            st.session_state['selected_stock'] = stock
            st.experimental_rerun()
        st.markdown(
            f"""
            <div style="text-align:center; margin-top:-55px; margin-bottom:10px">
                <img src="data:image/png;base64,{b64_img}" width="60"/><br/>
                <strong style="font-size:14px;">{stock}</strong>
            </div>
            """, unsafe_allow_html=True
        )

@st.cache_data
def load_stock_data(stock):
    df = pd.read_csv(f"data/{stock}_features.csv", parse_dates=["Date"])
    df = df.iloc[1:]
    df["Date"] = pd.to_datetime(df["Date"])
    df.set_index("Date", inplace=True)
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
    df.dropna(subset=["Close"], inplace=True)
    return df

@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=True).encode("utf-8")

def get_latest_close_price(stock):
    try:
        df = pd.read_csv(f"data/{stock}.csv")
        return float(df.iloc[-1]["Close"])
    except:
        return None

def plot_price(df, stock, indicators=[]):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df["Close"], label="Close", color="blue")

    colors = {
        "SMA_14": "orange",
        "EMA_14": "green",
        "MACD": "red",
        "MACD_signal": "purple",
    }

    for ind in indicators:
        if ind in df.columns and ind != "RSI":
            ax.plot(df[ind], label=ind, color=colors.get(ind, "gray"))

    ax.set_title(f"{stock} - Price and Indicators")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend()
    ax.grid(True)

    if "RSI" in indicators:
        ax2 = ax.twinx()
        ax2.plot(df["RSI"], label="RSI", color="magenta", linestyle="--")
        ax2.set_ylabel("RSI", color="magenta")
        ax2.tick_params(axis='y', labelcolor="magenta")

    st.pyplot(fig)

# ----------------------------
# App Setup
# ----------------------------
st.set_page_config(page_title="Stock Analyzer", layout="wide")
stocks = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "LT", "BAJFINANCE", "SBIN", "HINDUNILVR", "MARUTI"]

# ----------------------------
# Sidebar Navigation
# ----------------------------
st.sidebar.markdown("## 🧭 Navigation")

main_nav = st.sidebar.radio("Go to", ["🏠 Home", "📊 Compare", "📈 Stocks"])
if main_nav == "📈 Stocks":
    selected_mode = st.sidebar.selectbox("Choose a Stock", stocks)
else:
    selected_mode = main_nav.replace("🏠 ", "").replace("📊 ", "")

# Redirect from logo click
if 'selected_stock' not in st.session_state:
    st.session_state['selected_stock'] = None

if st.session_state['selected_stock']:
    selected_mode = st.session_state['selected_stock']
    st.session_state['selected_stock'] = None

if selected_mode in stocks:
    st.sidebar.markdown(f"**📌 Selected Stock:** `{selected_mode}`")

st.sidebar.markdown("### 💡 Tips")
st.sidebar.info("• Use **Compare** to analyze 2 stocks side-by-side.\n"
                "• Click a logo on Home to view prediction.\n"
                "• Use **Stocks** for full model view.")

# =========================
# HOME PAGE
# =========================
if selected_mode == "Home":
    st.title("👋 Welcome to Stock Trend Analyzer")

    st.markdown("""
    #### 👨‍💻 Developed by: **Vraj Patel**  
    🎓 B.E. Computer Science @ LJ Institute of Engineering & Technology  
    📍 Ahmedabad, India  
    🔗 [GitHub](https://github.com/pvraj1011) | [LinkedIn](https://www.linkedin.com/in/vraj-patel-82542822a) | [Resume](https://your-resume-link.com)

    ---
    ### 💡 Project Overview:
    This ML-powered dashboard predicts next-day stock price **UP or DOWN** using technical indicators and a Random Forest model.
    """)
    st.markdown("### 📂 Click any stock below to start")

    cols = st.columns(5)
    for i, stock in enumerate(stocks):
        with cols[i % 5]:
            logo_path = f"logos/{stock}.png"
            if os.path.exists(logo_path):
                st.image(logo_path, width=60)
                if st.button(stock, key=f"btn_home_{stock}"):
                    st.session_state['selected_stock'] = stock
                    st.rerun()


# =========================
# COMPARE MODE
# =========================
elif selected_mode == "Compare":
    st.title("📊 Compare Two Stocks")
    start_date, end_date = st.date_input("Select date range", [date(2022, 1, 1), date.today()])
    selected = st.multiselect("Select 2 stocks", stocks, default=["RELIANCE", "TCS"])

    if len(selected) != 2:
        st.warning("Please select exactly 2 stocks.")
    else:
        s1, s2 = selected
        df1, df2 = load_stock_data(s1), load_stock_data(s2)
        df1 = df1[start_date:end_date]
        df2 = df2[start_date:end_date]
        csv1, csv2 = convert_df_to_csv(df1), convert_df_to_csv(df2)

        col1, col2 = st.columns(2)

        for col, stock, df, csv in zip([col1, col2], [s1, s2], [df1, df2], [csv1, csv2]):
            with col:
                logo_col, txt_col = st.columns([1, 4])
                with logo_col: show_logo(stock)
                with txt_col:
                    price = get_latest_close_price(stock)
                    if price:
                        st.markdown(f"### {stock}\n**₹{price:.2f}**")

                plot_price(df, stock)
                st.download_button(f"📥 Download {stock} CSV", data=csv, file_name=f"{stock}.csv")

# =========================
# INDIVIDUAL STOCK MODE
# =========================
elif selected_mode in stocks:
    col_logo, col_txt = st.columns([1, 4])
    with col_logo: show_logo(selected_mode)
    with col_txt:
        price = get_latest_close_price(selected_mode)
        if price:
            st.markdown(f"### {selected_mode} Stock Analysis\n💰 **₹{price:.2f}**")

    model_path = f"models/{selected_mode}.pkl"
    scaler_path = f"models/{selected_mode}_scaler.pkl"

    if not os.path.exists(model_path):
        st.error("Model not found.")
    else:
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        df = load_stock_data(selected_mode)

        latest_date = df.index[-1].date()
        today = date.today()

        if latest_date < today:
            st.warning(f"⚠️ Latest data till {latest_date}. No update for today.")
        else:
            st.success(f"✅ Data updated till today: {today}")

        all_dates = df.index.tolist()
        st.subheader("📅 Select date to predict next-day trend")
        date_selected = st.date_input("Date", value=all_dates[-1], min_value=all_dates[0], max_value=all_dates[-1])

        try:
            idx = df.index.get_loc(pd.to_datetime(date_selected))
            features = ["SMA_14", "EMA_14", "RSI", "MACD", "MACD_signal", "BB_upper", "BB_lower"]
            sample = df.iloc[idx][features].values.reshape(1, -1)
            pred = model.predict(scaler.transform(sample))[0]

            next_day = pd.to_datetime(date_selected) + timedelta(days=1)
            pred_str = "📈 UP" if pred else "📉 DOWN"
            color = "#28a745" if pred else "#dc3545"

            if next_day in df.index:
                actual = df.loc[next_day]["Target"]
                actual_str = "📈 UP" if actual == 1 else "📉 DOWN"
                actual_color = "#28a745" if actual == 1 else "#dc3545"
                actual_html = f"<p style='color:{actual_color};'><strong>✅ Actual:</strong> {actual_str}</p>"
            else:
                actual_html = "<p style='color:gray;'>📭 No data for next day</p>"

            st.markdown("### 🔮 Prediction Result")
            st.markdown(
                f"""
                <div style='background-color:#1e1e1e; padding:25px; border-left:6px solid {color}; color:white;'>
                    <h4>📅 Prediction for {next_day.strftime('%d %b %Y')}</h4>
                    <h2 style='color:{color};'>{pred_str}</h2>
                    {actual_html}
                </div>
                """, unsafe_allow_html=True
            )

            st.subheader("📌 Indicators")
            selected_indicators = st.multiselect("Select indicators", ["SMA_14", "EMA_14", "MACD", "MACD_signal", "RSI"], default=["SMA_14"])
            st.subheader("📈 Closing Price Chart")
            plot_price(df, selected_mode, indicators=selected_indicators)

            st.download_button("📥 Download CSV", convert_df_to_csv(df), file_name=f"{selected_mode}_data.csv")

        except Exception as e:
            st.error(f"Error predicting: {e}")

