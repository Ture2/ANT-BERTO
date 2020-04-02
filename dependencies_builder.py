import constants
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
        path_to_input_file = constants.PATH_TO_MAIN_DIRECTORY + constants.PATH_TO_INPUT + input_file
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


# Given and output file and parent directory the method save the results
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
