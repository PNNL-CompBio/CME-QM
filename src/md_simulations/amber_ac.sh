#!/bin/bash
# amber_ac.sh
#	-Executes ANTECHAMBER runs in the "ANTECHAMBER" directory to assign AM1-BCC charges 
#	 to the atoms in the molecule structure file.
#	-Does a parameter check.
#
# Author:  Dr. Dennis Thomas (PNNL)
#
# Usage:
#	./amber_ac.sh {mol} {mol2f} {rindex} {amberdir}
# Input arguments
#       mol:  molecule directory name (this will be the name of the mol2 file
#               used in the MD simulations)
#	mol2f:  name of the molecule structure file .mol2 file format (assumed to be located in 
#		the RUN{rindex} directory)
#       rindex: integer number to create "RUN{rindex}" directory
#               (e.g., if rindex = 1, then directory "RUN1" will be
#               created.)
#	amberdir:  path to the AMBER directory
# Output
#	-{mol2f}_md.mol2 file in directories, ANTECHAMBER and RUN{rindex}
#	-other files from the ANTECHAMBER runs
#
echo -e "\n==========In amber_ac.sh :"
start_time=$(date +%s)
mol=$1
mol2f=$2
totchg=$3
rindex=$4

cwd=$(pwd)
echo "current directory" $cwd
moldir=$cwd/${mol} # molecule simulation directory
rundir=$moldir/RUN1   #$rindex  # run directory
#rundir=$moldir/RUN$rindex  # run directory
acdir=$rundir/ANTECHAMBER # antechamber
mdext="_md"
cd $acdir



pid="${!}"

#echo " raj:   check, $amberdir"
echo "moldir: "$moldir
echo "acdir: "$acdir
echo "antechamber path: "$ANTECHAMBER
echo "rundir: "$rundir
echo "agr1: "$mol2f.mol2
echo "agr2: "$mol2f$mdext.mol2

antechamber -i $rundir/$mol2f.mol2 -fi mol2 -o $mol2f$mdext.mol2 -fo mol2 -c bcc -s -du -nc $totchg

#$amberdir/bin/antechamber -i $rundir/$mol2f.mol2 -fi mol2 -o $mol2f$mdext.mol2 -fo mol2 -c rc -cf $moldir/$mol2f.crg -s -du
wait $pid

pid="${!}"
echo "parmchk2 path: "$PARMCHK2
parmchk2 -i ANTECHAMBER_AC.AC -f ac -o $mol2f$mdext.frcmod

wait $pid

cp $mol2f$mdext.mol2 $rundir/


finish_time=$(date +%s)

runtime=$(( $(( finish_time - start_time))/60 ))

echo "run time = $runtime minutes."
