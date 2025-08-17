import streamlit as st
from datetime import datetime
from scanner_module import load_nifty200, get_top10, get_index_signals

# ✅ CSV फाईलचा योग्य path
CSV_PATH = "Nifty200list.csv"

# 🖥️ Page Setup
st.set_page_config(page_title="📊 Marathi Trading Dashboard", layout="centered")
st.title("📈 माझा ट्रेडिंग साथी – Suresh")
st.caption(f"🔄 Updated at: {datetime.now().strftime('%H:%M:%S')} IST")

# ✅ CSV फाईल चेक करा
try:
    df = load_nifty200(CSV_PATH)
    st.success("✅ CSV फाईल यशस्वीपणे लोड झाली!")
except FileNotFoundError as e:
    st.error(f"❌ CSV फाईल सापडली नाही:\n\n{e}")
    st.stop()

# 📌 Stock Suggestions
top10 = get_top10(df)
st.subheader("📌 आजचे Intraday Stocks – Nifty 200 मधून")
for _, row in top10.iterrows():
    st.markdown(f"✅ {row['Company Name']} ({row['Symbol']}) – {row['Industry']}")

# 📊 Index Options Signals
index_signals = get_index_signals()
st.subheader("📊 आजचे Index Options संकेत")
for signal in index_signals:
    st.markdown(
        f"💡 **{signal['Index']} {signal['Type']} {signal['Strike']}**\n"
        f"💰 Premium: ₹{signal['Premium']} | 🎯 Target: ₹{signal['Target']} | 🛑 SL: ₹{signal['Stoploss']}"
    )
# 🔹 1. Imports
import streamlit as st
import pandas as pd

# 🔹 2. Direction Logic Function
def get_trade_direction(rsi, macd_signal, sector_trend):
    if rsi > 55 and macd_signal.lower() == "bullish" and sector_trend.lower() == "positive":
        return "Buy ✅"
    elif rsi < 45 and macd_signal.lower() == "bearish" and sector_trend.lower() == "negative":
        return "Short Sell ❌"
    else:
        return "Watch Only 👀"

# 🔹 3. Sample Data (तू हे CSV मधून घेऊ शकतोस)
stocks = [
    {"Stock": "BPCL", "Sector": "Oil & Gas", "RSI": 62, "MACD": "Bullish", "Sector Trend": "Positive"},
    {"Stock": "Tata Motors", "Sector": "Automobile", "RSI": 38, "MACD": "Bearish", "Sector Trend": "Negative"},
    {"Stock": "SBI Cards", "Sector": "Financial", "RSI": 50, "MACD": "Neutral", "Sector Trend": "Neutral"},
]

# 🔹 4. Apply Direction Logic
for stock in stocks:
    stock["Direction"] = get_trade_direction(stock["RSI"], stock["MACD"], stock["Sector Trend"])

# 🔹 5. Convert to DataFrame
df = pd.DataFrame(stocks)

# 🔹 6. Display in Dashboard
st.markdown("## 📊 आजचे Intraday संकेत — Direction सहित")
st.dataframe(df, use_container_width=True)




