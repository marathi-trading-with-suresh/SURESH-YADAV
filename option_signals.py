# option_signals.py
# -----------------------------------------------------------
# Index Option Signal generator:
# - generate_option_signal(name, spot=None, side="CALL",
#                          entry_band_inr=2.0, target_pct=0.95, sl_pct=0.58)
# Returns: dict with name, strike, expiry, spot, entry_low/high/avg, target, stoploss, RR, verdict
# -----------------------------------------------------------

from datetime import date, datetime, timedelta
from math import log, sqrt, exp
from typing import Optional, Dict

import numpy as np
import pandas as pd
import yfinance as yf
from scipy.stats import norm


# ---------- utilities ----------
def _next_expiry(today: date) -> date:
    """Next weekly Thursday expiry. If Thu after 3:30 PM -> next week."""
    wd = today.weekday()            # Mon=0..Sun=6
    days = (3 - wd) % 7             # Thursday = 3
    expiry = today + timedelta(days=days)
    now = datetime.now().replace(microsecond=0)
    mclose = now.replace(hour=15, minute=30, second=0)
    if wd == 3 and now >= mclose:
        expiry += timedelta(days=7)
    if expiry <= today:
        expiry += timedelta(days=7)
    return expiry


def _nearest_strike(x: float, step: int) -> int:
    return int(round(x / step) * step)


def _bs_price(S, K, T, r, sigma, opt="C") -> float:
    """Black–Scholes premium (approx)."""
    if min(S, K, T, sigma) <= 0:
        return 0.0
    d1 = (log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    if opt == "C":
        return S * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)
    return K * exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)


def _hist_vol_yf(ticker: str, lookback=60, fallback=0.22) -> float:
    """Annualized hist vol from yfinance; fallback if not available."""
    try:
        df = yf.download(ticker, period="1y", interval="1d", progress=False, auto_adjust=True)
        rets = np.log(df["Close"] / df["Close"].shift(1)).dropna()
        vol = rets.tail(lookback).std() * sqrt(252)
        return float(vol) if np.isfinite(vol) and vol > 0 else fallback
    except Exception:
        return fallback


def _index_specs(name: str) -> Dict:
    """Strike step + yfinance ticker mapping for major indices."""
    n = name.strip().lower()
    if n in ("nifty", "nifty50", "nifty 50"):
        return {"step": 50, "yf": "^NSEI"}
    if n in ("banknifty", "nifty bank", "bank nifty", "niftybank"):
        return {"step": 100, "yf": "^NSEBANK"}
    if n in ("finnifty", "fin nifty", "nifty fin service", "nifty financial services"):
        # yfinance mapping for FinNifty can vary; adjust if needed
        return {"step": 50, "yf": "^NSEI"}  # fallback to Nifty spot if exact ticker unavailable
    # default fallback
    return {"step": 50, "yf": "^NSEI"}


# ---------- main API ----------
def generate_option_signal(
    name: str,
    spot: Optional[float] = None,
    side: str = "CALL",            # "CALL" / "PUT"
    entry_band_inr: float = 2.0,   # Recommended range width (₹)
    target_pct: float = 0.95,      # +95% of entry avg  (≈ almost double)
    sl_pct: float = 0.58,          # -58% of entry avg  (62 -> 26 approx)
    risk_free: float = 0.07,
) -> Dict:
    """
    Build option trade levels for the given index.
    - Chooses ATM strike using index-specific step.
    - Estimates premium with Black–Scholes using hist vol of the index.
    - Returns entry band (low/high), average entry, target, SL, and R:R verdict.
    """
    specs = _index_specs(name)
    expiry = _next_expiry(date.today())
    T = max((expiry - date.today()).days, 1) / 365.0

    # Get spot if not provided
    if spot is None:
        try:
            df = yf.download(specs["yf"], period="5d", interval="1m", progress=False)
            spot = float(df["Close"].dropna().iloc[-1])
        except Exception:
