import csv
from datetime import datetime

def strip_time(date_str):
    if date_str and date_str.strip():  # Check for non-empty string
        try:
            # Parse the datetime string with various possible formats
            for fmt in ['%m/%d/%Y %I:%M %p', '%m/%d/%Y %I:%M:%S %p', '%m/%d/%Y']:
                try:
                    parsed_date = datetime.strptime(date_str, fmt)
                    return parsed_date.strftime('%m/%d/%Y')
                except ValueError:
                    continue
            return date_str  # Return unchanged if no format matches
        except ValueError:
            return date_str  # Return unchanged if parsing fails
    return date_str

# Input and output file paths
input_file = 'SF Customer Products.csv'
output_file = 'SF Customer Products_output.csv'

# Fields to process
date_fields = ['Release Date', 'Product Installed Date', 'Product Updated Date', 'Support Expiration']

# Read input CSV and write to output CSV
with open(input_file, 'r', newline='', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    
    # Write header
    writer.writeheader()
    
    # Process each row
    for row in reader:
        # Update date fields
        for field in date_fields:
            if field in row:
                row[field] = strip_time(row[field])
        writer.writerow(row)