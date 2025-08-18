import streamlit as st
import pandas as pd
import random
from datetime import datetime

# 📂 CSV path
CSV_PATH = "Nifty200list.csv"

# 🖥️ Streamlit UI
st.set_page_config(page_title="📊 माझा ट्रेडिंग साथी – Suresh", layout="centered")
st.title("📈 माझा ट्रेडिंग साथी – Suresh")
st.caption(f"🔄 अपडेट वेळ: {datetime.now().strftime('%H:%M:%S')} IST")

# 📥 CSV लोड करा
try:
    df = pd.read_csv(CSV_PATH)
    st.success("✅ Nifty200 CSV यशस्वीपणे लोड झाली!")
except FileNotFoundError:
    st.error("❌ CSV फाईल सापडली नाही. कृपया path तपासा.")
    st.stop()

# 🛡️ आवश्यक कॉलम्स तपासा
required_cols = ["stock", "sector", "rsi", "macd", "sector trend"]
missing = set(required_cols) - set(df.columns)
if missing:
    st.error("❌ काही आवश्यक कॉलम नाहीत: " + ", ".join(missing))
    st.stop()

# 🔍 Top 10 Intraday Stocks
df.columns = df.columns.str.strip().str.lower()
df["score"] = 0
df.loc[df["rsi"] > 55, "score"] += 1
df.loc[df["macd"].str.lower() == "bullish", "score"] += 1
df.loc[df["sector trend"].str.lower() == "positive", "score"] += 1
top10 = df.sort_values(by="score", ascending=False).head(10)

# 🧠 Verdict logic
def get_trade_verdict(rsi, macd, sector_trend):
    if rsi > 55 and macd.lower() == "bullish" and sector_trend.lower() == "positive":
        return "🟢 खरेदी"
    elif rsi < 45 and macd.lower() == "bearish" and sector_trend.lower() == "negative":
        return "🔴 विक्री"
    else:
        return "⚪️ थांबा"

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
    strike = round(spot / 50) * 50 if "Nifty" in name else round(spot / 100) * 100
    direction = random.choice(["Call", "Put"])
    entry = random.randint(90, 180)
    target = entry + random.randint(30, 60)
    stoploss = entry - random.randint(20, 40)
    verdict = "🟢 खरेदी" if direction == "Call" else "🔴 विक्री"

    st.markdown(
        f"💡 **{name} {direction} {strike}**\n"
        f"💰 Premium: ₹{entry} | 🎯 Target: ₹{target} | 🛑 SL: ₹{stoploss} | 📢 Verdict: {verdict}"
    )
