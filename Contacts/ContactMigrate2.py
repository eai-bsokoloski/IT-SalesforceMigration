import pandas as pd

# Load the CSV files
old_contacts = pd.read_csv('SF Contacts Old.csv')
new_contacts = pd.read_csv('SF Contacts New.csv')

# Remove rows from new_contacts where Contact ID exists in old_contacts
filtered_contacts = new_contacts[~new_contacts['ContactID'].isin(old_contacts['ContactID'])]

# Write the filtered data to a new CSV file
filtered_contacts.to_csv('SF Contacts Filtered.csv', index=False)

print("Filtered CSV file 'SF Contacts Filtered.csv' has been created successfully.")