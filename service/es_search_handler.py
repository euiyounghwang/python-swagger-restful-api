import json
from elasticsearch import Elasticsearch, exceptions
import elasticsearch.exceptions
from service.status_handler import (StatusHanlder, StatusException)
from service.es_util import response_payload_transform, source_hosts_with_http, generate_es_host
from fastapi.responses import JSONResponse
from fastapi import Depends
import jsondiff
import requests
import os
import warnings
warnings.filterwarnings("ignore")

class SearchCommonHandler(object):

    @staticmethod
    def get_headers():
        ''' Elasticsearch Header '''
        return {
            'Content-type': 'application/json', 
            'Authorization' : '{}'.format(os.getenv('BASIC_AUTH')),
            'Connection': 'close'
        }
    

class SearchOmniHandler(object):
    
    def __init__(self, logger, hosts):
        self.logger = logger
        self.hosts = hosts
        
    
    async def search(self, query_builder, oas_query=None):
        ''' Search with QuerBuilder '''
        if not oas_query:
            oas_query = {}

        
        es_query = query_builder.build_query(oas_query)
        self.logger.info('query_builder_build_query:oas_query - {}'.format(json.dumps(es_query, indent=2)))

        source_hosts = source_hosts_with_http(oas_query.get("source_es_host").split(","))
        self.logger.info('source_hosts - {}'.format(json.dumps(source_hosts, indent=2)))

        try:
            if oas_query.get("source_es_host"):
                source_host = oas_query.get("source_es_host")
                """
                for source_host in source_hosts:
                    try:
                        self.es_client = Elasticsearch(hosts=source_host,
                                            headers=SearchCommonHandler.get_headers(),
                                            verify_certs=False,
                                            max_retries=0,
                                            timeout=5)
                        
                        es_result = self.es_client.search(
                            index = oas_query.get("index_name", ""),
                            body=es_query,
                        )

                    except Exception as e:
                        continue

                    else:
                        #This is when code on try is done OK!
                        break
                """
                self.es_client = Elasticsearch(hosts=source_host,
                                            headers=SearchCommonHandler.get_headers(),
                                            # http_auth=('test', 'test'),
                                            verify_certs=False,
                                            max_retries=0,
                                            timeout=5)
                        
                es_result = self.es_client.search(
                           index = oas_query.get("index_name", ""),
                            body=es_query,
                            )

                    
        # This is what Elasticserch throws as an exception if the point in time context has expired
        except Exception as e:
           return StatusException.raise_exception(str(e))

        es_hits = es_result["hits"]
        '''
        results = [es_hit for es_hit in es_hits["hits"]]
        # print(results)
        '''
        return es_hits
    


class SearchAPIHandler(object):
    
    def __init__(self, logger, hosts):
        self.logger = logger
        self.hosts = hosts
        self.all_same_mapping =  []
        self.response = {}

    
    def get_es_health(self, es_host):
        ''' Get the information of cluster's health from the specific cluster'''
        error_msg = ""
        try:
            """
            self.logger.info(es_host)
            # es_hosts = generate_es_host(self.hosts, es_host)
            es_hosts = es_host
            self.logger.info(es_hosts)
            for es_host in [es_hosts]:
                try:
                    self.es_client = Elasticsearch(hosts=es_host,
                                headers=SearchCommonHandler.get_headers(),
                                verify_certs=False,
                                max_retries=0,
                                timeout=5)
                    # print(type(self.es_client.cluster.health()))
                    return self.es_client.cluster.health()
                except Exception as e:
                        error_msg = e
                        continue
                else:
                    #This is when code on try is done OK!
                    break
            return StatusException.raise_exception(error_msg)
            """
            self.es_client = Elasticsearch(hosts=es_host,
                                headers=SearchCommonHandler.get_headers(),
                                verify_certs=False,
                                max_retries=0,
                                timeout=5)
            # print(type(self.es_client.cluster.health()))
            return self.es_client.cluster.health()
        except Exception as e:
            return StatusException.raise_exception(e)
        finally:
            self.es_client.close()
    

    async def get_index_by_id(self, es_host, index_name, id):
        ''' Get index id from the specific cluster'''
        try:
            self.es_client = Elasticsearch(hosts=es_host,
                                headers=SearchCommonHandler.get_headers(),
                                verify_certs=False,
                                max_retries=0,
                                timeout=5)
            
            # -- It can't be used get method on ES5 and higher thatn ES5 simultaneously
            # raw_data = self.es_client.get(index=index_name, id=id)
            raw_data = self.es_client.search(index=index_name, body={"query": {"match": {"_id": id}}})
            self.logger.info(f"get_index_by_id - {json.dumps(raw_data, indent=2)}")

            return raw_data
        except Exception as e:
            return StatusException.raise_exception(e)
        finally:
            self.es_client.close()


    def get_index_lists(self, es_host):
        ''' Get index lists from the specific cluster'''
        try:
            self.es_client = Elasticsearch(hosts=es_host,
                                headers=SearchCommonHandler.get_headers(),
                                verify_certs=False,
                                max_retries=0,
                                timeout=5)
            raw_data = self.es_client.indices.get_alias("*")
            self.logger.info(f"get_index_lists - {json.dumps(raw_data, indent=2)}")

            return raw_data
        except Exception as e:
            return StatusException.raise_exception(e)
        finally:
            self.es_client.close()
                

    def get_index_mapping(self, es_host, index_name):
        ''' Get index mapping from the specific cluster'''
        try:
            self.es_client = Elasticsearch(hosts=es_host,
                                headers=SearchCommonHandler.get_headers(),
                                verify_certs=False,
                                max_retries=0,
                                timeout=5)
            raw_data = self.es_client.indices.get_mapping(index_name)
            self.logger.info(f"index mapping - {json.dumps(raw_data, indent=2)}")

            return raw_data
        except Exception as e:
            return StatusException.raise_exception(e)
        finally:
            self.es_client.close()

    
    async def get_index_mapping_compare_all(self, source, target):
        ''' get index list from source cluster'''
        response = self.get_index_lists(source)
        # logging.info(response)
        # logging.info(response.keys())
        real_index_lists = [each_index for each_index in response.keys() if '.' not in each_index]
        # logging.info(real_index_lists)

        ''' compare the mapping between clusters'''
        diff_index = []
        for each_index in real_index_lists:
            diff = self.get_index_mapping_compare(each_index, source, target)
            if isinstance(diff, dict):
                print(type(diff), json.dumps(diff, indent=2))
                if diff['diff'] == 'Different mapping':
                    # diff_index.append({'source_host' : _source_host, 'target_host' : _target_host, each_index : diff['result']})
                    # print(diff.get("result", {}), type(diff.get("result", {})))
                    diff_index.append(diff.get("result", {}))

        return diff_index
        


    def get_index_mapping_compare(self, index_name, source, target):
        ''' Compare index mapping between two clusters'''
        index_name = str(index_name).strip()
        try:
            ''' There should be an option to disable certificate verification during SSL connection. It will simplify developing and debugging process. '''
            self.es_client_source = Elasticsearch(hosts=source,
                                headers=SearchCommonHandler.get_headers(),
                                verify_certs=False,
                                max_retries=0,
                                timeout=5)
            self.es_client_target = Elasticsearch(hosts=target,
                                headers=SearchCommonHandler.get_headers(),
                                verify_certs=False,
                                max_retries=0,
                                timeout=5)
            
            try:
                source_mapping = self.es_client_source.indices.get_mapping(index=index_name)
                self.logger.info(source_mapping)
            except Exception as e:
                # return {"error" : 'Index [{}]was not found in {} [Source:Elasticsearch Cluster]'.format(index_name, source)}
                return StatusException.raise_exception('Index [{}]was not found in {} [Source:Elasticsearch Cluster]'.format(index_name, source))

            try:
                target_mapping = self.es_client_target.indices.get_mapping(index=index_name)
            except exceptions.NotFoundError:
                # return {"error" : 'Index [{}]was not found in {} [Target:Elasticsearch Cluster]'.format(index_name, target)}
                return StatusException.raise_exception('Index [{}]was not found in {} [Target:Elasticsearch Cluster]'.format(index_name, target))
            
            # Compare JSON objects using jsondiff
            diff = jsondiff.diff(source_mapping, target_mapping, marshal=True, syntax="symmetric")
            # diff = jsondiff.diff(source_mapping, target_mapping, marshal=True)

            # Print the difference between the two JSON objects
            # self.logger.info(json.dumps(diff, indent=2))

            return response_payload_transform(diff)
        except Exception as e:
            return {"error" : str(e)}


    def compare_mapping(self, index_name, diff):
        ''' compare diff using jsondiff library '''
        if not diff:
            self.all_same_mapping.append(True)
            self.response.update({index_name : {'diff' : 'Same mapping'}})
        else:
            self.all_same_mapping.append(False)
            self.response.update({index_name : {'diff' : 'Different mapping', 'result' : diff}})
        return self.response, self.all_same_mapping


    def get_mapping_from_properties(self, mapping, es_v5=False):
        if es_v5:
            return {"properties" : v2.get("properties") for k, v in mapping.items() for k1, v1 in v.items() for k2, v2 in v1.items() if self.lookup_type_in_indices(k2)}    
        else:
            return {'properties': v2 for k, v in mapping.items() for k1, v1 in v.items() for k2, v2 in v1.items() }
        

    def es_version_verify(self, es_client):
        # print(es_client.info()['version']['number'], type(es_client.info()['version']['number']))
        ''' if es_client v.5.X '''
        if "5." in es_client.info()['version']['number']:
            return True
        else:
            return False
        
    def lookup_type_in_indices(self, key):
        ''' lookup type we want to compare from the source es cluster '''
        if "OM_" in key or "WX_" in key or "ES_" in key or "ARCHIVE_" in key:
            return True
        return False


    def get_index_all_mapping_compare(self, source, target):
        ''' Compare all index mapping between two clusters for a given ES indices'''
        source_idx_cnt, target_idx_cnt = 0, 0
        try:
            # self.logger.info(SearchCommonHandler.get_headers())
            self.es_client_source = Elasticsearch(hosts=source,
                                headers=SearchCommonHandler.get_headers(),
                                verify_certs=False,
                                max_retries=0,
                                timeout=30)
            self.es_client_target = Elasticsearch(hosts=target,
                                headers=SearchCommonHandler.get_headers(),
                                verify_certs=False,
                                max_retries=0,
                                timeout=30)
            try:
                source_idx_lists = list(self.es_client_source.indices.get("*"))

                for index_name in source_idx_lists:
                    ''' real index '''
                    if index_name.startswith("wx_") or index_name.startswith("om_") or index_name.startswith("es_") or index_name.startswith("archive_es_"):
                        source_idx_cnt +=1
                        try:
                            source_mapping = self.es_client_source.indices.get_mapping(index=index_name)

                            if not self.es_client_target.indices.exists(index_name):
                                continue

                            target_mapping = self.es_client_target.indices.get_mapping(index=index_name)
                        
                            ''' Get ES v.5.6.4 mapping '''
                            source_mapping = self.get_mapping_from_properties(source_mapping, es_v5=self.es_version_verify(self.es_client_source))
                            # print(source_mapping)

                            ''' Get ES v.8.17 mapping if es_version_verify False '''
                            target_mapping = self.get_mapping_from_properties(target_mapping, es_v5=self.es_version_verify(self.es_client_target))
                            # print(target_mapping)
                                    
                            ''' Get ES v.8.17 mapping '''
                            # target_mapping = get_mapping_from_properties(target_mapping)
                            # print(target_mapping)
                            # self.logger.info(f"index name : {index_name}")
                        
                            # Compare JSON objects using jsondiff
                            diff = jsondiff.diff(source_mapping, target_mapping, marshal=True, syntax="symmetric")
                            # diff = jsondiff.diff(source_mapping, target_mapping, marshal=True)
                        
                            ''' Compare mapping the specific index_name between source/target cluster '''
                            self.compare_mapping(index_name, diff)
                            target_idx_cnt += 1
                        
                        except elasticsearch.ConnectionError as e:
                            return StatusException.raise_exception(f'elasticsearch.ConnectionError : {str(e)}')
                            # raise Exception(f'elasticsearch.ConnectionError : {str(e)}')
                        '''
                        except Exception as e:
                            print(e)
                            # return StatusException.raise_exception('Index [{}]was not found in {} [Source:Elasticsearch Cluster]'.format(index_name, source))
                        '''

            except Exception as e:
                print(e)
                # return {"error" : str(e)}

            resp = {
                "source_es_cluster" : source,
                "target_es_cluster" : target,
                "The number of ES indices in the source es cluster" : source_idx_cnt,
                "The number of ES indices in the target es cluster that have the same index name as the source cluster" : target_idx_cnt,
                "mappings_same" : all(self.all_same_mapping),
                "mapping_details" : self.response
            }

            # return self.response, self.all_same_mapping
            return resp
            # return all(self.all_same_mapping)
        
        except Exception as e:
            # return StatusException.raise_exception(str(e))
            return {"error" : str(e)}
      

    async def get_index_mapping_compare_test(self, source_mapping, target_mapping):
        ''' Compare index mapping as test between two clusters'''
        try:

            print(source_mapping, type(source_mapping))
            print(target_mapping, type(target_mapping))
            
            # Compare JSON objects using jsondiff
            # diff = jsondiff.diff(source_mapping, target_mapping, syntax='symmetric')
            diff = jsondiff.diff(source_mapping, target_mapping, marshal=True, syntax="symmetric")
            
            return response_payload_transform(diff)
        except Exception as e:
            # return {"error" : str(e)}
            return StatusException.raise_exception(str(e))
    

    async def get_node_lists(self, es_host):
        ''' Get the information of cluster's node lists from the specific cluster'''
        try:
            self.es_client = Elasticsearch(hosts=es_host,
                                headers=SearchCommonHandler.get_headers(),
                                verify_certs=False,
                                max_retries=0,
                                timeout=5)
            # print(type(self.es_client.cluster.health()))
            return self.es_client.nodes.stats()
        except Exception as e:
            return StatusException.raise_exception(e)
        finally:
            self.es_client.close()


    async def get_heapspace(self, es_host):
        ''' Get the information of cluster's node heapspace from the specific cluster'''
        try:
            response_json = []
            r_list = requests.get(f"{es_host}/_cat/nodes?format=json")
            # print(json.dumps(r_list.json(), indent=2))
           
            for node in r_list.json():
                r = requests.get("http://{}:9200/_cat/nodes?h=heap*&format=json".format(node['ip']))
                if r.status_code != 200:
                    return None
                response_json.append({str(node['ip']) : r.json()[0]})
            return response_json
        except Exception as e:
            return StatusException.raise_exception(e)
        

    def get_heapspace_each(self, es_host):
        ''' Get the information of cluster's node heapspace from the specific cluster'''
        try:
            r = requests.get("http://{}:9200/_cat/nodes?h=heap*&format=json".format(es_host), timeout=5)
            if r.status_code != 200:
                return None
            return {str(es_host) : r.json()[0]}
        except Exception as e:
            return StatusException.raise_exception(e)
        