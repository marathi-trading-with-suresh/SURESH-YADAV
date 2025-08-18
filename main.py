import streamlit as st
import pandas as pd
from datetime import datetime
from utils import (
    validate_csv_columns,
    filter_top_stocks,
    get_emoji_verdict,
    generate_marathi_caption,
    safe_display_dataframe
)

# 📂 CSV path
CSV_PATH = "Nifty200list.csv"

# 🖥️ Streamlit UI
st.set_page_config(page_title="📊 माझा ट्रेडिंग साथी – Suresh", layout="centered")
st.title("📈 माझा ट्रेडिंग साथी – Suresh")
st.caption(f"🔄 अपडेट वेळ: {datetime.now().strftime('%H:%M:%S')} IST")

# 📥 CSV लोड करा
try:
    df = pd.read_csv(CSV_PATH)
    st.success("✅ Nifty200 CSV यशस्वीपणे लोड झाली!")
except FileNotFoundError:
    st.error("❌ CSV फाईल सापडली नाही. कृपया path तपासा.")
    st.stop()

# 🛡️ आवश्यक कॉलम्स तपासा
required_cols = ["stock", "sector", "rsi", "macd", "sector trend"]
if not validate_csv_columns(df, required_cols):
    st.stop()

# 🔍 टॉप 10 स्टॉक्स निवडा
top10 = filter_top_stocks(df)

# 🧠 Verdict आणि Caption तयार करा
top10["Verdict"] = top10.apply(get_emoji_verdict, axis=1)
top10["Caption"] = top10.apply(lambda row: generate_marathi_caption(row["stock"], row["Verdict"]), axis=1)

# 📊 डिस्प्ले टेबल
display_cols = ["stock", "sector", "rsi", "macd", "sector trend", "Verdict", "Caption"]
safe_display_dataframe(top10, display_cols, title="📌 आजचे Intraday Stocks – Nifty200 मधून")
