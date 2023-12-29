# utils.py

from datetime import datetime


def should_create_new_page(repeat_value, page_date, current_date):
    # Determines if a new page should be created based on repeat criteria.

    if repeat_value == "daily":
        return True
    elif repeat_value == "weekly" and page_date.weekday() == current_date.weekday():
        return True
    elif (
        repeat_value == "bi-weekly"
        and page_date.weekday() == current_date.weekday()
        and (current_date - page_date).days % 14 == 0
    ):
        return True
    elif repeat_value == "monthly" and page_date.day == current_date.day:
        return True
    elif (
        repeat_value == "yearly"
        and page_date.month == current_date.month
        and page_date.day == current_date.day
    ):
        return True
    elif repeat_value == "weekends" and current_date.weekday() >= 5:
        return True
    elif repeat_value == "workdays" and current_date.weekday() < 5:
        return True
    else:
        return False


def duplicate_page_data(database_id, page):
    # Constructs the data payload for a new Notion page based on an existing page.

    current_date = datetime.now().isoformat()
    title = (
        page["properties"]["Name"]["title"][0]["text"]["content"]
        if page["properties"]["Name"]["title"]
        else "Default Title"
    )
    projects = [
        {"id": project["id"]}
        for project in page["properties"]["📰 Projects"]["relation"]
    ]
    area = page["properties"]["Area"]["select"]

    new_page_data = {
        "parent": {"database_id": database_id},
        "properties": {
            "Name": {"title": [{"text": {"content": title}}]},
            "📰 Projects": {"relation": projects},
            "Area": {"select": area},
            "Type": {"select": {"name": "Task"}},
            "Date": {"date": {"start": current_date, "end": None}},
        },
        "icon": {
            "type": "external",
            "external": {
                "url": "https://www.notion.so/icons/sync-reverse_brown.svg?mode=dark"
            },
        },
    }

    return new_page_data


# You can add more utility functions as needed.
