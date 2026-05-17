# Portfolio Pulse

This repository contains a portfolio briefing system for options positions, stock technicals, and a Claude-generated daily summary.

## What is included so far

- `src/`: Python modules for data fetching, technical calculations, and dashboard generation
- `src/config.py`: environment and path configuration
- `src/positions.py`: seeded positions for GOOGL, ASTS, and LMND
- `src/tradier_client.py`: Tradier sandbox API helpers
- `src/analytics.py`: SMA, RSI, ATR, 52-week range, and mark-to-market logic
- `src/briefer.py`: prompt builder for Claude Sonnet 4.6
- `src/gmail_reader.py`: placeholder for future Patreon email reading
- `src/dashboard.py`: static HTML dashboard writer
- `src/main.py`: orchestration script that generates `docs/index.html`
- `.gitignore` and `requirements.txt`

## GitHub Actions workflow

A scheduled workflow has been added at `.github/workflows/portfolio-briefing.yml`.

It will:
- run on weekdays at 22:00 UTC
- install dependencies
- generate `docs/index.html` via `python -m src.main`
- commit and push the updated dashboard back to the repo

## What you need to do next

1. Add these repository secrets under Settings > Secrets and variables > Actions:
   - `TRADIER_SANDBOX_TOKEN`
   - `ANTHROPIC_API_KEY`
   - `GMAIL_CREDENTIALS_JSON` (future Gmail setup)
   - `GMAIL_TOKEN_JSON` (future Gmail setup)

2. Enable GitHub Pages for this repository:
   - Go to Settings > Pages
   - Select branch `main` and folder `/docs`
   - Save the settings

3. Optionally run the workflow manually:
   - Go to Actions > Portfolio Pulse Daily Briefing > Run workflow

After the first successful run, your static dashboard will be published at the GitHub Pages URL shown in Settings > Pages.
