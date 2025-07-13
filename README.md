# 📈 Stock Trend Predictor

A Machine Learning–powered web app that forecasts the **next-day UP/DOWN trend** of major Indian stocks using **technical indicators** and visual insights — built with ❤️ using **Python**, **Streamlit**, and **scikit-learn**.

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Built_with-Streamlit-orange?logo=streamlit)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 🚀 Features

✅ Predicts **next-day stock trend** using machine learning (Random Forest)  
✅ Compare two stocks side-by-side in **Compare Mode**  
✅ **Logo-based navigation** & intuitive dashboard  
✅ Integrated **technical indicators** (SMA, EMA, RSI, MACD, Bollinger Bands)  
✅ Real-time **accuracy tracking** per stock  
✅ Automatic daily data & model updates (no manual refresh needed)  
✅ Built with clean UI and minimalistic design via **custom sidebar** buttons

---

## 🧠 Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Backend**: Python, Pandas, NumPy, scikit-learn
- **Machine Learning**: Random Forest Classifier
- **Data Source**: Yahoo Finance via `yfinance`
- **Scheduling**: Windows Task Scheduler + `.bat` script
- **Deployment**: Local / Streamlit Cloud

---

## ⚙️ How to Run

```bash
# 1. Clone the repository
git clone https://github.com/your-username/stock-trend-predictor.git
cd stock-trend-predictor

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```
