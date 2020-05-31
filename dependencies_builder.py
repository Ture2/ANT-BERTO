import shutil
import constants
import mdcontracts
import os
import logging
import tempfile
from contract_class import Contract

logger = logging.getLogger(constants.LOGGER_NAME)


def get_content(id):
    bytecode = mdcontracts.get_contract(id)['bytecode']
    solidity_code = mdcontracts.get_contract(id)['solidity']
    content = {}
    extensions = []
    address = mdcontracts.get_contract(id)['address']
    if str(bytecode) != '0x':
        content['hex'] = str.split(str(bytecode), 'x')[1]
        extensions.append('.hex')
    if type(solidity_code) is list:
        content['sol'] = solidity_code[0].get('SourceCode')
        extensions.append('.sol')
    return content, extensions, address


# Input file creation method
def doc_creation(contract):
    name = contract.get_name()
    for ext in contract.extensions:
        input_file = "input_{}{}".format(name, ext)
        path_to_input_file = os.path.join(constants.DEFAULT_DIRECTORY + constants.DEFAULT_INPUT, input_file)
        f = open(path_to_input_file, "w+")
        content = contract.get_content_by_extension(str.split(ext, '.')[1])
        f.write(content)
        f.close()


# Create contract object
def create_contract(id):
    contract = Contract(id)
    content, ext, address = get_content(id)
    contract.set_content(content)
    contract.set_extensions(ext)
    contract.set_address(address)
    doc_creation(contract)
    return contract


# data[0]: smart contract written in solidity
# data[1]: bytecode
def create_contract_from_address(address, data):
    contract = Contract(address)
    ext = ['.hex']
    content = {'hex': str.split(str(data[1]), 'x')[1]}
    if data[0] != '':
        ext.append('.sol')
        content['sol'] = data[0][0].get('SourceCode')
    contract.set_content(content)
    contract.set_extensions(ext)
    contract.set_address(address)
    doc_creation(contract)
    return contract


def is_address(param):
    return str(param[:2]) == '0x'


def get_version(path):
    with open(path, "r+") as f:
        line = f.readline()
        version = str.split(line.replace("pragma solidity ", ""), ';')[0]
    return version


def create_output_dir(path):
    if path[-1:] != '/':
        path += '/'
    if path[:0] != '/':
        path = '/' + path
    path = constants.DEFAULT_DIRECTORY + path
    constants.DEFAULT_OUTPUT = path
    if not os.path.exists(path):
        os.mkdir(path)
        logger.info('Succesfully output path created -> {}'.format(path))
    else:
        logger.warning('The following path already exits {}.'.format(path))


def clean_input_folder():
    path = constants.DEFAULT_DIRECTORY + constants.DEFAULT_INPUT
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            logger.exception('Failed to delete %s. Reason: %s' % (file_path, e))
