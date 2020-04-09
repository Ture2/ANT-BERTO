MONGO_DATABASE = 'my'
MONGO_COLLECTION = 'contratos_full'
MONGO_RESULTS_DATABASE = 'store_results'
MONGO_RESULTS_COLLECTION = 'results'
DEFAULT_DIRECTORY = '/Users/Ture/Documents/Blockchain/ANT-BERTO'
DEFAULT_INPUT = '/inputs'
DEFAULT_OUTPUT = '/outputs'
DEFAULT_TOOL = 'all'
LOG_FILENAME = 'stack_trace.log'
LOGGER_NAME = 'Default_logger'

SOLC_SLITHER = '/home/slither/.py-solc/solc-v{}/bin/solc'

EOF_STRING = '---!!!---'

#TOOLS = ['solgraph', 'oyente', 'smartcheck', 'solmet', 'osiris', 'vandal', 'ethir', 'mythril','securify']
#CONTAINERS = ['vsolgraph', 'voyente', 'vsolmet', 'vethir', 'vosiris', 'vvandal', 'vsmartcheck', 'mythril','securify']
TOOLS = ['mythril','securify', 'slither']
CONTAINERS = ['mythril','securify', 'vslither']

TOOLS_PROPERTIES = [
    {
        "name" : "mythril",
        "container": "mythril",
        "workdir": "/home/mythril",
        "cmd": "myth analyze  --solv {} ../../tmp/inputs/{} --execution-timeout 60 --max-depth 20",
        "ext": ".sol"
    },
    {
        "name" : "securify",
        "container": "securify",
        "workdir": "/sec",
        "cmd": "securify ../../tmp/inputs/{}",
        "ext": ".sol"
    },
    {
        "name" : "slither",
        "container": "vslither",
        "workdir": "/home/slither/slither",
        "cmd": "slither ../../../tmp/inputs/{1} --solc {0}",
        "ext": ".sol"
    }


]



SOL_TOOLS = [
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
    },{
        "name" : "mythril",
        "container": "mythril",
        "workdir": "/home/mythril",
        "cmd": "myth analyze  --solv {} ../../tmp/inputs/{}",
        "ext": ".sol"
    },
    {
        "name" : "securify",
        "container": "securify",
        "workdir": "/sec",
        "cmd": "securify ../../tmp/inputs/{}",
        "ext": ".sol"
    },
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

