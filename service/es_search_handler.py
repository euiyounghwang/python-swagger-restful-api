import json
from elasticsearch import Elasticsearch, exceptions
import elasticsearch.exceptions
from service.status_handler import (StatusHanlder, StatusException)
from service.es_util import response_payload_transform
from fastapi.responses import JSONResponse
import jsondiff


class SearchOmniHandler(object):
    
    def __init__(self, logger):
        self.logger = logger
        
    
    def get_headers(self):
        ''' Elasticsearch Header '''
        return {
            'Content-type': 'application/json', 
            'Authoriztion' : 'Basic ZWxhc3RpYzpnc2FhZG1pbg==',
            'Connection': 'close'
        }
    
    async def search(self, query_builder, oas_query=None):
        ''' Search with QuerBuilder '''
        if not oas_query:
            oas_query = {}

        es_query = query_builder.build_query(oas_query)
        self.logger.info('query_builder_build_query:oas_query - {}'.format(json.dumps(es_query, indent=2)))

        try:
            if oas_query.get("source_es_host"):
                self.es_client = Elasticsearch(hosts=oas_query.get("source_es_host"),
                                    headers=self.get_headers(),
                                    verify_certs=False,
                                    max_retries=0,
                                    timeout=5)
                
                es_result = self.es_client.search(
                    index = "test",
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
    
    def __init__(self, logger):
        self.logger = logger

    
    def get_headers(self):
        ''' Elasticsearch Header '''
        return {'Content-type': 'application/json', 'Authoriztion' : 'Basic ZWxhc3RpYzpnc2FhZG1pbg==','Connection': 'close'}    
    
    def get_es_health(self, es_host):
        ''' Get the information of cluster's health from the specific cluster'''
        try:
            self.es_client = Elasticsearch(hosts=es_host,
                                headers=self.get_headers(),
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
                                headers=self.get_headers(),
                                verify_certs=False,
                                max_retries=0,
                                timeout=5)
            raw_data = self.es_client.get(index=index_name, id=id)
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
                                headers=self.get_headers(),
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
                                headers=self.get_headers(),
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
            self.es_client_source = Elasticsearch(hosts=source,
                                headers=self.get_headers(),
                                verify_certs=False,
                                max_retries=0,
                                timeout=5)
            self.es_client_target = Elasticsearch(hosts=target,
                                headers=self.get_headers(),
                                verify_certs=False,
                                max_retries=0,
                                timeout=5)
            try:
                source_mapping = self.es_client_source.indices.get_mapping(index=index_name)
            except Exception as e:
                # return {"error" : 'Index [{}]was not found in {} [Source:Elasticsearch Cluster]'.format(index_name, source)}
                return StatusException.raise_exception('Index [{}]was not found in {} [Source:Elasticsearch Cluster]'.format(index_name, source))

            try:
                target_mapping = self.es_client_target.indices.get_mapping(index=index_name)
            except exceptions.NotFoundError:
                # return {"error" : 'Index [{}]was not found in {} [Target:Elasticsearch Cluster]'.format(index_name, target)}
                return StatusException.raise_exception('Index [{}]was not found in {} [Target:Elasticsearch Cluster]'.format(index_name, target))
            
            # Compare JSON objects using jsondiff
            # diff = jsondiff.diff(source_mapping, target_mapping, marshal=True, syntax="symmetric")
            diff = jsondiff.diff(source_mapping, target_mapping, marshal=True)

            # Print the difference between the two JSON objects
            # print(json.dumps(diff, indent=2))
            return response_payload_transform(diff)
        except Exception as e:
            return {"error" : str(e)}
        finally:
            self.es_client_source.close()
            self.es_client_target.close()


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
                                headers=self.get_headers(),
                                verify_certs=False,
                                max_retries=0,
                                timeout=5)
            # print(type(self.es_client.cluster.health()))
            return self.es_client.nodes.stats()
        except Exception as e:
            return StatusException.raise_exception(e)
        finally:
            self.es_client.close()
        