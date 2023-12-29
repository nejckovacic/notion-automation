import os
import base64
import pickle
from googleapiclient.discovery import build
from datetime import datetime, timedelta

class GoogleAPI:
    def __init__(self):
        self.token_base64 = self._get_token_from_env()
        self.service = self.authenticate_google_api()

    def _get_token_from_env(self):
        token_base64 = os.getenv('GOOGLE_TOKEN')
        if not token_base64:
            raise ValueError("No GOOGLE_TOKENfound in environment variables")
        return token_base64

    def authenticate_google_api(self):
        # Deserialize the credentials from base64 string
        creds = pickle.loads(base64.b64decode(self.token_base64))

        if not creds or not creds.valid:
            raise ValueError("Token not valid, re-run authentication on a GUI-enabled machine.")

        return build('calendar', 'v3', credentials=creds)


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
