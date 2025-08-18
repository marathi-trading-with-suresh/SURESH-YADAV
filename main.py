import streamlit as st
import pandas as pd
from datetime import datetime

# ----------------------------
# Helpers (scanner_module मधलं logic इथे)
# ----------------------------
def _find_col(df: pd.DataFrame, names):
    low = {c.lower(): c for c in df.columns}
    for n in names:
        if n.lower() in low:
            return low[n.lower()]
    return None

def load_nifty200(csv_path="Nifty200list.csv"):
    try:
        df = pd.read_csv(csv_path)
        df.columns = [c.strip() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"[load_nifty200] {e}")
        return pd.DataFrame()

def get_top10(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    col_stock = _find_col(df, ["stock", "symbol", "name"])
    col_sector = _find_col(df, ["sector", "industry"])
    col_rsi = _find_col(df, ["rsi"])
    col_macd = _find_col(df, ["macd"])
    col_sector_trend = _find_col(df, ["sector trend", "sector_trend", "trend"])

    work = df.copy()
    work["score"] = 0

    if col_rsi:
        work.loc[pd.to_numeric(work[col_rsi], errors="coerce") > 55, "score"] += 1
    if col_macd:
        macd_series = work[col_macd].astype(str).str.strip().str.lower()
        work.loc[macd_series == "bullish", "score"] += 1
    if col_sector_trend:
        pos_vals = {"positive", "up", "bullish"}
        sect_series = work[col_sector_trend].astype(str).strip().str.lower()
        work.loc[sect_series.isin(pos_vals), "score"] += 1

    top10 = work.sort_values("score", ascending=False).head(10).copy()

    if col_stock and "stock" not in top10.columns:
        top10.rename(columns={col_stock: "stock"}, inplace=True)
    if col_sector and "sector" not in top10.columns:
        top10.rename(columns={col_sector: "sector"}, inplace=True)
    if col_rsi and "rsi" not in top10.columns:
        top10.rename(columns={col_rsi: "rsi"}, inplace=True)
    if col_macd and "macd" not in top10.columns:
        top10.rename(columns={col_macd: "macd"}, inplace=True)
    if col_sector_trend and "sector trend" not in top10.columns:
        top10.rename(columns={col_sector_trend: "sector trend"}, inplace=True)

    return top10

def get_index_signals():
    indices = {
        "Nifty50": 22450,
        "BankNifty": 48200,
        "Sensex": 74200,
        "Midcap": 37000,
        "Smallcap": 14500,
        "FinNifty": 21500,
    }
    out = []
    for name, spot in indices.items():
        direction = "CALL" if spot % 2 == 0 else "PUT"
        strike = round(spot / 50) * 50
        out.append({
            "name": name,
            "spot": spot,
            "direction": direction,
            "strike": strike,
            "entry": 100,
            "target": 140,
            "stoploss": 80,
            "verdict": "खरेदी" if direction == "CALL" else "विक्री",
        })
    return out

# verdict helper (fallback)
def get_trade_verdict(rsi, macd, sector_trend) -> str:
    bull = (pd.to_numeric(pd.Series([rsi]), errors="coerce").iloc[0] or 0) > 55
    macd_ok = str(macd).strip().lower() == "bullish"
    sector_ok = str(sector_trend).strip().lower() in ("positive", "up", "bullish")
    return "खरेदी" if (bull and macd_ok and sector_ok) else "विक्री/थांबा"

# ----------------------------
# UI
# ----------------------------
st.set_page_config(page_title="📊 माझा ट्रेडिंग साथी – Suresh", layout="centered")
st.title("📈 माझा ट्रेडिंग साथी – Suresh")
st.caption(f"🔄 अपडेट वेळ: {datetime.now().strftime('%H:%M:%S')} IST")

df = load_nifty200("Nifty200list.csv")
if df.empty:
    st.stop()

st.success("✅ CSV यशस्वीपणे लोड झाली!")

top10 = get_top10(df).copy()

# add verdict
def _col(frame, name):
    for c in frame.columns:
        if c.lower() == name:
            return c
    return None

rsi_col = _col(top10, "rsi")
macd_col = _col(top10, "macd")
sect_col = _col(top10, "sector trend")

if rsi_col and macd_col and sect_col:
    top10["Verdict"] = top10.apply(
        lambda row: get_trade_verdict(row[rsi_col], row[macd_col], row[sect_col]),
        axis=1
    )
else:
    top10["Verdict"] = top10.get("score", 0).apply(lambda s: "खरेदी" if s >= 2 else "विक्री/थांबा")

st.subheader("📌 आजचे Intraday Stocks – Nifty200 मधून")
pref = ["stock", "sector", "rsi", "macd", "sector trend", "Verdict", "score"]
show = [c for c in pref if c in top10.columns]
st.dataframe(top10[show], use_container_width=True)

st.subheader("📊 आजचे Index संकेत – Options Trading साठी")
for sig in get_index_signals():
    st.markdown(
        f"💡 **{sig['name']} {sig['direction']} {sig['strike']}**  \n"
        f"💰 Premium: ₹{sig['entry']} | 🎯 Target: ₹{sig['target']} | 🛑 SL: ₹{sig['stoploss']} | "
        f"📢 Verdict: {sig['verdict']}"
    )
st.caption("ℹ️ शैक्षणिक डेमो. Live trading आधी स्वतः पडताळणी करा.")
