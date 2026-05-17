import json
import os
import re
from typing import Optional

from google.auth.exceptions import GoogleAuthError
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def _load_credentials() -> Optional[Credentials]:
    token_json = os.environ.get("GMAIL_TOKEN_JSON", "").strip()
    if not token_json:
        print("WARNING: GMAIL_TOKEN_JSON is not set. Gmail insights will be skipped.")
        return None

    try:
        token_data = json.loads(token_json)
        creds = Credentials.from_authorized_user_info(token_data, scopes=SCOPES)
        if not creds.valid and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        return creds
    except Exception as e:
        print(f"ERROR: Unable to load Gmail credentials: {e}")
        return None


def _extract_message_snippet(message: dict) -> str:
    snippet = message.get("snippet", "")
    if snippet:
        return snippet
    payload = message.get("payload", {})
    parts = payload.get("parts", [])
    texts = [part.get("body", {}).get("data", "") for part in parts if part.get("mimeType") == "text/plain"]
    return "\n".join(texts)


def read_patreon_insights() -> str:
    creds = _load_credentials()
    if creds is None:
        return (
            "Gmail integration is not configured yet. "
            "When you set up Gmail API access, this function will read Patreon newsletter summaries "
            "and include them in the briefing."
        )

    try:
        service = build("gmail", "v1", credentials=creds)
        query = "subject:Patreon OR from:(patreon.com)"
        results = service.users().messages().list(userId="me", q=query, maxResults=5).execute()
        messages = results.get("messages", [])

        if not messages:
            return "No recent Patreon emails were found."

        insights = []
        for item in messages:
            msg = service.users().messages().get(userId="me", id=item["id"], format="full").execute()
            snippet = msg.get("snippet", "")
            thread_subject = ""
            headers = msg.get("payload", {}).get("headers", [])
            for header in headers:
                if header.get("name", "").lower() == "subject":
                    thread_subject = header.get("value", "")
                    break
            insights.append(f"{thread_subject}: {snippet}")

        return "\n".join(insights)
    except HttpError as e:
        return f"Gmail API error: {e}"
    except GoogleAuthError as e:
        return f"Gmail authentication error: {e}"
    except Exception as e:
        return f"Unexpected Gmail error: {e}"
