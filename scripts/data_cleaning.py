import pandas as pd
import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())
    return result['encoding']
file_path = "data/raw_data.csv"
encoding = detect_encoding(file_path)
print(f"Detected encoding: {encoding}")

try:
    data = pd.read_csv(file_path, encoding=encoding)
except UnicodeDecodeError:
    print("Error reading with detected encoding. Trying 'ISO-8859-1'...")
    data = pd.read_csv(file_path, encoding="ISO-8859-1")

log = []

if data['Authors'].isnull().sum() > 0:
    log.append(f"Missing Authors: {data['Authors'].isnull().sum()} rows fixed.")
    data['Authors'].fillna("Unknown", inplace=True)

if data['Journal'].isnull().sum() > 0:
    log.append(f"Missing Journal Names: {data['Journal'].isnull().sum()} rows fixed.")
    data['Journal'].fillna("Unknown Journal", inplace=True)

data['Authors'] = data['Authors'].str.title()
data['Journal'] = data['Journal'].str.title()

duplicates = data.duplicated(subset=['DOI'])
if duplicates.sum() > 0:
    log.append(f"Duplicates removed: {duplicates.sum()} rows.")
    data = data[~duplicates]

data.to_csv("data/cleaned_data.csv", index=False)

with open("logs/cleaning_log.txt", "w") as log_file:
    log_file.write("\n".join(log))

print("Data cleaning complete.")
