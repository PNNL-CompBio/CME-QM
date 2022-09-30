from __future__ import print_function

import os
import sys


def md(mol2_file,charge_file):
    '''
    This function Invokes
        1. calculate_total_charge.sh
            input: .mol2
            output: total_charges.txt
        2. batch_setupallfiles.sh
            input:
            output:
    :param InChI_key:
    :return:
    '''
    md_dir = os.path.join('/'.join(mol2_file.split('/')[:-2]), 'md')
    mol2_dir= '/'.join(mol2_file.split('/')[:-1])
    os.system("src/md_simulations/calculate_total_charge.sh %s %s" % (mol2_dir, md_dir))
    os.system("src/md_simulations/batch_setupallfiles.sh %s %d %d %d %d %s" % (mol2_dir, 1, 1, 1, 1, md_dir))

if __name__ == '__main__':

    mol2_file,charge_file="",""
    for arg in sys.argv:
        if arg.endswith((".mol2")):
            mol2_file = arg
        if arg.endswith((".charge")):
            charge_file = arg

    md(mol2_file,charge_file)
