MONGO_COLLECTION = 'contratos_full'
PATH_TO_MAIN_DIRECTORY = '/Users/Ture/Documents/Blockchain/ANT-BERTO/'
PATH_TO_INPUT = '/inputs/'
PATH_TO_OUTPUT = '/outputs/'
SELECTED_TOOL = 'all'
LOG_FILENAME = 'stack_trace.log'
LOGGER_NAME = 'Default_logger'

SPLIT_BETWEEN_TOOLS = '---!!!---'

TOOLS = ['solgraph', 'oyente', 'smartcheck', 'solmet', 'osiris', 'vandal', 'ethir']
CONTAINERS = ['vsolgraph', 'voyente', 'vsolmet', 'vethir', 'vosiris', 'vvandal']


TOOLS_PROPERTIES = [
    {
        "name" : "solgraph",
        "container": "vsolgraph",
        "workdir": "/tmp/inputs/",
        "cmd": "solgraph {0} > {0}.dot",
        "ext": ".sol"
    },
    {
        "name" : "smartcheck",
        "container": "vsmartcheck",
        "workdir": "/tmp/inputs/",
        "cmd": "smartcheck -p {0} ",
        "ext": ".sol"
    },
    {
        "name" : "solmet",
        "container": "vsolmet",
        "workdir": "/home/SolMet-Solidity-parser/target/",
        "cmd": "java -jar SolMet-1.0-SNAPSHOT.jar -inputFile ../../../tmp/inputs/{0} -outFile output.csv",
        "ext": ".sol"
    },
{
        "name" : "oyente",
        "container": "voyente",
        "workdir": "/oyente/oyente/",
        "cmd": "python oyente.py -s ../../tmp/inputs/{} -b",
        "ext": ".hex"
    },
    {
        "name" : "osiris",
        "container": "vosiris",
        "workdir": "/root/osiris",
        "cmd": "python osiris.py -s /tmp/inputs/{} -b",
        "ext" : ".hex"
    },
    {
        "name" : "ethir",
        "container": "vethir",
        "workdir": "/home/EthIR/ethir/",
        "cmd": "python oyente-ethir.py -s ../../../tmp/inputs/{} -b",
        "ext": ".hex"
    },
    {
        "name" : "vandal",
        "container": "vvandal",
        "workdir": "/home/vandal/bin/",
        "cmd": "bash ./analyze.sh ../../../tmp/inputs/{} ../datalog/demo_analyses.dl",
        "ext": ".hex"
    }
]



SOL_TOOLS = [
    {
        "name" : "solgraph",
        "container": "vsolgraph",
        "workdir": "/tmp/inputs/",
        "cmd": "solgraph {0} > {0}.dot"
    },
    {
        "name" : "smartcheck",
        "container": "vsmartcheck",
        "workdir": "/tmp/inputs/",
        "cmd": "smartcheck -p {0} "
    },
    {
        "name" : "solmet",
        "container": "vsolmet",
        "workdir": "/home/SolMet-Solidity-parser/target/",
        "cmd": "java -jar SolMet-1.0-SNAPSHOT.jar -inputFile ../../../tmp/inputs/{0} -outFile output.csv"
    },
]
HEX_TOOLS = [
    {
        "name" : "oyente",
        "container": "voyente",
        "workdir": "/oyente/oyente/",
        "cmd": "python oyente.py -s ../../tmp/inputs/{} -b"
    },
    {
        "name" : "osiris",
        "container": "vosiris",
        "workdir": "/osiris/",
        "cmd": "python osiris.py -s ../tmp/inputs/{} -b"
    },
    {
        "name" : "ethir",
        "container": "vethir",
        "workdir": "/home/EthIR/ethir/",
        "cmd": "python oyente-ethir.py -s ../../../tmp/inputs/{} -b"
    },
    {
        "name" : "vandal",
        "container": "vvandal",
        "workdir": "/home/vandal/bin/",
        "cmd": "analyze.sh ../../../tmp/inputs/{} ../datalog/demo_analyses.dl"
    }
]

