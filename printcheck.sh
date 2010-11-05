#!/bin/bash
printers=( 'EB325BW1' 'EB325BW1' 'EB423BW1' )
printfile=$HOME/scripts/data/printfile.txt
for printer in ${printers[@]}
do
	echo "lpr $printfile -P $printer"
done
