// Import necessary libraries
#import "@preview/cades:0.3.0": qr-code

// Read CSV file
#let results = csv("part.csv", delimiter: ";")

// Set the page margins
#set page(
  width: 29mm, 
  height: 19.1mm,
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

  // Create a box to contain information
  #box(height: 40pt,
    columns(2, gutter: 0pt)[
      //#set par(justify: true) // strech text in even spacing
      #align(center + horizon)[
        // Create a QR code with part information
        #let x = "{\"" + c.at(4) + "\":" + c.at(0) +"}"
        #qr-code(x, height: 14mm) 
        
        // Set text size and display part information
        #set text(6pt)
        *#c.at(2)* \ // Display the name of the part
        #set text(5pt)
        #c.at(3) // Display the description of the part
      ]  
    ]
  )
]
