import os
import sys
sys.path.append(os.path.dirname(__file__))

import streamlit as st
from scanner_module import scan_stocks  # ✅ Fixed import

# 📊 Marathi Trading Dashboard
st.set_page_config(page_title="📈 माझा ट्रेडिंग साथी", layout="wide")

st.title("📊 माझा ट्रेडिंग साथी – Suresh")
st.markdown("#### आजचे ट्रेडिंग सल्ले आणि ऑप्शन सिग्नल्स")

# 🔍 Scan stocks
try:
    stock_data = scan_stocks()
    for stock in stock_data:
        st.write(f"🟢 {stock['name']} | स्ट्राइक प्राइस: ₹{stock['strike']} | Verdict: {stock['verdict']}")
except Exception as e:
    st.error(f"डेटा मिळवताना त्रुटी आली: {e}")

# 📢 Footer
st.markdown("---")
st.caption("© Suresh Yadav | Insta-ready | Mentor-grade Marathi dashboard")

