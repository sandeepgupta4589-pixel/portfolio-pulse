import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DOCS_DIR = ROOT.parent / "docs"
DATA_DIR.mkdir(exist_ok=True)
DOCS_DIR.mkdir(exist_ok=True)

TRADIER_SANDBOX_TOKEN = os.environ.get("TRADIER_SANDBOX_TOKEN", "")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
GMAIL_CREDENTIALS_JSON = os.environ.get("GMAIL_CREDENTIALS_JSON", "")
GMAIL_TOKEN_JSON = os.environ.get("GMAIL_TOKEN_JSON", "")

GIT_BRANCH = os.environ.get("GITHUB_REF_NAME", "main")

# The dashboard is generated into docs/ so GitHub Pages can publish it from the repository.
HTML_OUTPUT_PATH = DOCS_DIR / "index.html"
