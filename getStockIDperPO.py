import requests
from dotenv import dotenv_values

# Load environment variables from the '.env' file using dotenv
secrets = dotenv_values(".env")

# Extract the server address and API token from the loaded environment variables
INVENTREE_URL = secrets["SERVER_ADDRESS"]
API_TOKEN = secrets["API_TOKEN"]

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

def get_stock_items_from_po(inventree_url, api_token, purchase_order_id):
    """
    Fetch all stock items for a received purchase order in InvenTree.
    
    :param inventree_url: Base URL of the InvenTree instance (e.g., 'http://localhost:8000')
    :param api_token: API token for authentication
    :param purchase_order_id: ID of the received purchase order
    :return: List of stock item PKs associated with the purchase order
    """
    headers = {
        "Authorization": f"Token {api_token}",
        "Accept": "application/json"
    }
    
    # Fetch stock items directly using the purchase order ID
    stock_url = f"{inventree_url}/api/stock/?purchase_order={purchase_order_id}"
    response = requests.get(stock_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch stock items: {response.status_code} - {response.text}")
        return None
    
    stock_items = response.json()
    
    return [item.get("pk") for item in stock_items if item.get("pk") is not None]

# Example usage
if __name__ == "__main__":
    PURCHASE_ORDER_ID = inputNumber("Purchase Order ID: ")  # Replace with your purchase order ID
    
    stock_pks = get_stock_items_from_po(INVENTREE_URL, API_TOKEN, PURCHASE_ORDER_ID)
    if stock_pks:
        print("Stock item PKs for the received purchase order:")
        print(" ".join(map(str, sorted(stock_pks))))
