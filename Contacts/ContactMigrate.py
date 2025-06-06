import csv
import os

def ensure_file_exists(filepath):
    """Check if a file exists, raise informative error if not."""
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"Input file not found: {filepath}")

def process_phone_data(phone_file_path):
    """Read and organize phone data by ContactID."""
    phone_data = {}
    try:
        with open(phone_file_path, 'r', newline='') as phone_file:
            phone_reader = csv.DictReader(phone_file)
            for row in phone_reader:
                contact_id = row['ContactID']
                phone_number = row['Phone Number']
                phone_type = row['Phone Type'].lower().strip()
                
                if contact_id not in phone_data:
                    phone_data[contact_id] = {'mobile': '', 'fax': '', 'others': []}
                
                if phone_type == 'mobile':
                    phone_data[contact_id]['mobile'] = phone_number
                elif phone_type == 'fax':
                    phone_data[contact_id]['fax'] = phone_number
                else:
                    if phone_type == 'office':
                        phone_data[contact_id]['others'].append(f"Office ({phone_number})")
                    elif phone_type == 'mill':
                        phone_data[contact_id]['others'].append(f"Mill ({phone_number})")
                    else:
                        phone_data[contact_id]['others'].append(f"{phone_type} ({phone_number})")
    except Exception as e:
        raise RuntimeError(f"Error processing phone data from {phone_file_path}: {str(e)}")
    
    return phone_data

def process_customer_data(customer_data_file):
    """Read and organize customer data by Company Name."""
    customer_data = {}
    try:
        with open(customer_data_file, 'r', newline='') as customer_file:
            customer_reader = csv.DictReader(customer_file)
            for row in customer_reader:
                company_name = row['Company Name'].strip()
                customer_id = row['Customer ID']
                customer_data[company_name] = customer_id
    except Exception as e:
        raise RuntimeError(f"Error processing customer data from {customer_data_file}: {str(e)}")
    
    return customer_data

def update_and_write_contacts(customer_file_path, phone_data, customer_data, output_file_path):
    """Update contact data with phone and customer information and write to output."""
    fieldnames = [
        'ContactID', 'Email', 'First Name', 'Last Name', 'Middle Name',
        'Organization', 'Title', 'Other Phones', 'Mobile', 'Fax',
        'Customer ID', 'Mailing Street', 'Mailing City', 'Mailing State/Province',
        'Mailing Zip/Postal Code', 'Mailing Country'
    ]
    
    try:
        with open(customer_file_path, 'r', newline='') as customer_file:
            customer_reader = csv.DictReader(customer_file)
            
            with open(output_file_path, 'w', newline='') as output_file:
                writer = csv.DictWriter(output_file, fieldnames=fieldnames)
                writer.writeheader()
                
                for row in customer_reader:
                    contact_id = row['ContactID']
                    organization = row.get('Organization', '').strip()
                    
                    # Update phone data
                    phone_info = phone_data.get(contact_id, {'mobile': '', 'fax': '', 'others': []})
                    mobile = phone_info['mobile']
                    fax = phone_info['fax']
                    other_phones = ';'.join(phone_info['others']) if phone_info['others'] else ''
                    
                    # Get Customer ID
                    customer_id = customer_data.get(organization, '')
                    
                    # Create new row with only the specified fieldnames
                    new_row = {
                        'ContactID': row.get('ContactID', ''),
                        'Email': row.get('Email', ''),
                        'First Name': row.get('First Name', ''),
                        'Last Name': row.get('Last Name', ''),
                        'Middle Name': row.get('Middle Name', ''),
                        'Organization': organization,
                        'Title': row.get('Title', ''),
                        'Other Phones': other_phones,
                        'Mobile': mobile,
                        'Fax': fax,
                        'Customer ID': customer_id,
                        'Mailing Street': row.get('Mailing Street', ''),
                        'Mailing City': row.get('Mailing City', ''),
                        'Mailing State/Province': row.get('Mailing State/Province', ''),
                        'Mailing Zip/Postal Code': row.get('Mailing Zip/Postal Code', ''),
                        'Mailing Country': row.get('Mailing Country', '')
                    }
                    
                    writer.writerow(new_row)
    except Exception as e:
        raise RuntimeError(f"Error processing contact data: {str(e)}")

def main():
    """Main function to orchestrate the processing."""
    phone_file = 'SF Contact Phones.csv'
    customer_file = 'SF Contacts.csv'
    customer_data_file = 'SF Customers.csv'
    output_file = 'SF Contacts_updated.csv'
    
    # Verify input files exist
    for f in [phone_file, customer_file, customer_data_file]:
        ensure_file_exists(f)
    
    # Process data
    phone_data = process_phone_data(phone_file)
    customer_data = process_customer_data(customer_data_file)
    update_and_write_contacts(customer_file, phone_data, customer_data, output_file)
    
    print(f"Successfully created {output_file}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {str(e)}")