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

VERSION = 0.2

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
            logger.WARNING("The awaiten docker" + container + "doesn't exits")

# src: str to source file directory
# dst: str to destiny inside container
# cname: target container name

def execute_command(type, file, output_file, parent_dir):
    if os.path.isfile(constants.PATH_TO_MAIN_DIRECTORY + constants.PATH_TO_INPUT + file):
        if type == 1:
            for tool in constants.HEX_TOOLS:
                cmd = tool.get("cmd").format(file)
                execution = docker_client.exec_create(tool.get('container'), cmd=cmd, workdir=tool.get('workdir'),
                                                      privileged=True)
                res_iter = docker_client.exec_start(execution, stream=True, demux=True)
                result = ""
                for line in res_iter:
                    result += line[1].decode('utf-8')
                dependencies_builder.save_results(result, output_file, tool.get('name'), parent_dir)
        elif type == 0:
            for tool in constants.SOL_TOOLS:
                cmd = tool.get("cmd").format(file)
                execution = docker_client.exec_create(tool.get('container'), cmd=cmd, workdir=tool.get('workdir'),
                                                      privileged=True)
                res_iter = docker_client.exec_start(execution, stream=True, demux=True)
                result = ""
                for line in res_iter:
                    result += line[0].decode('utf-8')
                dependencies_builder.save_results(result, output_file, tool.get('name'), parent_dir)

def copy_file_to_container(src, dst, cname):
    os.chdir(os.path.dirname(src))
    srcname = os.path.basename(src)
    file = src + '.tar'
    tar = tarfile.open(file, 'w')
    try:
        tar.add(srcname)
    finally:
        tar.close()
        data = open(file, 'rb').read()
        docker_client.put_archive(cname, os.path.dirname(dst), data)
        os.remove(file)

def analyze(contract):
    #try:
        input_sol_file = 'input_' + contract.get_name() + '.sol'
        input_hex_file = 'input_' + contract.get_name() + '.hex'
        current_time = current_milli_time()

        parent_dir = constants.PATH_TO_MAIN_DIRECTORY + constants.PATH_TO_OUTPUT + '/{}'.format(current_time)
        os.mkdir(parent_dir)

        # TODO: seleccionar archivo
        # output_file = '{}.txt'.format(current_milli_time())
        output_file = 'output_{}.txt'.format(contract.get_name())

        execute_command(0, input_sol_file, output_file, parent_dir)
        execute_command(1, input_hex_file, output_file, parent_dir)

        #logger.info('Contract {} successfully analyzed', contract.get_name())
    #except:
     #   logger.exception('Exeception analysing a contract')



def test():
    c_contracts = mdcontracts.get_all_contract_id()
    for contract in c_contracts:
        for tool in constants.TOOLS:
            tool_factory.analyze(tool, contract['contract_id'])


def test_sigle_contract(id):
    contract = mdcontracts.get_contract(id)
    c = dependencies_builder.create_contract(contract['contract_id'])
    analyze(c)


def test_range(*args):
    if len(args) == 2:
        c_contracts = mdcontracts.get_range_contract(args[0], args[1])
    else:
        c_contracts = mdcontracts.get_from_number(args[0])
    for contract in c_contracts:
        c = dependencies_builder.create_contract(contract['contract_id'])
        analyze(c)

def define_logger():
    logger = logging.getLogger(constants.LOGGER_NAME)
    logger.setLevel(logging.DEBUG)
    #Log file
    fh = logging.FileHandler(constants.LOG_FILENAME)
    fh.setLevel(logging.DEBUG)
    #Console
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    formater = logging.Formatter('%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')

    ch.setFormatter(formater)
    fh.setFormatter(formater)
    logger.addHandler(fh)
    logger.addHandler(ch)


def main():
    define_logger()
    info = []
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", help="Launch default test.",
                        action="store_true")
    parser.add_argument("-uc", "--unique-contract", type=int, help="Analyze the given input contract.")
    parser.add_argument("-r", "--range", nargs='+', type=int, help="Analyze the given input number range contracts.")
    parser.add_argument("-fn", "--from-number", type=int,
                        help="Analyze from given input number contract until last one.")
    parser.add_argument("-d", "--directory", type=str, help="Custom output directory.")

    args = parser.parse_args()
    constants.PATH_TO_MAIN_DIRECTORY = os.getcwd() + '/'

    logger.info('Execution begins')
    logger.info('Current working directory set to ' + constants.PATH_TO_MAIN_DIRECTORY)

    init()

    try:
        if args.directory:
            logger.info('Own output directory selected -> ' + args.directory)
            dependencies_builder.create_output_dir(args.directory)
            constants.PATH_TO_OUTPUT = args.directory
        if args.test and (args.unique_contract is None and args.range is None and args.from_number is None):
            logger.info('Default test selected')
            test()
        elif args.unique_contract:
            logger.info('Unique contract test selected. Contract number {}\n'.format(args.unique_contract))
            test_sigle_contract(args.unique_contract)
        elif args.range:
            if args.range[0] < 0 or args.range[1] < 0:
                raise exceptions.InputError('parser', 'The range can not be less than 0')
            elif (isinstance(args.range[0], int) or isinstance(args.range[1], int)) is not True:
                raise exceptions.InputError('parser', 'The range must be a number')
            else:
                logger.info('Range test selected. Range: {} - {}\n'.format(args.range[0], args.range[1]))
                test_range(args.range[0], args.range[1])
        elif args.from_number:
            if args.from_number < 0 or isinstance(args.from_number, int) is not True:
                raise exceptions.InputError('parser', 'The range must be a number and higher than 0')
            else:
                logger.info('Range from number selected. Range: {} - end\n'.format(args.from_number))
                test_range(args.from_number)
        else:
            raise exceptions.InputError('You must select a value')
    except:
        logger.exception('Got exception parsing arguments')
    finally:
        dependencies_builder.create_settings_file(info)


if __name__ == "__main__":
    main()
