# Metadata Cleaning 

This project is a Python script designed to clean and process metadata from a CSV file. The script ensures that the data is standardized, valid, and ready for further analysis or use.

## Features
- **Encoding Detection**: Automatically detects the file encoding for reading non-UTF-8 files.
- **Data Cleaning**: 
  - Fills missing values in key fields.
  - Standardizes case for names and descriptions.
  - Validates latitude and longitude ranges.
  - Converts and standardizes date formats.
  - Removes duplicate records based on a unique identifier.
  - Handles missing text fields with default values.
- **Logging**: Generates a log file summarizing the cleaning process and actions taken.
- **Output**: Saves the cleaned data to a new CSV file.

## Project Structure
