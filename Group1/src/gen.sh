#!/bin/bash

unset a
unset k
unset p

while getopts ":a:k:p" o;do
	case "${o}" in
		
		a)
			a=${OPTARG}
			;;
		k)
			k=${OPTARG}
			;;
		p)
			p=${OPTARG}
			;;
		*)
			echo "Invalid Parameter"
			exit 0
			;;
	esac
done
echo $a
echo $k
if [ -z "$a" ] || [ -z "$k" ]; then
	echo "usage: ./gen.sh -a <smooth-parameter> -k <context-size>"
	exit 1
fi

echo $a
echo $k
for (( i=1; i<=5; i++))
do	
	echo "python3 generator.py -a $a -k $k -path ../example/example.txt -p beast" 
	python3 generator.py -a $a -k $k -path ../example/example.txt -p beast
done

#python3 generator.py -a 0.01 -k 5 -path ../example/example.txt -p beast


