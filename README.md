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