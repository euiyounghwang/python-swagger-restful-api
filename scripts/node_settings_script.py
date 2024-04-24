
import yaml
from deepdiff import DeepDiff
import json
import argparse
import logging
import os, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from service.es_search_handler import SearchAPIHandler

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def read_server(server_file):
    server_list_dict = {}
    with open(server_file) as data_file:
        for line in data_file:
            line = line.strip().split("\t")
            # logging.info(f"{line}")
            server_list_dict.update({str(line[len(line)-1]).lower() : line[0]})
    return server_list_dict



if __name__ == '__main__':
    '''
    # python ./scripts/node_settings_script.py --source http://localhost:9200
    python ./scripts/node_settings_script.py
    '''
    parser = argparse.ArgumentParser(description="Script that might allow us to investigate the heapspace of node in the cluster")
    # parser.add_argument('-s', '--source', dest='source', default="http://localhost:9200", help='source cluster')
    parser.add_argument('-f', '--server_info', dest='server_info', default="C://Users//euiyoung.hwang/", help='server_info config file')
    args = parser.parse_args()

    # if args.source:
    #     source = args.source

    if args.server_info:
        _server_list_file_path = args.server_info

    # server_list_dict = read_server(_server_list_file_path + "server_info_columns_test")
    server_list_dict = read_server(_server_list_file_path + "server_info_columns")
    logging.info(server_list_dict)

    SearchOmniHandlerInject = SearchAPIHandler(logging)

    results_json = {}
    loop = 1
    for k, v in server_list_dict.items():
        response = SearchOmniHandlerInject.get_heapspace_each(k)
        print("{} : Current Host {} -> {}".format(str(loop).zfill(3), k, response))
        if isinstance(response, dict):
            host = list(response.keys())[0]
            for sub_key, sub_value in response[host].items():
                # print(sub_key, sub_value)
                if sub_key == 'heap.max':
                    if sub_value in results_json.keys():
                        results_json[sub_value].append(host)
                    else:
                        results_json.update({sub_value : [host]})
        loop += 1
    
    logging.info(json.dumps(results_json, indent=2))
