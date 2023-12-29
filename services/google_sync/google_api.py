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
        credentials_json = os.getenv("GOOGLE_CREDENTIALS")
        if credentials_json is None:
            raise ValueError("No GOOGLE_CREDENTIALS found in environment variables")

        return json.loads(credentials_json)

    def authenticate_google_api(self):
        credentials = service_account.Credentials.from_service_account_file(
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
