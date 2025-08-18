def get_top10(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    def _find_col(frame, names):
        low = {c.lower(): c for c in frame.columns}
        for n in names:
            if n.lower() in low:
                return low[n.lower()]
        return None

    col_stock = _find_col(df, ["stock", "symbol", "name"])
    col_sector = _find_col(df, ["sector", "industry"])
    col_rsi = _find_col(df, ["rsi"])
    col_macd = _find_col(df, ["macd"])
    col_sector_trend = _find_col(df, ["sector trend", "sector_trend", "trend"])

    work = df.copy()
    work["score"] = 0

    # RSI rule (numeric cast)
    if col_rsi:
        rsi_num = pd.to_numeric(work[col_rsi], errors="coerce")
        work.loc[rsi_num > 55, "score"] += 1

    # MACD rule (text == 'bullish')
    if col_macd:
        macd_series = work[col_macd].astype(str).str.strip().str.lower()
        work.loc[macd_series == "bullish", "score"] += 1

    # Sector Trend rule (positive/up/bullish)
    if col_sector_trend:
        sect_series = work[col_sector_trend].astype(str).str.strip().str.lower()
        work.loc[sect_series.isin({"positive", "up", "bullish"}), "score"] += 1

    # Order and top 10
    top10 = work.sort_values("score", ascending=False).head(10).copy()

    # Friendly column names
    if col_stock and "stock" not in top10.columns:
        top10.rename(columns={col_stock: "stock"}, inplace=True)
    if col_sector and "sector" not in top10.columns:
        top10.rename(columns={col_sector: "sector"}, inplace=True)
    if col_rsi and "rsi" not in top10.columns:
        top10.rename(columns={col_rsi: "rsi"}, inplace=True)
    if col_macd and "macd" not in top10.columns:
        top10.rename(columns={col_macd: "macd"}, inplace=True)
    if col_sector_trend and "sector trend" not in top10.columns:
        top10.rename(columns={col_sector_trend: "sector trend"}, inplace=True)

    return top10
