#brother_ql -b pyusb discover
export BROTHER_QL_PRINTER=usb://0x04f9:0x2042
export BROTHER_QL_MODEL=QL-700  

#!/bin/bash

# Prompt the user to select the label size
PS3="Select the label size: "
select label_size in small medium quit; do
    case $label_size in
        small|medium)
            break
            ;;
        quit)
            exit
            ;;
        *)
            echo "Invalid option $REPLY"
            ;;
    esac
done

# Function to process a single Stock ID
process_stock_id() {
    local stock_id=$1

    Python3 inv-stock.py "$stock_id" "$label_size"

    brother_ql print -l 29 --600dpi label.png
    rm *.csv
    rm *.png
}

# Main loop
while true; do
    read -p "Enter a space-separated list of Stock IDs (or 'quit' to exit): " stock_ids

    # Check if the user wants to quit
    if [ "$stock_ids" == "quit" ]; then
        break
    fi

    # Process each Stock ID in the list
    for stock_id in $stock_ids; do
        process_stock_id "$stock_id"
    done
done
