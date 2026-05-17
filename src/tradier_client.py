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
        print(f"WARNING: TRADIER_SANDBOX_TOKEN not set, cannot fetch quote for {symbol}")
        return {"error": "missing Tradier sandbox token"}

    try:
        response = requests.get(
            f"{BASE_URL}/markets/quotes",
            headers=_get_headers(),
            params={"symbols": symbol},
        )
        response.raise_for_status()
        payload = response.json()
        
        if "errors" in payload:
            print(f"ERROR: Tradier API error for {symbol}: {payload.get('errors')}")
            return {}
        
        quote = payload.get("quotes", {}).get("quote", {})
        return quote
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Tradier API request failed for {symbol}: {e}")
        return {}
    except Exception as e:
        print(f"ERROR: Unexpected error fetching quote for {symbol}: {e}")
        return {}


def get_historical_prices(symbol: str, start_date: str, end_date: str) -> List[Dict]:
    if not TRADIER_SANDBOX_TOKEN:
        print(f"WARNING: TRADIER_SANDBOX_TOKEN not set, cannot fetch history for {symbol}")
        return []

    try:
        response = requests.get(
            f"{BASE_URL}/markets/history",
            headers=_get_headers(),
            params={"symbol": symbol, "start": start_date, "end": end_date, "interval": "daily"},
        )
        response.raise_for_status()
        payload = response.json()
        
        if "errors" in payload:
            print(f"ERROR: Tradier API error for {symbol}: {payload.get('errors')}")
            return []
        
        return payload.get("history", {}).get("day", [])
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Tradier API request failed for {symbol}: {e}")
        return []
    except Exception as e:
        print(f"ERROR: Unexpected error fetching history for {symbol}: {e}")
        return []


def find_option_quote(symbol: str, expiry: str, strike: float, option_type: str) -> Optional[Dict]:
    if not TRADIER_SANDBOX_TOKEN:
        print(f"WARNING: TRADIER_SANDBOX_TOKEN not set, cannot fetch option quote for {symbol}")
        return None

    try:
        response = requests.get(
            f"{BASE_URL}/markets/options/chains",
            headers=_get_headers(),
            params={"symbol": symbol, "expiration": expiry, "greeks": "false"},
        )
        response.raise_for_status()
        payload = response.json()
        
        if payload is None:
            print(f"ERROR: Tradier API returned None for {symbol} {expiry}")
            return None
        
        if "errors" in payload:
            print(f"ERROR: Tradier API error: {payload.get('errors')}")
            return None
        
        chain = payload.get("options", {}).get("option", [])
        if not chain:
            print(f"WARNING: No options chain found for {symbol} expiry {expiry}")
            return None
        
        target = None
        for option in chain:
            if option.get("strike") == strike and option.get("option_type") == option_type:
                target = option
                break
        
        if not target:
            print(f"WARNING: Option not found: {symbol} {option_type} {expiry} strike {strike}")
        
        return target
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Tradier API request failed for {symbol}: {e}")
        return None
    except Exception as e:
        print(f"ERROR: Unexpected error fetching option quote for {symbol}: {e}")
        return None
