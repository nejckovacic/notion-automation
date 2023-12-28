#!/bin/bash

# Capture environment variables and append them to /etc/environment
printenv | grep -v "no_proxy" >> /etc/environment

# Run cron in the foreground
cron -f
