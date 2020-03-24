import constants
<<<<<<< HEAD
import mdcontracts
import os
import logging
from contract_class import Contract

logger = logging.getLogger(constants.LOGGER_NAME)


def get_content(id):
    bytecode = mdcontracts.get_contract(id)['bytecode']
    solidity_code = mdcontracts.get_contract(id)['solidity']
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

=======
from pymongo import MongoClient

# HOST

TOOL = ['SOLGRAPH', 'OYENTE']

# TODO: Cambiar el path para leer el actual
PATH_TO_MAIN_DIRECTORY = '/Users/Ture/Documents/Blockchain/ANT-BERTO'
PATH_TO_TMP = '/tmp'
PATH_TO_OUTPUT = '/outputs'
PATH_TO_VOLUME = '/var/lib/docker/volumes/outputs/_data'


def get_contract(id):
    client = MongoClient("127.0.0.1",
                         27017)  # OJO! La IP de MongoDB aqui es 127.0.0.1. (Desde dentro de un docker es 172.17.0.1, que es la IP del anfitrion)
    db = client.my
    collection = db[constants.MONGO_COLLECTION]
    cursor = collection.find({'contract_id': id})
    return cursor.next()


def get_content(tool, id):
>>>>>>> parent of 723aaa0... v0.2 Solgraph and Oyente works correctly, refactored code

    if tool.upper() in ['SOLGRAPH']:
        file_extension = 'sol'
        content = get_contract(id)['solidity']
        if type(content) is list:
            return content[0].get('SourceCode'), file_extension
    elif tool.upper() in ['OYENTE']:
        file_extension = 'hex'
        content = get_contract(id)['bytecode']
    return content, file_extension

<<<<<<< HEAD
# TODO: modificar el dirname, ahora mismo usa el path to main, si se usa una ruta custom que no este dentro del path fallara
def save_results(content, output_file, tool, parent_dir):
    os.chdir(parent_dir)
    if not os.path.exists(tool):
        os.mkdir(tool)
    path_to_output = parent_dir + "/{}/{}".format(tool, output_file)
    f = open(path_to_output, "a+")
    f.write(content)
    f.write(constants.SPLIT_BETWEEN_TOOLS)
    f.close()
    os.chdir(constants.PATH_TO_MAIN_DIRECTORY)


def create_settings_file(info):
    path_to_settings = constants.PATH_TO_MAIN_DIRECTORY + constants.PATH_TO_OUTPUT + '/settings.txt'
    with open(path_to_settings, "w+") as f:
        for line in info:
            f.write(line)
    f.close()


def create_output_dir(path):
    if path[-1:] != '/':
        path += '/'
    path = constants.PATH_TO_MAIN_DIRECTORY + path
    if not os.path.exists(path):
        os.mkdir(path)
        logger.info('Succesfully output path created -> {}'.format(path))
    else:
        logger.warning('The following path already exits {}.'.format(path))
=======
def doc_creation(tool, id):
    code, file_extension = get_content(tool, id)
    if code:
        generic_file = "tmp_{}_{}".format(tool, id)
        path_to_input_file = PATH_TO_MAIN_DIRECTORY + PATH_TO_OUTPUT + "/{}.{}".format(generic_file, file_extension)
        f = open(path_to_input_file, "w+")
        f.write(code)
        f.close()
        return generic_file
    else:
        return False
>>>>>>> parent of 723aaa0... v0.2 Solgraph and Oyente works correctly, refactored code
