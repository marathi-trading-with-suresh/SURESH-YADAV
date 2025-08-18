import streamlit as st

def auto_column_mapper(df):
    column_map = {
        "stock": ["stock", "symbol", "company"],
        "sector": ["sector", "industry", "segment"],
        "rsi": ["rsi", "rsi value"],
        "macd": ["macd", "macd signal"],
        "sector trend": ["sector trend", "trend"]
    }

    df.columns = df.columns.str.strip().str.lower()
    renamed = {}
    for expected, options in column_map.items():
        for actual in options:
            if actual in df.columns:
                renamed[actual] = expected
                break

    df.rename(columns=renamed, inplace=True)

    missing = [col for col in column_map if col not in df.columns]
    if missing:
        st.warning("⚠️ काही अपेक्षित कॉलम सापडले नाहीत: " + ", ".join(missing))

    return df
