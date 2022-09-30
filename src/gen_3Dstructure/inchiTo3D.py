from __future__ import print_function

import rdkit
from pybel import *

from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Draw
import sys

def inchiTo3D(args):
    """Reads the InChI string from the .inchi file, which is in a {inchi-key} molecule folder.
       Converts the InChI string to .mol, .mol2, .xyz, and .png files
    """
    with open(args['inchifile']) as f:
        inchi = f.readline()  # read the InChI string from the .inchi file
    # TODO: catch the error! try:
    m4 = Chem.inchi.MolFromInchi(inchi)
    AllChem.Compute2DCoords(m4)
    m5 = Chem.AddHs(m4)
    if m5.GetNumAtoms() > 110:
        AllChem.EmbedMolecule(m5, useRandomCoords=True)
    else:
        AllChem.EmbedMolecule(m5)

    AllChem.MMFFOptimizeMolecule(m5)
    ii = Chem.MolToMolBlock(m5).splitlines()

    # create .xyz file
    try:
        with open(args['xyzfile'], 'w') as f:

            f.write(str(m5.GetNumAtoms()))
            f.write('\n\n')
            for i in range(4, 4 + m5.GetNumAtoms()):
                jj = ' '.join((ii[i].split()))
                kk = jj.split()
                f.write("{}\t{:>8}  {:>8}  {:>8}\n".format(kk[3], kk[0], kk[1], kk[2]))
    except Exception as e:
        print("Written to .xyz file")

    # create .charge file
    try:
        with open(args['chargefile'], 'w') as ff:
            ff.write(str(args['chargefile']).split('/')[0] + '\t')
            ff.write(str(rdkit.Chem.rdmolops.GetFormalCharge(m5)) + '\t')
            ff.write(str(m5.GetNumAtoms()))
    except Exception as e:
        print("Written to .charge file")

    # create .mol file
    try:
        with open(args['molfile'], 'w') as f:
            m4 = Chem.inchi.MolFromInchi(inchi)
            AllChem.Compute2DCoords(m4)
            m5 = Chem.AddHs(m4)
            #
            if m5.GetNumAtoms() > 110:
                AllChem.EmbedMolecule(m5, useRandomCoords=True)
            else:
                AllChem.EmbedMolecule(m5)

            AllChem.MMFFOptimizeMolecule(m5)
            f.write(Chem.MolToMolBlock(m5))
    except Exception as e:
        print("Written to .mol file")

    # create .png file
    try:
        Draw.MolToFile(m5, args['pngfile'])
    except Exception as e:
        print("Written to .png file")
    # create .mol2 file
    try:
        mol22 = readfile('mol', args['molfile']).__next__()
        output = Outputfile('mol2' , args['mol2file'],overwrite=True)
        output.write(mol22)
    except Exception as e:
        print("Written to .mol2 file")

if __name__ == '__main__':
    args = {}
    print("inchiTo3D.py rule is working!")
    for arg in sys.argv:
        if arg.endswith((".inchi")):
            args['inchifile'] = arg
        if arg.endswith((".xyz")):
            args['xyzfile'] = arg
        if arg.endswith((".mol")):
            args['molfile'] = arg
        if arg.endswith((".mol2")):
            args['mol2file'] = arg
        if arg.endswith((".png")):
            args['pngfile'] = arg
        if arg.endswith((".charge")):
            args['chargefile'] = arg

    print(args)
    inchiTo3D(args)