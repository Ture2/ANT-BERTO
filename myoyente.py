import subprocess, sys, getopt
from pymongo import MongoClient

TOOL = 'OYENTE'
MONGO_COLLECTION = 'contratos'
PATH_TO_MAIN_DIRECTORY = '/Users/Ture/Documents/Blockchain/ANT-BERTO/'

def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hc:", ["contract-id="])
    except getopt.GetoptError:
        print("myoyente.py -c <contract id> ")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("myoyente.py -i <contract id> ")
            sys.exit()
        elif opt in ("-c", "--contract-id"):
            inputfile = arg
            print('Input file is ', inputfile)
            launch(doc_creation(int(inputfile)))  # El id se pasa al resto de funciones como un INT

def doc_creation():
    generic_file = "tmp_OYENTE_{}".format(id)
    path_to_input_file = "{}.evm".format(generic_file)
    f = open(path_to_input_file, "w+")
    contract_code = get_contract(id)['solidity']
    print(contract_code)
    f.write(contract_code)
    f.close()




def get_contract(id):
    client = MongoClient("172.17.0.1", 27017)  # OJO! La IP de MongoDB aqui es 127.0.0.1. (Desde dentro de un docker es 172.17.0.1, que es la IP del anfitrion)
    db = client.mydb
    collection = db[MONGO_COLLECTION]
    cursor = collection.find({'contract_id': id})
    return cursor.next()


def launch(file):
    path_to_output_file = PATH_TO_MAIN_DIRECTORY + '/tmp/{}.txt'.format(file)
    with open(path_to_output_file, 'w+') as f:
        p = subprocess.Popen(['solgraph', "{}.sol".format(file)], stdout=f, stderr=f)
        output, errors = p.communicate()


if __name__ == "__main__":
    main(sys.argv[1:])
