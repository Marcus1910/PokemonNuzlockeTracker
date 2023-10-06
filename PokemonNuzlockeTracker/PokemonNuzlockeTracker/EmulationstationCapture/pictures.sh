#!/bin/bash

# Set the screenshot directory
SCREENSHOT_DIR="/home/pi/screenshots/"

# Set the screenshot file name
SCREENSHOT_FILE_NAME=$(date +%Y-%m-%d_%H-%M-%S).png

# Take the screenshot and save it to the file
scrot $SCREENSHOT_DIR/$SCREENSHOT_FILE_NAME