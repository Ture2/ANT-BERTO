import shlex, subprocess, sys, getopt

TOOL = 'SOLGRAPH'
PATH_TO_TMP = '/tmp'
PATH_TO_OUTPUT = '/outputs'

def launch(file):
    file_path = '../tmp/outputs/{}.sol'.format(file)
    output_file = '../tmp/outputs/solgraph/{}.dot'.format(file)
    cmd = ['solgraph', file_path]
    #args = shlex.split(cmd)
    #print(args)
    with open(output_file, 'w+') as f:
        p = subprocess.Popen(cmd, stdout=f, stderr=f)
        output, errors = p.communicate()
        print(output, errors)


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