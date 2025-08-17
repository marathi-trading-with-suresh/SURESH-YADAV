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

# 📤 Caption Exporter
st.subheader("📤 Instagram Caption Exporter")
selected_caption = options_data["Caption"][0]  # Default caption
if st.button("Generate Marathi Caption"):
    st.success(f"✅ Caption तयार: \n\n{selected_caption}")

# 🖼️ Footer
st.markdown("---")
st.markdown("© Suresh Yadav | Marathi Trading Dashboard")
