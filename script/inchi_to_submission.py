"""
Script to read INCHIKEY and INCHI-STRING to generate .xyz, .mol, .nw and .sbatch
files and to submit jobs

Needs test.csv file with data

--> excute these two first in shell to activate rdkit

conda create -c rdkit -n my-rdkit-env rdkit
conda activate my-rdkit-env

"""

from __future__ import print_function

import os
from csv import DictReader

import rdkit
from pybel import *
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Draw

# Generate dft folder from inchi string

os.system('rm -rf Z* A* B* C* K* D* F* P* W* X*')


def inchi_to_dft(InChI_key, InChIes):
    dd = dict(zip(InChI_key, InChIes))
    for key, value in dd.items():
        os.mkdir(key)
        os.chdir(key)
        m4 = Chem.inchi.MolFromInchi(value)
        AllChem.Compute2DCoords(m4)
        m5 = Chem.AddHs(m4)
        if m5.GetNumAtoms() > 110:
            AllChem.EmbedMolecule(m5, useRandomCoords=True)
        else:
            AllChem.EmbedMolecule(m5)

        AllChem.MMFFOptimizeMolecule(m5)
        ii = Chem.MolToMolBlock(m5).splitlines()

        os.mkdir('dft')  # create dft files
        os.chdir('dft')

        f = open(str(key) + ".xyz", 'w')
        f.write(str(m5.GetNumAtoms()))
        f.write('\n\n')
        for i in range(4, 4 + m5.GetNumAtoms()):
            jj = ' '.join((ii[i].split()))
            kk = jj.split()
            f.write("{}\t{:>8}  {:>8}  {:>8}\n".format(kk[3], kk[0], kk[1], kk[2]))
        f.close()

        #
        #   write .nw file
        #

        nw.write("title " + '"' + key + '"' + '\n')
        nw.write('start ' + key + '\n\n')
        nw.write('memory global 1600 mb heap 100 mb stack 600 mb' + '\n\n')
        nw.write('permanent_dir ' + os.getcwd() + '\n')
        nw.write('#scratch_dir /scratch' + '\n\n')
        nw.write('echo' + '\n')
        nw.write('print low' + '\n\n')
        nw.write('charge ' + str(rdkit.Chem.rdmolops.GetFormalCharge(m5)) + '\n')
        nw.write('geometry noautoz noautosym' + '\n')
        nw.write('load ' + os.getcwd() + '/' + key + '.xyz' + '\n')
        nw.write('end' + '\n')
        nw.write('basis' + '\n')
        nw.write('* library 6-31G*' + '\n')
        nw.write('end' + '\n\n')
        nw.write('driver' + '\n')
        nw.write(' maxiter 500' + '\n')
        nw.write('xyz FXEUKVKGTKDDIQ-UWVGGRQHSA-M_geom' + '\n')
        nw.write('end' + '\n\n')
        nw.write('set lindep:n_dep 0' + '\n\n')
        nw.write('dft' + '\n')
        nw.write('  maxiter 500' + '\n')
        nw.write('  xc b3lyp' + '\n')
        nw.write('  disp vdw 3' + '\n')
        nw.write('  mulliken' + '\n')
        nw.write('  print "mulliken ao"' + '\n')
        nw.write('  print "final vectors analysis"' + '\n')
        nw.write('end' + '\n\n')
        nw.write('task dft optimize ignore' + '\n')
        nw.write('task dft freq' + '\n\n')
        nw.write('cosmo' + '\n')
        nw.write(' dielec 80.4' + '\n')
        nw.write(' lineq  0' + '\n')
        nw.write('end' + '\n\n')
        nw.write('task dft energy' + '\n\n')
        nw.write('property' + '\n')
        nw.write(' dipole' + '\n')
        nw.write('end' + '\n\n')
        nw.write('task dft property' + '\n')
        nw.close()

        #
        #   write .sbatch file
        #
        #        batch=open(str(key)+'.sbatch', 'w')
        #        batch.write('#!/bin/csh -f'+'\n')
        #        batch.write('#SBATCH -N 1'+'\n')
        #        batch.write('#SBATCH --ntasks-per-node 4'+'\n')
        #        batch.write('#SBATCH -t 1:00:00'+'\n')
        #        batch.write('#SBATCH -A emslc50597'+'\n')
        #        batch.write('#SBATCH -o ./'+key+'/'+key+'.out.%j'+'\n')
        #        batch.write('#SBATCH -e ./'+key+'/'+key+'.err.%j'+'\n')
        #        batch.write('#SBATCH -J '+key+'\n')
        #        batch.write('#SBATCH --export ALL'+'\n')
        #        batch.write('##SBATCH --mail-type=FAIL,END'+'\n')
        #        batch.write('##SBATCH --mail-user rajendra.joshi@emsl.pnl.gov'+'\n\n')
        #        batch.write('############################################################################'+'\n')
        #        batch.write('# Print out some information for refund purposes'+'\n')
        #        batch.write('############################################################################'+'\n\n')
        #        batch.write('echo "refund: UserID = thom510"'+'\n')
        #        batch.write('echo "refund: SLURM Job ID = ${SLURM_JOBID}"'+'\n')
        #        batch.write('echo "refund: Number of nodes          = 1"'+'\n')
        #        batch.write('echo "refund: Number of cores per node = 1"'+'\n')
        #        batch.write('echo "refund: Number of cores          = 1"'+'\n')
        #        batch.write('echo "refund: Amount of time requested = 0:30"'+'\n')
        #        batch.write('echo "refund: Directory = ${PWD}"'+'\n')
        #        batch.write('echo " "'+'\n')
        #        batch.write('echo Processor list'+'\n')
        #        batch.write('echo " "'+'\n')
        #        batch.write('echo "${SLURM_JOB_NODELIST}"'+'\n')
        #        batch.write('echo " "'+'\n\n')
        #        batch.write('# Actually run the job'+'\n')
        #        batch.write('source /etc/profile.d/modules.csh'+'\n')
        #        batch.write('module purge'+'\n')
        #        batch.write('#module load nwchem/6.3'+'\n')
        #        batch.write('# module load intel/14.0.3'+'\n')
        #        batch.write('# module load micsetup'+'\n')
        #        batch.write('# module load impi'+'\n')
        #        batch.write('# module load intel/ips_17_u4'+'\n')
        #        batch.write('# module load impi/5.1.2.150'+'\n')
        #        batch.write('module load nwchem/6.8.1_rhel7'+'\n\n')
        #        batch.write('cd /scratch'+'\n\n')
        #        batch.write('setenv ARMCI_DEFAULT_SHMMAX 131072'+'\n')
        #        batch.write('#this disables xeon phi offload'+'\n')
        #        batch.write('setenv NWC_RANKS_PER_DEVICE 0'+'\n')
        #        batch.write('setenv OMP_NUM_THREADS 1'+'\n')
        #        batch.write('setenv MKL_NUM_THREADS 1'+'\n')
        #        batch.write('setenv NWC_RANKS_PER_DEVICE 0'+'\n')
        #        batch.write('setenv ARMCI_OPENIB_DEVICE mlx4_0'+'\n')
        #        batch.write('setenv OFFLOAD_INIT on_offload'+'\n\n\n')
        #        batch.write('setenv MPIRETURN 999'+'\n')
        #        batch.write('srun --mpi=pmi2 -n $SLURM_NPROCS -K1    /dtemp/scicons/bin/nwchem6.8.1_rhel7 '+ os.getcwd()+'/'+key+'.nw'+'\n')
        #        batch.write('setenv MPIRETURN $?'+'\n\n')
        #        batch.write('############################################################################'+'\n')
        #        batch.write('# End of the job script'+'\n')
        #        batch.write('############################################################################'+'\n\n')
        #        batch.write('exit $MPIRETURN'+'\n')
        #        batch.close()
        #    #
        #   submit .sbatch job reading .nw and .xyz files
        #
        #        key_nw = str(key)+".sbatch"
        #    os.system("sbatch %s" %str(key)+".sbatch")    # uncomment this if you want to submit jobs
        #       os.chdir('../')
        #
        #    to generate files for molecular dynamics simulations
        #
        os.mkdir('md')
        os.chdir('md')

        file = open(str(key) + '.mol', 'w')
        m4 = Chem.inchi.MolFromInchi(value)
        AllChem.Compute2DCoords(m4)
        m5 = Chem.AddHs(m4)
        #
        if m5.GetNumAtoms() > 110:
            AllChem.EmbedMolecule(m5, useRandomCoords=True)
        else:
            AllChem.EmbedMolecule(m5)

        AllChem.MMFFOptimizeMolecule(m5)
        file.write(Chem.MolToMolBlock(m5))
        file.close()

        mol22 = readfile('mol', str(key) + '.mol').__next__()
        output = Outputfile('mol2', str(key) + '.mol2')
        output.write(mol22)

        os.chdir('../../')

        os.mkdir('geometry')
        os.chdir('geometry')

        png_file = str(key)
        Draw.MolToFile(m5, str(key) + '.png')

        file = open(str(key) + '.inchi', 'w')
        file.write(str(value))

        outfile = str(key) + '_nwchem.out'
        os.system("mpirun -np 2 --allow-run-as-root nwchem *.nw > {}".format(outfile))

        os.system('cp ../md/* .')
        os.system("cp ../dft/*.xyz .")
        os.chdir('../../')
        os.chdir('../../')


# Reads InChI and InChI-key from .csv file

if __name__ == '__main__':
    inchilist = sys.argv[1]
    #
    with open(inchilist) as f:
        InChI_key = [row["InChI-Key"].split('InChIKey=')[1] for row in DictReader(f)]
        key_file = open('InChI_key', 'w')
        key_file.write(InChI_key)
        key_file.close()
    with open(inchilist) as f:
        InChIes = [row["InChI"] for row in DictReader(f)]
    #
    inchi_to_dft(InChI_key, InChIes)
