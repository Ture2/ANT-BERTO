MONGO_COLLECTION = 'contratos_full'
PATH_TO_MAIN_DIRECTORY = '/Users/Ture/Documents/Blockchain/ANT-BERTO/'
<<<<<<< HEAD
PATH_TO_INPUT = '/inputs/'
PATH_TO_OUTPUT = '/outputs/'
LOG_FILENAME = 'stack_trace.log'
LOGGER_NAME = 'Default_logger'

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
=======

TOOLS = (
    {
        "container_name": "vsolgraph",
        "workdir": "/home/",
        "tool_script": "solgraph.py",
        "tool_name_inside_container": "solgraph",
        "tool_name": "solgraph",
        "type": "npm",
        "outputdir": ""
    },
    {
        "container_name": "voyente",
        "workdir": "/oyente/oyente/",
        "tool_script": "myoyente.py",
        "tool_name_inside_container": "oyente.py",
        "tool_name": "oyente",
        "type": "python",
        "outputdir": ""
    },
)
>>>>>>> parent of 723aaa0... v0.2 Solgraph and Oyente works correctly, refactored code
