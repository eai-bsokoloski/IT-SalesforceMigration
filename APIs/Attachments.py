import requests
import base64
from xml.etree import ElementTree as ET
import io
import os
import csv
import time  # <-- Import time module

def create_company():
    start_time = time.time()  # <-- Start the timer

    os.makedirs('Files', exist_ok=True)

    # Open output CSV file for writing
    with open('attachmentWithName.csv', mode='w', newline='', encoding='utf-8') as out_csv:
        writer = csv.writer(out_csv)
        # Write header
        writer.writerow(['ticketNumber', 'actionId', 'attachmentId', 'save_file_name'])

        with open('Attachments by ticket number.csv', mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header

            for i, row in enumerate(reader):
                if i >= 10:
                    break

                ticketNumber = row[0]
                actionId = row[2]
                attachmentId = row[1]
                fileName = row[6]
                print("Starting record on row: " + str(i) + " with ticketNumber: " + ticketNumber + " with attachmentId: " + attachmentId)

                URI = f"https://app.na3.teamsupport.com/api/xml/Tickets/{ticketNumber}/Actions/{actionId}/Attachments/{attachmentId}"
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
                    try:
                        # Build the output file path
                        save_file_name = fileName.replace(".", "_" + attachmentId + ".", 1)
                        newFileName = f'Files/{save_file_name}'

                        with open(newFileName, 'wb') as f:
                            f.write(response.content)
                        print(f"File saved to {newFileName}")

                        # Write success info to CSV
                        writer.writerow([ticketNumber, actionId, attachmentId, save_file_name])
                    except Exception as e:
                        print(f"Error writing to file: {str(e)}")
                else:
                    print(f"Request failed with status code: {response.status_code}")
                    print(f"Response: {response.text}")

    # Print total runtime
    end_time = time.time()
    total_runtime = end_time - start_time
    print(f"\nTotal runtime: {total_runtime:.2f} seconds")

if __name__ == "__main__":
    create_company()
