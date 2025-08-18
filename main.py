import streamlit as st
import pandas as pd
import random
from datetime import datetime

# 📁 CSV path
CSV_PATH = "Nifty200list.csv"

# 📘 Trade direction logic
def get_trade_direction(rsi, macd, sector_trend):
    if rsi > 55 and macd.lower() == "bullish" and sector_trend.lower() == "positive":
        return "खरेदी करा ✅"
    elif rsi < 45 and macd.lower() == "bearish" and sector_trend.lower() == "negative":
        return "शॉर्ट सेल करा ❌"
    else:
        return "फक्त निरीक्षण करा 👀"

# 🔍 Filter top 10 stocks
def filter_top_stocks(df):
    df.columns = df.columns.str.strip().str.lower()
    df["score"] = 0
    df.loc[df["rsi"] > 55, "score"] += 1
    df.loc[df["macd"] == "bullish", "score"] += 1
    df.loc[df["sector trend"] == "positive", "score"] += 1
    top10 = df.sort_values(by="score", ascending=False).head(10)
    return top10

# 📈 Index signal generator
def generate_index_signals():
    indices = {
        "Nifty50": 22450,
        "BankNifty": 48200,
        "Sensex": 74200,
        "Midcap": 37000,
        "Smallcap": 14500,
        "FinNifty": 21500
    }

    signals = []
    for name, spot in indices.items():
        strike = round(spot / 50) * 50 if "Nifty" in name else round(spot / 100) * 100
        direction = random.choice(["Call", "Put"])
        entry = random.randint(90, 180)
        target = entry + random.randint(30, 60)
        stoploss = entry - random.randint(20, 40)
        verdict = "खरेदी करा ✅" if direction == "Call" else "शॉर्ट सेल करा ❌"

        signals.append({
            "Index": name,
            "Type": direction,
            "Strike": strike,
            "Premium": entry,
            "Target": target,
            "Stoploss": stoploss,
            "Verdict": verdict
        })
    return signals

# 🖥️ Streamlit UI
st.set_page_config(page_title="📊 माझा ट्रेडिंग साथी – Suresh", layout="centered")
st.title("📈 माझा ट्रेडिंग साथी – Suresh")
st.caption(f"🔄 अपडेट वेळ: {datetime.now().strftime('%H:%M:%S')} IST")

# 📂 Load CSV
try:
    df = pd.read_csv(CSV_PATH)
    st.success("✅ Nifty200 CSV यशस्वीपणे लोड झाली!")
except FileNotFoundError:
    st.error("❌ CSV फाईल सापडली नाही. कृपया path तपासा.")
    st.stop()

# 🔍 Top 10 stocks
top10 = filter_top_stocks(df)
top10["Verdict"] = top10.apply(
    lambda row: get_trade_direction(row["rsi"], row["macd"], row["sector trend"]),
    axis=1
)

# 📊 Display Stock Table
st.subheader("📌 आजचे Intraday Stocks – Nifty200 मधून")
st.dataframe(top10[["stock", "sector", "rsi", "macd", "sector trend", "Verdict"]], use_container_width=True)

# 📈 Display Index Signals
st.subheader("📊 आजचे Index संकेत – सर्व प्रमुख निर्देशांक")
index_signals = generate_index_signals()
for signal in index_signals:
    st.markdown(
        f"💡 **{signal['Index']} {signal['Type']} {signal['Strike']}**\n"
        f"💰 Premium: ₹{signal['Premium']} | 🎯 Target: ₹{signal['Target']} | 🛑 SL: ₹{signal['Stoploss']} | 📢 Verdict: {signal['Verdict']}"
    )






