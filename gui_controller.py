import os

import app_engine
import dependencies_builder
import constants
import contract_downloader
from shutil import copyfile


def start_analysis(files, tools, is_local_analysis, address):
    app_engine.init()
    if not constants.output_created:
        dependencies_builder.create_output_dir(constants.DEFAULT_OUTPUT)
        constants.output_created = True
    if is_local_analysis:
        local_analysis(files, tools)
    else:
        return address_analysis(address, tools)


def local_analysis(files_path, tools):
    files = []
    results = []

    for file in files_path:
        ext = str(file).split('.')[1:][0]
        filename = str(file).split('/')[-1]
        files.clear()
        if ext == 'sol':
            files.append(filename)
            files.append('nofile')
        else:
            files.append('nofile')
            files.append(filename)
        path = str(file).replace('/' + filename, '')
        if constants.DEFAULT_DIRECTORY != path:
            dst = os.path.join(constants.DEFAULT_DIRECTORY + constants.DEFAULT_INPUT, filename)
            copyfile(file, dst)
        results.append(app_engine.exec_start_gui(files, get_tools_selected(tools)))
    code = '200'
    return results, code


def address_analysis(address, tools):
    data = contract_downloader.walk_contracts_dir(address)
    contract = dependencies_builder.create_contract_from_address(address, data)
    input_hex_file = 'input_' + contract.get_name() + '.hex'
    if len(contract.get_extensions()) > 1:
        input_sol_file = 'input_' + contract.get_name() + '.sol'
    else:
        input_sol_file = 'nofile'
    files = [input_sol_file, input_hex_file]
    results = app_engine.exec_start_gui(files, get_tools_selected(tools))
    code = '200'
    return results, code


def get_tools_selected(tools):
    temp = []
    for i in range(0, len(tools)):
        if tools[i].get():
            temp.append(constants.TOOLS_PROPERTIES[i])
    return temp
