import csv

input_file = 'SF Ticket Actions.csv'
output_file = 'SF Ticket Actions Updated.csv'

try:
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # Read header row
        header = next(reader)
        header.append('Total Minutes')
        writer.writerow(header)
        
        # Process each data row
        for row in reader:
            # Check if 9th column (index 8) is greater than 0
            total_minutes = 0
            try:
                if float(row[8]) > 0:
                    total_minutes = float(row[8])
            except (ValueError, IndexError):
                pass
                
            # Append Total Minutes to row
            row.append(str(total_minutes))
            writer.writerow(row)
except UnicodeDecodeError as e:
    print(f"Encoding error: {e}")
    print("Try opening the file with a different encoding, e.g., 'latin1' or 'iso-8859-1'.")