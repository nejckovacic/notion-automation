import os
from notion_client import Client

notion_token = os.environ.get('NOTION_TOKEN')
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
