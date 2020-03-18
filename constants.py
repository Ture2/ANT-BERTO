MONGO_COLLECTION = 'contratos_full'
PATH_TO_MAIN_DIRECTORY = '/Users/Ture/Documents/Blockchain/ANT-BERTO/'
PATH_TO_INPUT = '/inputs/'
PATH_TO_OUTPUT = '/outputs/'

SPLIT_BETWEEN_TOOLS = '---!!!---'

CONTAINERS = ['vsolgraph', 'voyente']

SOL_TOOLS = [
    {
        "name" : "solgraph",
        "container": "vsolgraph",
        "workdir": "/tmp/inputs/",
        "cmd": "solgraph {0} > {0}.dot"
    },
]
HEX_TOOLS = [
    {
        "name" : "oyente",
        "container": "voyente",
        "workdir": "/oyente/oyente/",
        "cmd": "python oyente.py -s ../../tmp/inputs/{} -b"
    }
]