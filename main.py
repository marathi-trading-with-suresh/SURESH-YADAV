import streamlit as st
import scanner_module  # ✅ Standard import

# 📊 Page config + Marathi header
st.set_page_config(page_title="📈 माझा ट्रेडिंग साथी", layout="centered")
st.markdown("<h1 style='text-align: center;'>📈 माझा ट्रेडिंग साथी – Suresh</h1>", unsafe_allow_html=True)
st.markdown("#### आजचे ट्रेडिंग सल्ले आणि ऑप्शन सिग्नल्स")

# 🔁 Refresh button
if st.button("🔁 डेटा Refresh करा"):
    st.experimental_rerun()

# 🔍 Scan stocks + display Marathi captions
stock_data = []
try:
    stock_data = scanner_module.scan_stocks()
    for stock in stock_data:
        st.write(stock["caption"])
except Exception as e:
    st.error(f"डेटा मिळवताना त्रुटी आली: {e}")

# 📤 Insta Caption Exporter
if stock_data:
    with st.expander("📤 Instagram साठी Caption Export करा"):
        captions = "\n".join([s["caption"] for s in stock_data])
        st.code(captions, language="markdown")

# 📅 Timestamp + Footer
if stock_data:
    st.markdown("---")
    st.caption(f"🔄 शेवटचा अपडेट: {stock_data[0]['timestamp']}")
st.caption("© Suresh Yadav | Insta-ready | Mentor-grade Marathi dashboard")
