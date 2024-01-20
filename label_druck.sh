#brother_ql -b pyusb discover
export BROTHER_QL_PRINTER=usb://0x04f9:0x2042
export BROTHER_QL_MODEL=QL-700  

#!/bin/bash

echo "Excel trick -> =TEXTVERKETTEN(" ";WAHR;matrix)"

# Prompt the user to choose whether to process Part IDs or Stock IDs
PS3="Choose an option: "
select option in Part_IDs Stock_IDs quit; do
    case $option in
        Part_IDs)
            entity_type="part"
            break
            ;;
        Stock_IDs)
            entity_type="stock"
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

# Function to process a single ID (either Part ID or Stock ID)
process_id() {
    local entity_id=$1

    Python3 inv-stock.py "$entity_id" "$label_size" "$entity_type"

    brother_ql print -l 29 --600dpi label.png
    rm *.csv
    rm *.png
}

# Main loop
while true; do
    read -p "Enter a space-separated list of $entity_type IDs (or 'quit' to exit): " entity_ids

    # Check if the user wants to quit
    if [ "$entity_ids" == "quit" ]; then
        break
    fi

    # Process each ID in the list
    for entity_id in $entity_ids; do
        process_id "$entity_id"
    done
done
