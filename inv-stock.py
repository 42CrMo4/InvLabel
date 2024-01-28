# Import necessary modules from the InvenTree library
from inventree.api import InvenTreeAPI
from inventree.part import Part
from inventree.stock import StockItem
from inventree.stock import StockLocation 

# Import necessary image moduel for brother_ql
from PIL import Image

# Import necessary modules from the brother_ql library
from brother_ql.conversion import convert
from brother_ql.backends.helpers import send
from brother_ql.raster import BrotherQLRaster

# import Typst
import typst

# Import additional modules
from dotenv import dotenv_values
import csv

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
        # If the entity is a part, retrieve information using Part class
        entity = Part(api, entity_id)
        ipn = entity.IPN
        entity_type_description = "part"
    elif entity_type == "stock":
        # If the entity is a stock item, retrieve information using StockItem and Part classes
        stock = StockItem(api, entity_id)
        entity = Part(api, stock.part)
        ipn = entity.IPN
        entity_type_description = "stockitem"
    elif entity_type == "location":
        # If the entity is a stock item, retrieve information using StockItem and Part classes
        entity = StockLocation(api, entity_id)
        ipn = ''
        entity_type_description = "stocklocation"
    else:
        print("Invalid entity type")
        return

    # Print information about the entity
    print(entity.description)
    print(entity.name)
    print(ipn)

    # Write entity information to a CSV file
    with open('part.csv', mode='w', encoding="utf-8") as entity_csv:
        entity_writer = csv.writer(entity_csv, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # Write a row to the CSV file containing ID, IPN, name, description, and entity type
        entity_writer.writerow([entity_id, ipn, entity.name, entity.description, entity_type_description])

    # Typst compile
    typst_label_size = f"{label_size}.typ"

    typst.compile(typst_label_size, output="label.png", format="png", ppi=600.0)

    # image preperation
    im = Image.open('label.png')
    # im.resize((306, 991)) 

    # brother ql setup
    backend = 'pyusb'    # 'pyusb', 'linux_kernal', 'network'
    model = 'QL-700' # your printer model.
    printer = 'usb://0x04f9:0x2042'    # Get these values from the Windows usb driver filter.  Linux/Raspberry Pi uses '/dev/usb/lp0'.

    qlr = BrotherQLRaster(model)
    qlr.exception_on_warning = True

    # brother ql label setup
    # https://stackoverflow.com/a/61771673
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

    # brother_ql send
    send(instructions=instructions, printer_identifier=printer, backend_identifier=backend, blocking=True)

# Dictionary for mapping numerical options to entity types
entity_type_options = {1: "part", 2: "stock", 3: "location"}

# Dictionary for mapping numerical options to label sizes
label_size_options = {1: "small", 2: "medium", 3: "Text+Barcode"}

def inputNumber(message):
    while True:
        try:
            userInput = int(input(message))       
        except ValueError:
            print("Not an integer! Try again.")
            continue
        else:
            return userInput 
            break 

# Main loop
while True:
    print("Options:")
    print("1. Process Part IDs")
    print("2. Process Stock IDs")
    print("3. Process Location IDs")
    print("0. Quit")

    # Prompt the user to choose an option
    option = inputNumber("Choose an option: ")

    if option == 0:
        break
    elif option in entity_type_options:
        # Prompt the user to select the label size
        entity_type = entity_type_options[option]

        print("Label Sizes:")
        print("1. Small")
        print("2. Medium")
        print("3. Text+Barcode")

        # Prompt the user until a valid label size is entered
        while True:
            label_option = inputNumber("Select the label size: ")
            
            if label_option in label_size_options:
                label_size = label_size_options[label_option]
                break
            else:
                print("Invalid label size option")
                continue  # Restart the loop to ask for a valid option
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


