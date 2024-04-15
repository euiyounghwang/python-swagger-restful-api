
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

import jsondiff
import requests, json
import argparse
from elasticsearch import Elasticsearch, exceptions
from datetime import datetime
from threading import Thread
from service.es_search_handler import SearchAPIHandler
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# https://www.tutorialspoint.com/how-to-compare-json-objects-regardless-of-order-in-python

response = {}


def json_diff_test():
    ''' mapping compare between two jsons'''

    def response_payload_transform(diff):
        if not diff:
            response.update({'diff' : 'Same'})
        else:
            response.update({'diff' : 'Different', 'result' : diff})

        return response
    
    # JSON objects to compare
    # json_obj1 = '{"name": "John", "age": 30, "city": "New York"}'
    # json_obj2 = '{"name": "John1", "age": 30, "city": "New York"}'
    # json_obj2 = '{"age": 30, "city": "New York", "name": "John"}'

    # json_obj1 = "{ \
    #     'employee': {  \
    #         'name':       'sonoo',  \
    #         'salary':      56000,   \
    #         'married':    true  \
    #     }  \
    # }"
    # json_obj2 =  "{ \
    #     'employee': {  \
    #         'name':       'sonoo',   \
    #         'salary':      56000,   \
    #         'married':    true  \
    #     }  \
    # }"


    json_obj1 = { 
        'employee': {  
            'name':       'sonoo',  
            'salary':      56000,   
            'married':    True  
        }  
    }
    json_obj2 =  { 
        'employee': {  
            'name':       'sonoo1',    
            'salary':      56000,   
            'married':    True  
        },
        "test" : 1  
    }


    """
    json_obj1 = {
        "properties": {
            "ACTUALDELIVERYDATE": {
                "type": "date",
                "format": "MM/dd/yyyy hh:mm:ss"
            },
            "title": {
                "type": "keyword"
            },
            "content": {
                "type": "text",
                "fields": {
                "keyword": {
                    "type": "keyword",
                    "ignore_above": 256
                }
                }
            }
        }
    }

    json_obj2 = {
        "properties": {
            "ACTUALDELIVERYDATE": {
                "type": "date",
                "format": "MM/dd/yyyy hh:mm:ss"
            },
             "content": {
                 "fields": {
                "keyword": {
                    "type": "keyword",
                    "ignore_above": 256
                 }
                },
                "type": "text"
            },
            "title": {
                "type": "keyword"
            }
        }
    }

    """

    # json_obj2 = {
    #     "properties": {
    #         "ACTUALDELIVERYDATE": {
    #             "type": "date",
    #             "format": "MM/dd/yyyy hh:mm:ss"
    #         },
    #         "title": {
    #             "type": "text"
    #         },
    #         "content": {
    #             "type": "text",
    #             "fields": {
    #             "keyword": {
    #                 "type": "keyword",
    #                 "ignore_above": 2561
    #             }
    #             }
    #         }
    #     }
    # }

    # Compare JSON objects using jsondiff
    diff = jsondiff.diff(json_obj1, json_obj2, marshal=True, syntax="symmetric")
    # from opslib.icsutils.jsondiff import Comparator
    # engine = Comparator(json_obj1, json_obj2)
    # diff = engine.compare_dicts()

    # Print the difference between the two JSON objects
    # print(json.dumps(diff, indent=2))
    print(json.dumps(response_payload_transform(diff), indent=2))
    

def read_server(server_file):
    server_list_dict = {}
    with open(server_file) as data_file:
        for line in data_file:
            line = line.strip().split("\t")
            # logging.info(f"{line}")
            server_list_dict.update({str(line[len(line)-1]).lower() : line[0]})
    return server_list_dict


def lookup_env(server_list_dict, lookup_str):
    ''' lookup environment from server_list_dict '''
    if ":" not in lookup_str:
        return lookup_str
    return str(server_list_dict.get(lookup_str.replace('http://','').split(":")[0], ''))


def export_file(_source_host, _target_host, server_list_dict, diff_index):
    ''' export to file '''
    with open("./scripts/export_mapping_diff", "w") as f:
        for item in diff_index:
            # print(server_list_dict)
            f.write(lookup_env(server_list_dict, _source_host) + '\t' + 
                    str(_source_host) + '\t' + 
                    lookup_env(server_list_dict, _target_host) + '\t' + 
                    str(_target_host) + '\t' + str(item) + '\n')


def work(_index_name, _source_host, _target_host, server_list_dict):
    print(_index_name, _source_host, _target_host)

    SearchOmniHandlerInject = SearchAPIHandler(logging)

    ''' get index list from source cluster'''
    response = SearchOmniHandlerInject.get_index_lists(_source_host)
    # logging.info(response)
    # logging.info(response.keys())
    real_index_lists = [each_index for each_index in response.keys() if '.' not in each_index]
    # logging.info(real_index_lists)

    ''' compare the mapping between clusters'''
    failure_index, diff_index = [], []
    for each_index in real_index_lists:
        diff = SearchOmniHandlerInject.get_index_mapping_compare(each_index, _source_host, _target_host)
        if isinstance(diff, dict):
            print(type(diff), json.dumps(diff, indent=2))
            if diff['diff'] == 'Different mapping':
                # diff_index.append({'source_host' : _source_host, 'target_host' : _target_host, each_index : diff['result']})
                # print(diff.get("result", {}), type(diff.get("result", {})))
                diff_index.append(diff.get("result", {}))

        else:
            failure_index.append(each_index)
           
    # response = compare_mapping(_es_client_source, _es_client_target, _index_name)
    # print(json.dumps(response, indent=2))
    logging.info(f"failure index : {failure_index}")
    logging.info(f"diff_index : {json.dumps(diff_index, indent=2)}")

    # --
    # write to file
    export_file(_source_host, _target_host, server_list_dict, diff_index)


if __name__ == "__main__":
    '''
    python ./scripts/mapping_diff_script.py --test true --es http://localhost:9292/ --ts http://localhost:9292/
    python ./scripts/mapping_diff_script.py --es http://localhost:9292/ --ts http://localhost:9292/
    '''
    parser = argparse.ArgumentParser(description="Script that might allow us to use it as an application of ES mapping compares")
    parser.add_argument('-a', '--test', dest='test', default="false", help='test diff logic')
    parser.add_argument('-e', '--es', dest='es', default="http://localhost:9209", help='host source')
    parser.add_argument('-t', '--ts', dest='ts', default="http://localhost:9292", help='host target')
    parser.add_argument('-s', '--server_info', dest='server_info', default="C://Users//euiyoung.hwang/", help='server_info config file')
    parser.add_argument('-i', '--index', dest='index', default="test", help='index name')
    args = parser.parse_args()

    if args.test:
        is_test = args.test

    is_test = json.loads(is_test.lower())
    
    if args.es:
        _source_host = args.es
        
    if args.ts:
        _target_host = args.ts

    if args.index:
        _index_name = args.index

    if args.server_info:
        _server_list_file_path = args.server_info


    if is_test:
        json_diff_test()
    else:
        logging.info('-- diff --')

        # server_file = "C://Users//euiyoung.hwang/server_info_columns"
        server_list_dict = read_server(_server_list_file_path + "server_info_columns")
        # logging.info(server_list_dict)

        logging.info(f"{_source_host} -> {_target_host}")
    
        th1 = Thread(target=work, args=(_index_name, _source_host, _target_host, server_list_dict))
        th1.start()
        th1.join()
        
    
