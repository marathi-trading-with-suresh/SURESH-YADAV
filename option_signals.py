# ---- option_signals.py (append or replace) ----
from datetime import date, datetime, timedelta
from math import log, sqrt, exp
from typing import Optional, Dict

import numpy as np
import pandas as pd
import yfinance as yf
from scipy.stats import norm

# ---------- helpers ----------
def _next_expiry(today: date) -> date:
    """Next weekly Thursday expiry (post-Thu 3:30pm -> next week)."""
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

def _bs_price(S, K, T, r, sigma, opt="C"):
    if min(S, K, T, sigma) <= 0:
        return 0.0
    d1 = (log(S/K) + (r + 0.5*sigma*sigma)*T) / (sigma*sqrt(T))
    d2 = d1 - sigma*sqrt(T)
    if opt == "C":
        return S*norm.cdf(d1) - K*exp(-r*T)*norm.cdf(d2)
    return K*exp(-r*T)*norm.cdf(-d2) - S*norm.cdf(-d1)

def _hist_vol(ticker: str, lookback=60, fallback=0.22) -> float:
    try:
        df = yf.download(ticker, period="1y", interval="1d", progress=False, auto_adjust=True)
        rets = np.log(df["Close"] / df["Close"].shift(1)).dropna()
        vol = rets.tail(lookback).std() * sqrt(252)
        return float(vol) if np.isfinite(vol) and vol > 0 else fallback
    except Exception:
        return fallback

def _index_specs(name: str) -> Dict:
    """Step + yfinance ticker for spot fetching."""
    n = name.strip().lower()
    if n in ("nifty", "nifty50", "nifty 50"):
        return {"step": 50,  "yf": "^NSEI"}              # fallback ticker
    if n in ("banknifty", "nifty bank", "bank nifty"):
        return {"step": 100, "yf": "^NSEBANK"}
    if n in ("finnifty", "fin nifty", "nifty fin service"):
        return {"step": 50,  "yf": "NIFTY_FIN_SERVICE.NS"}  # may vary on yfinance
    # default
    return {"step": 50, "yf": "^NSEI"}

def _nearest_strike(x: float, step: int) -> int:
    return int(round(x / step) * step)

# ---------- main API ----------
def generate_option_signal(
    name: str,
    spot: Optional[float] = None,
    side: str = "CALL",            # "CALL" / "PUT"
    entry_band_inr: float = 2.0,   # Recommended range width (₹)
    target_pct: float = 0.90,      # +90% of entry avg -> ~double
    sl_pct: float = 0.58,          # -58% of entry avg (entry 62 -> SL ~26)
    risk_free: float = 0.07,
) -> Dict:
    """
    Returns dict with: name, direction, strike, expiry, entry_low, entry_high, entry, target, stoploss, verdict.
    - Premium is estimated by Black-Scholes using hist vol of the index ticker (rough estimate).
    - Entry range is centered around estimated premium (± entry_band_inr/2).
    """

    specs = _index_specs(name)
    expiry = _next_expiry(date.today())
    T = max((expiry - date.today()).days, 1) / 365.0

    # spot fetch if not supplied
    if spot is None:
        try:
            tkr = specs["yf"]
            df = yf.download(tkr, period="5d", interval="1m", progress=False)
            spot = float(df["Close"].dropna().iloc[-1])
        except Exception:
            spot = 25000.0  # safe fallback

    step = specs["step"]
    strike = _nearest_strike(spot, step)

    # sigma from index hist vol
    sigma = _hist_vol(specs["yf"], lookback=60, fallback=0.22)

    # estimated premium
    opt_type = "C" if side.upper().startswith("C") else "P"
    est = _bs_price(spot, strike, T, risk_free, sigma, opt=opt_type)
    est = float(max(est, 1.0))  # avoid too small

    # entry band & risk management
    entry_low  = max(1.0, round(est - entry_band_inr/2))
    entry_high = round(est + entry_band_inr/2)
    entry_avg  = round((entry_low + entry_high) / 2)

    target  = max(1.0, round(entry_avg * (1 + target_pct)))
    stoploss = max(1.0, round(entry_avg * (1 - sl_pct)))

    rr = (target - entry_avg) / max(1e-6, (entry_avg - stoploss))
    verdict = "खरेदी" if rr >= 1.2 else "थांबा"

    return {
        "name": name.upper(),
        "direction": "CALL" if opt_type == "C" else "PUT",
        "strike": strike,
        "expiry": expiry.strftime("%d-%b-%y"),
        "spot": round(spot, 2),
        "entry_low": entry_low,
        "entry_high": entry_high,
        "entry": entry_avg,
        "target": target,
        "stoploss": stoploss,
        "risk_reward": round(rr, 2),
        "verdict": verdict,
    }
