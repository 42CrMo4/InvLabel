from inventree.api import InvenTreeAPI
#from inventree.part import PartCategory
from inventree.part import Part
from inventree.stock import StockItem
from inventree.part import Parameter
from inventree.part import ParameterTemplate

from dotenv import dotenv_values

import csv

secrets = dotenv_values(".env")

SERVER_ADDRESS = secrets["SERVER_ADDRESS"]
API_TOKEN = secrets["API_TOKEN"]

api = InvenTreeAPI(SERVER_ADDRESS, token=API_TOKEN)

stock_id = input("Stock ID ")

item = StockItem(api, stock_id)

part = Part(api, item.part)

#StockItems = part.getStockItems()
#par = category.getParameters()

#parts = Part.list(api)

#print(len(part))
print(part.description)
print(part.name)
print(part.IPN)

print(item.part)

with open('part.csv', mode='w') as part_csv:
 part_writer = csv.writer(part_csv, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

 part_writer.writerow([stock_id, part.IPN, part.name, part.description])

