#!/bin/bash

# Export the environment variables
export NOTION_TOKEN=$(printenv NOTION_TOKEN)

# Execute the Python script
/usr/local/bin/python /app/main.py
