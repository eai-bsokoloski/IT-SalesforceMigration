import csv

input_file = 'SF Tickets.csv'
output_file = 'SF Tickets Modified.csv'

with open(input_file, 'r', newline='') as infile, open(output_file, 'w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    
    # Read and write the header, adding 'Billable' and 'Type' columns
    header = next(reader)
    header.extend(['Billable', 'Type'])
    writer.writerow(header)
    
    # Process each row
    for row in reader:
        # Change Status (10th field, index 9) to 'In Progress' if not 'Closed'
        if row[9].strip().lower() != 'closed':
            row[9] = 'In Progress'
        
        # Check fields 19, 20, 21, 22, 23, 24, 25 (indices 18, 19, 20, 21, 22, 23, 24)
        billable_fields = [row[i].strip().lower() == 'yes' for i in range(18, 25)]
        billable = any(billable_fields)
        # Append Billable and Type values to row
        row.extend([str(billable), 'On Support'])
        
        if row[29].strip().lower() == 'small project team':
            row[29] = 'Jacy Kosbab'
        if row[29].strip().lower() == 'none':
            row[29] = ''

        # Write the modified row
        writer.writerow(row)