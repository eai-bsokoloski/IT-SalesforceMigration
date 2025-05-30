import csv
import xml.etree.ElementTree as ET

def read_all_products(file_path):
    product_dict = {}
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # Find all Product elements under Products root
        for product in root.findall('Product'):  # Use direct 'Product' since it's a child of Products
            name_elem = product.find('Name')
            product_id_elem = product.find('ProductID')
            if name_elem is not None and product_id_elem is not None and name_elem.text and product_id_elem.text:
                product_dict[name_elem.text.strip()] = product_id_elem.text.strip()
            else:
                print(f"Warning: Skipping product with missing Name or ProductID: {ET.tostring(product, encoding='unicode')}")
    except FileNotFoundError:
        print(f"Error: {file_path} not found")
    except ET.ParseError:
        print(f"Error: Invalid XML format in {file_path}")
    return product_dict

def update_sf_products(sf_file_path, all_products_dict, output_file_path):
    with open(sf_file_path, 'r', newline='') as infile, open(output_file_path, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # Read and write header
        header = next(reader)
        writer.writerow(header)
        
        # Process each row
        for row in reader:
            if len(row) >= 2:
                product_name = row[1].strip()
                # Look up product ID from all_products_dict
                product_id = all_products_dict.get(product_name, row[0])  # Keep original ID if not found
                if product_id == row[0]:
                    print(f"Warning: No matching ProductID found for Product Name '{product_name}'")
                row[0] = product_id
            writer.writerow(row)

def main():
    all_products_file = 'product_info.xml'
    sf_products_file = 'SF Products.csv'
    output_file = 'SF Products Updated.csv'
    
    # Read all products into dictionary
    all_products_dict = read_all_products(all_products_file)
    
    # Update SF Products with matching product IDs
    update_sf_products(sf_products_file, all_products_dict, output_file)
    print(f"Updated file written to {output_file}")

if __name__ == "__main__":
    main()