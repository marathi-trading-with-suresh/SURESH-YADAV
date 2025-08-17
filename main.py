import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="माझा ट्रेडिंग साथी – Suresh", layout="wide")

# 🟢 Header
st.title("📈 माझा ट्रेडिंग साथी – Suresh")
st.caption(f"🔄 Updated at: {datetime.now().strftime('%H:%M:%S')} IST")

# 📈 Intraday Stock Suggestions
st.subheader("📊 Intraday Stock Suggestions")
intraday_data = pd.DataFrame({
    "Stock": ["TATASTEEL", "RELIANCE", "INFY"],
    "Verdict": ["✅ Buy", "❌ Sell", "🟡 Hold"],
    "Strike Price": ["₹1420 CE", "₹2600 PE", "₹1500 CE"],
    "Marathi Caption": [
        "TATASTEEL वर खरेदीचा सूर – ₹1420 CE",
        "RELIANCE मध्ये विक्रीचा इशारा – ₹2600 PE",
        "INFY साठी थांबा – ₹1500 CE"
    ]
})
st.dataframe(intraday_data, use_container_width=True)

# 📊 Options Trading Signals
with st.expander("📈 Options Trading Signals"):
    options_data = pd.DataFrame({
        "Stock": ["TATASTEEL", "RELIANCE"],
        "Expiry": ["22 Aug", "22 Aug"],
        "Strike": ["₹1420 CE", "₹2600 PE"],
        "Signal": ["Buy", "Sell"],
        "Verdict": ["✅", "❌"],
        "Caption": [
            "📈 TATASTEEL ₹1420 CE – खरेदी करा",
            "📉 RELIANCE ₹2600 PE – विक्री करा"
        ]
    })
    st.table(options_data)

# 📈 Nifty & Bank Nifty PCR Signals
st.subheader("📈 Nifty & Bank Nifty Call-Put Signals")

# Static PCR values (can be automated later)
nifty_pcr = 1.0905
banknifty_pcr = 0.6982

def get_signal(pcr):
    if pcr > 1.0:
        return "✅ Call Signal – Bullish"
    elif pcr < 1.0:
        return "❌ Put Signal – Bearish"
    else:
        return "🟡 Neutral – Range-bound"

nifty_signal = get_signal(nifty_pcr)
banknifty_signal = get_signal(banknifty_pcr)

st.metric(label="📈 Nifty PCR", value=nifty_pcr, delta=nifty_signal)
st.metric(label="🏦 Bank Nifty PCR", value=banknifty_pcr, delta=banknifty_signal)

# 📤 Marathi Caption Exporter
st.subheader("📤 Instagram Caption Exporter")

nifty_caption = f"📈 Nifty PCR {nifty_pcr} – खरेदीचा सूर" if "Call" in nifty_signal else f"📈 Nifty PCR {nifty_pcr} – विक्रीचा इशारा"
banknifty_caption = f"🏦 Bank Nifty PCR {banknifty_pcr} – खरेदीचा सूर" if "Call" in banknifty_signal else f"🏦 Bank Nifty PCR {banknifty_pcr} – विक्रीचा इशारा"

final_caption = f"{nifty_caption}\n{banknifty_caption}\n#MarathiTrading #SureshSignals"

if st.button("Generate Marathi Caption"):
    st.success(f"✅ Caption तयार:\n\n{final_caption}")

# 🖼️ Footer
st.markdown("---")
st.markdown("© Suresh Yadav | Marathi Trading Dashboard")

