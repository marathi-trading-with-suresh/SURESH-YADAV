import streamlit as st

def safe_display_dataframe(df, expected_cols, title="📊 आजचे स्टॉक्स"):
    available_cols = [col for col in expected_cols if col in df.columns]
    st.subheader(title)
    if available_cols:
        st.dataframe(df[available_cols])
    else:
        st.warning("⚠️ अपेक्षित कॉलम उपलब्ध नाहीत.")

def validate_csv_columns(df, required_cols):
    missing_cols = set(required_cols) - set(df.columns)
    if missing_cols:
        st.error("❌ काही आवश्यक कॉलम नाहीत: " + ", ".join(missing_cols))
        return False
    return True