def get_trade_verdict(rsi, macd, sector_trend):
    macd = str(macd).lower()
    sector_trend = str(sector_trend).lower()

    if rsi > 55 and macd == "bullish" and sector_trend == "positive":
        return "🟢 खरेदी"
    elif rsi < 45 and macd == "bearish" and sector_trend == "negative":
        return "🔴 विक्री"
    else:
        return "⚪️ थांबा"
