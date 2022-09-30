import sys
import os
import re
import mmap
import glob
import openbabel as obabel

# This program is for collecting data from nwchem output files: Neeraj Kumar's group working with Yarrowia Molecules
# ***** This code is not optimized *****

# Core Functions
#################################################################
#gets the number of atoms      could grab the last xyz file
def getNumberOfAtoms(inchi_key):
    # os.chdir(inchi_key)
    xyz_list = []
    xyz_list += [each for each in os.listdir('./') if each.endswith('.xyz')]

    start_geom = sorted(xyz_list)[0]

    with open(start_geom, 'r') as geom_file:
         lines = geom_file.readlines()
         # print(lines[0].rstrip())
         atomCount = lines[0].rstrip()
    os.chdir('../')
    return atomCount

#################################################################
#gets the Consecutive, 1-based integer identifier of molecule      job output number
def get1BasedIdentifier(fileName):
    result = fileName.split('.')
    return(result[2])

#################################################################
# gets the dipole moment in Debye
def getDipoleMoment(open_file):
    open_file.seek(0,os.SEEK_SET) # goes to beginning of the file
    line = open_file.readline()
    while "Dipole moment" and "Debye" not in line:
        line = open_file.readline()
    result = re.findall("[+-]?\d+\.\d+",line)
    return (result[0])

#################################################################
#gets the energy of the Highest Occupied Molecular Orbital (HOMO) and the Lowest Unoccupied Molecular Orbital (LUMO)
def getHOMO_LUMO(open_file):
    HOMO,LUMO=[],[]
    open_file.seek(0,os.SEEK_SET) # goes to beginning of the file
    lineList = open_file.readlines()
    for line in reversed(lineList):
        # FIXME:
        if "Occ=0" in line:
            LUMO = re.findall("[+-]?\d+\.\d+[D+-]*\d+",line)
            LUMO = [i.replace('D', 'E') for i in LUMO]
#            LUMO = re.findall("[+-]?\d+\.\d+",line) # will rewrite this one each time Occ=0 is found until Occ=2 is found
        # FIXME
        elif "Occ=2" in line or "Occ=1" in line:
            HOMO = re.findall("[+-]?\d+\.\d+[D+-]*\d+",line)
            HOMO = [i.replace('D', 'E') for i in HOMO]
#            HOMO = re.findall("[+-]?\d+\.\d+",line)
            break
    return float(HOMO[1]), float(LUMO[1])

#################################################################
#gets the difference between LUMO and HOMO
def getGap(LUMO,HOMO):
    return LUMO - HOMO

#################################################################
#gets zero point vibrational energy
def getZeroPointVibrationEnergy(correction, open_file):
    open_file.seek(0,os.SEEK_SET) # goes to beginning of the file
    line = open_file.readline()
    while "Total Entropy" not in line:
        line = open_file.readline()
    open_file.readline()
    open_file.readline()
    line = open_file.readline()
    result = re.findall("[+-]?\d+\.\d+",line)
    return (float(result[0]) / (1000*627.509469)) + correction

#################################################################
#gets internal energy at 298 K
def getInternalEnergy(internal,Thermalcorrection):
    return internal + float(Thermalcorrection)

def ThermalCorrectionEnergy(open_file):
    open_file.seek(0,os.SEEK_SET) # goes to beginning of the file
    line = open_file.readline()
    while "Thermal correction to Energy" not in line:
        line = open_file.readline()
    correction = re.findall("[+-]?\d+\.\d+",line)
    return correction[1]
#################################################################
#gets internal energy at 0 K
def getInternalEnergy0K(open_file):
    line=''
    open_file.seek(0,os.SEEK_SET) # goes to end of the file
    lineList = open_file.readlines()
    for line in reversed(lineList):
#        if "Total DFT energy" in line:
        if "sol phase energy" in line:
            break
    result = re.findall("[+-]?\d+\.\d+",line)
    return result[0]

#################################################################
#gets Enthalpy at 298.15 K. Does this by taking Internal Energy and adding it to the thermal correction to Enthalpy
def getEnthalpy(internalEnergy, open_file):
    open_file.seek(0,os.SEEK_SET) # goes to beginning of the file
    line = open_file.readline()
    while "Thermal correction to Enthalpy" not in line:
        line = open_file.readline()
    correction = re.findall("[+-]?\d+\.\d+",line)
    return float(correction[1]) + internalEnergy        # [0]= kcal  [1]= au

#################################################################
# gets free energy at 298.15 K. free energy (G) is Correction + Enthalpy*627.509469 - Temperature*(Total Entropy / (1000))
# this gives results in kcal
def getFreeEnergy(internalEnergy,open_file):
    open_file.seek(0,os.SEEK_SET) # goes to beginning of the file
    line = open_file.readline()
    while "Thermal correction to Enthalpy" not in line:
        line = open_file.readline()
    correction = re.findall("[+-]?\d+\.\d+",line)
    while "Total Entropy" not in line:
        line = open_file.readline()
    totalEntropy = re.findall("[+-]?\d+\.\d+",line)
    return float(correction[0]) + internalEnergy*627.509469 - (298.15*(float(totalEntropy[0]) / (1000)))        # [0]= kcal  [1]= au
#################################################################
#gets the solvation energy
def getSolvationEnergy(open_file):
    open_file.seek(0,os.SEEK_SET) # goes to beginning of the file
    line = open_file.readline()
    while "solvation energy" not in line:
        line = open_file.readline()
    result = re.findall("[+-]?\d+\.\d+",line)
    return float(result[0]) * 627.509469       # 627.509469 is a conversion factor

#################################################################
#gets heat capacity at 298.15 K
def getHeatCapacity(open_file):
    open_file.seek(0,os.SEEK_SET) # goes to beginning of the file
    line = open_file.readline()
    while "heat capacity" not in line:
        line = open_file.readline()
    result = re.findall("[+-]?\d+\.\d+",line)
    return result[0]

#################################################################
#gets the Element type, coordinate (x,y,z)(Angstrom), and Mulliken partial charge (e) of the atom)
def getMullikenCharge(open_file, nAtoms):
    open_file.seek(0,os.SEEK_SET)
    lineList = open_file.readlines()
    atom_coords = []

    xyz_ind =  len(lineList) - 1 - lineList[::-1].index('                         Geometry "geometry" -> "geometry"\n')
    atoms = nAtoms #int(getNumberOfAtoms(inchi_key))
    for i in range(xyz_ind+7, xyz_ind+7+atoms):
        atom_coords.append(lineList[i].split())

    ind = len(lineList) - 1 - lineList[::-1].index('      Total Density - Mulliken Population Analysis\n')
    atoms = nAtoms #int(getNumberOfAtoms(inchi_key))
    for i in range(ind+5, ind+5+atoms):
        atom_coords.append(lineList[i].split()[3])

    output = "%s\t%12s\t%12s\t%12s\t%12s" % (atom_coords[0][1], atom_coords[0][3], atom_coords[0][4], atom_coords[0][5],str(float(atom_coords[0][2]) - float(atom_coords[atoms+0]))+'\n')
    for l in range(1, atoms):
        if l < atoms-1:
           output += "%s\t%12s\t%12s\t%12s\t%8s" % (atom_coords[l][1], atom_coords[l][3], atom_coords[l][4], atom_coords[l][5], str(float(atom_coords[l][2]) - float(atom_coords[atoms+l]))+'\n')
        else:
           output += "%s\t%12s\t%12s\t%12s\t%8s" % (atom_coords[l][1], atom_coords[l][3], atom_coords[l][4], atom_coords[l][5], str(float(atom_coords[l][2]) - float(atom_coords[atoms+l])))
    return output

#################################################################
#gets the frequencies (3na-5 or 3na-6)
def getFrequencies(open_file, nAtoms):
    open_file.seek(0,os.SEEK_SET)
    lineList = open_file.readlines()
    output = ""

    ind = len(lineList) - 1 - lineList[::-1].index(' Normal Eigenvalue ||           Projected Infra Red Intensities\n')
    atoms = nAtoms #int(getNumberOfAtoms(inchi_key))
    for i in range(ind+3, ind+3+3*atoms):
        output += lineList[i].split()[1] + '\t'
    return output
#################################################################
#gets the starting and optimized SMILES
def getSMILES(dft_dir):
    os.chdir(dft_dir)
    xyz_files = []
    xyz_files += [each for each in os.listdir('.') if each.endswith('.xyz')]
    print("In getSMILES")
    print("xyz_files Count", len(xyz_files))
    print(xyz_files)
    converged_geom = sorted(xyz_files)[-2]
    os.system('obabel %s -O converged.smiles' % (converged_geom))
#
    file = open('converged.smiles', 'r')
    smiles_lines = file.readlines()
    converged_smiles = smiles_lines[0].split('\t')[0]
    os.chdir('..')
    return ('%s' %(converged_smiles))

#################################################################
#gets the starting and optimized InChI
def getInChI(dft_dir):
    os.chdir(dft_dir)
    xyz_files = []
    xyz_files += [each for each in os.listdir('./') if each.endswith('.xyz')]
    print("In getInChI")
    print("xyz_files Count", len(xyz_files))
    print(xyz_files)
    converged_geom = sorted(xyz_files)[-2]
    os.system('obabel %s -O converged.inchi' % (converged_geom))
#
    file = open('converged.inchi', 'r')
    inchi_lines = file.readlines()
    converged_inchi = inchi_lines[0].rstrip()
    os.chdir('..')
    return (('%s' %(converged_inchi)))

#================================================================#
#Support Functionality
def getZeroPointCorrection(open_file):
    open_file.seek(0 ,os.SEEK_SET) # goes to beginning of the file
    line = open_file.readline()
    while "Zero-Point" not in line:
        line = open_file.readline()
    result = re.findall("[+-]?\d+\.\d+",line)
    return result[1]        # [0]= kcal  [1]= au

def getRotationalConstants(open_file):
    open_file.seek(0,os.SEEK_SET) # goes to beginning of the file
    line = open_file.readline()
    while "Rotational Constants" not in line:
        line = open_file.readline()
    line = open_file.readline()
    A_line = open_file.readline()
    A = re.findall('\d.\d*', A_line)[0]
    B_line = open_file.readline()
    B = re.findall('\d.\d*', B_line)[0]
    C_line = open_file.readline()
    C = re.findall('\d.\d*', C_line)[0]
    return (float(A), float(B), float(C))

def calculate(dft_dir, mol_name, out_file):
    '''
    call all functions to extract properties to a file
    :param dft_dir:
    :param mol_name:
    :return:
    '''
    InChI_key= mol_name
    # matches = []
    os.chdir(dft_dir)
    index = mol_name #pattern.split('.')[1]

    print("dft_dir", dft_dir)
    print("mol_name", mol_name)
    print("outfile", out_file)

    with open(out_file,'r') as f:
        zero = float(getZeroPointCorrection(f))
        nAtoms = int(getNumberOfAtoms(mol_name))
        A,B,C=getRotationalConstants(f)
        mu = getDipoleMoment(f)
        HOMO, LUMO = getHOMO_LUMO(f)
        gap = getGap(LUMO,HOMO)
        ZPVE = getZeroPointVibrationEnergy(zero,f)
        E0K = getInternalEnergy0K(f)
        internalEnergy = float(E0K)
        ThermalCorr = ThermalCorrectionEnergy(f)
        E = getInternalEnergy(internalEnergy,ThermalCorr)
        H = getEnthalpy(internalEnergy,f)
        G = getFreeEnergy(internalEnergy,f)/627.509469
        tEsolvation = getSolvationEnergy(f)
        cV = getHeatCapacity(f)
        SMILES = getSMILES(dft_dir)
        InChI = getInChI(dft_dir)

        outputData = ("%s\n%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (nAtoms, mol_name, index, A, B, C, mu, HOMO, LUMO, gap, ZPVE, E0K, E, H, G, cV))
        outputData += "\n" + getMullikenCharge(f, nAtoms) + "\n" + getFrequencies(f, nAtoms) + '\n'
        outputData += SMILES + "\n"
        outputData += InChI
        calc_prop_v2_outfile= os.path.join(dft_dir, "%s_calc_prop_v2.dat" % (mol_name) )
        with open(calc_prop_v2_outfile, 'w') as output:
            output.write(outputData)

        print("Written output to :",calc_prop_v2_outfile)
        print("*"*20)
        os.chdir('../')

if __name__ == '__main__':
    print("In extract_properties_v2.py")
    out_file=""
    for arg in sys.argv:
        if arg.endswith((".out")):
            out_file = arg
    dft_dir = os.path.join(os.getcwd(), '/'.join(out_file.split('/')[:-2]), 'dft')
    mol_name = os.path.splitext(out_file)[0].split('/')[-1]
    calculate(dft_dir, mol_name, os.path.join(dft_dir, out_file.split('/')[-1] ))
