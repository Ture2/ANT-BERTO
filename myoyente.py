import subprocess, sys, getopt
import argparse
from pymongo import MongoClient

TOOL = 'OYENTE'
MONGO_COLLECTION = 'contratos'
PATH_TO_MAIN_DIRECTORY = '/Users/Ture/Documents/Blockchain/ANT-BERTO/'


def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hn:", ["contract-name="])
    except getopt.GetoptError:
        print("myoyente.py -n <contract-name> ")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("myoyente.py -n <contract-name> ")
            sys.exit()
        elif opt in ("-n", "--contract-name"):
            inputfile = arg
            print('Input file is ', inputfile)
            launch(inputfile)  # El id se pasa al resto de funciones como un INT


def launch(file):
    with open(file, 'w+') as f:
        p = subprocess.Popen(['oyente.py', "-s {}".format(file)], stdout=f, stderr=f)
        output, errors = p.communicate()


if __name__ == "__main__":
    main(sys.argv[1:])
