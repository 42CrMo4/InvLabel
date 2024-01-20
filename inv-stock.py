# Import necessary modules from the InvenTree library
from inventree.api import InvenTreeAPI
from inventree.part import Part
from inventree.stock import StockItem
from inventree.part import Parameter
from inventree.part import ParameterTemplate

# Import additional modules
from dotenv import dotenv_values
import csv
import os
import subprocess

# Load environment variables from the '.env' file using dotenv
secrets = dotenv_values(".env")

# Extract the server address and API token from the loaded environment variables
SERVER_ADDRESS = secrets["SERVER_ADDRESS"]
API_TOKEN = secrets["API_TOKEN"]

# Create an InvenTreeAPI instance with the server address and API token
api = InvenTreeAPI(SERVER_ADDRESS, token=API_TOKEN)

# Set brother_ql parameters
os.environ['BROTHER_QL_PRINTER'] = 'usb://0x04f9:0x2042'
os.environ['BROTHER_QL_MODEL'] = 'QL-700'

# Function to process a single ID (either Part ID or Stock ID)
def process_id(entity_id, label_size, entity_type):
    if entity_type == "part":
        # If the entity is a part, retrieve information using Part class
        entity = Part(api, entity_id)
        entity_type_description = "part"
    elif entity_type == "stock":
        # If the entity is a stock item, retrieve information using StockItem and Part classes
        stock = StockItem(api, entity_id)
        entity = Part(api, stock.part)
        entity_type_description = "stockitem"
    else:
        print("Invalid entity type")
        return

    # Print information about the entity
    print(entity.description)
    print(entity.name)
    print(entity.IPN)

    # Write entity information to a CSV file
    with open('part.csv', mode='w') as entity_csv:
        entity_writer = csv.writer(entity_csv, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # Write a row to the CSV file containing ID, IPN, name, description, and entity type
        entity_writer.writerow([entity_id, entity.IPN, entity.name, entity.description, entity_type_description])

    # Use the provided label size for the typst command
    typst_command = f"typst compile -f png --ppi 600 {label_size}.typ label.png"
    
    # Run the typst command and capture the output
    typst_output = subprocess.run(typst_command, shell=True, text=True, capture_output=True)
    
    # Print typst output
    print("Typst Output:")
    print(typst_output.stdout)
    print(typst_output.stderr)

    # Print the label using brother_ql with specified parameters
    brother_ql_command = f"brother_ql print -l 29 --600dpi label.png"
    
    # Run the brother_ql command and capture the output
    brother_ql_output = subprocess.run(brother_ql_command, shell=True, text=True, capture_output=True)
    
    # Print brother_ql output
    print("Brother_QL Output:")
    print(brother_ql_output.stdout)
    print(brother_ql_output.stderr)

# Prompt the user to choose whether to process Part IDs or Stock IDs
entity_type = input("Choose an option (part/stockitem): ").lower()

# Prompt the user to select the label size
label_size = input("Select the label size (small/medium): ").lower()

# Main loop
while True:
    # Prompt the user for a space-separated list of IDs
    entity_ids = input(f"Enter a space-separated list of {entity_type} IDs (or 'quit' to exit): ")

    # Check if the user wants to quit
    if entity_ids.lower() == "quit":
        break

    # Process each ID in the list
    for entity_id in entity_ids.split():
        process_id(entity_id, label_size, entity_type)
