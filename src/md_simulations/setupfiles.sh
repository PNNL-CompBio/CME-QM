#!/bin/bash
# setupfiles.sh
# Author:  Dr. Dennis Thomas (PNNL)
# 
# Usage:
#	./setupfiles.sh {mol} {rindex} {saindex}
# Input arguments
#	mol:  molecule directory name (This will be the name of the mol2 file 
#		used in the MD simulations.)
#	rindex: integer number to create "RUN{rindex}" directory 
#		(e.g., if rindex = 1, then directory "RUN1" will be
#		created.)
#	saindex:  integer number to create "ANNEAL{saindex}" directory 
#		(e.g., if saindex = 1, then directory "ANNEAL1" will 
#		be created."
#
# Directories created in RUN{rindex} directory:  ANTECHAMBER, TLEAP, EM, MD0,
# 		ANNEAL{saindex}
# Input parameter files created for AMBER (sander) runs:
#	em.in  in directory "EM"	
#	md0.in in directory "MD0"
#	anneal.in in directory "ANNEAL{saindex}"
echo -e "\n==========In setupfiles.sh!"
start_time=$(date +%s)
mol=$1
rindex=$2
saindex=$3

mol2f=${mol##*/}
echo "mol2f" $mol2f
cwd=$(pwd)
moldir=$cwd/${mol} # molecular directory
rundir=$moldir/RUN$rindex  # run directory
acdir=$rundir/ANTECHAMBER # antechamber
tldir=$rundir/TLEAP  # tleap
emdir=$rundir/EM	# energy minimization
md0dir=$rundir/MD0	# 1st MD run at target temperature (e.g., 300 K)

sadir=$rundir/ANNEAL$saindex

# create directories

mkdir $moldir
mkdir $rundir
mkdir $acdir
mkdir $tldir
mkdir $emdir
mkdir $md0dir
mkdir $sadir

echo "creating following directories at: "$cwd
echo "moldir: "$moldir
echo "rundir:"$rundir
echo "acdir: "$acdir
echo "tldir: "$tldir
echo "emdir: "$emdir
echo "md0dir: "$md0dir
echo "sadir: "$sadir

#cp ${mol}.crg $moldir/
# create leap.in file
cd ${tldir}

cat > leap.in <<EOF
source $LEAPRC_GAFF
source $LEAPRC_FF14SB
loadAmberParams ../ANTECHAMBER/${mol2f}_md.frcmod
loadAmberParams frcmod.ionsjc_spce
TP = loadMol2 ../ANTECHAMBER/mol_tleapinput.mol2
saveAmberParm TP prmtop inpcrd
quit
EOF
# copy leap.in file to TLEAP directory

cp leap.in $tldir/


# create anneal.in file for simulated annealing runs

cd $sadir

cat > anneal.in <<EOF

1100ps $mol simulated annealing
 &cntrl
  imin = 0, irest = 1, ntx=5,
  ntc=2, ntf=2,
  ntpr=100, ntwx=100, ntwr=1600000
  ntb = 0, cut = 999.0, rgbmax=999.0,
  igb = 0,
  nstlim = 1600000, nscm= 100,
  dt = 0.001,
  ntt = 3, gamma_ln=1.0,
  temp0=300,
  nmropt = 1, ig=-1,
 /
 &wt type='TEMP0', istep1=0,istep2=300000,
   value1=300.0, value2=600.0
 /
 &wt type='TEMP0', istep1=300001,istep2=800000,
   value1=600.0, value2=600.0
 /
 &wt type='TEMP0', istep1=800001,istep2=1100000,
   value1=600.0, value2=300.0
 /
 &wt type='TEMP0', istep1=1100001,istep2=1600000,
   value1=300.0, value2=300.0
 /
# &wt type='TEMP0', istep1=1600001,istep2=250000,
#   value1=500.0, value2=300.0
# /
# &wt type='TEMP0', istep1=250001,istep2=300000,
#   value1=300.0, value2=300.0
# /
 &wt type='END'
 /

EOF

cd ..

# create em.in file for energy minimization

cd $emdir
cat > em.in <<EOF

$mol: energy minimization prior to MD
 &cntrl
  imin = 1,
  maxcyc = 500,
  ncyc = 250,
  nscm = 1,
  ntb = 0,
  igb = 0,
  cut = 999,
  rgbmax = 999
 /

EOF

# create md0.in file for 1st MD run at target temperature
cd $md0dir
cat > md0.in <<EOF

$mol: 1st MD run (md0) in-vacuo, no cut off
 &cntrl
  imin = 0,
  ntb = 0,
  ntf=2,
  ntc=2,
  ntx = 1,
  igb = 0,
  ntpr = 100,
  ntwx = 100,
  ntt = 3,
  nscm = 1,
  gamma_ln = 1.0,
  tempi = 0.0,
  temp0 = 300.0,
  nstlim = 100000,
  dt = 0.0005,
  cut = 999,ig=-1
 /

EOF


finish_time=$(date +%s)

runtime=$(( $(( finish_time - start_time))/60 ))

echo "run time = $runtime minutes."
