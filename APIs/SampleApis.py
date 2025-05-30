import requests
import base64
from xml.etree import ElementTree as ET
import io
import os
import csv
import time
from datetime import datetime

def create_company():
    start_time = time.time()  # <-- Start the timer

    ticketNumber = ""
    actionId = ""
    attachmentId = ""
    fileName = ""
    URI = f"https://app.na3.teamsupport.com/api/xml/Customers/2277673/notes/240416"
    organization_id = "1903299"
    api_token = "ec00c5b8-90be-4de6-bcbe-2c97436c2cd7"
    user_agent = "Easy Automation Inc."

    credentials = f"{organization_id}:{api_token}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/xml",
        "User-Agent": user_agent
    }

    response = requests.get(URI, headers=headers)
    if response.status_code == 200:
         # Generate output filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"api_response_{timestamp}.xml"
        
        # Write response to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"Response successfully written to {output_file}")
    else:
        print(f"Request failed with status code: {response.status_code}")
        print(f"Response: {response.text}")

    # Print total runtime
    end_time = time.time()
    total_runtime = end_time - start_time
    print(f"\nTotal runtime: {total_runtime:.2f} seconds")

if __name__ == "__main__":
    create_company()
