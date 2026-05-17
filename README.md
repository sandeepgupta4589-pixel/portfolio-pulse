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

3. Set up Gmail API for your Patreon-forwarding Gmail account:
   - Follow the steps in the next section below

4. Optionally run the workflow manually:
   - Go to Actions > Portfolio Pulse Daily Briefing > Run workflow

After the first successful run, your static dashboard will be published at the GitHub Pages URL shown in Settings > Pages.

## Gmail API setup (Patreon email account)

### Step 1: Create Google Cloud credentials
1. Open `https://console.cloud.google.com/`
2. Sign in with your Gmail account that receives Patreon emails
3. In the top-left menu, click `APIs & Services` → `Library`
4. Search for `Gmail API` and click it
5. Click `Enable`
6. In `APIs & Services`, click `Credentials`
7. Click `Create Credentials` → `OAuth client ID`
8. If prompted, configure the OAuth consent screen:
   - Choose `External`
   - Enter an app name (for example, `Portfolio Pulse`)
   - Save the settings
9. For `Application type`, choose `Desktop app`
10. Name it `Portfolio Pulse Gmail`
11. Click `Create`
12. Download the JSON file and save it as `gmail_credentials.json`

### Step 2: Generate the Gmail token
1. Install dependencies locally:
   - `python -m pip install -r requirements.txt`
2. Run this helper script:
   - `python -m src.gmail_auth`
3. When prompted, enter the path to `gmail_credentials.json`
4. The script will open a browser and ask you to sign in to your Gmail account
5. After approval, it creates `gmail_token.json`
6. Open `gmail_token.json` and copy its full contents
7. In GitHub repository secrets, create `GMAIL_TOKEN_JSON` and paste the contents

### Step 3: Enable the Gmail secrets in the workflow
- Confirm `GMAIL_TOKEN_JSON` is stored in GitHub Secrets
- The workflow already reads it when generating the briefing

### Step 4: Test the Gmail connection
1. Run the workflow manually
2. If Gmail is configured, the briefing will include Patreon email snippets
3. If not, the dashboard will still generate and will say Gmail integration is not configured yet
