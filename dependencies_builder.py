import docker
import subprocess, sys, getopt
from pymongo import MongoClient

TOOL = ['SOLGRAPH', 'OYENTE']
MONGO_COLLECTION = 'contratos'

# TODO: Cambiar el path para leer el actual
PATH_TO_MAIN_DIRECTORY = '/Users/Ture/Documents/Blockchain/ANT-BERTO'
PATH_TO_TMP = '/tmp'
PATH_TO_OUTPUT = '/output'


def get_contract(id):
    client = MongoClient("172.17.0.1",
                         27017)  # OJO! La IP de MongoDB aqui es 127.0.0.1. (Desde dentro de un docker es 172.17.0.1, que es la IP del anfitrion)
    db = client.mydb
    collection = db[MONGO_COLLECTION]
    cursor = collection.find({'contract_id': id})
    return cursor.next()


def get_content(tool, id):
    if tool in ['SOLGRAPH']:
        return get_contract(id)['solidity']
    elif tool in ['OYENTE']:
        return get_contract(id)['bytecode']


def doc_creation(tool, id):
    generic_file = "tmp_{}_{}".format(tool, id)
    path_to_input_file = PATH_TO_MAIN_DIRECTORY + PATH_TO_TMP + "/{}.sol".format(generic_file)
    f = open(path_to_input_file, "w+")
    contract_code = get_content(tool, id)
    if contract_code:
        f.write(contract_code)
        f.close()
        return path_to_input_file
    else:
        return False
