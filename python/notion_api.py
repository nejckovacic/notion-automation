# notion_api.py

from notion_client import Client


class NotionAPI:
    def __init__(self, token):
        self.client = Client(auth=token)

    def create_page(self, database_id, page_data):
        return self.client.pages.create(
            parent={"database_id": database_id}, properties=page_data
        )


def format_page_data(title, additional_properties):
    properties = {"Name": {"title": [{"text": {"content": title}}]}}
    properties.update(additional_properties)
    return properties
