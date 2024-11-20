import pandas as pd
import chardet

# Detect file encoding
def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())
    return result['encoding']

# Clean metadata
def clean_metadata(data):
    log = []

    # Fill missing names
    if data['Name'].isnull().sum() > 0:
        log.append(f"Missing Names: {data['Name'].isnull().sum()} rows fixed.")
        data['Name'].fillna("Unknown Name", inplace=True)
    
    # Standardize case for names and feature descriptions
    data['Name'] = data['Name'].str.title()
    data['Feature_Description'] = data['Feature_Description'].str.title()

    # Validate latitude and longitude ranges
    invalid_coords = data[
        (data['Latitude'] < -90) | (data['Latitude'] > 90) |
        (data['Longitude'] < -180) | (data['Longitude'] > 180)
    ]
    if not invalid_coords.empty:
        log.append(f"Invalid coordinates: {len(invalid_coords)} rows removed.")
        data = data.drop(index=invalid_coords.index)

    # Handle missing dates
    if data['Date'].isnull().sum() > 0:
        log.append(f"Missing Dates: {data['Date'].isnull().sum()} rows fixed.")
        data['Date'].fillna("Unknown Date", inplace=True)
    
    # Standardize and convert date format
    try:
        data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
        if data['Date'].isnull().sum() > 0:
            log.append(f"Invalid Dates: {data['Date'].isnull().sum()} rows fixed.")
            data['Date'].fillna("1900-01-01", inplace=True)
    except Exception as e:
        log.append(f"Error during date conversion: {e}")
    
    # Remove duplicates
    duplicates = data.duplicated(subset=['pklid'])
    if duplicates.sum() > 0:
        log.append(f"Duplicates removed: {duplicates.sum()} rows.")
        data = data[~duplicates]

    # Fill missing text fields
    text_fields = ['Comments', 'Meaning']
    for field in text_fields:
        if data[field].isnull().sum() > 0:
            log.append(f"Missing {field}: {data[field].isnull().sum()} rows fixed.")
            data[field].fillna("Not Specified", inplace=True)
    
    return data, log

# Main processing
file_path = "meta/raw.csv"
encoding = detect_encoding(file_path)
print(f"Detected encoding: {encoding}")

try:
    data = pd.read_csv(file_path, encoding=encoding)
except UnicodeDecodeError:
    print("Error reading with detected encoding. Trying 'ISO-8859-1'...")
    data = pd.read_csv(file_path, encoding="ISO-8859-1")

# Clean the metadata
data, cleaning_log = clean_metadata(data)

# Save cleaned data and logs
data.to_csv("data/cleaned_data.csv", index=False)
with open("logs/metadata_cleaning_log.txt", "w") as log_file:
    log_file.write("\n".join(cleaning_log))

print("Metadata cleaning complete.")
