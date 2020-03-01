import docker
import tarfile
import os
import subprocess
import sys
import dependencies_builder
from pymongo import MongoClient

VERSION = 0.1
MONGO_COLLECTION = 'contratos'
docker_client = docker.APIClient(base_url='unix://var/run/docker.sock')
TYPE = ["npm, "]
TOOLS = ['vsolgraph']
SOL_TOOLS = ['vsolgraph']
SCRIPTS = ['solgraph']
PATH_TO_MAIN_DIRECTORY = '/Users/Ture/Documents/Blockchain/ANT-BERTO/'

def mongo_connection():
    client = MongoClient("127.0.0.1", 27017)
    db = client.mydb
    collection = db[MONGO_COLLECTION]
    return collection

def init():
    containers_running = docker_client.containers(all=True)
    final_name_list = list()
    for c in containers_running:
        name_list = c['Names']
        if len(name_list) > 0:
            final_name_list += name_list

    for tool in TOOLS:
        docker_client.start(tool)
        if not final_name_list.__contains__(tool):
            copy_file_to_container('/Users/Ture/Documents/Blockchain/ANT-BERTO/solgraph.py', '/home/', tool)
        print(docker_client.logs(tool))


def copy_file_to_container(src, dst, cname):
    os.chdir(os.path.dirname(src))
    srcname = os.path.basename(src)
    file = src + '.tar'
    tar = tarfile.open(file, 'w')
    try:
        tar.add(srcname)
    finally:
        tar.close()
        data = open(file, 'rb').read()
        docker_client.put_archive(cname, os.path.dirname(dst), data)
        os.remove(file)


def has_solidity_code(id):
    collection = mongo_connection()
    contract = collection.find({'contract_id': id})
    if not contract['solidity']:
        return False
    else:
        return True


class ToolFactory:
    def analyze(self, toolstr, contract_id):
        dependencies_builder.doc_creation(toolstr, contract_id)
        tool = self._get_tool(toolstr)
        return tool(contract_id)

    def _get_tool(self, container):
        if container == TOOLS[0]:
            return self._solgpraph_analyzer
        elif container == TOOLS[8]:
            return self._oyente_analyzer
        '''
        elif container == TOOLS[1]:
            return self._smartcheck_analyzer
        elif container == TOOLS[2]:
            return self._contractlarva_analyzer
        elif container == TOOLS[3]:
            return self._solmet_analyzer
        elif container == TOOLS[4]:
            return self._ethir_analyzer
        elif container == TOOLS[5]:
            return self._securify_analyzer
        elif container == TOOLS[6]:
            return self._madmax_analyzer
        elif container == TOOLS[7]:
            return self._osiris_analyzer
        elif container == TOOLS[8]:
            return self._oyente_analyzer
        '''

    def _solgpraph_analyzer(self, file):
        if file != False:
            cmd = ["python", "solgraph.py -n {}".format(file)]
            container = docker_client.exec_create('vsolgraph', cmd, workdir='/home', privileged=True)
            docker_client.exec_start(container)

    def _smartcheck_analyzer(self, custom_params):
        return 0

    def _contractlarva_analyzer(self, custom_params):
        return 0

    def _solmet_analyzer(self, custom_params):
        return 0

    def _vandal_analyzer(self, custom_params):
        return 0

    def _ethir_analyzer(self, custom_params):
        return 0

    def _securify_analyzer(self, custom_params):
        return 0

    def _madmax_analyzer(self, custom_params):
        return 0

    def _osiris_analyzer(self, custom_params):
        return 0

    def _oyente_analyzer(self, contract_id):
        cmd = ["python", "myoyente.py -c {}".format(contract_id)]
        return 0


def get_all_contract_id():
    collection = mongo_connection()
    c_contracts = collection.find({'contract_id': {"$exists": 'true', "$ne": ""}})
    return c_contracts


def test():
    # Get contract ids
    c_contracts = get_all_contract_id()
    cont = 0
    tool_factory = ToolFactory()
    for contract in c_contracts:
        for tool in TOOLS:
            tool_factory.analyze(tool, contract['contract_id'])


def main(argv):
    val = raw_input("Hello, welcome to Analyzer, do you want a complete test(t) or custom(c)?")
    init()
    if val == 't':
        print("Test selected")
        test()
    elif val == 'c':
        print("Custom selected")


if __name__ == "__main__":
    main(sys.argv[1:])



