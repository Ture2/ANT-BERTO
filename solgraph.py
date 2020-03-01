import subprocess, sys, getopt

TOOL = 'SOLGRAPH'


def launch(file):
    with open(file, 'w+') as f:
        p = subprocess.Popen(['solgraph', file], stdout=f, stderr=f)
        output, errors = p.communicate()


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hn:", ["contract-name="])
    except getopt.GetoptError:
        print("solgraph.py -n <input file>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("solgraph.py -n <input file> ")
            sys.exit()
        elif opt in ("-n", "--input-file"):
            inputfile = arg
            print('Input file is ', inputfile)
            launch(inputfile)


if __name__ == "__main__":
    main(sys.argv[1:])
