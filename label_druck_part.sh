#brother_ql -b pyusb discover
export BROTHER_QL_PRINTER=usb://0x04f9:0x2042
export BROTHER_QL_MODEL=QL-700  
while true
do
	Python3 inv-part.py

	#https://linuxize.com/post/bash-select/
	PS3="Select the operation: "

	select opt in small medium quit; do

		case $opt in
			small)
			typst compile -f png --ppi 600 small.typ label.png
			break
			;;
			medium)
			typst compile -f png --ppi 600 medium.typ label.png
			break
			;;
			quit)
			break
			;;
			*) 
			echo "Invalid option $REPLY"
			;;
		esac
	done 

	brother_ql print -l 29 --600dpi label.png
	rm *.csv
	rm *.png
done