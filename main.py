import streamlit as st
from datetime import datetime
from scanner_module import load_nifty200, get_top10, get_index_signals

CSV_PATH = "C:/Users/ASUS/Downloads/Telegram Desktop/Nifty200list.csv"

st.set_page_config(page_title="📊 Marathi Trading Dashboard", layout="centered")
st.title("📈 माझा ट्रेडिंग साथी – Suresh")
st.caption(f"🔄 Updated at: {datetime.now().strftime('%H:%M:%S')} IST")

# 📥 Stock Suggestions
df = load_nifty200(CSV_PATH)
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
