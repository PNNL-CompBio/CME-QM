#!/bin/csh -f
#SBATCH -N 1
#SBATCH --ntasks-per-node 1
#SBATCH -t 00:30:00
#SBATCH -A emsls51160
#SBATCH -o ./INCHIKEY/dft/INCHIKEY.out
#SBATCH -e ./INCHIKEY/dft/INCHIKEY.err.%j
#SBATCH -J INCHIKEY
#SBATCH --export ALL

############################################################################
# Print out some information for refund purposes
############################################################################

echo "refund: UserID = thom510"
echo "refund: SLURM Job ID = ${SLURM_JOBID}"
echo "refund: Number of nodes          = 1"
echo "refund: Number of cores per node = 1"
echo "refund: Number of cores          = 1"
echo "refund: Amount of time requested = 0:30"
echo "refund: Directory = ${PWD}"
echo " "
echo Processor list
echo " "
echo "${SLURM_JOB_NODELIST}"
echo " "

############################################################################
# Actually run the job
############################################################################

source /etc/profile.d/modules.csh
module purge
module load nwchem/6.8.1_rhel7

cd /scratch

setenv ARMCI_DEFAULT_SHMMAX 131072
#setenv NWCHEM_BASIS_LIBRARY "/home/scicons/cascade/apps/nwchem-6.8.1_rhel7/src/basis/libraries/"
#setenv NWCHEM_NWPW_LIBRARY "/home/scicons/cascade/apps/nwchem-6.8.1_rhel7/src/nwpw/libraryps/"
#this disables xeon phi offload
setenv NWC_RANKS_PER_DEVICE 0
#this disables threaded in MKL since it is better to keep it to advanced users
setenv OMP_NUM_THREADS 1
setenv MKL_NUM_THREADS 1
setenv NWC_RANKS_PER_DEVICE 0
setenv ARMCI_OPENIB_DEVICE mlx4_0
setenv OFFLOAD_INIT on_offload


setenv MPIRETURN 999
srun --mpi=pmi2 -n $SLURM_NPROCS -K1 nwchem /entire/results/AUJKJAMUKRIRHC-UHFFFAOYSA-N/dft/AUJKJAMUKRIRHC-UHFFFAOYSA-N.nw

setenv MPIRETURN $?

############################################################################
# End of the job script
############################################################################

exit $MPIRETURN

