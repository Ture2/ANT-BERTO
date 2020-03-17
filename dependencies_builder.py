import constants
from test import Contract
from pymongo import MongoClient

# HOST

TOOL = ['SOLGRAPH', 'OYENTE']


def get_contract(id):
    client = MongoClient("127.0.0.1",
                         27017)  # OJO! La IP de MongoDB aqui es 127.0.0.1. (Desde dentro de un docker es 172.17.0.1, que es la IP del anfitrion)
    db = client.my
    collection = db[constants.MONGO_COLLECTION]
    cursor = collection.find({'contract_id': id})
    return cursor.next()


def get_content(id):
    bytecode = get_contract(id)['bytecode']
    solidity_code = get_contract(id)['solidity']
    content = {}
    extensions = []
    if str(bytecode) != '0x':
        content['hex'] = str.split(str(bytecode), 'x')[1]
        extensions.append('.hex')
    if type(solidity_code) is list:
        content['sol'] = solidity_code[0].get('SourceCode')
        extensions.append('.sol')
    return content, extensions


def doc_creation(contract):
    name = contract.get_name()
    for ext in contract.extensions:
        input_file = "input_{}{}".format(name, ext)
        path_to_input_file = constants.PATH_TO_MAIN_DIRECTORY + constants.PATH_TO_INPUT + input_file
        f = open(path_to_input_file, "w+")
        content = contract.get_content_by_extension(str.split(ext, '.')[1])
        f.write(content)
        f.close()


def create_contract(id):
    contract = Contract(id)
    content, ext = get_content(id)
    contract.set_content(content)
    contract.set_extensions(ext)
    doc_creation(contract)
    return contract


def save_results(content, output_file):
    path_to_output = constants.PATH_TO_MAIN_DIRECTORY + constants.PATH_TO_OUTPUT + output_file
    f = open(path_to_output, "a+")
    f.write(content)
    f.write(constants.SPLIT_BETWEEN_TOOLS)
    f.close()
