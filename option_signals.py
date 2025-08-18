import random

def generate_option_signal(name, spot):
    strike = round(spot / 50) * 50 if "Nifty" in name else round(spot / 100) * 100
    direction = random.choice(["Call", "Put"])
    entry = random.randint(90, 180)
    target = entry + random.randint(30, 60)
    stoploss = entry - random.randint(20, 40)
    verdict = "🟢 खरेदी" if direction == "Call" else "🔴 विक्री"

    return {
        "name": name,
        "direction": direction,
        "strike": strike,
        "entry": entry,
        "target": target,
        "stoploss": stoploss,
        "verdict": verdict
    }
