import streamlit as st
import pandas as pd

# आपले modules
from scanner_module import load_nifty200, get_top10
from index_signals import generate_option_signal

# ----------------------------
# Streamlit App सुरू
# ----------------------------
st.set_page_config(page_title="📈 मराठी Trade with Suresh", layout="wide")

st.title("📈 मराठी Trade with Suresh")
st.markdown("Intraday Stock Scanner + Index Option Signals")

# ----------------------------
# Sidebar Parameters
# ----------------------------
st.sidebar.header("⚙️ Parameters")
entry_band = st.sidebar.slider("Entry band (₹)", 1.0, 5.0, 2.0, 0.5)
target_pct = st.sidebar.slider("Target % of entry", 0.5, 1.5, 0.95, 0.05)
sl_pct     = st.sidebar.slider("SL % of entry", 0.3, 0.8, 0.58, 0.02)

# ----------------------------
# Section 1: Nifty200 CSV Loader
# ----------------------------
st.subheader("📊 Nifty200 Intraday Scanner")

df = load_nifty200("Nifty200list.csv")
if df.empty:
    st.warning("⚠️ Nifty200list.csv सापडली नाही किंवा रिकामी आहे.")
else:
    top10 = get_top10(df).copy()
    st.dataframe(top10, use_container_width=True)

# ----------------------------
# Section 2: Index Option Signals
# ----------------------------
st.subheader("📊 आजचे Index संकेत – Options Trading साठी")

indices = {
    "Nifty50": None,     # spot=None => auto fetch from yfinance
    "BankNifty": None,
    "FinNifty": None,
}

for name, spot in indices.items():
    sig = generate_option_signal(
        name=name,
        spot=spot,            # जर manually द्यायचा असेल तर इथे number टाक
        side="CALL",          # "PUT" हवा असेल तर बदल
        entry_band_inr=entry_band,
        target_pct=target_pct,
        sl_pct=sl_pct,
    )

    st.markdown(
        f"**{sig['name']} {sig['expiry']} {sig['strike']} {sig['direction']}**  \n"
        f"Spot: ₹{sig['spot']}  \n"
        f"Recommended Price: **₹{sig['entry_low']} – ₹{sig['entry_high']}**  \n"
        f"🎯 Target: **₹{sig['target']}**   |   🛑 SL: **₹{sig['stoploss']}**  \n"
        f"R:R ≈ {sig['risk_reward']}  |  Verdict: **{sig['verdict']}**"
    )

