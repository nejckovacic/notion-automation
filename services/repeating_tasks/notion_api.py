# notion_api.py

import os
from notion_client import Client


class NotionAPI:
    def __init__(self):
        self.token = self._get_notion_token()
        self.client = Client(auth=self.token)

    def _get_notion_token(self):
        # Try to get NOTION_TOKEN from OS environment variables
        token = os.getenv("NOTION_TOKEN")
        
        if token is None:
            raise ValueError(
                "No NOTION_TOKEN found in environment variables or .env file"
            )
        return token

    def search_database(self, database_id, filter_conditions):
        # Queries a Notion database based on specified filters.
        query_payload = {"filter": filter_conditions}
        return self.client.databases.query(database_id=database_id, **query_payload)

    def create_page(self, page_data):
        # Creates a new page in Notion with the provided page data.
        return self.client.pages.create(**page_data)

    # Additional methods for other API interactions can be added here


# Example usage and testing code can be placed here for quick checks
