
# 📈 Stock Trend Predictor

A Machine Learning–powered web app that forecasts the **next-day UP/DOWN trend** of major Indian stocks using **technical indicators** and interactive visualizations — built with ❤️ using **Python**, **Streamlit**, and **scikit-learn**.

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Built_with-Streamlit-orange?logo=streamlit)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 🚀 Getting Started

To run this project on your local machine, follow these steps:

### 🔧 STEP 0: Clone the Repository & Setup Environment

```bash
# Clone the repository
git clone https://github.com/your-username/stock-trend-predictor.git
cd stock-trend-predictor

# Create and activate a virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate       # On Windows
# source venv/bin/activate    # On macOS/Linux

# Install all dependencies
pip install -r requirements.txt
```

---

## 🚦 Setup Instructions (MUST Follow Order)

### ✅ STEP 1: Download Historical Stock Data
Run this script first to fetch historical stock data using Yahoo Finance.

```bash
python stock_down.py
```

> Downloads CSV data for all predefined stocks into the `data/` folder.

---

### ✅ STEP 2: Train ML Models and Calculate Accuracy
Open and run this notebook to process the data, calculate technical indicators, train the model, and save accuracy.

```bash
# In VS Code or Jupyter Notebook:
data_prep.ipynb
```

> This generates model files and accuracy metrics for each stock.

---

### ✅ STEP 3: Launch the Streamlit App
Run the app and explore predictions, comparisons, and visual insights.

```bash
streamlit run app.py
```

> The app includes individual stock views, comparison mode, and accuracy metrics.

---

### ✅ STEP 4: Set Up Auto Update with Task Scheduler (Windows Only)

To automate daily data refresh and model updates:

1. Create a file named `run_update.bat` in your project folder with the following content:

   ```bat
   @echo off
   cd /d "C:\path\to\your\project"
   python update_data.py
   ```
🔁 Replace `"C:\path\to\your\project"` with your actual project directory path.

Then follow these steps to schedule the auto-update:

- Open **Task Scheduler** on Windows and click **Create Basic Task**
- Name it something like **"Stock Predictor Daily Update"**
- Select **Daily**, and set your preferred time (e.g., **6:00 PM**)
- Choose **Start a program**, then **Browse** to select your `run_update.bat` file
- Click **Finish**

---

## 🧠 Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python, Pandas, NumPy, scikit-learn
- **ML Model**: Random Forest Classifier
- **Data**: Yahoo Finance via `yfinance`
- **Automation**: Scheduled updates via `update_data.py`

---

## 📂 Project Structure

```
├── app.py                 # Streamlit UI app (run last)
├── data/stock_down.py     # Data downloader (run first)
├── data_prep.ipynb        # Model training notebook (run second)
├── update_data.py         # Daily prediction updater (optional)
├── models/                # Saved models per stock
├── stock_logos/           # Company logo images
├── run_update.bat         # To update 'update_data.py'
├── requirements.txt
└── README.md
```

---

## 📧 Contact

**Vraj N. Patel**  
📧 p.vraj2110@gmail.com  
🔗 [LinkedIn](https://linkedin.com/in/vraj-patel-82542822a) | 🔗 [GitHub](https://github.com/pvraj1011)

---

## 📜 License

This project is licensed under the MIT License.
