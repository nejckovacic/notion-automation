# utils.py


def format_page_data(title, additional_properties):
    properties = {"Name": {"title": [{"text": {"content": title}}]}}
    properties.update(additional_properties)
    return properties


# Add more utility functions as needed
