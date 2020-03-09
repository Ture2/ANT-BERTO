import constants
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

    if tool.upper() in ['SOLGRAPH']:
        file_extension = 'sol'
        content = get_contract(id)['solidity']
        if type(content) is list:
            return content[0].get('SourceCode'), file_extension
    elif tool.upper() in ['OYENTE']:
        file_extension = 'hex'
        content = get_contract(id)['bytecode']
    return content, file_extension

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
