MONGO_DATABASE = 'mydb'
MONGO_COLLECTION = 'contratos_full'
MONGO_RESULTS_DATABASE = 'results_db'
MONGO_RESULTS_COLLECTION = 'outputs_full'
DEFAULT_DIRECTORY = '/Users/Ture/Documents/TFG'
DEFAULT_INPUT = '/inputs'
DEFAULT_OUTPUT = 'resultados'
DEFAULT_TOOL = 'all'
LOG_FILENAME = 'stack_trace.log'
LOGGER_NAME = 'Default_logger'
PROGRESS_BAR_LEN = 180
output_created = False

SOLC_SLITHER = '/home/slither/.py-solc/solc-v{}/bin/solc'

EOF_STRING = '---!!!---'

TOOLS = ['solgraph', 'oyente', 'smartcheck', 'solmet', 'osiris', 'vandal', 'ethir', 'mythril', 'securify', 'slither',
         'manticore','madmax']
CONTAINERS = ['vsolgraph', 'voyente', 'vsolmet', 'vethir', 'vosiris', 'vvandal', 'vsmartcheck', 'vmythril','vsecurify',
              'vslither', 'vmanticore', 'vmadmax']


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
        "cmd": "java -jar SolMet-1.0-SNAPSHOT.jar -inputFile /tmp/inputs/{0} -outFile output.csv",
        "ext": ".sol"
    },
    {
        "name" : "oyente",
        "container": "voyente",
        "workdir": "/oyente/oyente/",
        "cmd": "python oyente.py -s /tmp/inputs/{} -b",
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
        "cmd": "python oyente-ethir.py -s /tmp/inputs/{} -b",
        "ext": ".hex"
    },
    {
        "name" : "vandal",
        "container": "vvandal",
        "workdir": "/home/vandal/bin/",
        "cmd": "bash ./analyze.sh /tmp/inputs/{} ../datalog/demo_analyses.dl",
        "ext": ".hex"
    },
    {
        "name" : "mythril",
        "container": "vmythril",
        "workdir": "/home/mythril",
        "cmd": "myth analyze  --solv {} /tmp/inputs/{} --execution-timeout 60 --max-depth 20",
        "ext": ".sol"
    },
    {
        "name" : "securify",
        "container": "vsecurify",
        "workdir": "/sec",
        "cmd": "securify /tmp/inputs/{}",
        "ext": ".sol"
    },
    {
        "name" : "slither",
        "container": "vslither",
        "workdir": "/home/slither/slither",
        "cmd": "slither /tmp/inputs/{1} --solc {0}",
        "ext": ".sol"
    },
    {
        "name" : "manticore",
        "container": "vmanticore",
        "workdir": "/manticore",
        "cmd": "manticore /tmp/inputs/{} --solc-solcs-bin solc-0.4.26,solc-0.4.25,solc-0.4.24,solc-0.4.23,solc-0.4.21,"
               "solc-0.4.20,solc-0.4.19,solc-0.4.18,solc-0.4.17,solc-0.4.16,solc-0.4.1",
        "ext": ".sol"
    },
    {
        "name" : "madmax",
        "container": "vmadmax",
        "workdir": "/home/MadMax",
        "cmd": "bin/decompile -n -v -g graph.html /tmp/inputs/{}",
        "ext": ".hex"
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

