import os
import argparse
import dependencies_builder
import constants
import mdcontracts
import docker
import exceptions
import logging
import app_engine
from multiprocessing import Process, Lock

from pathlib import Path

# HOST

VERSION = 0.6

docker_client = docker.APIClient(base_url='unix://var/run/docker.sock')
logger = logging.getLogger(constants.LOGGER_NAME)


def analyze(contract):
    try:
        input_sol_file = 'input_' + contract.get_name() + '.sol'
        input_hex_file = 'input_' + contract.get_name() + '.hex'

        files = [input_sol_file, input_hex_file]
        logger.info("Analyzing contract number {}".format(contract.get_id()))
        app_engine.execute_command(files, contract)
        logger.info("{} contract analyze ended.".format(contract.get_id()))
    except:
        logger.exception("Get exception analyzing contract id: {}".format(contract.get_id()))


def test():
    cont = 1
    c_contracts = mdcontracts.get_all_contract_id()
    for contract in c_contracts:
        c = dependencies_builder.create_contract(contract['contract_id'])
        analyze(c)
        if (cont % 50) == 0:
            dependencies_builder.clean_input_folder()
            logger.info("Cleaning inputs files from {}".format(constants.DEFAULT_INPUT))
        cont = cont + 1
    c_contracts.close()


def test_sigle_contract(param, is_address):
    if is_address:
        id = mdcontracts.get_contract_by_address(param)['contract_id']
    else:
        id = mdcontracts.get_contract(param)['contract_id']
    c = dependencies_builder.create_contract(id)
    analyze(c)


def test_range(*args):
    processes = []
    cont = 1
    if len(args) == 2:
        lengh = args[1] - args[0]
    else:
        lengh = 100000 - args[0]
    for i in range(0, lengh):
            if i % 100 == 0:
                update_count = 100 * (i / 100)
                c_contracts = mdcontracts.get_range_contract(args[0] + update_count, args[1] + update_count)
            id = c_contracts.next()['contract_id']
            c = dependencies_builder.create_contract(id)
            analyze(c)
            cont = cont + 1



def define_logger():
    logger = logging.getLogger(constants.LOGGER_NAME)
    logger.setLevel(logging.DEBUG)
    # Log file
    fh = logging.FileHandler(constants.LOG_FILENAME)
    fh.setLevel(logging.DEBUG)
    # Console
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

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
    parser.add_argument("-i", "--identifier", type=str, help="Analyze the given identifier. Choose a number"
                                                                   "or address")
    parser.add_argument("-r", "--range", nargs='+', type=int,
                        help="Analyze the given input number range contracts (both included).")
    parser.add_argument("-fn", "--from-number", type=int,
                        help="Analyze from given input number (included) contract until last one.")
    parser.add_argument("-d", "--directory", type=str, help="Custom output directory.")
    parser.add_argument("-s", "--select-tool", nargs='+', type=str, help="Select one "
                                                              "specific tool. Available tools: solgraph, oyente, "
                                                              "smartcheck, solmet, osiris, vandal, ethir, mythril,"
                                                              "securify, slither, manticore, madmax")

    args = parser.parse_args()
    constants.DEFAULT_DIRECTORY = os.getcwd()

    logger.info('Execution begins')
    logger.info('Current working directory set to ' + constants.DEFAULT_DIRECTORY)

    app_engine.init()

    try:
        if args.select_tool:
            tools = []
            for i in range(0, len(args.select_tool)):
                if str.lower(args.select_tool[i]) in constants.TOOLS:
                    tools.append(str.lower(args.select_tool[i]))
                else:
                    logger.info("{} is not admitted, check whether is not bad written".format(args.select_tool[i]))
            constants.DEFAULT_TOOL = tools
        if args.directory:
            logger.info('Own output directory selected -> ' + args.directory)
            dependencies_builder.create_output_dir(args.directory)
        if args.test and (args.identifier is None and args.range is None and args.from_number is None):
            logger.info('Default test selected')
            test()
        elif args.identifier:
            is_address = dependencies_builder.is_address(args.identifier)
            if is_address:
                logger.info('Unique contract test selected. Address {}'.format(args.identifier))
            else:
                logger.info('Unique contract test selected. Contract number {}'.format(args.identifier))
            test_sigle_contract(args.identifier, is_address)
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


if __name__ == "__main__":
    main()
