MONGO_COLLECTION = 'contratos'
PATH_TO_MAIN_DIRECTORY = '/Users/Ture/Documents/Blockchain/ANT-BERTO/'

TOOLS = (
    {
        "container_name": "vsolgraph",
        "workdir": "/home",
        "tool_script": "solgraph.py",
        "tool_name_inside_container": "solgraph",
        "tool_name": "solgraph",
        "type": "npm",
        "outputdir": ""
    },
    {
        "container_name": "voyente",
        "workdir": "/oyente/oyente",
        "tool_script": "myoyente.py",
        "tool_name_inside_container": "oyente.py",
        "tool_name": "oyente",
        "type": "python",
        "outputdir": ""
    },
)