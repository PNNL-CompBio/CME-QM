#!/bin/bash
#SBATCH -t 1:00:00
#SBATCH -N 1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH -A emsls51160
##SBATCH -N md0
##SBATCH -j oe

echo "==========In batch_md0.sbatch :"
cwd=$(pwd)
echo "Current dir "$cwd

mol2dir="$1"
rindex="$2"
saindex="$3"
start_count="$4"
end_count="$5"

echo "mol2dir: " $mol2dir
echo "mddir: " $mddir
echo "rindex: " $rindex "saindex: " $saindex
echo "start_count: " $start_count "end_count: " $end_count


#counter=0
for f in $mol2dir/*.mol2
do
start_time=$(date +%s) # added on 5/18/2018

#((counter += 1))
#if [ "$counter" -ge "$start_count" ] && [ "$counter" -le "$end_count" ];
#then # starting calculations

# get molecule name by stripping off .mol2 from the file name (f).
mol=${f%.mol2}
echo "molecule name:" $mol

mol2f=${mol##*/}
echo "mol2f" $mol2f
pid=${!}

echo
echo "Running amber_sander_em_md0.sh :"
echo "mol2dir: " $mol2dir
echo "mol2f: " $mol2f
echo "rindex: " $rindex
echo "saindex: " $saindex
src/md_simulations/amber_sander_em_md0.sh $mol2dir $mol2f $rindex $saindex
wait

cd $cwd
finish_time=$(date +%s)

runtime=$(( $(( finish_time - start_time))/60 ))

echo "run time = $runtime minutes."
done
