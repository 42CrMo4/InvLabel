// Import necessary libraries
#import "@preview/cades:0.3.0": qr-code

// Read CSV file
#let results = csv("part.csv", delimiter: ";")

// Set the page size and margins
#set page(
  width: 29mm, 
  height: 12mm,
  margin: (
    y: 0mm,
    x: 0.5mm,
  )
)

// Set the number of columns on the page
#set page(columns: 2)

// Set the default text size
#set text(5pt)

// Loop through the CSV data
#for c in results [
  // Center-align text horizontally and set the position
  #align(center + horizon)[
    // Create a QR code with part information
    #let x = "{\"" + c.at(4) + "\":" + c.at(0) +"}"
    #qr-code(x, height: 12mm, error-correction: "H") 

    // Display the part name and description
    = #c.at(1) \
    #c.at(2)
  ]
]
