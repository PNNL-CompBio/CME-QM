from __future__ import print_function

import sys
import os

def md2(input):
    '''
    This function Invokes
        batch_md0.sbatch
    :param InChI_key:
    :return:
    '''
    md_dir = os.path.join('/'.join(input.split('/')[:-2]), 'md')
    mol2_dir = '/'.join(input.split('/')[:-1])
   # sbatch to sh
    os.system("sh %s %s %d %d %d %d" % ("src/md_simulations/batch_md0.sbatch", mol2_dir, 1, 1, 1, 1))

if __name__ == '__main__':
    # InChI_key = sys.argv[1]
    # md2(InChI_key)
    mol2_file=""
    for arg in sys.argv:
        if arg.endswith((".mol2")):
            mol2_file = arg
    md2(mol2_file)
