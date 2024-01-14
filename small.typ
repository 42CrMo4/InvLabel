#import "@preview/cades:0.3.0": qr-code

#let results = csv("part.csv", delimiter: ";")

#set page(
  width: 29mm, 
  height: 12mm,
  margin: (
    y: 0mm,
    x: 0.5mm,
  )
)

#set page(columns: 2)

#set text(5pt)

#for c in results [
#align(center + horizon)[
  #let x = "{\"stockitem\":" + c.at(0) +"}"
  #qr-code(x, height: 12mm) 
  = #c.at(1) 
  #c.at(2)
]]

// brother_ql print -l 29 --600dpi Label.png
