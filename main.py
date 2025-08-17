import streamlit as st
from datetime import datetime

st.set_page_config(page_title="माझा ट्रेडिंग साथी – Suresh", layout="wide")

# 🟢 Header
st.title("📈 माझा ट्रेडिंग साथी – Suresh")
st.caption(f"🔄 Updated at: {datetime.now().strftime('%H:%M:%S')} IST")

# 📈 Nifty & Bank Nifty PCR Inputs
st.subheader("📊 Nifty & Bank Nifty PCR Input")

nifty_pcr = st.number_input("📈 Nifty PCR", min_value=0.0, max_value=2.0, value=0.79, step=0.01)
banknifty_pcr = st.number_input("🏦 Bank Nifty PCR", min_value=0.0, max_value=2.0, value=0.6982, step=0.01)

# 🧠 Signal Logic
def get_signal(pcr, index_name, strike):
    if pcr > 1.0:
        verdict = "✅ Call"
        caption = f"{index_name} वर तेजीचा सूर – Call @ {strike}"
    elif pcr < 1.0:
        verdict = "❌ Put"
        caption = f"{index_name} मध्ये दबाव – Put @ {strike}"
    else:
        verdict = "🟡 Hold"
        caption = f"{index_name} साठी थांबा – Range-bound"
    return verdict, caption

# 🎯 Strike Prices (editable)
nifty_strike = st.text_input("📈 Nifty Strike Price", value="24,700")
banknifty_strike = st.text_input("🏦 Bank Nifty Strike Price", value="55,500")

# 📊 Signal Output
nifty_verdict, nifty_caption = get_signal(nifty_pcr, "Nifty 50", nifty_strike)
banknifty_verdict, banknifty_caption = get_signal(banknifty_pcr, "Bank Nifty", banknifty_strike)

st.subheader("📈 Signal Summary")
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Nifty Verdict", value=nifty_verdict)
    st.success(nifty_caption)
with col2:
    st.metric(label="Bank Nifty Verdict", value=banknifty_verdict)
    st.error(banknifty_caption if "Put" in banknifty_verdict else banknifty_caption)

# 📤 Insta Caption Exporter
st.subheader("📤 Instagram Caption Exporter")
final_caption = f"📉 आजचे संकेत:\n{nifty_caption}\n{banknifty_caption}\n🎯 Target: 24,200 आणि 54,000\n#MarathiTrading #SureshSignals"

if st.button("Generate Marathi Caption"):
    st.text_area("📤 Caption तयार", value=final_caption, height=150)

# 🖼️ Footer
st.markdown("---")
st.markdown("© Suresh Yadav | Marathi Trading Dashboard")


