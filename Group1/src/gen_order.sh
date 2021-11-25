#!/bin/bash

# variação do texto em função de k

unset a
unset path
unset prior
unset text_size

while getopts ":t:s:" o;do
        case "${o}" in
                
		t)	path=${OPTARG}
			;;
		s)
			text_size=${OPTARG}
			;;
                *)
                        echo "Invalid Parameter"
                        exit 0
                        ;;
        esac
done

smooth=(0 0.1 1)
prior=(a or the same beast)
text_size=(20 100 500)
if [ -z "$path"];then
	path="../example/example.txt"
fi
for s in "${text_size[@]}"
do
	echo -e "------ text_size=$s ----------\n"
	for a in "${smooth[@]}"
	do
		echo -e "\t-------- a=$a ------- \n"
 
		for (( k=1; k<=5; k++))
			do
        			echo -e " ** python3 generator.py -a $a -k $k -path $path -p ${prior[$k-1]} -s $s \n"
        			python3 generator.py -a $a -k $k -path $path -p ${prior[$k-1]} -s $s
				echo "--------------------"
			done
		echo
	done
done
