def get_trade_verdict(rsi, macd, sector_trend):
    if rsi > 55 and macd.lower() == "bullish" and sector_trend.lower() == "positive":
        return "🟢 खरेदी"
    elif rsi < 45 and macd.lower() == "bearish" and sector_trend.lower() == "negative":
        return "🔴 विक्री"
    else:
        return "⚪️ थांबा"
