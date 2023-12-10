# main.py

import os
from notion_api import NotionAPI
from utils import format_page_data

# Try to get NOTION_TOKEN from OS environment variables
NOTION_TOKEN = os.getenv("NOTION_TOKEN")

# If NOTION_TOKEN is not found, then load from .env file
if NOTION_TOKEN is None:
    from dotenv import load_dotenv
    load_dotenv()
    NOTION_TOKEN = os.getenv("NOTION_TOKEN")

# Raise error if NOTION_TOKEN is still None after loading .env
if NOTION_TOKEN is None:
    raise ValueError("No NOTION_TOKEN found in environment variables or .env file")

notion = NotionAPI(NOTION_TOKEN)

# Rest of your script
database_id = "a2e30c8fddfe4c78af393e767afcc4af"
new_page_title = "New Test Page 222"
additional_properties = {}  # Add additional properties if needed

page_data = format_page_data(new_page_title, additional_properties)
response = notion.create_page(database_id, page_data)
print("New page created:", response)
