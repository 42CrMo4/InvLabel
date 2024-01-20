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

# Function to process a single Stock ID
def process_stock_id(stock_id, label_size):
    item = StockItem(api, stock_id)
    part = Part(api, item.part)

    print(part.description)
    print(part.name)
    print(part.IPN)

    print(item.part)

    with open('part.csv', mode='w') as part_csv:
        part_writer = csv.writer(part_csv, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        part_writer.writerow([stock_id, part.IPN, part.name, part.description])

    # Use the provided label size for the typst command
    typst_command = f"typst compile -f png --ppi 600 {label_size}.typ label.png"
    os.system(typst_command)

# Check if Stock IDs are provided as command-line arguments
if len(sys.argv) > 2:
    stock_ids = sys.argv[1]
    label_size = sys.argv[2]

    # Process each Stock ID in the list
    for stock_id in stock_ids:
        process_stock_id(stock_id, label_size)
else:
    # Prompt the user for a Stock ID
    stock_id = input("Enter a Stock ID: ")
    process_stock_id(stock_id, label_size)
