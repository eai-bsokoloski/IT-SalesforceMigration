import csv

input_file = 'SF Tickets.csv'
customer_file = 'SF Customers.csv'
output_file = 'SF Tickets Modified.csv'
contacts_file = 'SF Contacts.csv'

# Read customer data into a dictionary for lookup
customer_id_map = {}
with open(customer_file, 'r', newline='') as cust_file:
    customer_reader = csv.reader(cust_file)
    customer_header = next(customer_reader)  # Skip header
    for row in customer_reader:
        customer_id_map[row[1].strip().lower()] = row[2]

# Read contact data into a dictionary for lookup
contact_id_map = {}
with open(contacts_file, 'r', newline='') as cont_file:
    contact_reader = csv.reader(cont_file)
    contact_header = next(contact_reader)  # Skip header
    for row in contact_reader:
        contact_id_map[row[2].strip().lower() + ' ' + row[3].strip().lower()] = row[0]

with open(input_file, 'r', newline='') as infile, open(output_file, 'w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    
    # Read and write the header, adding 'Billable', 'Type', and 'Customer ID' columns
    header = next(reader)
    header.extend(['Billable', 'Type', 'Customer ID', 'Contact ID'])
    writer.writerow(header)
    
    # Process each row
    for row in reader:
        # Change Status (10th field, index 9) to 'In Progress' if not 'Closed'
        if row[9].strip().lower() != 'closed':
            row[9] = 'In Progress'
        
        # Check fields 19, 20, 21, 22, 23, 24, 25 (indices 18, 19, 20, 21, 22, 23, 24)
        billable_fields = [row[i].strip().lower() == 'yes' for i in range(18, 25)]
        billable = any(billable_fields)
        
        # Lookup Customer ID based on Customers field (assuming it's in column 1, index 0)
        customer_name = row[2].strip().lower()
        customer_id = customer_id_map.get(customer_name, '')  # Default to empty string if not found
        
        contact_name = row[1].strip().lower()
        contact_id = contact_id_map.get(contact_name, '')

        # Append Billable, Type, and Customer ID values to row
        row.extend([str(billable), 'On Support', customer_id, contact_id])
        
        # Update field 30 (index 29) for 'small project team' or 'none'
        if row[29].strip().lower() == 'small project team':
            row[29] = 'Jacy Kosbab'
        if row[29].strip().lower() == 'none':
            row[29] = ''

        # Write the modified row
        writer.writerow(row)