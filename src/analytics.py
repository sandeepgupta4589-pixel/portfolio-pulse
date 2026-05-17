import pandas as pd
from typing import Dict, List, Optional


def simple_moving_average(prices: pd.Series, window: int) -> Optional[float]:
    if len(prices) < window:
        return None
    return float(prices.rolling(window=window).mean().iloc[-1])


def compute_rsi(prices: pd.Series, window: int = 14) -> Optional[float]:
    if len(prices) < window + 1:
        return None
    delta = prices.diff().dropna()
    gain = delta.clip(lower=0).rolling(window=window).mean()
    loss = -delta.clip(upper=0).rolling(window=window).mean()
    rs = gain / loss
    return float(100 - (100 / (1 + rs.iloc[-1])))


def compute_atr(high: pd.Series, low: pd.Series, close: pd.Series, window: int = 14) -> Optional[float]:
    if len(close) < window + 1:
        return None
    tr1 = high - low
    tr2 = (high - close.shift()).abs()
    tr3 = (low - close.shift()).abs()
    true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    return float(true_range.rolling(window=window).mean().iloc[-1])


def compute_52_week_range(prices: pd.Series) -> Optional[Dict[str, float]]:
    if len(prices) < 252:
        return None
    return {
        "low": float(prices.min()),
        "high": float(prices.max()),
    }


def extract_price_series(history: List[Dict]) -> pd.DataFrame:
    rows = []
    for item in history:
        rows.append({
            "date": item.get("date"),
            "open": float(item.get("open", 0)),
            "high": float(item.get("high", 0)),
            "low": float(item.get("low", 0)),
            "close": float(item.get("close", 0)),
            "volume": int(item.get("volume", 0)),
        })
    df = pd.DataFrame(rows)
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date")
        df = df.set_index("date")
    return df


def estimate_mark_to_market_pnl(position: Dict, option_quote: Dict) -> Dict:
    current = float(option_quote.get("last", 0) or option_quote.get("ask", 0))
    quantity = int(position.quantity)
    multiplier = 100
    value = current * quantity * multiplier
    pnl = None
    if position.entry_price is not None:
        pnl = (current - position.entry_price) * quantity * multiplier
    return {
        "mark_price": current,
        "position_value": value,
        "estimated_pnl": pnl,
    }
