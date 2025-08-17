import datetime

def scan_stocks():
    now = datetime.datetime.now().strftime("%d-%m-%Y %I:%M %p")

    stocks = [
        {"name": "TCS", "strike": 3800, "verdict": "✅ BUY"},
        {"name": "INFY", "strike": 1450, "verdict": "⚠️ WATCH"},
        {"name": "RELIANCE", "strike": 2500, "verdict": "❌ AVOID"},
    ]

    verdict_map = {
        "✅ BUY": "🟢 खरेदी",
        "⚠️ WATCH": "🟡 निरीक्षण",
        "❌ AVOID": "🔴 टाळा"
    }

    enhanced = []
    for stock in stocks:
        verdict = verdict_map.get(stock["verdict"], stock["verdict"])
        caption = f"{stock['name']} – स्ट्राइक ₹{stock['strike']} – {verdict}"
        enhanced.append({
            "name": stock["name"],
            "strike": stock["strike"],
            "verdict": verdict,
            "caption": caption,
            "timestamp": now
        })

    return enhanced
