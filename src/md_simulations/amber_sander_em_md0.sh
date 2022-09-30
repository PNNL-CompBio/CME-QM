#!/bin/bash
# amber_sander_em_md0.sh
#	- Uses 'sander' to do the energy minimization, and an initial MD run at the target
#	  temperature for 100 picoseconds.
# Author:  Dr. Dennis Thomas (PNNL)
# Usage:
#	./amber_sander_em_md0.sh ${mol2dir} {mol} {rindex} {saindex} {amberdir}
#
# Input arguments
#       mol:  molecule directory name (this will be the name of the mol2 file
#               used in the MD simulations)
#       rindex: integer number to create "RUN{rindex}" directory
#               (e.g., if rindex = 1, then directory "RUN1" will be created.)
#       saindex:  integer number to create "ANNEAL{saindex}" directory
#               (e.g., if saindex = 1, then directory "ANNEAL1" will
#               be created."
#       amberdir:  path to the AMBER directory
#
# Input files required for energy minimization
#	- em.in : input parameter file for energy minimization, located in the EM directory
#	- {mol}.top : amber topology file of the molecule, located in the TLEAP directory
#	- {mol}.crd : amber coordinate file of the molecule, located in the TLEAP directory
#
#	
# Output files from energy minimization run: {mol}_em.out, {mol}_em.rst
# The output files will be in the EM directory.
# Input files required for initial MD run
#	- md0.in : input parameter file for an initial MD run at the target temperature
#	- {mol}_em.rst : output coordinate file from the energy minimization run
#	- {mol}.top : amber topology file of the molecule, located in the TLEAP directory
#
# Output files from initial MD run:  {mol}_md0.out, {mol}_md0.crd, {mol}_md0.rst
# The output files will be in the MD0 directory.

echo -e "\n==========In amber_sander_em_md0.sh :"

start_time=$(date +%s)
mol2dir=$1
mol=$2
rindex=$3
saindex=$4
#export AMBERHOME=/home/scicons/cascade/apps/amber/amber14
#amberdir=$5


cwd=$(pwd)
moldir=$cwd/${mol2dir}/${mol} # molecule simulation directory
rundir=$moldir/RUN$rindex  # run directory
acdir=$rundir/ANTECHAMBER # antechamber
tldir=$rundir/TLEAP # tleap
emdir=$rundir/EM # energy minimization
md0dir=$rundir/MD0 # 1st MD run at target temperature (e.g., 300 K)
sadir=$rundir/ANNEAL$saindex

echo "creating following directories at: "$cwd
echo "moldir: "$moldir
echo "rundir:"$rundir
echo "acdir: "$acdir
echo "tldir: "$tldir
echo "emdir: "$emdir
echo "md0dir: "$md0dir
echo "sadir: "$sadir

mdext="_md"

# energy minimization
cd $emdir
emext="_em"
pid="${!}"

echo "1. Running SANDER :"
echo "agr1: " $mol$emext.out
echo "agr2: " $tldir/$mol.crd
echo "agr3: " $tldir/$mol.top
echo "agr4: " $mol$emext.rst

sander -O -i em.in -o $mol$emext.out -c $tldir/$mol.crd -p $tldir/$mol.top -r $mol$emext.rst

wait $pid

# 1st MD run at target temperature

i=0
cd $md0dir

pid="${!}"

echo "2. Running SANDER :"
echo "agr1: " md$i.in
echo "agr2: " $mol$i.out
echo "agr3: " $emdir/$mol$emext.rst
echo "agr4: " $tldir/$mol.top
echo "agr5: " $mol$i.rst
echo "agr6: " $mol$i.crd

sander -i md$i.in -o $mol$i.out -c $emdir/$mol$emext.rst -p $tldir/$mol.top -r $mol$i.rst -x $mol$i.crd

wait $pid
cp $mol$i.rst $sadir/
cp $tldir/$mol.top $sadir/

finish_time=$(date +%s)

runtime=$(( $(( finish_time - start_time))/60 ))

echo "run time = $runtime minutes."
