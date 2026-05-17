import json
import os

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def run_gmail_oauth():
    client_secrets_file = input("Enter the path to your Google OAuth client secrets JSON file: ")
    if not os.path.isfile(client_secrets_file):
        print(f"File not found: {client_secrets_file}")
        return

    flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
    creds = flow.run_local_server(port=0)

    token_path = os.path.join(os.getcwd(), "gmail_token.json")
    with open(token_path, "w", encoding="utf-8") as f:
        f.write(creds.to_json())

    print(f"Saved Gmail token to {token_path}")
    print("Open gmail_token.json and copy its contents into the GMAIL_TOKEN_JSON repository secret.")
