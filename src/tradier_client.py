import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from .config import TRADIER_SANDBOX_TOKEN

BASE_URL = "https://sandbox.tradier.com/v1"


def _get_headers() -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {TRADIER_SANDBOX_TOKEN}",
        "Accept": "application/json",
    }


def get_stock_quote(symbol: str) -> Dict:
    if not TRADIER_SANDBOX_TOKEN:
        return {"error": "missing Tradier sandbox token"}

    response = requests.get(
        f"{BASE_URL}/markets/quotes",
        headers=_get_headers(),
        params={"symbols": symbol},
    )
    response.raise_for_status()
    payload = response.json()
    quote = payload.get("quotes", {}).get("quote", {})
    return quote


def get_historical_prices(symbol: str, start_date: str, end_date: str) -> List[Dict]:
    if not TRADIER_SANDBOX_TOKEN:
        return []

    response = requests.get(
        f"{BASE_URL}/markets/history",
        headers=_get_headers(),
        params={"symbol": symbol, "start": start_date, "end": end_date, "interval": "daily"},
    )
    response.raise_for_status()
    payload = response.json()
    return payload.get("history", {}).get("day", [])


def find_option_quote(symbol: str, expiry: str, strike: float, option_type: str) -> Optional[Dict]:
    if not TRADIER_SANDBOX_TOKEN:
        return None

    response = requests.get(
        f"{BASE_URL}/markets/options/chains",
        headers=_get_headers(),
        params={"symbol": symbol, "expiration": expiry, "greeks": "false"},
    )
    response.raise_for_status()
    payload = response.json()
    chain = payload.get("options", {}).get("option", [])
    target = None
    for option in chain:
        if option.get("strike") == strike and option.get("option_type") == option_type:
            target = option
            break
    return target
