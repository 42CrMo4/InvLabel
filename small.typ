// Import necessary libraries
#import "@preview/tiaoma:0.1.0": qrcode

// Read CSV file
#let results = csv("part.csv", delimiter: ";")

// Set the page size and margins
#set page(
  width: 25.91mm, 
  height: 13mm,
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
    #qrcode(x, height: 10.8mm) 
    #let y = c.at(4) + ": " + c.at(0)
    #pad(top:-1.5mm, text(y))

    // Display the part name and description
    = #c.at(1) \
    #c.at(2)
  ]
]
