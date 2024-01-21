# InvLabel

Label printing and design with Typst and local or wireless printing with Brother_QL.

## Overview

This project is designed to streamline the process of generating labels for inventory items stored in an InvenTree database. It utilizes the InvenTree API to retrieve information about parts or stock items and generates labels in different sizes using the Typst and Brother_QL tools.

## Prerequisites

- [InvenTree Server](https://github.com/inventree/InvenTree): Ensure you have InvenTree Server running and set up with your inventory data.
- [InvenTree Python](https://github.com/inventree/inventree-python): Ensure you have InvenTree Python installed.
- [Typst](https://github.com/typst/typst): Install Typst to compile label templates into images.
- [Brother_QL](https://github.com/pklaus/brother_ql): Install Brother_QL to print labels on a Brother QL series label printer.
- Python 3.x: Ensure you have Python 3.x installed.
- [Python Dotenv](https://github.com/theskumar/python-dotenv): Install python dotenv.

## Setup

1. Clone the repository:

```bash
git clone https://github.com/your-username/inventory-labeling.git
```

2. Navigate to the project directory:

```bash
cd inventory-labeling
```

3.Create a .env file in the project root with the following content:

```ini
SERVER_ADDRESS=your_inventree_server_address
API_TOKEN=your_inventree_api_token
```
Replace `your_inventree_server_address` and `your_inventree_api_token` with your InvenTree server address and API token.

## Steup brother_ql

Ensure your Brother QL label printer is connected to your computer.

You only need to do this at the frist time to sept up the Printer.
run the following command to find the USB Printer.

:bangbang: Please make sure the needed backend of brother_ql is istalled according to the documentation https://github.com/pklaus/brother_ql#backends

```bash
brother_ql -b pyusb discover
```

use the output to edit the line `export BROTHER_QL_PRINTER` in the `inv-stock.py` file.

Set the printer Model in the same file at line `export BROTHER_QL_MODEL` see therfore the brother QL documentation. 

This should look like this, but with your values.
```bash
export BROTHER_QL_PRINTER=usb://0x04f9:0x2042 
export BROTHER_QL_MODEL=QL-700  
```

### Label Modification

to alter the design you can adjsut the `medium.typ` and `small.typ` files. These are Typst compiled files. 
For this see the documntation of the Typst lib or the online editor at http://typst.app .
You can try and iterate quickly with only havin the `csv` and `typ` file present in the editor. 

## Usage

Run the label printing script:

```bash
python3 inv-stock.py
```

Follow the prompts to choose the entity type (Part or Stock Item), label size, and enter a space-separated list of entity IDs to generate labels.
Example

To print labels for parts with IDs 1, 2, and 3 in small size:

```bash
python3 inv-stock.py 1 2 3 small
```
## Additional Notes

Ensure the Brother QL printer is correctly set up and configured on your system.
See also the Documentation for [brother_ql](https://github.com/pklaus/brother_ql)

Modify the label templates in the .typ files to customize the label format.

The generated labels and CSV file will be saved in the project directory.
