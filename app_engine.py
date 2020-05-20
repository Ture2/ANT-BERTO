import os
import time
import dependencies_builder
import constants
import mdcontracts
import docker
import exceptions
import logging

docker_client = docker.APIClient(base_url='unix://var/run/docker.sock')
logger = logging.getLogger(constants.LOGGER_NAME)


# TODO: continuar desarrollando la funcion intermedia que devuelve todas las ejecuciones que hay que realizar
def intermediate_exec(tool, cmd, version):
    if version != '':
        version = int(version.replace(".", ""))
    if tool.get("name") == 'securify' and version <= 510:
        return '', 0
    if tool.get("name") == 'slither' and version <= 430:
        if version <= 430:
            cmd.format(version)
        else:
            return 'Unable to run analysis because solidity pragma code version.', 0

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
    if tool.get("name") == 'madmax':
        executions.append(docker_client.exec_create(tool.get('container'), cmd='cat graph.html',
                                                    workdir='/home/MadMax/',
                                                    privileged=True))

    result = ''
    for exe in executions:
        time_start = time.perf_counter()
        res_iter = docker_client.exec_start(exe, stream=True, demux=True)
        time_end = time.perf_counter()
        for line in res_iter:
            if line[0]:
                result += line[0].decode('utf-8')
            if line[1]:
                result += line[1].decode('utf-8')
            result += '\n'
    return result, (time_end - time_start)


def get_tool():
    for tool in constants.TOOLS_PROPERTIES:
        if tool.get('name') == constants.DEFAULT_TOOL:
            ret = tool
    return ret


def get_version(tool, path):
    if tool.get('ext') == '.sol':
        return dependencies_builder.get_version(path)
    else:
        return ''


def exec_start_gui(file, tools):
    results = []
    for tool in tools:
        path = os.path.join(constants.DEFAULT_DIRECTORY, file)
        if os.path.isfile(path):
            version = get_version(tool, path)
            if tool.get('name') == 'mythril' :
                cmd = tool.get("cmd").format(version, file)
            elif tool.get("name") == 'slither':
                cmd = tool.get("cmd").format(constants.SOLC_SLITHER.format(version), file)
            else:
                cmd = tool.get("cmd").format(file)
            result, time_elapsed = intermediate_exec(tool, cmd, version)
        else:
            result = "{} doesn't allow {} files format".format(tool.get('name'))
            time_elapsed = 0
        results.append(
            {
                tool.get('name') : [
                    {'Resultado': result},
                    {'Tiempo de ejecución': time_elapsed}
                ]
            }
        )
    return results


# Se corren todas las herramientas diferenciando por analisis
def exec_start(files, contract, tools):
    for tool in tools:
        if tool.get('ext') == '.sol':
            file = files[0]
        else:
            file = files[1]
        path = os.path.join(constants.DEFAULT_DIRECTORY + constants.DEFAULT_INPUT, file)
        if os.path.isfile(path):
            version = get_version(tool, path)
            if tool.get('name') == 'mythril' :
                cmd = tool.get("cmd").format(version, file)
            elif tool.get("name") == 'slither':
                cmd = tool.get("cmd").format(constants.SOLC_SLITHER.format(version), file)
            else:
                cmd = tool.get("cmd").format(file)
            logger.debug("Running {} ...".format(tool.get('name')))
            result, time_elapsed = intermediate_exec(tool, cmd, version)
            logger.debug("Completed. Saving results...")
            mdcontracts.insert_result(contract.get_id(), contract.get_address(), tool.get('name'), result, time_elapsed)
            logger.debug("Completed.")
        else:
            mdcontracts.insert_result(contract.get_id(), contract.get_address(), tool.get('name'),
                                      "Contract extension doesn't allow this analysis", '0')


def execute_command(files, contract):
    if constants.DEFAULT_TOOL == 'all':
        exec_start(files, contract, constants.TOOLS_PROPERTIES)
    else:
        exec_start(files, contract, [get_tool()])


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