import pymongo
from pathlib import Path
import os

# RESULT_PATH=os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..', "results"))
# RESULT_PATH="/Volumes/MSSHARE/Anubhav/darpacme/Sep20/results"
RESULT_PATH="/Volumes/MSSHARE/Anubhav/darpacme/Oct26/test/results"
# RESULT_PATH="/Volumes/MSSHARE/Anubhav/darpacme/test/"
FILEPATTERN='*_calc_prop_v2.dat'

DATABASENAME="darpe_cme"
COLLNAME="calcProp_uvSpec"

def setup_db():
    uri = "mongodb://localhost:27017"
    client = pymongo.MongoClient(uri)
    calc_prop_coll= client[DATABASENAME][COLLNAME]
    return calc_prop_coll

def check_in_db(coll, chem_id):
    filter = {'_id': {'$eq': chem_id}}
    if coll.count_documents(filter) == 0:
        print("populate!")
        return False
    else:
        print("record exists")
        return True

def populate_db(coll, doc):
    coll.insert_one(doc)

def parse_calc_prop(path, mol_name):

    # read the chem_id_calc_prop_v2.dat
    with open(path,'r') as calc_prop:

        # set atomic number
        atomic_num=next(calc_prop).split()
        print("atomic_num", atomic_num)
        # set 15 col
        INCHIKEY, index, A, B, C, mu, HOMO, LUMO, gap, ZPVE, U0, U, H, G, Cv= next(calc_prop).split()

        # set Geometry block with ["symbol", "x","y","z","Mulliken_population_charge"]
        geo_block = []
        # set Frequency block
        freq_block = None
        # set Converged SMILE
        converg_smile=""
        # set Converged InChI
        converg_inchi=""
        lines= calc_prop.readlines()
        for line in lines:
            line_list= line.split()

            if len(line_list)==5:
                print(line_list)
                symbol, x, y, z, Mulliken_population_charge =line_list
                geo_block.append( [symbol,float(x),float(y),float(z), float(Mulliken_population_charge)] )
            if len(line_list)>5:
                freq_block = [float(freq) for freq in line_list]
            if len(line_list)==1:
                if line_list[0].split('=')[0] == 'InChI':
                    converg_inchi=line_list[0].split('=')[1]
                else:
                    converg_smile=line_list[0]


        # prepare a doc
        doc={}
        doc['_id'] = mol_name
        doc['atomic_num'] = int(atomic_num[0])
        doc['INCHIKEY'] = INCHIKEY
        doc['index'] = index
        doc['A'] = float(A)
        doc['B'] = float(B)
        doc['C'] = float(C)
        doc['mu'] = float(mu)
        doc['HOMO'] = float(HOMO)
        doc['LUMO'] = float(LUMO)
        doc['gap'] = float(gap)
        doc['ZPVE'] = float(ZPVE)
        doc['U0'] = float(U0)
        doc['U'] = float(U)
        doc['H'] = float(H)
        doc['G'] = float(G)
        doc['Cv'] = float(Cv)
        doc['geo_block']= geo_block
        doc['freq_block'] = freq_block
        doc['converg_smile'] = converg_smile
        doc['converg_inchi'] = converg_inchi
        return doc

if __name__ == '__main__':

    coll =setup_db()
    counter=0

    for path in Path(RESULT_PATH).rglob(FILEPATTERN):
        mol_name = str(path).split('/')[-3]
        doc = parse_calc_prop(str(path), mol_name)
        if not check_in_db(coll, mol_name):
            populate_db(coll, doc)
        else:
            # return the existing doc in the database.!
            print("return the existing doc in the database.!")
