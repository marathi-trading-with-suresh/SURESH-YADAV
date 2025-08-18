# index_signals.py
# --- Generate Option Trading Signals for Indexes (Nifty/BankNifty etc.) ---

from typing import Dict
from scipy.stats import norm as _norm

def generate_option_signal(name: str, spot: int, side: str = "CALL") -> Dict:
    """
    दिलेल्या Index साठी Option Trading Signal तयार करा.
    Rules (demo):
      - spot round to nearest 50
      - CALL = खरेदी, PUT = विक्री
    """
    if not spot:
        return {
            "name": name,
            "direction": "NA",
            "strike": 0,
            "entry": 0,
            "target": 0,
            "stoploss": 0,
            "verdict": "NA",
        }

    strike = round(spot / 50) * 50
    entry = 100
    target = int(entry * 1.4)
    stoploss = int(entry * 0.8)

    return {
        "name": name,
        "direction": side,
        "strike": strike,
        "entry": entry,
        "target": target,
        "stoploss": stoploss,
        "verdict": "खरेदी" if side.upper() == "CALL" else "विक्री",
    }
