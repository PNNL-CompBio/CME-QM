#!/bin/bash
#SBATCH -t 01:00:00
#SBATCH -N 1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=2
#SBATCH -A emsls51160
##SBATCH -N setupfiles
##SBATCH -j oe


moldir=$1
rindex=$2
saindex=$3
start_count="$4"
end_count="$5"

start_time=$(date +%s)
#export AMBERHOME=/home/scicons/cascade/apps/amber/amber14
#export AMBERHOME=/Users/mcna892/Desktop/amber14
cwd=$(pwd)

./batch_setupallfiles.sh $moldir $rindex $saindex $start_count $end_count
#./batch_setupallfiles.sh $moldir $rindex $saindex 56 60


finish_time=$(date +%s)

runtime=$(( $(( finish_time - start_time))/60 ))

echo "run time = $runtime minutes."

