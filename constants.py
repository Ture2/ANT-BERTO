MONGO_COLLECTION = 'contratos_full'
PATH_TO_MAIN_DIRECTORY = '/Users/Ture/Documents/Blockchain/ANT-BERTO/'
PATH_TO_INPUT = '/inputs/'
PATH_TO_OUTPUT = '/outputs/'

SPLIT_BETWEEN_TOOLS = '---!!!---'


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


TOOLS = (
    {
        "container_name": "vsolgraph",
        "workdir": "/tmp/outputs/",
        "tool_script": "solgraph.py",
        "tool_name_inside_container": "solgraph",
        "tool_name": "solgraph",
        "type": "npm",
        "test_command": "solgraph {0}.sol > {0}.dot",
        "outputdir": "/outputs/solgraph/"
    },
    {
        "container_name": "voyente",
        "workdir": "/oyente/oyente/",
        "tool_script": "myoyente.py",
        "tool_name_inside_container": "oyente.py",
        "tool_name": "oyente",
        "type": "python",
        "test_command": "python oyente.py -s ../../tmp/outputs/{}.hex -b",
        "outputdir": "/outputs/solgraph/"
    },
)