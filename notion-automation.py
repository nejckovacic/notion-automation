import os
from notion_client import Client

notion_token = os.environ.get('NOTION_TOKEN')
if not notion_token:
    raise ValueError("No NOTION_TOKEN found in environment variables")

notion = Client(auth=notion_token)

new_page_data = {
    "parent": {"database_id": "a2e30c8fddfe4c78af393e767afcc4af"},
    "properties": {
        "Name": {
            "title": [{"text": {"content": "New Test Page"}}]
        }
    }
}

notion.pages.create(**new_page_data)
