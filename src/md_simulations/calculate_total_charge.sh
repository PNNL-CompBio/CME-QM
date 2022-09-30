#!/bin/bash

# Function: write out total charge of each molecule, rounded of to nearest integer

# Input arguments
# 1. directory path to .mol2 files
# 2. directory path to save the the file containing the total charges of all the molecules
# 

# Output
#	output file containing the total charges
echo -e "\n==========In calculate_total_charge.sh"

moldir=$1
output_dirpath=$2

output_file=${output_dirpath}/'total_charges.txt'

counter=0
for f in $moldir/*.mol2
do
((counter += 1))
# get molecule name

n1=$(sed -n '/@<TRIPOS>ATOM/ =' ${f})
n2=$(sed -n '/@<TRIPOS>BOND/ =' ${f})

((n1 += 1)) 
((n2 -= 1)) 

#echo "first line number = ${n1}"
#echo "second line number = ${n2}"

line_num=0
charge=0
atom_count=0

while read line; do 
((line_num += 1))

if [ "$line_num" -ge "$n1" ] && [ "$line_num" -le "$n2" ];
then
#line_array=($line)
chg1=$(echo "line: "$line | awk '{print $9}')
#chg1=${line_array[8]}"
#echo "chg1 = $chg1"

chg2=$( bc -l <<< "$charge + $chg1" )
charge=$(printf "%.4f" $chg2)
((atom_count += 1))

fi
done < $f

nc=$(printf "%.*f" 0 $charge)
if [ "$counter" -eq "1" ]; then
echo "${f}	$nc 	$atom_count" > $output_file
fi

if [ "$counter" -gt "1" ]; then
echo "${f}	$nc	$atom_count" >> $output_file
fi

echo "$f        $nc             $charge"

done

# writing out total charge from $output_file

#for f in $moldir/*.mol2
#do

#charge_line=$(grep $f $output_file)
#nc1=$(echo $charge_line | awk '{print $2}')

# round off the charge
#nc=$(printf "%.*f" 4 $nc1)

#echo "$f	$nc		$charge"

#done



