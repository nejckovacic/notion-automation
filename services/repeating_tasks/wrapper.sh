#!/bin/bash

# Dump all environment variables to a file
printenv > /etc/environment

# Source the file to export all environment variables
source /etc/environment

# Execute the Python script
/usr/local/bin/python /app/main.py
