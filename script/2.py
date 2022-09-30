import glob
import os
import re


# This program is for collecting data from nwchem output files: Neeraj Kumar's group working with Yarrowia Molecules
# ***** This code is not optimized *****

# Core Functions
#################################################################
# gets the number of atoms      could grab the last xyz file
def getNumberOfAtoms(open_file):
    # gets the line with "Charge" as this only occurs twice, and the first time is above the list of atoms
    open_file.seek(0, os.SEEK_SET)  # goes to beginning of the file
    line = open_file.readline()
    while "Charge" not in line:
        line = open_file.readline()
    open_file.readline()  # moves to the horizontal --- ------
    line = open_file.readline()  # moves to the first atom

    # counts the number of atoms
    atomCount = 0;
    while not line.isspace():
        line = open_file.readline()  # moves to the next atom
        atomCount += 1
    return atomCount


#################################################################
# gets the Consecutive, 1-based integer identifier of molecule      job output number
def get1BasedIdentifier(fileName):
    result = fileName.split('.')
    return (result[2])


#################################################################
# gets the dipole moment in Debye
def getDipoleMoment(open_file):
    open_file.seek(0, os.SEEK_SET)  # goes to beginning of the file
    line = open_file.readline()
    while "Dipole moment" and "Debye" not in line:
        line = open_file.readline()
    result = re.findall("[+-]?\d+\.\d+", line)
    return (result[0])


#################################################################
# gets the energy of the Highest Occupied Molecular Orbital (HOMO) and the Lowest Unoccupied Molecular Orbital (LUMO)
def getHOMO_LUMO(open_file):
    open_file.seek(0, os.SEEK_SET)  # goes to beginning of the file
    lineList = open_file.readlines()
    for line in reversed(lineList):
        if "Occ=0" in line:
            LUMO = re.findall("[+-]?\d+\.\d+[D+-]*\d+", line)
            LUMO = [i.replace('D', 'E') for i in LUMO]
        #            LUMO = re.findall("[+-]?\d+\.\d+",line) # will rewrite this one each time Occ=0 is found until Occ=2 is found
        elif "Occ=2" in line:
            HOMO = re.findall("[+-]?\d+\.\d+[D+-]*\d+", line)
            HOMO = [i.replace('D', 'E') for i in HOMO]
            #            HOMO = re.findall("[+-]?\d+\.\d+",line)
            break
    return (float(HOMO[1]), float(LUMO[1]))


#################################################################
# gets the difference between LUMO and HOMO
def getGap(LUMO, HOMO):
    return LUMO - HOMO


#################################################################
# gets zero point vibrational energy
def getZeroPointVibrationEnergy(correction, open_file):
    open_file.seek(0, os.SEEK_SET)  # goes to beginning of the file
    line = open_file.readline()
    while "Total Entropy" not in line:
        line = open_file.readline()
    open_file.readline()
    open_file.readline()
    line = open_file.readline()
    result = re.findall("[+-]?\d+\.\d+", line)
    return (float(result[0]) / (1000 * 627.509469)) + correction


#################################################################
# gets internal energy at 298 K
def getInternalEnergy(internal, Thermalcorrection):
    return internal + float(Thermalcorrection)


def ThermalCorrectionEnergy(open_file):
    open_file.seek(0, os.SEEK_SET)  # goes to beginning of the file
    line = open_file.readline()
    while "Thermal correction to Energy" not in line:
        line = open_file.readline()
    correction = re.findall("[+-]?\d+\.\d+", line)
    return correction[1]


#################################################################
# gets internal energy at 0 K
def getInternalEnergy0K(open_file):
    open_file.seek(0, os.SEEK_SET)  # goes to end of the file
    lineList = open_file.readlines()
    for line in reversed(lineList):
        #        if "Total DFT energy" in line:
        if "sol phase energy" in line:
            break
    result = re.findall("[+-]?\d+\.\d+", line)
    return result[0]


#################################################################
# gets Enthalpy at 298.15 K. Does this by taking Internal Energy and adding it to the thermal correction to Enthalpy
def getEnthalpy(internalEnergy, open_file):
    open_file.seek(0, os.SEEK_SET)  # goes to beginning of the file
    line = open_file.readline()
    while "Thermal correction to Enthalpy" not in line:
        line = open_file.readline()
    correction = re.findall("[+-]?\d+\.\d+", line)
    return float(correction[1]) + internalEnergy  # [0]= kcal  [1]= au


#################################################################
# gets free energy at 298.15 K. free energy (G) is Correction + Enthalpy*627.509469 - Temperature*(Total Entropy / (1000))
# this gives results in kcal
def getFreeEnergy(internalEnergy, open_file):
    open_file.seek(0, os.SEEK_SET)  # goes to beginning of the file
    line = open_file.readline()
    while "Thermal correction to Enthalpy" not in line:
        line = open_file.readline()
    correction = re.findall("[+-]?\d+\.\d+", line)
    while "Total Entropy" not in line:
        line = open_file.readline()
    totalEntropy = re.findall("[+-]?\d+\.\d+", line)
    return float(correction[0]) + internalEnergy * 627.509469 - (
                298.15 * (float(totalEntropy[0]) / (1000)))  # [0]= kcal  [1]= au


#################################################################
# gets the solvation energy
def getSolvationEnergy(open_file):
    open_file.seek(0, os.SEEK_SET)  # goes to beginning of the file
    line = open_file.readline()
    while "solvation energy" not in line:
        line = open_file.readline()
    result = re.findall("[+-]?\d+\.\d+", line)
    return float(result[0]) * 627.509469  # 627.509469 is a conversion factor


#################################################################
# gets heat capacity at 298.15 K
def getHeatCapacity(open_file):
    open_file.seek(0, os.SEEK_SET)  # goes to beginning of the file
    line = open_file.readline()
    while "heat capacity" not in line:
        line = open_file.readline()
    result = re.findall("[+-]?\d+\.\d+", line)
    return result[0]


#################################################################
# gets the Element type, coordinate (x,y,z)(Angstrom), and Mulliken partial charge (e) of the atom)
def getElementType(open_file):
    open_file.seek(0, os.SEEK_SET)  # goes to beginning of the file
    line = open_file.readline()
    while 'Geometry "geometry" -> "geometry"' not in line:
        line = open_file.readline()
    open_file.readline()
    open_file.readline()
    open_file.readline()
    open_file.readline()
    open_file.readline()
    open_file.readline()

    line = open_file.readline()  # moves to the first atom
    result = [x.strip() for x in line.split()]
    output = "%s\t%12s\t%12s\t%12s" % (result[1], result[3], result[4], result[5])
    while not line.isspace():
        result = [x.strip() for x in line.split()]
        output += "\n%s\t%12s\t%12s\t%12s" % (result[1], result[3], result[4], result[5])
        line = open_file.readline()  # moves to the next atom
    return output


#################################################################
# gets the frequencies (3na-5 or 3na-6)
def getFrequencies(open_file):
    open_file.seek(0, os.SEEK_SET)  # goes to beginning of the file
    line = open_file.readline()
    while "Normal Eigenvalue" not in line:
        line = open_file.readline()
    open_file.readline()
    open_file.readline()
    line = open_file.readline()
    output = ""
    while "-" not in line:
        result = [x.strip() for x in line.split()]
        output += result[1] + " \t"
        line = open_file.readline()  # moves to the next atom
    return output


#################################################################
# gets the SMILES
def getSMILES(open_file):
    open_file.seek(0, os.SEEK_SET)  # goes to beginning of the file


#################################################################
# gets the InChI
def getInChI(open_file):
    open_file.seek(0, os.SEEK_SET)  # goes to beginning of the file


# ================================================================#
# Support Functionality
def getZeroPointCorrection(open_file):
    open_file.seek(0, os.SEEK_SET)  # goes to beginning of the file
    line = open_file.readline()
    while "Zero-Point" not in line:
        line = open_file.readline()
    result = re.findall("[+-]?\d+\.\d+", line)
    return result[1]  # [0]= kcal  [1]= au


def getRotationalConstants(open_file):
    open_file.seek(0, os.SEEK_SET)  # goes to beginning of the file
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


#################################################################
# main
# dirs = [d for d in os.listdir('./') if os.path.isdir(os.path.join('./', d))]

dirs = [line.rstrip('\n') for line in open('302_Inchi_key')]

for each_dir in dirs:
    pattern = each_dir + '.out.1*'
    matches = glob.glob(os.path.join(each_dir, pattern))
    for m in matches:
        index = m.split('.')[2]
    for j in matches:
        #
        with open(j, 'r') as f:
            outputData = ("nAtoms\tindex\tmu\tHOMO\tLUMO\tgap\tZPVE\tE\tE0K\tH\tG\tS\tCv\n")

            zero = float(getZeroPointCorrection(f))
            nAtoms = getNumberOfAtoms(f)
            #            index = get1BasedIdentifier(each_dir)
            A, B, C = getRotationalConstants(f)
            mu = getDipoleMoment(f)
            HOMO, LUMO = getHOMO_LUMO(f)
            gap = getGap(LUMO, HOMO)
            ZPVE = getZeroPointVibrationEnergy(zero, f)
            E0K = getInternalEnergy0K(f)
            internalEnergy = float(E0K)
            ThermalCorr = ThermalCorrectionEnergy(f)
            E = getInternalEnergy(internalEnergy, ThermalCorr)
            H = getEnthalpy(internalEnergy, f)
            G = getFreeEnergy(internalEnergy, f)
            tEsolvation = getSolvationEnergy(f)
            cV = getHeatCapacity(f)
            print(each_dir, index, nAtoms, A, B, C, mu, HOMO, LUMO, gap, ZPVE, E, E0K, H, G, tEsolvation, cV)
            os.chdir(each_dir)
            outputData += ("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (
            nAtoms, index, mu, HOMO, LUMO, gap, ZPVE, E, E0K, H, G, tEsolvation, cV))
            outputData += "\n" + getElementType(f) + "\n"  # + getFrequencies(f)
            with open("calculated_properties.txt", 'w') as output:
                output.write(outputData)
            os.chdir('../../')
