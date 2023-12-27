# main.py

from datetime import datetime
from notion_api import NotionAPI
from utils import should_create_new_page, duplicate_page_data


def main():
    notion = NotionAPI()
    database_id = "a2e30c8fddfe4c78af393e767afcc4af"
    filter_conditions = {
        "and": [
            {"property": "Date", "date": {"is_not_empty": True}},
            {"property": "repeat", "select": {"is_not_empty": True}},
            {"property": "Area", "select": {"is_not_empty": True}},
        ]
    }

    search_results = notion.search_database(database_id, filter_conditions)
    current_date = datetime.now()

    for page in search_results.get("results", []):
        repeat_property = (
            page.get("properties", {}).get("repeat", {}).get("select", {}).get("name")
        )
        date_property_str = (
            page.get("properties", {}).get("Date", {}).get("date", {}).get("start")
        )
        date_property = (
            datetime.fromisoformat(date_property_str) if date_property_str else None
        )

        if date_property and should_create_new_page(
            repeat_property, date_property, current_date
        ):
            page_data = duplicate_page_data(database_id, page)
            notion.create_page(page_data)
            print(
                "New page created:"
                + page["properties"]["Name"]["title"][0]["text"]["content"]
            )


if __name__ == "__main__":
    main()
