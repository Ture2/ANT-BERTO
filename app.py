import docker
import tarfile
import os
import subprocess
import sys
import dependencies_builder
import constants
from pymongo import MongoClient

# HOST

VERSION = 0.2
docker_client = docker.APIClient(base_url='unix://var/run/docker.sock')
TOOLS = ['vsolgraph', 'voyente']
SOL_TOOLS = ['vsolgraph', 'voyente']
SCRIPTS = ['solgraph']


def mongo_connection():
    client = MongoClient("127.0.0.1", 27017)
    db = client.my
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



def execute_command(type ,file, output_file):
    if os.path.isfile(constants.PATH_TO_MAIN_DIRECTORY + constants.PATH_TO_INPUT + file):
        if type == 1:
            for tool in constants.HEX_TOOLS:
                cmd = tool.get("cmd").format(file)
                execution = docker_client.exec_create(tool.get('container'), cmd=cmd, workdir=tool.get('workdir'), privileged=True)
                res_iter = docker_client.exec_start(execution, stream=True, demux=True)
                result = ""
                for line in res_iter:
                    result += line[1]
                dependencies_builder.save_results(result, output_file)
        elif type == 0:
            for tool in constants.SOL_TOOLS:
                cmd = tool.get("cmd").format(file)
                execution = docker_client.exec_create(tool.get('container'), cmd=cmd, workdir=tool.get('workdir'),
                                                      privileged=True)
                res_iter = docker_client.exec_start(execution, stream=True, demux=True)
                result = ""
                for line in res_iter:
                    result += line[0]
                dependencies_builder.save_results(result, output_file)


def analyze(contract):
    input_sol_file = 'input_' + contract.get_name() + '.sol'
    input_hex_file = 'input_' + contract.get_name() + '.hex'
    output_file = 'output_{}.txt'.format(contract.get_name())
    execute_command(0, input_sol_file, output_file)
    execute_command(1, input_hex_file, output_file)



def get_all_contract_id():
    collection = mongo_connection()
    c_contracts = collection.find({'contract_id': {"$exists": 'true', "$ne": ""}})
    return c_contracts


def test():
    c_contracts = get_all_contract_id()
    for contract in c_contracts:
        c = dependencies_builder.create_contract(contract['contract_id'])
        analyze(c)


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
