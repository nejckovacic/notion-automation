from notion_client import Client

notion = Client(auth="your-integration-token")

new_page_data = {
    "parent": {"database_id": "a2e30c8fddfe4c78af393e767afcc4af"},
    "properties": {
        "Name": {
            "title": [{"text": {"content": "New Test Page"}}]
        }
    }
}

notion.pages.create(**new_page_data)
