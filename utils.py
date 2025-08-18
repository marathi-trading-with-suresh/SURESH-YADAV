import streamlit as st

def auto_column_mapper(df):
    """
    कोणत्याही CSV मध्ये अपेक्षित कॉलम्स शोधून rename करणारे फंक्शन.
    वापरकर्त्याला मराठीत संदेश देतो आणि fallback logic वापरतो.
    """

    # ✅ अपेक्षित कॉलम्स आणि त्यांचे संभाव्य पर्याय
    column_map = {
        "stock": ["stock", "symbol", "company"],
        "sector": ["sector", "industry", "segment"],
        "rsi": ["rsi", "rsi value"],
        "macd": ["macd", "macd signal", "macd line", "macd histogram"],
        "sector trend": ["sector trend", "trend", "sector outlook"]
    }

    # 📋 Normalize कॉलम्स
    df.columns = df.columns.str.strip().str.lower()

    # 🔁 Rename logic
    renamed = {}
    for expected, options in column_map.items():
        for actual in options:
            if actual in df.columns:
                renamed[actual] = expected
                break

    df.rename(columns=renamed, inplace=True)

    # 🛡️ Missing कॉलम्स तपासा
    missing = [col for col in column_map if col not in df.columns]
    if missing:
        st.warning("⚠️ काही अपेक्षित कॉलम सापडले नाहीत: " + ", ".join(missing))

    return df
