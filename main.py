import streamlit as st
import pandas as pd
from datetime import datetime
from utils import auto_column_mapper
from verdict_logic import get_trade_verdict
from option_signals import generate_option_signal

# 📂 CSV path
CSV_PATH = "Nifty200list.csv"

# 🖥️ Streamlit UI
st.set_page_config(page_title="📊 माझा ट्रेडिंग साथी – Suresh", layout="centered")
st.title("📈 माझा ट्रेडिंग साथी – Suresh")
st.caption(f"🔄 अपडेट वेळ: {datetime.now().strftime('%H:%M:%S')} IST")

# 📥 CSV लोड करा
try:
    df = pd.read_csv(CSV_PATH)
    df = auto_column_mapper(df)
    st.success("✅ CSV यशस्वीपणे लोड झाली!")
except Exception as e:
    st.error(f"❌ CSV लोड करताना त्रुटी: {e}")
    st.stop()

# 🔍 Top 10 Intraday Stocks
df["score"] = 0
df.loc[df["rsi"] > 55, "score"] += 1
df.loc[df["macd"].str.lower() == "bullish", "score"] += 1
df.loc[df["sector trend"].str.lower() == "positive", "score"] += 1
top10 = df.sort_values(by="score", ascending=False).head(10)

top10["Verdict"] = top10.apply(
    lambda row: get_trade_verdict(row["rsi"], row["macd"], row["sector trend"]),
    axis=1
)

# 📊 Display Stock Table
st.subheader("📌 आजचे Intraday Stocks – Nifty200 मधून")
st.dataframe(top10[["stock", "sector", "rsi", "macd", "sector trend", "Verdict"]], use_container_width=True)

# 📈 Index Option Signals
st.subheader("📊 आजचे Index संकेत – Options Trading साठी")

indices = {
    "Nifty50": 22450,
    "BankNifty": 48200,
    "Sensex": 74200,
    "Midcap": 37000,
    "Smallcap": 14500,
    "FinNifty": 21500
}

for name, spot in indices.items():
    signal = generate_option_signal(name, spot)
    st.markdown(
        f"💡 **{signal['name']} {signal['direction']} {signal['strike']}**\n"
        f"💰 Premium: ₹{signal['entry']} | 🎯 Target: ₹{signal['target']} | 🛑 SL: ₹{signal['stoploss']} | 📢 Verdict: {signal['verdict']}"
    )

