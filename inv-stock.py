# Import necessary modules from the InvenTree library
from inventree.api import InvenTreeAPI
from inventree.part import Part
from inventree.stock import StockItem
from inventree.part import Parameter
from inventree.part import ParameterTemplate

# Import additional modules
from dotenv import dotenv_values
import csv
import sys  # Added to handle command-line arguments
import os

# Load environment variables from the '.env' file using dotenv
secrets = dotenv_values(".env")

# Extract the server address and API token from the loaded environment variables
SERVER_ADDRESS = secrets["SERVER_ADDRESS"]
API_TOKEN = secrets["API_TOKEN"]

# Create an InvenTreeAPI instance with the server address and API token
api = InvenTreeAPI(SERVER_ADDRESS, token=API_TOKEN)

# Function to process a single ID (either Part ID or Stock ID)
def process_id(entity_id, label_size, entity_type):
    if entity_type == "part":
        entity = Part(api, entity_id)
        entity_type_description = "part"
    elif entity_type == "stock":
        stock = StockItem(api, entity_id)
        entity = Part(api, stock.part)
        entity_type_description = "stockitem"
    else:
        print("Invalid entity type")
        return

    print(entity.description)
    print(entity.name)
    print(entity.IPN)

    print(entity)

    with open('part.csv', mode='w') as entity_csv:
        entity_writer = csv.writer(entity_csv, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        entity_writer.writerow([entity_id, entity.IPN, entity.name, entity.description, entity_type_description])

    # Use the provided label size for the typst command
    typst_command = f"typst compile -f png --ppi 600 {label_size}.typ label.png"
    os.system(typst_command)

# Check if IDs are provided as command-line arguments
if len(sys.argv) > 3:
    entity_ids = sys.argv[1:-2]
    label_size = sys.argv[-2]
    entity_type = sys.argv[-1]

    # Process each ID in the list
    for entity_id in entity_ids:
        process_id(entity_id, label_size, entity_type)
else:
    # Prompt the user for an ID
    entity_id = input(f"Enter a {entity_type.capitalize()} ID: ")
    process_id(entity_id, label_size, entity_type)
