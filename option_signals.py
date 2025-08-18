# option_signals.py
# --- Generate Option Trading Signals for Nifty200 stocks ---

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import date, timedelta, datetime
from math import log, sqrt, exp
from scipy.stats import norm

# -----------------------
# Helper Functions
# -----------------------

def next_expiry(today: date) -> date:
    """Next Thursday expiry (default)."""
    weekday = today.weekday()  # Monday=0
    days_ahead = (3 - weekday) % 7  # Thursday = 3
    expiry = today + timedelta(days=days_ahead)
    now = datetime.now()
    market_close = now.replace(hour=15, minute=30, second=0, microsecond=0)
    if weekday == 3 and now >= market_close:
        expiry = expiry + timedelta(days=7)
    if expiry <= today:
        expiry = expiry + timedelta(days=7)
    return expiry

def hist_vol(prices: pd.Series, lookback: int = 30) -> float:
    """Annualized historical volatility."""
    returns = np.log(prices / prices.shift(1)).dropna()
    vol = returns.tail(lookback).std() * sqrt(252)
    return float(vol) if not np.isnan(vol) else 0.25

def black_scholes_price(S, K, T, r, sigma, option_type="C") -> float:
    """Black–Scholes option pricing."""
    if S <= 0 or K <= 0 or T <= 0 or sigma <= 0:
        return 0.0
    d1 = (log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    if option_type == "C":
        return S * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)
    else:
        return K * exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

def strike_step_from_price(price: float) -> int:
    """ATM strike step rule."""
    if price >= 1000:
        return 50
    if price >= 500:
        return 20
    if price >= 200:
        return 10
    if price >= 50:
        return 5
    return 1

def nearest_step(x: float, step: int) -> int:
    return int(round(x / step) * step)

def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    close = df["Close"]
    ema200 = close.ewm(span=200, adjust=False).mean()
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    delta = close.diff()
    gain = (delta.clip(lower=0)).ewm(alpha=1/14, adjust=False).mean()
    loss = (-delta.clip(upper=0)).ewm(alpha=1/14, adjust=False).mean()
    rs = gain / (loss + 1e-9)
    rsi = 100 - (100 / (1 + rs))
    out = pd.DataFrame({
        "close": close,
        "ema200": ema200,
        "macd": macd,
        "macd_signal": signal,
        "rsi": rsi
    })
    return out

def generate_signal(ind: pd.Series) -> str:
    """Buy/Sell rules."""
    if ind["close"] > ind["ema200"] and ind["rsi"] > 55 and ind["macd"] > ind["macd_signal"]:
        return "CALL"
    if ind["close"] < ind["ema200"] and ind["rsi"] < 45 and ind["macd"] < ind["macd_signal"]:
        return "PUT"
    return "HOLD"

# -----------------------
# Main function
# -----------------------

def get_option_signals(symbols_df, lookback=30, risk_free=0.07, sl_pct=25, trg_pct=40, limit=10):
    """Return top N option signals with ATM strike, premium, SL, Target."""
    expiry_dt = next_expiry(date.today())
    T = max((expiry_dt - date.today()).days, 1) / 365.0

    rows = []
    for _, row in symbols_df.iterrows():
        try:
            ticker = row["yahoo"]
            data = yf.download(ticker, period="6mo", interval="1d", progress=False, auto_adjust=True)
            if data.empty:
                continue
            ind_df = compute_indicators(data)
            last = ind_df.iloc[-1]
            signal = generate_signal(last)
            ltp = float(last["close"])
            step = strike_step_from_price(ltp)
            atm_strike = int(nearest_step(ltp, step))
            sigma = hist_vol(ind_df["close"], lookback)
            if signal == "CALL":
                est_premium = black_scholes_price(ltp, atm_strike, T, risk_free, sigma, "C")
            elif signal == "PUT":
                est_premium = black_scholes_price(ltp, atm_strike, T, risk_free, sigma, "P")
            else:
                est_premium = 0.0
            sl = est_premium * (1 - sl_pct / 100.0) if est_premium > 0 else 0.0
            target = est_premium * (1 + trg_pct / 100.0) if est_premium > 0 else 0.0
            strength = (last["close"] / last["ema200"]) if last["ema200"] > 0 else 0

            rows.append({
                "symbol": row["symbol"],
                "ltp": round(ltp, 2),
                "signal": signal,
                "atm_strike": atm_strike,
                "est_premium": round(est_premium, 2),
                "SL": round(sl, 2),
                "Target": round(target, 2),
                "RSI": round(last["rsi"], 1),
                "MACD": round(last["macd"], 2),
                "MACD_sig": round(last["macd_signal"], 2),
                "EMA200": round(last["ema200"], 2),
                "trend_strength": round(strength, 3)
            })
        except Exception as e:
            print(f"Error {row['symbol']}: {e}")

    signals_df = pd.DataFrame(rows)
    valid = signals_df[signals_df["signal"].isin(["CALL", "PUT"])]
    if valid.empty:
        return pd.DataFrame()
    return valid.sort_values(["trend_strength"], ascending=False).head(limit)