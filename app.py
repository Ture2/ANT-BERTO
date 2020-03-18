import os
import time
import argparse
import dependencies_builder
import constants
import mdcontracts
import docker

# HOST

VERSION = 0.2

docker_client = docker.APIClient(base_url='unix://var/run/docker.sock')
current_milli_time = lambda: int(round(time.time() * 1000))


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
            print ("El docker " + container + " no existe")


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
                    result += line[1]
                dependencies_builder.save_results(result, output_file, tool.get('name'), parent_dir)
        elif type == 0:
            for tool in constants.SOL_TOOLS:
                cmd = tool.get("cmd").format(file)
                execution = docker_client.exec_create(tool.get('container'), cmd=cmd, workdir=tool.get('workdir'),
                                                      privileged=True)
                res_iter = docker_client.exec_start(execution, stream=True, demux=True)
                result = ""
                for line in res_iter:
                    result += line[0]
                dependencies_builder.save_results(result, output_file, tool.get('name'), parent_dir)


def analyze(contract):
    input_sol_file = 'input_' + contract.get_name() + '.sol'
    input_hex_file = 'input_' + contract.get_name() + '.hex'
    current_time  = current_milli_time()

    parent_dir = constants.PATH_TO_MAIN_DIRECTORY + constants.PATH_TO_OUTPUT + '/{}'.format(current_time)
    os.mkdir(parent_dir)

    # TODO: seleccionar archivo
    #output_file = '{}.txt'.format(current_milli_time())
    output_file = 'output_{}.txt'.format(contract.get_name())

    execute_command(0, input_sol_file, output_file, parent_dir)
    execute_command(1, input_hex_file, output_file, parent_dir)


def test():
    c_contracts = mdcontracts.get_all_contract_id()
    for contract in c_contracts:
        c = dependencies_builder.create_contract(contract['contract_id'])
        analyze(c)


def test_sigle_contract(id):
    contract = mdcontracts.get_contract(id)
    c = dependencies_builder.create_contract(contract['contract_id'])
    analyze(c)


def main():
    info = []
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", help="Launch default test.",
                        action="store_true")
    parser.add_argument("-uc", "--unique-contract", type=int, help="Analyze the given input contract.")
    parser.add_argument("-r", "--range", nargs='+', type=list, help="Analyze the given input number range contracts.")
    parser.add_argument("-fn", "--from-number", type=int,
                        help="Analyze from given input number contract until last one.")
    parser.add_argument("-d", "--directory", type=str, help="Custom output directory.")

    args = parser.parse_args()
    init()

    args.directory = "../tmp"

    try:
        if args.directory:
            info.append("Own output directory selected: \n")
            dependencies_builder.create_output_dir(args.directory)
            constants.PATH_TO_OUTPUT = args.directory

        if args.test:
            info.append("Default test\n")
            test()
        elif args.unique_test:
            info.append("Unique contract test selected. Contract number {}\n".format(args.unique_test))
            test_sigle_contract(args.unique_test)
        elif args.range:
            info.append("Range test selected. Range: {} - {}\n".format(args.range[0], args.range[1]))
            # TODO: implementar rango
            print("x")
        elif args.from_number:
            info.append("Range from number selected. Range: {} - end\n".format(args.from_number))
            # TODO: implementar desde un numero
            print("x")
    finally:
        dependencies_builder.create_settings_file(info)


if __name__ == "__main__":
    main()
