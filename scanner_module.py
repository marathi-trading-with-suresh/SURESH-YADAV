# scanner_module.py
# Utility helpers + core functions used by main.py
# - load_nifty200(csv_path)      -> DataFrame
# - get_top10(df)                -> DataFrame (Top 10 by score)
# - get_index_signals()          -> List[Dict] (demo index option signals)

from typing import List, Dict
import pandas as pd

# -----------------------------
# 1) Nifty200 CSV Loader
# -----------------------------
def load_nifty200(csv_path="Nifty200list.csv"):
    ...

    """
    Nifty200 CSV फाईल लोड करा.
    अपेक्षित कॉलम्स (case-insensitive): stock/symbol, sector, rsi, macd, sector trend
    """
    try:
        df = pd.read_csv(csv_path)
        # Trim spaces in column names
        df.columns = [c.strip() for c in df.columns]
        return df
    except Exception as e:
        print(f"[load_nifty200] Error loading {csv_path}: {e}")
        return pd.DataFrame()

# -----------------------------
# Internals: column resolver
# -----------------------------
def _find_col(df: pd.DataFrame, candidates: List[str]) -> str:
    """
    दिलेल्या संभाव्य नावांपैकी (case-insensitive) जो कॉलम आहे तो परत करते.
    न मिळाल्यास रिकामं स्ट्रिंग परत करते.
    """
    lowmap = {c.lower(): c for c in df.columns}
    for name in candidates:
        key = name.lower()
        if key in lowmap:
            return lowmap[key]
    return ""

# -----------------------------
# 2) Top 10 Stock Scanner
# -----------------------------
def get_top10(df: pd.DataFrame) -> pd.DataFrame:
    """
    RSI + MACD + Sector Trend वरून score काढून Top 10 परत करा.
    नियम:
      - RSI > 55  => +1
      - MACD == 'bullish' (text) => +1
      - Sector Trend in {'positive','up','bullish'} => +1
    """
    if df.empty:
        return df

    # Resolve columns (case-insensitive, flexible names)
    col_stock = _find_col(df, ["stock", "symbol", "name"])
    col_sector = _find_col(df, ["sector", "industry"])
    col_rsi = _find_col(df, ["rsi"])
    col_macd = _find_col(df, ["macd"])
    col_sector_trend = _find_col(df, ["sector trend", "sector_trend", "trend"])

    # If missing essential cols, just return top 10 rows with a warning score
    work = df.copy()
    if not col_rsi:
        work["score"] = 0
        return work.head(10)

    # Start with zero score
    work["score"] = 0

    # RSI rule
    with pd.option_context("mode.chained_assignment", None):
        work.loc[pd.to_numeric(work[col_rsi], errors="coerce") > 55, "score"] += 1

    # MACD rule (treat string "bullish" as positive)
    if col_macd:
        macd_series = work[col_macd].astype(str).str.strip().str.lower()
        work.loc[macd_series == "bullish", "score"] += 1

    # Sector Trend rule
    if col_sector_trend:
        pos_vals = {"positive", "up", "bullish"}
        sect_series = work[col_sector_trend].astype(str).strip().str.lower()
        work.loc[sect_series.isin(pos_vals), "score"] += 1

    # Order by score desc and pick top 10
    top10 = work.sort_values(by="score", ascending=False).head(10).copy()

    # Ensure display-friendly columns exist
    if "stock" not in top10.columns and col_stock:
        top10.rename(columns={col_stock: "stock"}, inplace=True)
    if "sector" not in top10.columns and col_sector:
        top10.rename(columns={col_sector: "sector"}, inplace=True)
    if "rsi" not in top10.columns and col_rsi:
        top10.rename(columns={col_rsi: "rsi"}, inplace=True)
    if "macd" not in top10.columns and col_macd:
        top10.rename(columns={col_macd: "macd"}, inplace=True)
    if "sector trend" not in top10.columns and col_sector_trend:
        top10.rename(columns={col_sector_trend: "sector trend"}, inplace=True)

    return top10

# -----------------------------
# 3) Index Option Signals (demo)
# -----------------------------
def get_index_signals() -> List[Dict]:
    """
    Demo index option signals (static spot values).
    तुमच्या गरजेनुसार इथे live/derived logic जोडू शकता.
    """
    indices = {
        "Nifty50": 22450,
        "BankNifty": 48200,
        "Sensex": 74200,
        "Midcap": 37000,
        "Smallcap": 14500,
        "FinNifty": 21500,
    }

    out: List[Dict] = []
    for name, spot in indices.items():
        # Simple demo rule: even spot -> CALL, odd -> PUT
        direction = "CALL" if (spot % 2 == 0) else "PUT"
        # Nearest strike step assumption (50)
        strike = round(spot / 50) * 50
        signal = {
            "name": name,
            "spot": spot,
            "direction": direction,
            "strike": strike,
            "entry": 100,      # demo premium
            "target": 140,     # demo target
            "stoploss": 80,    # demo stoploss
            "verdict": "खरेदी" if direction == "CALL" else "विक्री",
        }
        out.append(signal)
    return out

