# main.py  — Streamlit app (copy–paste ready)

import streamlit as st
import pandas as pd
from datetime import datetime

# --- Project imports (must exist in repo) ---
from scanner_module import load_nifty200, get_top10, get_index_signals

# Optional helpers (fallbacks if module/func missing)
try:
    from utils import auto_column_mapper
except Exception:
    def auto_column_mapper(df: pd.DataFrame) -> pd.DataFrame:
        return df  # no-op if utils not present

try:
    from verdict_logic import get_trade_verdict
except Exception:
    def get_trade_verdict(rsi, macd, sector_trend) -> str:
        # simple fallback verdict
        bull = (pd.to_numeric(pd.Series([rsi]), errors="coerce").iloc[0] or 0) > 55
        macd_ok = str(macd).strip().lower() == "bullish"
        sector_ok = str(sector_trend).strip().lower() in ("positive", "up", "bullish")
        return "खरेदी" if (bull and macd_ok and sector_ok) else "विक्री/थांबा"

# ---------------- UI ----------------
st.set_page_config(page_title="📊 माझा ट्रेडिंग साथी – Suresh", layout="centered")
st.title("📈 माझा ट्रेडिंग साथी – Suresh")
st.caption(f"🔄 अपडेट वेळ: {datetime.now().strftime('%H:%M:%S')} IST")

# 1) Load Nifty200 CSV
df = load_nifty200("Nifty200list.csv")
if df.empty:
    st.error("❌ Nifty200list.csv लोड होत नाही. कृपया फाईल तपासा.")
    st.stop()

# Normalize columns if helper available
df = auto_column_mapper(df)
st.success("✅ CSV यशस्वीपणे लोड झाली!")

# 2) Top 10 Intraday stocks (scanner_module logic)
top10 = get_top10(df).copy()

# 3) Verdict column (uses verdict_logic if present)
if {"rsi", "macd", "sector trend"}.issubset(set(map(str.lower, top10.columns))):
    # make sure we access the correct-case columns
    # find actual names present
    def col(name):
        for c in top10.columns:
            if c.lower() == name:
                return c
        return name

    rsi_col = col("rsi")
    macd_col = col("macd")
    sect_col = col("sector trend")

    top10["Verdict"] = top10.apply(
        lambda row: get_trade_verdict(row[rsi_col], row[macd_col], row[sect_col]),
        axis=1
    )
else:
    # fallback if expected cols missing
    top10["Verdict"] = top10.get("score", 0).apply(lambda s: "खरेदी" if s >= 2 else "विक्री/थांबा")

# 4) Show table
st.subheader("📌 आजचे Intraday Stocks – Nifty200 मधून")

# choose safe display columns
pref_cols = ["stock", "sector", "rsi", "macd", "sector trend", "Verdict", "score"]
show_cols = [c for c in pref_cols if c in top10.columns]
st.dataframe(top10[show_cols], use_container_width=True)

# 5) Index option signals
st.subheader("📊 आजचे Index संकेत – Options Trading साठी")
for sig in get_index_signals():
    st.markdown(
        f"💡 **{sig['name']} {sig['direction']} {sig['strike']}**  \n"
        f"💰 Premium: ₹{sig['entry']} | 🎯 Target: ₹{sig['target']} | 🛑 SL: ₹{sig['stoploss']} | "
        f"📢 Verdict: {sig['verdict']}"
    )

st.caption("ℹ️ सूचनाः हे शैक्षणिक डेमो आहे. Live trading आधी स्वतःची पडताळणी करा.")
