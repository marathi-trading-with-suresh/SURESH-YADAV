import os
import importlib.util
import streamlit as st

# ✅ Load scanner_module.py dynamically
module_path = os.path.join(os.path.dirname(__file__), "scanner_module.py")
spec = importlib.util.spec_from_file_location("scanner_module", module_path)
scanner_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scanner_module)

scan_stocks = scanner_module.scan_stocks  # ✅ Now available

# 📊 Page config + Marathi header
st.set_page_config(page_title="📈 माझा ट्रेडिंग साथी", layout="centered")
st.markdown("<h1 style='text-align: center;'>📈 माझा ट्रेडिंग साथी – Suresh</h1>", unsafe_allow_html=True)
st.markdown("#### आजचे ट्रेडिंग सल्ले आणि ऑप्शन सिग्नल्स")

# 🔁 Refresh button
if st.button("🔁 डेटा Refresh करा"):
    st.experimental_rerun()

# 🔍 Scan stocks + display Marathi captions
try:
    stock_data = scan_stocks()
    for stock in stock_data:
        st.write(stock["caption"])
except Exception as e:
    st.error(f"डेटा मिळवताना त्रुटी आली: {e}")

# 📤 Insta Caption Exporter
with st.expander("📤 Instagram साठी Caption Export करा"):
    captions = "\n".join([s["caption"] for s in stock_data])
    st.code(captions, language="markdown")

# 📅 Timestamp + Footer
st.markdown("---")
st.caption(f"🔄 शेवटचा अपडेट: {stock_data[0]['timestamp']}")
st.caption("© Suresh Yadav | Insta-ready | Mentor-grade Marathi dashboard")


