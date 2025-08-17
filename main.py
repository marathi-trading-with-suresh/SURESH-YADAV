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

def get_trade_direction(rsi, macd_signal, sector_trend):
    if rsi > 55 and macd_signal.lower() == "bullish" and sector_trend.lower() == "positive":
        return "Buy ✅"
    elif rsi < 45 and macd_signal.lower() == "bearish" and sector_trend.lower() == "negative":
        return "Short Sell ❌"
    else:
        return "Watch Only 👀"

def filter_top_stocks(df):
    df["Score"] = 0
    df["MACD"] = df["MACD"].str.lower()
    df["Sector Trend"] = df["Sector Trend"].str.lower()

    df.loc[(df["RSI"] > 55), "Score"] += 1
    df.loc[(df["MACD"] == "bullish"), "Score"] += 1
    df.loc[(df["Sector Trend"] == "positive"), "Score"] += 1

    top10 = df.sort_values(by="Score", ascending=False).head(10)
    return top10

# 📂 Load CSV with technical data
df = pd.read_csv("Nifty200list.csv")  # CSV must include RSI, MACD, Sector Trend

# 🎯 Filter top 10 stocks
top_stocks = filter_top_stocks(df)

# ➕ Add direction
top_stocks["Direction"] = top_stocks.apply(
    lambda row: get_trade_direction(row["RSI"], row["MACD"], row["Sector Trend"]),
    axis=1
)

# 📊 Display
st.markdown("## 🔟 आजचे Top 10 Intraday संकेत (Nifty 200 मधून)")
st.dataframe(top_stocks[["Stock", "Sector", "RSI", "MACD", "Sector Trend", "Direction"]], use_container_width=True)



