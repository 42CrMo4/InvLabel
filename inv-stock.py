# Import necessary modules from the InvenTree library
from inventree.api import InvenTreeAPI
from inventree.part import Part
from inventree.stock import StockItem

# Import necessary modules from the brother_ql library
from PIL import Image
import PIL 
PIL.Image.ANTIALIAS = PIL.Image.LANCZOS
from brother_ql.conversion import convert
from brother_ql.backends.helpers import send
from brother_ql.raster import BrotherQLRaster

# import Typst
#import typst

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
#os.environ['BROTHER_QL_PRINTER'] = 'usb://0x04f9:0x2042'
#os.environ['BROTHER_QL_MODEL'] = 'QL-700'

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

    #typst.compile("{label_size}.typ", output="label.png", format="png", ppi=600.0)

    # Print the label using brother_ql with specified parameters
    #brother_ql_command = f"brother_ql print -l 29 --600dpi label.png"
    
    # Run the brother_ql command and capture the output
    #brother_ql_output = subprocess.run(brother_ql_command, shell=True, text=True, capture_output=True)
    
    # Print brother_ql output
    #print("Brother_QL Output:")
    #print(brother_ql_output.stdout)
    #print(brother_ql_output.stderr)

    im = Image.open('label.png')
    # im.resize((306, 991)) 

    backend = 'pyusb'    # 'pyusb', 'linux_kernal', 'network'
    model = 'QL-700' # your printer model.
    printer = 'usb://0x04f9:0x2042'    # Get these values from the Windows usb driver filter.  Linux/Raspberry Pi uses '/dev/usb/lp0'.

    qlr = BrotherQLRaster(model)
    qlr.exception_on_warning = True

    instructions = convert(

            qlr=qlr, 
            images= [im],    #  Takes a list of file names or PIL objects.
            label='29', 
            rotate='0',    # 'Auto', '0', '90', '270'
            threshold=70.0,    # Black and white threshold in percent.
            dither=True, 
            compress=False, 
            red=False,    # Only True if using Red/Black 62 mm label tape.
            dpi_600=True, 
            hq=True,    # False for low quality.
            cut=True

    )

    send(instructions=instructions, printer_identifier=printer, backend_identifier=backend, blocking=True)

# Dictionary for mapping numerical options to entity types
entity_type_options = {1: "part", 2: "stock"}

# Dictionary for mapping numerical options to label sizes
label_size_options = {1: "small", 2: "medium"}

# Main loop
while True:
    print("Options:")
    print("1. Process Part IDs")
    print("2. Process Stock IDs")
    print("0. Quit")

    # Prompt the user to choose an option
    option = int(input("Choose an option: "))

    if option == 0:
        break
    elif option in entity_type_options:
        # Prompt the user to select the label size
        entity_type = entity_type_options[option]

        print("Label Sizes:")
        print("1. Small")
        print("2. Medium")

        # Prompt the user until a valid label size is entered
        while True:
            label_option = int(input("Select the label size: "))
            
            if label_option in label_size_options:
                label_size = label_size_options[label_option]
                break
            else:
                print("Invalid label size option")
    else:
        print("Invalid option. Please enter a valid option.")
        continue  # Restart the loop to ask for a valid option

    # Prompt the user for a space-separated list of IDs
    entity_ids = input(f"Enter a space-separated list of {entity_type} IDs (or 'quit' to exit): ")

    # Check if the user wants to quit
    if entity_ids.lower() == "quit":
        break

    # Process each ID in the list
    for entity_id in entity_ids.split():
        process_id(entity_id, label_size, entity_type)
