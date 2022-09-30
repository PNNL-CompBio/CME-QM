import os
import sys


def create_nw_file(dft_dir, config_nwfile, charge_file, mol_name, xyz_file):
    '''
    Does variable subsitution in config/template_dft.nw file
    :param dft_dir:
    :param config_nwfile:
    :param charge_file:
    :param mol_name:
    :param xyz_file:
    :return:
    '''
    write_to_nwfile = os.path.join(dft_dir, mol_name + '.nw')

    os.chdir(dft_dir)
    path = os.getcwd()
    with open(config_nwfile, 'r') as rfile:
        lines = rfile.read()
        lines = lines.replace('INCHIKEY', mol_name)
        lines = lines.replace('XYZ_FILE_PATH', xyz_file)
        lines = lines.replace('DFT_DIR_PATH', dft_dir)


        with open(charge_file, 'r') as chgfile:
            for i in chgfile.readlines():
                CHARGE = i.split('\t')[1]
        lines = lines.replace('CHARGE', CHARGE)

    with open(write_to_nwfile, 'w') as wfile:
        wfile.write(lines)

    os.chdir('../../')


def create_sbatch_file(dft_dir, mol_name, config_sbatchFile):
    '''
    Does variable subsitution in config/template_dft.sbatch file
    :param dft_dir:
    :param mol_name:
    :param config_sbatchFile:
    :return:
    '''
    write_to_sbatchFile = os.path.join(dft_dir, mol_name+'.sbatch')
    read_nwfile = os.path.join(dft_dir, mol_name + '.nw')

    os.chdir(dft_dir)
    path = os.getcwd()
    with open(config_sbatchFile, 'r') as rfile:
        lines = rfile.read()
        lines = lines.replace('PATH_TO_NW_FILE', read_nwfile)

    with open(write_to_sbatchFile, 'w') as wfile:
        wfile.write(lines)
    os.chdir('../../')

if __name__ == '__main__':

    md_info_file,xyz_file,charge_file="","",""
    for arg in sys.argv:
        if arg.endswith(("mdinfo")):
            md_info_file = arg
        if arg.endswith((".charge")):
            charge_file = arg
        if arg.endswith((".xyz")):
            xyz_file = arg

    dft_dir = os.path.join(os.getcwd(), '/'.join(md_info_file.split('/')[:-5]), 'dft')
    config_nwfile =os.path.join(os.getcwd(),"config/template_dft.nw" )
    config_sbatchFile=os.path.join(os.getcwd(),"config/template_dft.sbatch" )
    mol_name = os.path.splitext(charge_file)[0].split('/')[-1]
    charge_file=os.path.join(os.getcwd(), charge_file)
    xyz_file = os.path.join(os.getcwd(), xyz_file)
    print(dft_dir,"\n",config_nwfile,"\n",config_sbatchFile,"\n", mol_name,"\n",charge_file)

    create_nw_file(dft_dir, config_nwfile, charge_file, mol_name, xyz_file)
    create_sbatch_file(dft_dir,mol_name,config_sbatchFile)
