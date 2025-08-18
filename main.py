import streamlit as st
import pandas as pd
from datetime import datetime

import scanner_module as scan  # ✅ safer import

# Optional helpers
try:
    from utils import auto_column_mapper
except Exception:
    def auto_column_mapper(df: pd.DataFrame) -> pd.DataFrame:
        return df

try:
    from verdict_logic import get_trade_verdict
except Exception:
    def get_trade_verdict(rsi, macd, sector_trend) -> str:
        bull = (pd.to_numeric(pd.Series([rsi]), errors="coerce").iloc[0] or 0) > 55
        macd_ok = str(macd).strip().lower() == "bullish"
        sector_ok = str(sector_trend).strip().lower() in ("positive", "up", "bullish")
        return "खरेदी" if (bull and macd_ok and sector_ok) else "विक्री/थांबा"

st.set_page_config(page_title="📊 माझा ट्रेडिंग साथी – Suresh", layout="centered")
st.title("📈 माझा ट्रेडिंग साथी – Suresh")
st.caption(f"🔄 अपडेट वेळ: {datetime.now().strftime('%H:%M:%S')} IST")

# 1) Load CSV
df = scan.load_nifty200("Nifty200list.csv")
if df.empty:
    st.error("❌ Nifty200list.csv लोड होत नाही. कृपया फाईल तपासा.")
    st.stop()

df = auto_column_mapper(df)
st.success("✅ CSV यशस्वीपणे लोड झाली!")

# 2) Top 10
top10 = scan.get_top10(df).copy()

# 3) Verdict
def colfind(frame, name):
    for c in frame.columns:
        if c.lower() == name:
            return c
    return None

rsi_col = colfind(top10, "rsi")
macd_col = colfind(top10, "macd")
sect_col = colfind(top10, "sector trend")

if rsi_col and macd_col and sect_col:
    top10["Verdict"] = top10.apply(
        lambda row: get_trade_verdict(row[rsi_col], row[macd_col], row[sect_col]),
        axis=1
    )
else:
    top10["Verdict"] = top10.get("score", 0).apply(lambda s: "खरेदी" if s >= 2 else "विक्री/थांबा")

# 4) Table
st.subheader("📌 आजचे Intraday Stocks – Nifty200 मधून")
pref = ["stock", "sector", "rsi", "macd", "sector trend", "Verdict", "score"]
show = [c for c in pref if c in top10.columns]
st.dataframe(top10[show], use_container_width=True)

# 5) Index signals
st.subheader("📊 आजचे Index संकेत – Options Trading साठी")
for sig in scan.get_index_signals():
    st.markdown(
        f"💡 **{sig['name']} {sig['direction']} {sig['strike']}**  \n"
        f"💰 Premium: ₹{sig['entry']} | 🎯 Target: ₹{sig['target']} | 🛑 SL: ₹{sig['stoploss']} | "
        f"📢 Verdict: {sig['verdict']}"
    )
