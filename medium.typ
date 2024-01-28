// Import necessary libraries
#import "@preview/tiaoma:0.1.0": qrcode

// Read CSV file
#let results = csv("part.csv", delimiter: ";")

// Set the page margins
#set page(
  width: 25.91mm,
  height: 18mm,
  margin: (
    y: 0mm,
    x: 0.5mm,
  )
)

// Loop through the CSV data
#for c in results [
  // Set text position
  #set text(3mm)
  #align(center)[= #c.at(1)] // Center-align the text of the second column
  #set text(5pt)
  // Create a box to contain information
  #box(height: 36pt,
    columns(2, gutter: 0pt)[
      //#set par(justify: true) // strech text in even spacing
      #align(center + top)[
        // Create a QR code with part information
        #let x = "{\"" + c.at(4) + "\":" + c.at(0) +"}"
        #qrcode(x, height: 10.5mm) 
        #let y = c.at(4) + ": " + c.at(0)
        #pad(top:-1.5mm, text(y))

        // Set text size and display part information
        *#c.at(2)* \ // Display the name of the part
        #set text(4pt)
        #c.at(3) // Display the description of the part
      ]  
    ]
  )
]
