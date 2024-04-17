from config.log_config import create_log
from config import config
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
# import yaml
import json
import os
from service.es_search_handler import (
                                        SearchAPIHandler,
                                        SearchOmniHandler
                                      )
from service.query_builder import QueryBuilder

# def read_config_yaml():
#     with open('./config.yaml', 'r') as f:
#         doc = yaml.load(f, Loader=yaml.FullLoader)
        
#     logger.info(json.dumps(doc, indent=2))
    
#     return doc




load_dotenv()
    
# Initialize & Inject with only one instance
logger = create_log()


SearchAPIHandlerInject = SearchAPIHandler(logger)
SearchOmniHandlerInject = SearchOmniHandler(logger)

QueryBuilderInject = QueryBuilder(logger)
