import datetime

def scan_stocks():
    suggestions = [
        {"stock": "टाटा मोटर्स", "strike": 720, "verdict": "बाय करा 🚀"},
        {"stock": "रिलायन्स", "strike": 2450, "verdict": "थांबा ⏳"},
        {"stock": "इन्फोसिस", "strike": 1520, "verdict": "सेल करा 📉"}
    ]
    timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
    return {
        "timestamp": timestamp,
        "stocks": suggestions
    }