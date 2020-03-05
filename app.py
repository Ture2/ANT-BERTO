import docker
import tarfile
import os
import subprocess
import sys
import dependencies_builder
import constants
from pymongo import MongoClient

# HOST

VERSION = 0.1
docker_client = docker.APIClient(base_url='unix://var/run/docker.sock')
TOOLS = ['vsolgraph', 'voyente']
SOL_TOOLS = ['vsolgraph', 'voyente']
SCRIPTS = ['solgraph']
PATH_TO_MAIN_DIRECTORY = '/Users/Ture/Documents/Blockchain/ANT-BERTO/'


def mongo_connection():
    client = MongoClient("127.0.0.1", 27017)
    db = client.mydb
    collection = db[constants.MONGO_COLLECTION]
    return collection


def init():
    containers_running = docker_client.containers(all=True)
    final_name_list = list()

    for c in containers_running:
        name_list = c['Names']
        if len(name_list) > 0:
            final_name_list += name_list

    for tool in constants.TOOLS:
        try:
            docker_client.start(tool.get('container_name'))
        except:
            print ("El docker " + tool.get('container_name') + " no existe")
        if not final_name_list.__contains__(tool.get('container_name')):
            copy_file_to_container(constants.PATH_TO_MAIN_DIRECTORY + tool.get('tool_script'), tool.get('workdir'),
                                   tool.get('container_name'))
        print(docker_client.logs(tool.get('container_name')))


# src: str to source file directory
# dst: str to destiny inside container
# cname: target container name


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
    def analyze(self, tool_data, contract_id):
        file_name = dependencies_builder.doc_creation(tool_data.get('tool_name'), contract_id)
        if file_name:
            tool = self._get_tool(tool_data)
            return tool(tool_data, file_name)
        else:
            return False

    def _get_tool(self, tool_data):
        cname = tool_data.get('container_name')
        if cname == TOOLS[0]:
            return self._solgpraph_analyzer
        elif cname == TOOLS[1]:
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

    def _solgpraph_analyzer(self, tool_data, file):
        if file:
            cmd = ["python", "{} -n {}".format(tool_data.get('tool_script'), file)]
            container = docker_client.exec_create(tool_data.get('container_name'), cmd,
                                                  workdir=tool_data.get('workdir'), privileged=True)
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

    def _oyente_analyzer(self, tool_data, file):
        cmd = ["python", "{} -n {}".format(tool_data.get('tool_script'), file)]
        container = docker_client.exec_create(tool_data.get('container_name'), cmd, workdir=tool_data.get('workdir'), privileged=True)
        docker_client.exec_start(container)


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
        for tool in constants.TOOLS:
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
