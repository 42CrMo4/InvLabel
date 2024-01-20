# Inventory Labeling Project

## Overview

This project is designed to streamline the process of generating labels for inventory items stored in an InvenTree database. It utilizes the InvenTree API to retrieve information about parts or stock items and generates labels in different sizes using the Typst and Brother_QL tools.

## Prerequisites

- [InvenTree](https://github.com/inventree/InvenTree): Ensure you have InvenTree installed and set up with your inventory data.

- [Typst](https://www.npmjs.com/package/typst): Install Typst to compile label templates into images.

- [Brother_QL](https://github.com/pklaus/brother_ql): Install Brother_QL to print labels on a Brother QL series label printer.

- Python 3.x: Ensure you have Python 3.x installed.

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
Replace your_inventree_server_address and your_inventree_api_token with your InvenTree server address and API token.

Ensure your Brother QL label printer is connected to your computer.

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

    Modify the label templates in the .typ files to customize the label format.

    The generated labels and CSV file will be saved in the project directory.












# InvLabel
Label printing and design with Typst and BrotherQL.
For now only with MocOS compatible. 

## installation

install the following packages for MacOS

- inevntree python (https://github.com/inventree/inventree-python)
- typst (https://github.com/typst/typst)
- brother QL (https://github.com/pklaus/brother_ql)
- Libusb for brother QL
- python-dotenv

```shell
pip3 install --upgrade inventree
brew install typst
pip3 install --upgrade brother_ql
brew install libusb
pip3 install --upgrade python-dotenv
```

## use

### first run setup

Create and setup the `.env` file.

```
SERVER_ADDRESS = ''
API_TOKEN = ''
```

You only need to do this at the frist time to sept up the Printer.
run the following command to find the USB Printer.

```bash
brother_ql -b pyusb discover
```

use the putput to edit the line `export BROTHER_QL_PRINTER` in the `label_druck.sh` file.

Set the printer Model in the same file at line `export BROTHER_QL_MODEL` see therfore the brother QL documentation. 

```bash
#brother_ql -b pyusb discover
export BROTHER_QL_PRINTER=usb://0x04f9:0x2042 
export BROTHER_QL_MODEL=QL-700  
```

### after the first setup

run sh file in the folder

```bash
sh label_druck.sh
```
### Modification

to alter the design you can adjsut the `medium.typ` and `small.typ` files. These are Typst compiled files. For this see the documntation of the Typst lib. 