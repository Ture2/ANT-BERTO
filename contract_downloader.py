import concurrent.futures
import json
import urllib.request

ETHERSCAN_APIKEY = '54N95X4Y7SKUVADKINYY98MTF192MD9PEG'
PAUSE = 120

def load_url(url):
    with urllib.request.urlopen(url) as conn:
        return conn.read()


def walk_contracts_dir(dir, solidity=True, bytecode=True):
    contract_error = False
    log = {}

    etherscan_api_urls = []
    etherscan_api_url_to_label = {}
    etherscan_api_responses = {}

    if solidity:
        url='https://api.etherscan.io/api?module=contract&action=getsourcecode&address='+dir+'&apikey='+ETHERSCAN_APIKEY
        etherscan_api_urls.append(url)
        etherscan_api_url_to_label[url] = 'solidity'

    if bytecode:
        url = 'https://api.etherscan.io/api?module=proxy&action=eth_getCode&address='+dir+'&apikey='+ETHERSCAN_APIKEY
        etherscan_api_urls.append(url)
        etherscan_api_url_to_label[url] = 'bytecode'

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(load_url, url): url for url in etherscan_api_urls}

        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]

            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))
            else:
                etherscan_api_responses[etherscan_api_url_to_label[url]] = data

    if etherscan_api_responses['solidity']:
        res_json=json.loads(etherscan_api_responses['solidity'])

        if res_json['status'] == '1':
            if len(res_json['result'])>0 and res_json['result'][0]['SourceCode']:
                solidity_code = res_json['result']
                log.update({'sc': '(SOLIDITY OK)'})
            else:
                log.update({'sc': '(SOLIDITY NO)'})
                solidity_code = ""
        else:
            contract_error = True
    else:
        contract_error = True

    if etherscan_api_responses['bytecode']:
        res_json = json.loads(etherscan_api_responses['bytecode'])
        if res_json['result'] != '0x':
            bytecode = res_json['result']
            log.update({'bc': '(BYTECODE OK)'})
        else:
            log.update({'bc': '(BYTECODE NO)'})
    else:
        contract_error = True

    return [solidity_code, bytecode, log, contract_error]

