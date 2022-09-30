#!/bin/bash
# setupallfiles.sh
# Author:  Dr. Dennis Thomas (PNNL)
#
# This script calls the setupfiles.sh for each .mol2 file in a directory. 
# Usage:
#	./setupallfiles.sh {mol2dir} {rindex} {saindex}
# Input arguments
#	mol2dir:  molecule directory name containing the .mol2 files
#	rindex: integer number to create "RUN{rindex}" directory 
#		(e.g., if rindex = 1, then directory "RUN1" will be
#		created.)
#	saindex:  integer number to create "ANNEAL{saindex}" directory 
#		(e.g., if saindex = 1, then directory "ANNEAL1" will 
#		be created."

#start_time=$(date +%s)
#export AMBERHOME=/home/scicons/cascade/apps/amber/amber14
#export AMBERHOME=/project/amber14
#AMBERHOME=/project/amber14
#amberdir=/home/scicons/cascade/apps/amber/amber14
echo -e "\n==========In batch_setupallfiles.sh :"

cwd=$(pwd)
echo "Current dir "$cwd

moldir=$1
rindex=$2
saindex=$3
start_count=$4
end_count=$5
md_dir=$6

echo "mol2dir: " $moldir
echo "mddir: " $mddir
echo "rindex: " $rindex "saindex: " $saindex
echo "start_count: " $start_count "end_count: " $end_count


counter=0
for f in $moldir/*.mol2
do
start_time=$(date +%s) # added on 5/18/2018

((counter += 1))
if [ "$counter" -ge "$start_count" ] && [ "$counter" -le "$end_count" ];
then # starting calculations

# get molecule name by stripping off .mol2 from the file name (f).
mol=${f%.mol2}
echo "molecule name:" $mol

# set up file directory structure for AMBER MD simulations
src/md_simulations/setupfiles.sh $mol $rindex $saindex

# copy .mol2 file into the respective AMBER MD RUN directory
#RJ
#cp ./$f ./$mol/RUN$rindex/ 
# FIXME: Why I'm copying .mol2 again?:
cp ./$f ./$mol/RUN1/

# assign AM1-BCC charges to the atoms

mol2f=${mol##*/}
echo "Assigning AM1-BCC charges to mol2 file, $mol2f"

echo "In directory mol = $mol"

# identify if the molecule is protonated, de-protonated or sodiated.

# first create a temporary .mol2 file from the original file located in the 
# top-level molecule directory (moldir)
echo "mol2f  = $mol2f"
echo "mol = $mol"


# remove all *tmp.mol2 files
#if [ -d "$mol" ]
#then
#rm ./$mol/RUN$rindex/${mol2f}_tmp.mol2
#rm ./$mol/RUN1/${mol2f}_tmp.mol2
#fi

# get total charge from total_charges.txt file
# first get line corresponding to the mol file
echo "total_charges dir" $md_dir
charge_line=$(find .  -path "*$md_dir*" -type f -name "total_charges.txt")
#charge_line=$(grep $md_dir total_charges.txt)
echo "charge_line :"$charge_line
nc1=$(echo $charge_line | awk '{print $2}')

# round off the charge
nc=$(printf "%.*f" 4 $nc1)
echo "total charge on the molecule: $nc"

pid="${!}"
echo "Running amber_ac.sh :"
src/md_simulations/amber_ac.sh $mol $mol2f $nc $rindex

wait $pid
#cp ./$mol/RUN$rindex/ANTECHAMBER/${mol2f}_md.mol2 ./$mol/RUN$rindex/ANTECHAMBER/mol_tleapinput.mol2  # creating a copy f$
cp ./$mol/RUN1/ANTECHAMBER/${mol2f}_md.mol2 ./$mol/RUN1/ANTECHAMBER/mol_tleapinput.mol2  # creating a copy f$

#-------------------------


# copy leap.in file to TLEAP directory
#cp leap.in ./$mol/RUN$rindex/TLEAP/

cd ./$mol/RUN$rindex/TLEAP
pid=${!}
#$AMBERHOME/bin/tleap
tleap -s -f leap.in
wait
mv inpcrd ${mol2f}.crd
mv prmtop ${mol2f}.top

cd $cwd

fi  # counter 


finish_time=$(date +%s)

runtime=$(( $(( finish_time - start_time))/60 ))

echo "run time = $runtime minutes."

done

echo "==========Finish"
