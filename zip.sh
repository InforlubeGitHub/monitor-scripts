#!/bin/bash

# Script to zip Python project files excluding venv and other common exclusions
# Designed to be run from inside the project directory

# Default values
OUTPUT_ZIP="monitor-app.zip"

# Help message
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo "Zip Python project files excluding venv and other unnecessary files"
    echo ""
    echo "Options:"
    echo "  -o, --output FILE     Specify the output zip file name (default: project_backup.zip)"
    echo "  -h, --help            Display this help message and exit"
    echo ""
    echo "Run this script from within your project directory."
}

# Process command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -o|--output)
            OUTPUT_ZIP="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

echo "Creating zip archive '$OUTPUT_ZIP' from current directory (excluding venv)..."

# Use direct exclusion patterns with the zip command instead of a file
zip -r "$OUTPUT_ZIP" . -x ".venv/*" ".venv/" "__pycache__/*" ".git/*" "./**/__pycache__/*" "./**/__pycache__" ".idea" ".idea/*" ".gitignore" "zip.sh" "setup.sh" ".env" "$OUTPUT_ZIP"

# Check if zip command was successful
if [ $? -eq 0 ]; then
    echo "Success! Project files zipped to: $OUTPUT_ZIP"
else
    echo "Error: Failed to create zip file"
    exit 1
fi

echo "Done!"