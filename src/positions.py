from dataclasses import dataclass
from typing import Optional

@dataclass
class Position:
    symbol: str
    option_type: str
    expiry: str
    strike: float
    quantity: int
    account: str
    description: str
    entry_price: Optional[float] = None


positions = [
    Position(
        symbol="GOOGL",
        option_type="call",
        expiry="2028-01-19",
        strike=300.0,
        quantity=1,
        account="TFSA",
        description="LEAP",
        entry_price=None,
    ),
    Position(
        symbol="ASTS",
        option_type="call",
        expiry="2028-01-19",
        strike=65.0,
        quantity=1,
        account="TFSA",
        description="LEAP",
        entry_price=None,
    ),
    Position(
        symbol="LMND",
        option_type="call",
        expiry="2026-09-18",
        strike=60.0,
        quantity=1,
        account="TFSA",
        description="Recovery play",
        entry_price=None,
    ),
]
