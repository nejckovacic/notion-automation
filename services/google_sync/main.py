from datetime import datetime
from google_api import GoogleAPI
from notion_api import NotionAPI
from utils import should_create_new_page, duplicate_page_data


def main():
    calendars = [
        {"name": "Personal", "id": "nejc.kovacic9@gmail.com", "area": "Personal"},
        {
            "name": "Family",
            "id": "family06939489949381963345@group.calendar.google.com",
            "area": "Personal",
        },
        {
            "name": "MAG",
            "id": "4cf21bbad8ae042084630042d288d84f80f4cf7186bbf8ab0ffa9d36ae1fd224@group.calendar.google.com",
            "area": "School",
        },
        {"name": "Ana", "id": "ana1.bertoncelj@gmail.com", "area": "Personal"},
        {
            "name": "MAG-Urnik",
            "id": "vh25mg35id59jrm7ipqe6t8jjllbn61r@import.calendar.google.com",
            "area": "School",
        },
        {"name": "Kalmia", "id": "nejc.kovacic@kalmia.si", "area": "Kalmia"},
    ]

    notion_api = NotionAPI("a2e30c8fddfe4c78af393e767afcc4af")
    google_api = GoogleAPI()

    for calendar in calendars:
        events = google_api.fetch_calendar_events(calendar["id"])
        if events:
            for event in events:
                notion_api.create_or_update_event(event, calendar)
                print(
                    event["summary"],
                    event["start"].get("dateTime", event["start"].get("date")),
                )
            # For testing only
        break


main()
