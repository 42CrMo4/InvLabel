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

#item = StockItem(api, 23)



part_id = input("Part ID ")

part = Part(api, part_id)
StockItems = part.getStockItems()
#par = category.getParameters()

#parts = Part.list(api)

#print(len(part))
print(part.description)
print(part.name)
print(part.IPN)

#print(item.part)

with open('part.csv', mode='w') as part_csv:
    part_writer = csv.writer(part_csv, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
 
    part_writer.writerow([part_id, part.IPN, part.name, part.description])
