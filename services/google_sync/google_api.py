import os
import json
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from google.oauth2 import service_account


class GoogleAPI:
    def __init__(self):
        self.credentials_json = self._get_credentials()
        self.token_file = "token.pickle"
        self.service = self.authenticate_google_api()

    def _get_credentials(self):
        # Try to get GOOGLE_CREDENTIALS from OS environment variables
        credentials_json = {
            "type": "service_account",
            "project_id": os.getenv("GOOGLE_PROJECT_ID"),
            "private_key_id": os.getenv("GOOGLE_PIRVATE_KEY_ID"),
            "private_key": os.getenv("GOOGLE_PRIVATE_KEY"),
            "client_email": os.getenv("GOOGLE_CLIENT_EMAIL"),
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": os.getenv("GOOGLE_CLIENT_CERT_URL"),
            "universe_domain": "googleapis.com",
        }

        if any(value is None for value in credentials_json.values()):
            raise ValueError(
                "Incomplete GOOGLE_CREDENTIALS found in environment variables"
            )

        return credentials_json

    def authenticate_google_api(self):
        credentials = service_account.Credentials.from_service_account_info(
            self.credentials_json,
            scopes=["https://www.googleapis.com/auth/calendar.readonly"],
        )
        return build("calendar", "v3", credentials=credentials)

    def fetch_calendar_events(self, calendar_id="primary", weeks=2):
        now = datetime.utcnow().isoformat() + "Z"
        later = (datetime.utcnow() + timedelta(weeks=weeks)).isoformat() + "Z"

        events_result = (
            self.service.events()
            .list(
                calendarId=calendar_id,
                timeMin=now,
                timeMax=later,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )

        return events_result.get("items", [])
