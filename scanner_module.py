import pandas as pd

# ✅ Nifty200 CSV Load करणारी Function
def load_nifty200(csv_path="Nifty200list.csv"):
    """Nifty200 CSV फाईल लोड करा"""
    try:
        df = pd.read_csv(csv_path)
        return df
    except Exception as e:
        print(f"Error loading {csv_path}: {e}")
        return pd.DataFrame()

# ✅ Top 10 stocks मिळवणारी Function
def get_top10(df):
    """Top 10 Intraday Stocks काढा (score नुसार)"""
    df["score"] = 0
    df.loc[df["rsi"] > 55, "score"] += 1
    df.loc[df["macd"].astype(str).str.lower() == "bullish", "score"] += 1
    df.loc[df["sector trend"].astype(str).str.lower() == "positive", "score"] += 1
    return df.sort_values(by="score", ascending=False).head(10).copy()

# ✅ Index Options signals (demo)
def get_index_signals():
    """Index Options signals परत करा"""
    indices = {
        "Nifty50": 22450,
        "BankNifty": 48200,
        "Sensex": 74200,
        "Midcap": 37000,
        "Smallcap": 14500,
        "FinNifty": 21500
    }

    signals = []
    for name, spot in indices.items():
        signals.append({
            "name": name,
            "spot": spot,
            "direction": "CALL" if spot % 2 == 0 else "PUT",
            "strike": round(spot / 50) * 50,
            "entry": 100,
            "target": 140,
            "stoploss": 80,
            "verdict": "खरेदी" if spot % 2 == 0 else "विक्री"
        })
    return signals
