import csv

# First, read all phone numbers and types, store them by Customer ID
phone_data = {}
with open('SF Customer Phones.csv', 'r') as phone_file:
    phone_reader = csv.DictReader(phone_file)
    for row in phone_reader:
        customer_id = row['Customer ID']
        phone_number = row['Phone Number']
        phone_type = row['Phone Type']
        
        if customer_id not in phone_data:
            phone_data[customer_id] = {'fax': '', 'others': []}
            
        if phone_type.lower() == 'fax':
            phone_data[customer_id]['fax'] = phone_number
        else:
            if phone_type.lower() == 'office':
                phone_data[customer_id]['others'].append(f"Office ({phone_number})")
            elif phone_type.lower() == 'mill':
                phone_data[customer_id]['others'].append(f"Mill ({phone_number})")
            else:
                phone_data[customer_id]['others'].append(f"{phone_type} ({phone_number})")

# Second, read address data and store by Customer ID
address_data = {}
with open('SF Customer Addresses.csv', 'r') as address_file:
    address_reader = csv.DictReader(address_file)
    for row in address_reader:
        customer_id = row['Customer ID']
        address_desc = row['Address Description'].lower()
        # Get address lines, filtering out if not present
        line1 = row.get('Line 1', '')
        line2 = row.get('Line 2', '')
        line3 = row.get('Line 3', '')
        
        # Combine address lines with carriage returns, only including non-empty lines
        street_lines = [line1]
        if line2:
            street_lines.append(line2)
        if line3:
            street_lines.append(line3)
        street = '\r'.join(street_lines)
        
        if customer_id not in address_data:
            address_data[customer_id] = {
                'billing': {'street': '', 'city': '', 'state': '', 'zip': '', 'country': ''},
                'shipping': {'street': '', 'city': '', 'state': '', 'zip': '', 'country': ''}
            }
        
        # Populate address data based on Address Description
        address_info = {
            'street': street,
            'city': row.get('City', ''),
            'state': row.get('State', ''),
            'zip': row.get('Zip', ''),
            'country': row.get('Country', '')
        }
        
        if 'billing' in address_desc and 'shipping' in address_desc:
            address_data[customer_id]['billing'] = address_info
            address_data[customer_id]['shipping'] = address_info
        elif 'billing' in address_desc:
            address_data[customer_id]['billing'] = address_info
        elif 'shipping' in address_desc:
            address_data[customer_id]['shipping'] = address_info

# Now read the customers file, update phone and address columns
with open('SF Customers.csv', 'r') as customer_file:
    customer_reader = csv.DictReader(customer_file)
    
    # Use the exact fieldnames provided for the output
    fieldnames = [
        'Company Description', 'Company Name', 'Customer ID', 'Service Agreement Expiration',
        'Website', 'Industry', 'Fax', 'Other Phones',
        'Billing Street', 'Billing City', 'Billing State/Province', 'Billing Zip/Postal Code', 'Billing Country',
        'Shipping Street', 'Shipping City', 'Shipping State/Province', 'Shipping Zip/Postal Code', 'Shipping Country'
    ]
    
    # Read all rows into memory
    rows = list(customer_reader)
    
    # Update rows with phone and address data
    for row in rows:
        customer_id = row['Customer ID']
        
        # Assign phone data directly (no need to check if exists in input)
        row['Fax'] = phone_data.get(customer_id, {}).get('fax', '')
        other_phones = phone_data.get(customer_id, {}).get('others', [])
        row['Other Phones'] = ';'.join(other_phones) if other_phones else ''
        
        # Address data
        billing = address_data.get(customer_id, {}).get('billing', {})
        shipping = address_data.get(customer_id, {}).get('shipping', {})
        
        row['Billing Street'] = billing.get('street', '')
        row['Billing City'] = billing.get('city', '')
        row['Billing State/Province'] = billing.get('state', '')
        row['Billing Zip/Postal Code'] = billing.get('zip', '')
        row['Billing Country'] = billing.get('country', '')
        
        row['Shipping Street'] = shipping.get('street', '')
        row['Shipping City'] = shipping.get('city', '')
        row['Shipping State/Province'] = shipping.get('state', '')
        row['Shipping Zip/Postal Code'] = shipping.get('zip', '')
        row['Shipping Country'] = shipping.get('country', '')

# Write the updated data to a new CSV file
with open('SF Customers_updated.csv', 'w', newline='') as output_file:
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)