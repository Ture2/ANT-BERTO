import os
import time
import argparse
import dependencies_builder
import constants
import mdcontracts
import docker
import exceptions
import logging

from pathlib import Path

# HOST

VERSION = 0.3

docker_client = docker.APIClient(base_url='unix://var/run/docker.sock')
current_milli_time = lambda: int(round(time.time() * 1000))
logger = logging.getLogger(constants.LOGGER_NAME)


def init():
    containers_running = docker_client.containers(all=True)
    final_name_list = list()

    for c in containers_running:
        name_list = c['Names']
        if len(name_list) > 0:
            final_name_list += name_list

    for container in constants.CONTAINERS:
        try:
            docker_client.start(container)
        except:
            logger.WARNING("The awaiten docker {} doesn't exits".format(container))


# TODO: continuar desarrollando la funcion intermedia que devuelve todas las ejecuciones que hay que realizar
def intermediate_exec(tool, cmd):
    executions = [docker_client.exec_create(tool.get('container'), cmd=cmd, workdir=tool.get('workdir'),
                                            privileged=True)]
    if tool.get("name") == 'solmet':
        executions.append(docker_client.exec_create(tool.get('container'), cmd='cat output.csv',
                                                    workdir=tool.get('workdir'),
                                                    privileged=True))
    if tool.get("name") == 'ethir':
        executions.append(docker_client.exec_create(tool.get('container'), cmd='cat rbr.rbr',
                                                    workdir='/tmp/costabs/',
                                                    privileged=True))
    result = ''
    for exe in executions:
        res_iter = docker_client.exec_start(exe, stream=True, demux=True)
        for line in res_iter:
            if line[0]:
                result += line[0].decode('utf-8')
            if line[1]:
                result += line[1].decode('utf-8')
            result += '\n'
    return result


def get_tool():
    for tool in constants.TOOLS_PROPERTIES:
        if tool.get('name') == constants.DEFAULT_TOOL:
            ret = tool
    return ret


# Se corren todas las herramientas diferenciando por analisis
def exec_start(files, id, tools):
    for tool in tools:
        if tool.get('ext') == '.sol':
            file = files[0]
        else:
            file = files[1]
        if os.path.isfile(constants.DEFAULT_DIRECTORY + constants.DEFAULT_INPUT + file):
            cmd = tool.get("cmd").format(file)
            logger.info("Running {} ...".format(tool.get('name')))
            result = intermediate_exec(tool, cmd)
            logger.info("Completed. Saving results...")
            mdcontracts.insert_result(id, tool.get('name'),result)
            logger.info("Completed.")


def execute_command(files, id):
    if constants.DEFAULT_TOOL == 'all':
        exec_start(files, id, constants.TOOLS_PROPERTIES)
    else:
        exec_start(files, id, [get_tool()])


def analyze(contract):
    input_sol_file = 'input_' + contract.get_name() + '.sol'
    input_hex_file = 'input_' + contract.get_name() + '.hex'

    files = [input_sol_file, input_hex_file]
    logger.info("Analyzing contract number {}".format(contract.get_id()))
    execute_command(files, contract.get_id())
    logger.info("{} contract analyze ended.".format(contract.get_id()))


def test():
    cont = 1
    c_contracts = mdcontracts.get_all_contract_id()
    for contract in c_contracts:
        c = dependencies_builder.create_contract(contract['contract_id'])
        analyze(c)
        if (cont % 50 ) == 0:
            dependencies_builder.clean_input_folder()
            logger.info("Cleaning inputs files from {}".format(constants.DEFAULT_INPUT))
        cont = cont + 1
    c_contracts.close()


def test_sigle_contract(id):
    contract = mdcontracts.get_contract(id)
    c = dependencies_builder.create_contract(contract['contract_id'])
    analyze(c)


def test_range(*args):
    cont = 1
    if len(args) == 2:
        c_contracts = mdcontracts.get_range_contract(args[0], args[1])
    else:
        c_contracts = mdcontracts.get_from_number(args[0])
    for contract in c_contracts:
        c = dependencies_builder.create_contract(contract['contract_id'])
        analyze(c)
        if (cont % 50 ) == 0:
            dependencies_builder.clean_input_folder()
            logger.info("Cleaning inputs files from {}".format(constants.DEFAULT_INPUT))
        cont = cont + 1
    c_contracts.close()


def define_logger():
    logger = logging.getLogger(constants.LOGGER_NAME)
    logger.setLevel(logging.DEBUG)
    # Log file
    fh = logging.FileHandler(constants.LOG_FILENAME)
    fh.setLevel(logging.DEBUG)
    # Console
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    formater = logging.Formatter('%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')

    ch.setFormatter(formater)
    fh.setFormatter(formater)
    logger.addHandler(fh)
    logger.addHandler(ch)


# TODO: poner la variables -d para añadir una bbdd o -c para setear el nombre de la coleccion
# TODO: modificar la lista para poner valores por defecto
def main():
    define_logger()
    info = []
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", help="Launch default test.",
                        action="store_true")
    parser.add_argument("-uc", "--unique-contract", type=int, help="Analyze the given input contract.")
    parser.add_argument("-r", "--range", nargs='+', type=int,
                        help="Analyze the given input number range contracts (both included).")
    parser.add_argument("-fn", "--from-number", type=int,
                        help="Analyze from given input number (included) contract until last one.")
    parser.add_argument("-d", "--directory", type=str, help="Custom output directory.")
    parser.add_argument("-l", "--list", type=str,
                        help="Available tools: solgraph, oyente, solmet, smartcheck, osiris, oyente.")
    parser.add_argument("-s", "--select-tool", type=str, help="Select one specific tool.")

    args = parser.parse_args()
    constants.DEFAULT_DIRECTORY = os.getcwd() + '/'

    logger.info('Execution begins')
    logger.info('Current working directory set to ' + constants.DEFAULT_DIRECTORY)

    init()

    try:
        if args.list:
            print("Available tools\nSolgraph\nOyente\nSolmet\nSmartcheck\nOsiris\nVandal\n")
        if args.select_tool and str.lower(args.select_tool) in constants.TOOLS:
            constants.DEFAULT_TOOL = str.lower(args.select_tool)
        if args.directory:
            logger.info('Own output directory selected -> ' + args.directory)
            dependencies_builder.create_output_dir(args.directory)
            constants.DEFAULT_OUTPUT = args.directory
        if args.test and (args.unique_contract is None and args.range is None and args.from_number is None):
            logger.info('Default test selected')
            test()
        elif args.unique_contract:
            logger.info('Unique contract test selected. Contract number {}'.format(args.unique_contract))
            test_sigle_contract(args.unique_contract)
        elif args.range:
            if args.range[0] < 0 or args.range[1] < 0:
                raise exceptions.InputError('parser', 'The range can not be less than 0')
            elif (isinstance(args.range[0], int) or isinstance(args.range[1], int)) is not True:
                raise exceptions.InputError('parser', 'The range must be a number')
            else:
                logger.info('Range test selected. Range: {} - {}'.format(args.range[0], args.range[1]))
                test_range(args.range[0], args.range[1])
        elif args.from_number:
            if args.from_number < 0 or isinstance(args.from_number, int) is not True:
                raise exceptions.InputError('parser', 'The range must be a number and higher than 0')
            else:
                logger.info('Range from number selected. Range: {} - end'.format(args.from_number))
                test_range(args.from_number)
        else:
            raise exceptions.InputError('You must select a value')
    except:
        logger.exception('Got exception parsing arguments')
    finally:
        dependencies_builder.create_settings_file(info)


if __name__ == "__main__":
    main()
