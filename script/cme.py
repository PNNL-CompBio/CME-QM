from script.cme import *


def cme():
    """The main function call for runnning the CME application """
    parser = argparse.ArgumentParser(prog='CME', description='Computational Modeling Engine')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0', help='print version and exit')
    parser.add_argument('--prepare', action='store_true', default=False, dest='prepare',
                        help='set prepare structure switch to true')
    parser.add_argument('--inchi', action='store_true', default=False, dest='inchi',
                        help='set inchi file creation switch to true')
    parser.add_argument('--configfile', default='config.yaml', help='snakemake configuration file')
    parser.add_argument('--dft', action='store_true', default=False, dest='dft', help='run DFT calculation')
    parser.add_argument('--md', action='store_true', default=False, dest='md', help='run MD simulation')

    args = parser.parse_args()

    if (args.inchi == True):
        print('Creating .inchi files from inchi strings in .csv file')
        snakemake(resource_filename('cme', 'rules/MD-pipeline.snakemake'), configfile=args.configfile)
    if (args.prepare == True):
        print('Preparing initial structure files for DFT and MD runs')
        snakemake(resource_filename('cme', 'rules/2.snakemake'), configfile=args.configfile)
    if (args.dft == True):
        print('Starting DFT runs')
        snakemake(resource_filename('cme', 'rules/rj-dft.snakemake'), configfile=args.configfile)
    if (args.md == True):
        print('Starting MD runs')
        snakemake(resource_filename('cme', 'rules/rj-md.snakemake'), configfile=args.configfile)
    #    if (args.md2 == True):
    #        print('Starting MD-2 runs')
    #        snakemake(resource_filename('cme', 'rules/rj-md2.snakemake'),configfile=args.configfile)
    print(args)


if __name__ == '__main__':
    cme()
