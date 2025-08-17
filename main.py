import streamlit as st
from datetime import datetime
from scanner_module import load_nifty200, get_top10, get_index_signals

# ✅ CSV फाईलचा योग्य path
CSV_PATH = "C:/Users/ASUS/OneDrive/Desktop/marathi_trade_with_suresh/Nifty200list.csv"

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


