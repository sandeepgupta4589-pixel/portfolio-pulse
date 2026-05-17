import os
import requests
from typing import Dict, List

from .config import ANTHROPIC_API_KEY

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/complete"


def build_briefing_prompt(
    portfolio_summary: str,
    technical_summary: str,
    position_rows: str,
    email_insights: str,
) -> str:
    return (
        "You are a financial briefing assistant. Use the information below to write a concise daily portfolio briefing. "
        "Mention the options positions, key technical levels, and any email-based insights. "
        "Write in clear language for a busy investor.\n\n"
        f"Portfolio Summary:\n{portfolio_summary}\n\n"
        f"Technical Summary:\n{technical_summary}\n\n"
        f"Open Positions:\n{position_rows}\n\n"
        f"Patreon Email Insights:\n{email_insights}\n\n"
        "Briefing:" 
    )


def generate_claude_briefing(prompt: str) -> str:
    if not ANTHROPIC_API_KEY:
        return "Anthropic API key is missing. Set ANTHROPIC_API_KEY in the repository secrets."

    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "model": "claude-sonnet-4.6",
        "prompt": prompt,
        "max_tokens_to_sample": 500,
        "temperature": 0.25,
    }
    response = requests.post(ANTHROPIC_API_URL, json=payload, headers=headers)
    response.raise_for_status()
    output = response.json()
    return output.get("completion", "")
