// import all libs
#import "@preview/cades:0.3.0": qr-code

// reas csv
#let results = csv("part.csv", delimiter: ";")

// set the page margins
#set page(
  width: 29mm, 
  height: 19.1mm,
  margin: (
    y: 0mm,
    x: 0.5mm,
  )
)

// loop through the csv
#for c in results [
  #set text(3mm)
  #align(center)[= #c.at(1)]

  #box(height: 40pt,
    columns(2, gutter: 0pt)[
      //#set par(justify: true) // strech text in even spacing
      #align(center + horizon)[
        #let x = "{\"stockitem\":" + c.at(0) +"}"
        #qr-code(x, height: 14mm) 
        #set text(6pt)
        *#c.at(2)*
        #set text(5pt)
        #c.at(3)
      ]  
    ]
  )
]