from __future__ import print_function

import os
import sys


def md(InChI_key):
    '''
    This function Invokes
        calculate_total_charge.sh
        batch_setupallfiles.sbatch
    :param InChI_key:
    :return:
    '''
    md_dir = InChI_key + '/' + 'md'
    print(md_dir)
    os.system("./calculate_total_charge.sh %s %s" % (md_dir, md_dir))
    os.system("sbatch %s %s %d %d %d %d" % ("batch_setupallfiles.sbatch", md_dir, 1, 1, 1, 1))


if __name__ == '__main__':
    InChI_key = sys.argv[1]
    md(InChI_key)
