import streamlit as st
import pandas as pd
from datetime import datetime

# --- project imports ---
from scanner_module import load_nifty200, get_top10
from index_signals import generate_option_signal   # ✅ नवीन फाईलमधून

# Optional helpers (असतील तर वापरा; नसतील तर fallback)
try:
    from verdict_logic import get_trade_verdict
except Exception:
    def get_trade_verdict(rsi, macd, sector_trend) -> str:
        bull = (pd.to_numeric(pd.Series([rsi]), errors="coerce").iloc[0] or 0) > 55
        macd_ok = str(macd).strip().lower() == "bullish"
        sector_ok = str(sector_trend).strip().lower() in ("positive", "up", "bullish")
        return "खरेदी" if (bull and macd_ok and sector_ok) else "विक्री/थांबा"

# ---------------- UI ----------------
st.set_page_config(page_title="📈 मराठी Trade with Suresh", layout="wide")
st.title("📈 मराठी Trade with Suresh")
st.caption(f"🔄 अपडेट वेळ: {datetime.now().strftime('%H:%M:%S')} IST")

# -------- Sidebar tuning for Index signals --------
st.sidebar.header("⚙️ Parameters")
entry_band = st.sidebar.slider("Entry band (₹)", 1.0, 5.0, 2.0, 0.5)
target_pct = st.sidebar.slider("Target % of entry", 0.5, 1.5, 0.95, 0.05)
sl_pct     = st.sidebar.slider("SL % of entry", 0.3, 0.8, 0.58, 0.02)

# -------- Section 1: Nifty200 Intraday Scanner --------
st.subheader("📊 Nifty200 Intraday Scanner")

df = load_nifty200("Nifty200list.csv")
if df.empty:
    st.warning("⚠️ Nifty200list.csv सापडली नाही किंवा रिकामी आहे.")
else:
    # get_top10 internally handles rsi/macd/sector trend & scoring
    top10 = get_top10(df).copy()

    # Verdict column (जर verdict_logic उपलब्ध असेल तर)
    def _col(frame, name):
        for c in frame.columns:
            if c.lower() == name:
                return c
        return None

    rsi_col  = _col(top10, "rsi")
    macd_col = _col(top10, "macd")
    sect_col = _col(top10, "sector trend")

    if rsi_col and macd_col and sect_col:
        top10["Verdict"] = top10.apply(
            lambda row: get_trade_verdict(row[rsi_col], row[macd_col], row[sect_col]),
            axis=1
        )

    # Friendly display columns (जे आहेत तेच दाखवा)
    pref = ["stock", "sector", "rsi", "macd", "sector trend", "Verdict", "score"]
    show = [c for c in pref if c in top10.columns]
    st.dataframe(top10[show] if show else top10, use_container_width=True)

# -------- Section 2: Index Option Signals --------
st.subheader("📊 आजचे Index संकेत – Options Trading साठी")

# spot=None ठेवलं तर तुमच्या index_signals.generate_option_signal मध्ये
# तुम्ही ज्याप्रमाणे logic लिहिलंय त्याप्रमाणे वापरा.
# (जर तुमचा generate_option_signal स्पॉट हवाच म्हणत असेल, तर खालील dict मध्ये संख्या द्या.)
indices = {
    "Nifty50":  25200,   # <- हवे असल्यास None करा (auto) किंवा actual spot द्या
    "BankNifty": 55200,
    "FinNifty":  23200,
}

for name, spot in indices.items():
    sig = generate_option_signal(name=name, spot=spot, side="CALL")
    # जर तुमच्या index_signals मध्ये entry_band/target_pct/sl_pct parameters असतील तर
    # generate_option_signal(...) मध्ये तेही पास करू शकता.
    # उदा.: generate_option_signal(name, spot, side="CALL", entry_band_inr=entry_band, target_pct=target_pct, sl_pct=sl_pct)

    # Render
    st.markdown(
        f"**{sig.get('name', name)} {sig.get('strike', '')} {sig.get('direction', '')}**  \n"
        f"Spot: ₹{sig.get('spot', spot)}  \n"
        f"Recommended Price: **₹{sig.get('entry', sig.get('entry_low', '—'))}**  "
        f"(Band: {sig.get('entry_low', '—')}–{sig.get('entry_high', '—')})  \n"
        f"🎯 Target: **₹{sig.get('target', '—')}**   |   🛑 SL: **₹{sig.get('stoploss', '—')}**"
    )

st.caption("ℹ️ शिक्षणासाठी डेमो. Live trading आधी स्वतःची पडताळणी करा.")
