#!/bin/bash

# Simple script to unzip a Python project and set up a virtual environment in Linux

# Check if zip file argument is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <project_zip_file>"
    echo "Example: $0 project_backup.zip"
    exit 1
fi

ZIP_FILE=$1

# Check if the zip file exists
if [ ! -f "$ZIP_FILE" ]; then
    echo "Error: File $ZIP_FILE not found!"
    exit 1
fi

# Get project name from zip file (remove .zip extension)
PROJECT_NAME=$(basename "$ZIP_FILE" .zip)

# Create project directory
echo "Creating project directory: $PROJECT_NAME"
mkdir -p "$PROJECT_NAME"

# Extract the zip file
echo "Extracting $ZIP_FILE to $PROJECT_NAME..."
unzip -q "$ZIP_FILE" -d "$PROJECT_NAME"

# Go to the project directory
cd "$PROJECT_NAME" || exit 1

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements if requirements.txt exists
if [ -f requirements.txt ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
    echo "Dependencies installed successfully."
else
    echo "No requirements.txt found. Skipping dependency installation."
fi

echo ""
echo "Setup complete! The virtual environment is now active."
echo "To deactivate when finished, type: deactivate"
echo ""
echo "Your project is ready to use in the '$PROJECT_NAME' directory."