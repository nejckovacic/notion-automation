import os
from notion_client import Client
from datetime import datetime


class NotionAPI:
    def __init__(self, database_id):
        self.database_id = database_id
        self.token = self._get_notion_token()
        self.client = Client(auth=self.token)
        self.time_slots = [
            {
                "label": "07:00-07:45",
                "timeRange": (
                    datetime.strptime("07:00", "%H:%M"),
                    datetime.strptime("07:59", "%H:%M"),
                ),
            },
            {
                "label": "08:00-08:45",
                "timeRange": (
                    datetime.strptime("08:00", "%H:%M"),
                    datetime.strptime("08:59", "%H:%M"),
                ),
            },
            {
                "label": "09:00-09:45",
                "timeRange": (
                    datetime.strptime("09:00", "%H:%M"),
                    datetime.strptime("09:59", "%H:%M"),
                ),
            },
            {
                "label": "10:00-10:45",
                "timeRange": (
                    datetime.strptime("10:00", "%H:%M"),
                    datetime.strptime("10:59", "%H:%M"),
                ),
            },
            {
                "label": "11:00-11:45",
                "timeRange": (
                    datetime.strptime("11:00", "%H:%M"),
                    datetime.strptime("11:59", "%H:%M"),
                ),
            },
            {
                "label": "12:00-12:45",
                "timeRange": (
                    datetime.strptime("12:00", "%H:%M"),
                    datetime.strptime("12:59", "%H:%M"),
                ),
            },
            {
                "label": "13:00-13:45",
                "timeRange": (
                    datetime.strptime("13:00", "%H:%M"),
                    datetime.strptime("13:59", "%H:%M"),
                ),
            },
            {
                "label": "14:00-14:45",
                "timeRange": (
                    datetime.strptime("14:00", "%H:%M"),
                    datetime.strptime("14:59", "%H:%M"),
                ),
            },
            {
                "label": "15:00-15:45",
                "timeRange": (
                    datetime.strptime("15:00", "%H:%M"),
                    datetime.strptime("15:59", "%H:%M"),
                ),
            },
            {
                "label": "16:00-16:45",
                "timeRange": (
                    datetime.strptime("16:00", "%H:%M"),
                    datetime.strptime("16:59", "%H:%M"),
                ),
            },
            {
                "label": "17:00-17:45",
                "timeRange": (
                    datetime.strptime("17:00", "%H:%M"),
                    datetime.strptime("17:59", "%H:%M"),
                ),
            },
            {
                "label": "18:00-18:45",
                "timeRange": (
                    datetime.strptime("18:00", "%H:%M"),
                    datetime.strptime("18:59", "%H:%M"),
                ),
            },
            {
                "label": "19:00-19:45",
                "timeRange": (
                    datetime.strptime("19:00", "%H:%M"),
                    datetime.strptime("19:59", "%H:%M"),
                ),
            },
            {
                "label": "20:00-20:45",
                "timeRange": (
                    datetime.strptime("20:00", "%H:%M"),
                    datetime.strptime("20:59", "%H:%M"),
                ),
            },
            {
                "label": "21:00-21:45",
                "timeRange": (
                    datetime.strptime("21:00", "%H:%M"),
                    datetime.strptime("21:59", "%H:%M"),
                ),
            },
            {
                "label": "22:00-22:45",
                "timeRange": (
                    datetime.strptime("22:00", "%H:%M"),
                    datetime.strptime("22:59", "%H:%M"),
                ),
            },
            {"label": "All Day", "timeRange": (datetime.min, datetime.max)},
        ]

    def _get_notion_token(self):
        # Get NOTION_TOKEN from OS environment variables
        token = os.getenv("NOTION_TOKEN")
        if not token:
            raise ValueError("No NOTION_TOKEN found in environment variables.")
        return token

    def query_database(self, filter_conditions):
        # Queries the Notion database based on specified filters.
        return self.client.databases.query(
            database_id=self.database_id, filter=filter_conditions
        )

    def create_or_update_page(self, page_id=None, properties=None):
        # Creates or updates a page in Notion.
        page_data = {
            "parent": {"type": "database_id", "database_id": self.database_id},
            "properties": properties,
        }
        if page_id:
            return self.client.pages.update(page_id=page_id, **page_data)
        else:
            return self.client.pages.create(**page_data)

    def find_event_by_gid(self, gid):
        # Properly format the query for a text property
        query_filter = {"property": "gID", "rich_text": {"equals": gid}}
        response = self.client.databases.query(
            database_id=self.database_id, filter=query_filter
        )
        return response.get("results")

    def create_or_update_event(self, event, calendar):
        # Create or update an event in the Notion database.
        existing_events = self.find_event_by_gid(event["id"])
        event_properties = self._format_event_properties(event, calendar)

        if existing_events:
            return self.create_or_update_page(
                page_id=existing_events[0]["id"], properties=event_properties
            )
        else:
            return self.create_or_update_page(properties=event_properties)

    def _format_event_properties(self, event, calendar):
        # Parsing the event start and end times
        start_datetime = datetime.fromisoformat(
            event["start"].get("dateTime", event["start"].get("date"))
        )
        end_datetime = datetime.fromisoformat(
            event["end"].get("dateTime", event["end"].get("date"))
        )

        # Check if the event is an all-day event
        if (
            start_datetime.time() == datetime.min.time()
            and end_datetime.time() == datetime.min.time()
            and (end_datetime - start_datetime).days == 1
        ):
            # All-day event: include only the start date
            date_property = {"date": {"start": event["start"].get("date")}}
        else:
            # Time-specific event: include both start and end dates/times
            date_property = {
                "date": {
                    "start": event["start"].get("dateTime", event["start"].get("date")),
                    "end": event["end"].get("dateTime", event["end"].get("date")),
                }
            }

        allocated_time = self.determine_time_slots(start_datetime, end_datetime)

        return {
            "Name": {"title": [{"text": {"content": event["summary"]}}]},
            "Date": date_property,
            "gID": {"rich_text": [{"text": {"content": event["id"]}}]},
            "gCalendar": {"rich_text": [{"text": {"content": calendar["name"]}}]},
            "Type": {"select": {"name": "Event"}},
            "Area": {"select": {"name": calendar["area"]}},
            "eventStatus": {"select": {"name": event["status"]}},
            "Allocate time": {
                "multi_select": [{"name": slot} for slot in allocated_time]
            },
        }

    def determine_time_slots(self, start, end):
        if start.date() != end.date() or (
            start.time() == datetime.min.time() and end.time() == datetime.max.time()
        ):
            return ["All Day"]

        start_time = start.time()
        end_time = end.time()
        allocated_slots = []

        for slot in self.time_slots:
            if slot["label"] != "All Day":
                slot_start_time, slot_end_time = slot["timeRange"]
                if (start_time < slot_end_time.time()) and (
                    end_time > slot_start_time.time()
                ):
                    allocated_slots.append(slot["label"])

        return allocated_slots
