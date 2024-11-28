import requests
import json


import sys

# print ('argument list', sys.argv)

project_id = None
try:
    project_id = sys.argv[1]
except Exception as e:
    print(
        "Please enter the project id like this: python get_quickstatments.py 547383783"
    )

if project_id is None:
    raise Exception(
        "Please enter the project id like this: python get_quickstatments.py 547383783"
    )

base_url = "http://127.0.0.1:3333"

# 1. Get CSRF token
csrf_url = f"{base_url}/command/core/get-csrf-token"
csrf_response = requests.get(csrf_url)
csrf_token = csrf_response.json()["token"]

# 2. Make export-rows POST request
export_url = f"{base_url}/command/core/export-rows/statements.txt"
headers = {"Content-Type": "application/x-www-form-urlencoded"}  # important
data = {
    "csrf_token": csrf_token,
    "engine": '{"facets":[],"mode":"row-based"}',  # Example, adjust as needed
    "project": project_id,  # Replace with your project ID
    "format": "quickstatements",
}


response = requests.post(export_url, headers=headers, data=data)

output_file = "output_quickstatments.txt"
if response.status_code == 200:
    try:
        with open(output_file, "w", encoding="utf-8") as outfile:  # Handle encoding
            outfile.write(response.text)
        print(f"Data exported successfully to {output_file}")

    except Exception as e:  # Handle file writing errors
        print(f"Error writing to file: {e}")

else:
    print(f"Error exporting data: {response.status_code}")
    print(response.text)  # To see the error response from OpenRefine
