# scanner_module.py
import pandas as pd
import os
import random

def load_nifty200(csv_path):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV फाईल सापडली नाही: {csv_path}")
    df = pd.read_csv(csv_path)
    df = df[df["Symbol"].notna()]
    return df

def get_top10(df):
    return df.sample(10).reset_index(drop=True)

def get_index_signals():
    index_data = []

    # Nifty
    nifty_spot = 22450
    nifty_strike = round(nifty_spot / 50) * 50
    nifty_direction = random.choice(["Call", "Put"])
    nifty_entry = 110 if nifty_direction == "Call" else 95
    nifty_target = nifty_entry + 40
    nifty_stoploss = nifty_entry - 25

    index_data.append({
        "Index": "Nifty",
        "Type": nifty_direction,
        "Strike": nifty_strike,
        "Premium": nifty_entry,
        "Target": nifty_target,
        "Stoploss": nifty_stoploss
    })

    # BankNifty
    banknifty_spot = 48200
    banknifty_strike = round(banknifty_spot / 100) * 100
    banknifty_direction = random.choice(["Call", "Put"])
    banknifty_entry = 180 if banknifty_direction == "Call" else 160
    banknifty_target = banknifty_entry + 60
    banknifty_stoploss = banknifty_entry - 40

    index_data.append({
        "Index": "BankNifty",
        "Type": banknifty_direction,
        "Strike": banknifty_strike,
        "Premium": banknifty_entry,
        "Target": banknifty_target,
        "Stoploss": banknifty_stoploss
    })

    return index_data
