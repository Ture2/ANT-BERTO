import getopt
import os
import subprocess
import sys

TOOL = 'OYENTE'
MONGO_COLLECTION = 'contratos'
PATH_TO_MAIN_DIRECTORY = '/Users/Ture/Documents/Blockchain/ANT-BERTO/'
dir = '../../tmp/outputs/'


def launch(file):
    file_path = 'tmp/outputs/{}.hex'.format(file)
    output_file = '../../tmp/outputs/oyente/{}.txt'.format(file)
    cmd = ['python', 'oyente.py -s {} -b'.format(file_path)]
    os.chdir(dir)
    with open(output_file, 'w+') as f:
        p = subprocess.Popen(cmd=cmd, stdout=f, stderr=f)
        output, errors = p.communicate()
        print(output, errors)


def main(argv):
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


if __name__ == "__main__":
    main(sys.argv[1:])
