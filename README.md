# Notion Automation Project

## Overview

This project includes a set of scripts designed to automate specific tasks in Notion. It utilizes the Notion API to query and manipulate database pages based on custom logic, such as creating new pages based on certain conditions. The project is containerized using Docker, enabling easy deployment and scheduling.

## Features

- Query a Notion database based on custom filters.
- Create new pages in Notion with predefined properties.
- Schedule tasks to run at specific times using cron jobs inside Docker containers.
- Easily configurable for various automation tasks in Notion.

## Prerequisites

- Python 3.8 or later.
- Docker and Docker Compose (for containerization and scheduling).
- Notion API integration and access token.

## Installation and Setup

1. **Clone the Repository:**

2. **Configure Notion API Token:**
   - Obtain your Notion API token and set it as an environment variable `NOTION_TOKEN` in your system or in the Docker configuration.

3. **Building the Docker Image:**
   - Navigate to the root directory of the project.
   - Run `docker-compose build` to build the Docker image.

## Usage

1. **Starting the Services:**
   - Run `docker-compose up` to start the services.
   - The main script (`main.py`) is scheduled to run daily at 3 AM.

2. **Stopping the Services:**
   - Run `docker-compose stop` to stop the running services.

3. **Testing:**
   - For testing purposes, adjust the cron job timing in the Docker configuration as needed.

## Configuration

- Modify the `main.py` script to change the logic or add new automation tasks.
- Update the cron job schedule in the Docker configuration for different timing requirements.

