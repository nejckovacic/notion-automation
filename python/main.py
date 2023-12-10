# main.py

import os
from notion_api import NotionAPI


NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
if NOTION_TOKEN is None:
    raise ValueError("No NOTION_TOKEN found in environment variables")

notion = NotionAPI(NOTION_TOKEN)

# Example usage
database_id = "a2e30c8fddfe4c78af393e767afcc4af"
new_page_title = "New Test Page 222"
additional_properties = {}  # Add additional properties if needed

page_data = format_page_data(new_page_title, additional_properties)
response = notion.create_page(database_id, page_data)
print("New page created:", response)
