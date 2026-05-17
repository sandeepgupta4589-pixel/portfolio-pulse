from datetime import datetime, timedelta
from pathlib import Path
from typing import List
import sys

# Allow the script to run from the repository root with direct Python execution.
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import pandas as pd

from .analytics import (
    compute_atr,
    compute_52_week_range,
    compute_rsi,
    extract_price_series,
    estimate_mark_to_market_pnl,
    simple_moving_average,
)
from .briefer import build_briefing_prompt, generate_claude_briefing
from .config import HTML_OUTPUT_PATH
from .gmail_reader import read_patreon_insights
from .positions import positions
from .tradier_client import find_option_quote, get_historical_prices, get_stock_quote


def build_position_table(position_data: List[dict]) -> str:
    rows = [
        "<table>\n<tr><th>Symbol</th><th>Type</th><th>Expiry</th><th>Strike</th><th>Account</th>"
        "<th>Mark Price</th><th>Value</th><th>Estimated PnL</th><th>Notes</th></tr>"
    ]
    for row in position_data:
        pnl = row.get("estimated_pnl")
        pnl_text = f"${pnl:,.2f}" if pnl is not None else "N/A"
        rows.append(
            "<tr>"
            f"<td>{row['symbol']}</td>"
            f"<td>{row['option_type']}</td>"
            f"<td>{row['expiry']}</td>"
            f"<td>{row['strike']}</td>"
            f"<td>{row['account']}</td>"
            f"<td>${row['mark_price']:.2f}</td>"
            f"<td>${row['position_value']:,.2f}</td>"
            f"<td>{pnl_text}</td>"
            f"<td>{row['description']}</td>"
            "</tr>"
        )
    rows.append("</table>")
    return "\n".join(rows)


def build_technical_summary(technical_data: dict) -> str:
    lines = []
    for symbol, summary in technical_data.items():
        lines.append(f"{symbol}:")
        for key, value in summary.items():
            lines.append(f"  {key}: {value}")
        lines.append("")
    return "\n".join(lines)


def generate_date_range(days: int = 365) -> tuple[str, str]:
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=days)
    return str(start_date), str(end_date)


def main() -> int:
    position_data = []
    technical_data = {}
    email_insights = read_patreon_insights()
    start_date, end_date = generate_date_range()

    for position in positions:
        quote = get_stock_quote(position.symbol)
        history = get_historical_prices(position.symbol, start_date, end_date)
        option_quote = find_option_quote(position.symbol, position.expiry, position.strike, position.option_type)

        df = extract_price_series(history)
        technical_summary = {
            "20-day SMA": simple_moving_average(df["close"], 20) if not df.empty else None,
            "50-day SMA": simple_moving_average(df["close"], 50) if not df.empty else None,
            "200-day SMA": simple_moving_average(df["close"], 200) if not df.empty else None,
            "RSI(14)": compute_rsi(df["close"]) if not df.empty else None,
            "ATR(14)": compute_atr(df["high"], df["low"], df["close"]) if not df.empty else None,
            "52-week range": compute_52_week_range(df["close"]) if not df.empty else None,
        }
        technical_data[position.symbol] = technical_summary

        if option_quote is None:
            option_quote = {"last": 0.0, "ask": 0.0}

        pnl = estimate_mark_to_market_pnl(position, option_quote)
        position_data.append({
            "symbol": position.symbol,
            "option_type": position.option_type,
            "expiry": position.expiry,
            "strike": position.strike,
            "account": position.account,
            "description": position.description,
            **pnl,
        })

    summary_text = (
        f"Portfolio briefing generated on {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}.")
    position_rows_html = build_position_table(position_data)
    technical_summary_text = build_technical_summary(technical_data)
    prompt = build_briefing_prompt(summary_text, technical_summary_text, position_rows_html, email_insights)
    briefing_text = generate_claude_briefing(prompt)

    from .dashboard import write_dashboard

    write_dashboard(
        output_path=HTML_OUTPUT_PATH,
        title="Portfolio Pulse Daily Briefing",
        briefing=briefing_text,
        position_rows=position_rows_html,
        technical_summary=technical_summary_text,
    )

    print(f"Dashboard written to {HTML_OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
