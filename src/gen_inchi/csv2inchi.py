import os
import csv
import sys

def csv2inchi(inchi_file,result_dir):
    '''
    Create initial file structure
    :param inchi_file: path to .inchi file.
    :return:
    '''
    with open(inchi_file, 'r') as f:
        # if 'inchi.csv' in inchi_file:
        reader = csv.reader(f, delimiter=(','))

        lineCount = 0
        for row in reader:
            if lineCount == 0:
                InChIKey = row.index("InChI-Key")
                InChI = row.index("InChI")
                lineCount += 1
            else:
                # print(row)
                inchikey_str = row[InChIKey].split('=')[1]
                # print('inchikey string ', inchikey_str)

                moldir = os.path.join(result_dir,inchikey_str)
                if not os.path.exists(moldir):
                    os.mkdir(moldir)

                initial_structure_dir = os.path.join(moldir,'initial_structure')
                if not os.path.exists(initial_structure_dir):
                    os.mkdir(initial_structure_dir)

                md_structure_dir = os.path.join(moldir,'md')
                if not os.path.exists(md_structure_dir):
                    os.mkdir(md_structure_dir)

                dft_structure_dir =os.path.join(moldir,'dft')
                if not os.path.exists(dft_structure_dir):
                    os.mkdir(dft_structure_dir)

                inchifile_str = os.path.join(initial_structure_dir , inchikey_str + '.inchi')
                with open(inchifile_str, 'w+') as f:
                    f.write(row[InChI])

    print("Starting CME workflow")

if __name__ == '__main__':

    inchi_file, result_dir="",""
    for arg in sys.argv:
        if arg.endswith((".csv")):
            inchi_file = arg
        if arg.endswith((".inchi")):
            out_file = arg

    result_dir='/'.join(out_file.split('/')[:-3])
    csv2inchi(inchi_file,result_dir)