import csv
import sys

def create_mol_config(inchi_file):
    '''
    Creates config file with molecule names!
    :param inchi_file:
    :return:
    '''
    dict_file = []
    with open(inchi_file, 'r') as rfile,\
         open('config.yaml', 'w') as wfile:
        reader = csv.reader(rfile, delimiter=(','))
        lineCount = 0
        for row in reader:
            if lineCount == 0:
                InChIKey = row.index("InChI-Key")
                lineCount += 1
            else:
                # print(row)
                inchikey_str = row[InChIKey].split('=')[1]
                dict_file.append(inchikey_str)
        wfile.write("chemical_ids: "+ str(dict_file).replace('"', ''))


if __name__ == '__main__':

    inchi_file= ""
    for arg in sys.argv:
        if arg.endswith((".csv")):
            inchi_file = arg

    create_mol_config(inchi_file)